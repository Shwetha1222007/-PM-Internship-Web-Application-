"""
Waiting List Management System
Handles candidate selection, waiting list placement, and location-based alternatives
"""
import sqlite3
from datetime import datetime
from database import get_connection
from email_service import (
    send_update_to_candidate,
    send_hr_announcement,
    send_admin_rejection_audit
)
from ai_engine import ai_filter_candidates


def process_applications_for_position(company, location, requirements):
    """
    Process all applications for a specific company and location
    Returns: (ranked_candidates)
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
        return []

    available_seats = location_data['available_seats']
    allocated_seats = location_data['allocated_seats']
    remaining_seats = available_seats - allocated_seats

    if remaining_seats <= 0:
        return []

    # Get all applications for this company and location
    cur.execute("""
        SELECT a.*, u.name, u.email, u.phone, u.district, u.rural, u.social_category
        FROM applications a
        JOIN users u ON a.user_id = u.id
        WHERE a.company = ? AND a.location_pref = ? AND a.status = 'Applied'
    """, (company, location))

    applications = cur.fetchall()

    if not applications:
        return []

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
    conn.close()
    return ranked_candidates


def select_candidates_and_create_waiting_list(company, location, requirements):
    """
    Enhanced selection logic:
    1. Top candidate -> Review Pending (HR Review)
    2. Next candidate -> Shortlisted (Backup)
    3. Others -> Waiting List
    """
    ranked = process_applications_for_position(company, location, requirements)
    if not ranked:
        return {'review_pending': 0, 'shortlisted': 0, 'waiting_list': 0}

    conn = get_connection()
    cur = conn.cursor()

    # Get HR user for this company
    cur.execute("SELECT * FROM hr_users WHERE company = ?", (company,))
    hr_user = cur.fetchone()

    # Rule: If we have at least 1 candidate, we process
    # Requirement: 3 candidate case specially mentioned
    # Top 2 get Shortlisted mail. Top 1 goes to HR.

    for idx, item in enumerate(ranked):
        cand = item['data']
        score = item['score']
        app_id = cand['application_id']

        # Save score in both tables for redundancy and historical tracking
        cur.execute("UPDATE applications SET ai_score = ? WHERE id = ?", (score, app_id))

        if idx == 0:
            # Top Candidate -> Review Pending for HR
            cur.execute("UPDATE applications SET status = 'Review Pending' WHERE id = ?", (app_id,))

            # Send Shortlisted email to candidate
            send_update_to_candidate(cand['email'], "Shortlisted", company)

            # Send Detail disclosure to HR
            # Check for Same Qualification Tie with 2nd candidate
            same_qual = False
            if len(ranked) > 1 and abs(ranked[0]['score'] - ranked[1]['score']) < 0.001:
                same_qual = True

            if hr_user:
                app_data = {
                    'app_id': app_id,
                    'company': company,
                    'sector': cand.get('sector', 'N/A'),
                    'skills': cand['skills'],
                    'cgpa': cand['cgpa'],
                    'experience': cand['experience'],
                    'college_name': cand['college_name'],
                    'languages': cand['languages'],
                    'ai_score': f"{score:.2f}"
                }
                send_hr_announcement(cand, app_data, same_qualification=same_qual)

        elif idx == 1:
            # 2nd Place Candidate -> Shortlisted (The Backup)
            cur.execute("UPDATE applications SET status = 'Shortlisted' WHERE id = ?", (app_id,))
            send_update_to_candidate(cand['email'], "Shortlisted", company)

        else:
            # Others -> Waiting List
            cur.execute("UPDATE applications SET status = 'Waiting List' WHERE id = ?", (app_id,))

            # Add to waiting list table
            rank_pos = idx + 1
            cur.execute("""
                INSERT INTO waiting_list
                (application_id, user_id, company, preferred_location, rank_position, ai_score, status, notified_at)
                VALUES (?, ?, ?, ?, ?, ?, 'Waiting', ?)
            """, (app_id, cand['user_id'], company, location, rank_pos, score, datetime.now()))

            # Send waiting list email
            send_update_to_candidate(cand['email'], "Waiting List", company)

    conn.commit()
    conn.close()

    return {
        'review_pending': 1 if len(ranked) > 0 else 0,
        'shortlisted': 1 if len(ranked) > 1 else 0,
        'waiting_list': max(0, len(ranked) - 2)
    }


def handle_hr_decision(application_id, hr_username, action, reason=None):
    """
    Processes HR decision (Accept/Reject).
    If Accept -> Candidate selected.
    If Reject -> Candidate rejected, reason sent to Admin, Backup promoted.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Get application and candidate details
    cur.execute("""
        SELECT a.*, u.name, u.email
        FROM applications a
        JOIN users u ON a.user_id = u.id
        WHERE a.id = ?
    """, (application_id,))
    app = cur.fetchone()

    if not app:
        conn.close()
        return False, "Application not found"

    company = app['company']
    location = app['location_pref']

    if action == 'Accept':
        # Update Top Candidate to Selected
        cur.execute("""
            UPDATE applications
            SET status = 'Selected', selected_at = ?
            WHERE id = ?
        """, (datetime.now(), application_id))

        # Increment allocated seats
        cur.execute("""
            UPDATE company_locations
            SET allocated_seats = allocated_seats + 1
            WHERE company_name = ? AND location = ?
        """, (company, location))

        # Notify candidate
        send_update_to_candidate(app['email'], "Selected", company)

        # Check if there's a backup (Shortlisted) and move them to Waiting List (as they were only backup)
        cur.execute("""
            UPDATE applications SET status = 'Waiting List'
            WHERE company = ? AND location_pref = ? AND status = 'Shortlisted'
        """, (company, location))

        msg = f"Candidate {app['name']} successfully selected."

    elif action == 'Reject':
        if not reason:
            conn.close()
            return False, "Rejection reason is mandatory."

        # Update Top Candidate to Rejected
        cur.execute("""
            UPDATE applications
            SET status = 'Rejected', hr_rejection_reason = ?
            WHERE id = ?
        """, (reason, application_id))

        # Notify Admin for Audit (the 'consequences' part)
        send_admin_rejection_audit(hr_username, app['name'], company, reason)

        # Promote Backup (Search for candidate with status 'Shortlisted' for this company/location)
        cur.execute("""
            SELECT id, user_id FROM applications
            WHERE company = ? AND location_pref = ? AND status = 'Shortlisted'
            ORDER BY ai_score DESC LIMIT 1
        """, (company, location))
        backup = cur.fetchone()

        if backup:
            # Update backup to Selected
            cur.execute("""
                UPDATE applications
                SET status = 'Selected', selected_at = ?
                WHERE id = ?
            """, (datetime.now(), backup['id']))

            # Increment allocated seats
            cur.execute("""
                UPDATE company_locations
                SET allocated_seats = allocated_seats + 1
                WHERE company_name = ? AND location = ?
            """, (company, location))

            # Get backup user email
            cur.execute("SELECT email, name FROM users WHERE id = ?", (backup['user_id'],))
            backup_user = cur.fetchone()
            if backup_user:
                send_update_to_candidate(backup_user['email'], "Selected", company)

            msg = f"Candidate {app['name']} rejected. Backup candidate has been automatically selected."
        else:
            msg = f"Candidate {app['name']} rejected. No backup was found."

    conn.commit()
    conn.close()
    return True, msg


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
