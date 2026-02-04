"""
Waiting List Management System
Handles candidate selection, waiting list placement, and location-based alternatives
"""
import sqlite3
from datetime import datetime
from database import get_connection
from email_service import send_update_to_candidate
from ai_engine import ai_filter_candidates


def process_applications_for_position(company, location, requirements):
    """
    Process all applications for a specific company and location
    Returns: (selected_candidates, waiting_list_candidates)
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Get available seats for this company-location
    cur.execute("""
        SELECT available_seats, allocated_seats 
        FROM company_locations 
        WHERE company_name = ? AND location = ?
    """, (company, location))
    
    location_data = cur.fetchone()
    if not location_data:
        return [], []
    
    available_seats = location_data['available_seats']
    allocated_seats = location_data['allocated_seats']
    remaining_seats = available_seats - allocated_seats
    
    if remaining_seats <= 0:
        return [], []
    
    # Get all applications for this company and location
    cur.execute("""
        SELECT a.*, u.name, u.email, u.phone, u.district, u.rural, u.social_category
        FROM applications a
        JOIN users u ON a.user_id = u.id
        WHERE a.company = ? AND a.location_pref = ? AND a.status = 'Applied'
    """, (company, location))
    
    applications = cur.fetchall()
    
    if not applications:
        return [], []
    
    # Convert to list of dicts for AI processing
    candidates_list = []
    for app in applications:
        candidate = {
            'application_id': app['id'],
            'user_id': app['user_id'],
            'name': app['name'],
            'email': app['email'],
            'phone': app['phone'],
            'skills': app['skills'],
            'cgpa': app['cgpa'],
            'experience': app['experience'],
            'district': app['district'],
            'rural': app['rural'],
            'social_category': app['social_category'],
            'perc_12th': app['perc_12th'],
            'college_name': app['college_name'],
            'languages': app['languages']
        }
        candidates_list.append(candidate)
    
    # Use AI to rank candidates
    ranked_candidates = ai_filter_candidates(candidates_list, requirements)
    
    # Select top candidates based on available seats
    selected = ranked_candidates[:remaining_seats]
    waiting_list = ranked_candidates[remaining_seats:]
    
    conn.close()
    return selected, waiting_list


def select_candidates_and_create_waiting_list(company, location, requirements):
    """
    Select top candidates and place others on waiting list
    Send notifications to all candidates
    """
    selected, waiting_list = process_applications_for_position(company, location, requirements)
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Process selected candidates
    for idx, candidate_obj in enumerate(selected):
        candidate = candidate_obj['data']
        score = candidate_obj['score']
        
        # Update application status
        cur.execute("""
            UPDATE applications 
            SET status = 'Selected', selected_at = ?
            WHERE id = ?
        """, (datetime.now(), candidate['application_id']))
        
        # Update allocated seats
        cur.execute("""
            UPDATE company_locations 
            SET allocated_seats = allocated_seats + 1
            WHERE company_name = ? AND location = ?
        """, (company, location))
        
        # Send selection email
        try:
            send_update_to_candidate(
                candidate['email'],
                candidate['name'],
                company,
                f"🎉 Congratulations! You have been SELECTED for the internship at {company}, {location}!",
                f"""
                <h2>Congratulations {candidate['name']}!</h2>
                <p>We are pleased to inform you that you have been <strong>selected</strong> for the internship position at:</p>
                <ul>
                    <li><strong>Company:</strong> {company}</li>
                    <li><strong>Location:</strong> {location}</li>
                    <li><strong>Your AI Score:</strong> {score:.2f}</li>
                    <li><strong>Rank:</strong> #{idx + 1}</li>
                </ul>
                <p>Please check your dashboard for further details and next steps.</p>
                <p>You have 24 hours to accept this offer.</p>
                """
            )
        except Exception as e:
            print(f"Error sending selection email to {candidate['email']}: {e}")
    
    # Process waiting list candidates
    for idx, candidate_obj in enumerate(waiting_list):
        candidate = candidate_obj['data']
        score = candidate_obj['score']
        rank_position = len(selected) + idx + 1
        
        # Update application status
        cur.execute("""
            UPDATE applications 
            SET status = 'Waiting List'
            WHERE id = ?
        """, (candidate['application_id'],))
        
        # Add to waiting list table
        cur.execute("""
            INSERT INTO waiting_list 
            (application_id, user_id, company, preferred_location, rank_position, ai_score, status, notified_at)
            VALUES (?, ?, ?, ?, ?, ?, 'Waiting', ?)
        """, (candidate['application_id'], candidate['user_id'], company, location, 
              rank_position, score, datetime.now()))
        
        waiting_list_id = cur.lastrowid
        
        # Find alternative locations for this company
        alternative_locations = find_alternative_locations(company, location, cur)
        
        # Send waiting list email with alternatives
        try:
            alternatives_html = ""
            if alternative_locations:
                alternatives_html = "<h3>Alternative Locations Available:</h3><ul>"
                for alt_loc in alternative_locations:
                    alternatives_html += f"<li><strong>{alt_loc['location']}</strong> - {alt_loc['available_seats']} seats available</li>"
                    
                    # Create alternative offer record
                    cur.execute("""
                        INSERT INTO alternative_offers 
                        (waiting_list_id, user_id, company, alternative_location, response)
                        VALUES (?, ?, ?, ?, 'Pending')
                    """, (waiting_list_id, candidate['user_id'], company, alt_loc['location']))
                
                alternatives_html += "</ul><p>You can view and accept these alternatives from your dashboard.</p>"
            else:
                alternatives_html = "<p>Currently, no alternative locations are available for this company.</p>"
            
            send_update_to_candidate(
                candidate['email'],
                candidate['name'],
                company,
                f"📋 You are on the Waiting List for {company}, {location}",
                f"""
                <h2>Hello {candidate['name']},</h2>
                <p>Thank you for applying to <strong>{company}</strong> for the location <strong>{location}</strong>.</p>
                <p>While you were not selected for the primary position, you have been placed on the <strong>Waiting List</strong>.</p>
                <ul>
                    <li><strong>Company:</strong> {company}</li>
                    <li><strong>Preferred Location:</strong> {location}</li>
                    <li><strong>Your AI Score:</strong> {score:.2f}</li>
                    <li><strong>Waiting List Position:</strong> #{idx + 1}</li>
                </ul>
                {alternatives_html}
                <p>If you are not satisfied with the alternative locations, you can apply to other companies from your dashboard.</p>
                <p><strong>Note:</strong> If a selected candidate declines their offer, you may be promoted from the waiting list.</p>
                """
            )
        except Exception as e:
            print(f"Error sending waiting list email to {candidate['email']}: {e}")
    
    conn.commit()
    conn.close()
    
    return {
        'selected_count': len(selected),
        'waiting_list_count': len(waiting_list),
        'selected': selected,
        'waiting_list': waiting_list
    }


def find_alternative_locations(company, preferred_location, cur):
    """
    Find alternative locations for the same company
    Returns locations with available seats, excluding the preferred location
    """
    cur.execute("""
        SELECT location, available_seats, allocated_seats,
               (available_seats - allocated_seats) as remaining_seats
        FROM company_locations
        WHERE company_name = ? AND location != ? AND (available_seats - allocated_seats) > 0
        ORDER BY remaining_seats DESC
    """, (company, preferred_location))
    
    alternatives = []
    for row in cur.fetchall():
        alternatives.append({
            'location': row['location'],
            'available_seats': row['remaining_seats']
        })
    
    return alternatives


def get_waiting_list_for_user(user_id):
    """Get all waiting list entries for a user with alternative locations"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT wl.*, 
               a.company, a.location_pref, a.sector,
               (SELECT COUNT(*) FROM waiting_list wl2 
                WHERE wl2.company = wl.company 
                AND wl2.preferred_location = wl.preferred_location 
                AND wl2.rank_position < wl.rank_position) as ahead_count
        FROM waiting_list wl
        JOIN applications a ON wl.application_id = a.id
        WHERE wl.user_id = ? AND wl.status = 'Waiting'
        ORDER BY wl.created_at DESC
    """, (user_id,))
    
    waiting_entries = cur.fetchall()
    
    result = []
    for entry in waiting_entries:
        # Get alternative offers
        cur.execute("""
            SELECT * FROM alternative_offers
            WHERE waiting_list_id = ? AND response = 'Pending'
            ORDER BY offered_at DESC
        """, (entry['id'],))
        
        alternatives = cur.fetchall()
        
        result.append({
            'waiting_list_entry': dict(entry),
            'alternatives': [dict(alt) for alt in alternatives]
        })
    
    conn.close()
    return result


def accept_alternative_location(alternative_offer_id, user_id):
    """Accept an alternative location offer"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Get alternative offer details
    cur.execute("""
        SELECT ao.*, wl.application_id
        FROM alternative_offers ao
        JOIN waiting_list wl ON ao.waiting_list_id = wl.id
        WHERE ao.id = ? AND ao.user_id = ?
    """, (alternative_offer_id, user_id))
    
    offer = cur.fetchone()
    if not offer:
        conn.close()
        return False
    
    # Check if seats are still available
    cur.execute("""
        SELECT available_seats, allocated_seats
        FROM company_locations
        WHERE company_name = ? AND location = ?
    """, (offer['company'], offer['alternative_location']))
    
    location_data = cur.fetchone()
    if not location_data or location_data['available_seats'] <= location_data['allocated_seats']:
        conn.close()
        return False
    
    # Update application
    cur.execute("""
        UPDATE applications
        SET status = 'Selected', location_pref = ?, selected_at = ?
        WHERE id = ?
    """, (offer['alternative_location'], datetime.now(), offer['application_id']))
    
    # Update alternative offer
    cur.execute("""
        UPDATE alternative_offers
        SET response = 'Accepted', responded_at = ?
        WHERE id = ?
    """, (datetime.now(), alternative_offer_id))
    
    # Update waiting list status
    cur.execute("""
        UPDATE waiting_list
        SET status = 'Accepted Alternative'
        WHERE id = ?
    """, (offer['waiting_list_id'],))
    
    # Update allocated seats
    cur.execute("""
        UPDATE company_locations
        SET allocated_seats = allocated_seats + 1
        WHERE company_name = ? AND location = ?
    """, (offer['company'], offer['alternative_location']))
    
    conn.commit()
    conn.close()
    return True


def reject_alternative_location(alternative_offer_id, user_id):
    """Reject an alternative location offer"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE alternative_offers
        SET response = 'Rejected', responded_at = ?
        WHERE id = ? AND user_id = ?
    """, (datetime.now(), alternative_offer_id, user_id))
    
    conn.commit()
    conn.close()
    return True
