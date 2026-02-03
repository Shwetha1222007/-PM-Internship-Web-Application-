# HR Dashboard System - User Guide

## Overview
The HR Dashboard system allows company HR personnel to manage internship applications, view AI-filtered candidates, and track candidate responses with a 24-hour deadline.

## HR Login Credentials

The following HR accounts have been created:

| Company   | Username           | Password |
|-----------|-------------------|----------|
| Zoho      | 1208_zoho_HR      | 1234     |
| Infosys   | 1208_infosys_HR   | 1234     |
| TCS       | 1208_tcs_HR       | 1234     |
| Wipro     | 1208_wipro_HR     | 1234     |
| Google    | 1208_google_HR    | 1234     |

## Company Seat Allocation

Each company has a specific number of internship seats:

- **Zoho**: 1 seat
- **Infosys**: 5 seats
- **TCS**: 10 seats
- **Wipro**: 3 seats
- **Google**: 2 seats
- **Microsoft**: 1 seat
- **Amazon**: 5 seats
- **Flipkart**: 3 seats

## Features

### 1. **All Applications Tab**
- View all candidates who applied to your company
- See candidate details including:
  - Name, email, phone
  - Skills, CGPA, college
  - Location and social category
  - Application status (Applied, Selected, Rejected)

### 2. **AI Filtered Candidates Tab**
- AI automatically ranks candidates based on:
  - **Skills Match**: Matching required skills
  - **CGPA**: Academic performance (up to 50 points)
  - **Experience**: Work experience (+10 points)
  - **Rural Priority**: Rural candidates get +20 points
  - **Social Category Priority**: SC/ST/OBC/MBC candidates get +20 points

- **Top Candidates**: Shows top N candidates (based on available seats)
- **Waiting List**: Shows remaining candidates ranked by AI score

- **Actions**:
  - ✅ **Accept**: Select a candidate (if seats available)
  - ❌ **Reject**: Reject a candidate

### 3. **Selected Candidates Tab**
- View all candidates you have selected
- See selection timestamp and response deadline

### 4. **Response Tracking Tab**
- **24-Hour Deadline**: Candidates must respond within 24 hours of selection
- **Time Remaining**: Visual countdown showing hours and minutes left
- **Color Coding**:
  - 🟢 Green: More than 12 hours remaining
  - 🟡 Yellow: 6-12 hours remaining
  - 🔴 Red: Less than 6 hours remaining

- **Expired Offers**: 
  - If a candidate doesn't respond within 24 hours, the offer expires
  - HR can revoke the offer, which frees up the seat for other candidates

## Seat Allocation Logic

1. **Limited Seats**: Each company has a fixed number of seats (e.g., Zoho has 1 seat)
2. **Allocation Tracking**: When HR accepts a candidate, one seat is allocated
3. **Seat Availability**: HR can only accept candidates if seats are available
4. **Seat Recovery**: If an offer is revoked (due to no response), the seat becomes available again

## How to Use

### Step 1: Login
1. Go to the home page
2. Click "👔 HR LOGIN"
3. Enter your username (e.g., `1208_zoho_HR`) and password (`1234`)

### Step 2: View Applications
1. Navigate to the "📋 All Applications" tab to see all candidates who applied

### Step 3: Use AI Filtering
1. Go to "🤖 AI Filtered Candidates" tab
2. Review the top candidates recommended by AI
3. Check the waiting list for other qualified candidates

### Step 4: Accept/Reject Candidates
1. Click "✅ Accept" to select a candidate (if seats available)
2. Click "❌ Reject" to reject a candidate
3. The system will automatically:
   - Set a 24-hour response deadline
   - Update seat allocation
   - Move the candidate to "Selected" status

### Step 5: Track Responses
1. Go to "⏰ Response Tracking" tab
2. Monitor time remaining for each selected candidate
3. If deadline expires, click "🗑️ Revoke Offer" to free up the seat

## AI Scoring System

The AI assigns scores to candidates based on multiple factors:

- **Skills Match**: 15 points per matching skill
- **CGPA**: Up to 50 points (CGPA × 5)
- **Experience**: 10 points if experience description is substantial
- **Rural Priority**: +20 points for rural candidates
- **Social Category**: +20 points for SC/ST/OBC/MBC candidates

**Example**:
- Candidate with CGPA 8.5, 2 matching skills, rural background, OBC category
- Score = (8.5 × 5) + (2 × 15) + 20 + 20 = 42.5 + 30 + 40 = **112.5 points**

## Important Notes

1. **Company-Specific Access**: Each HR can only see applications for their own company
2. **Seat Limits**: You cannot accept more candidates than available seats
3. **24-Hour Rule**: Selected candidates must respond within 24 hours or lose the offer
4. **AI Recommendations**: The AI ranking is a recommendation; HR has final decision authority
5. **Waiting List**: If a seat becomes available (due to revoked offer), you can select from the waiting list

## Troubleshooting

**Q: I can't accept a candidate**
- Check if you have available seats in the dashboard header
- If all seats are allocated, you must wait for a response or revoke an expired offer

**Q: How do I free up a seat?**
- Go to "Response Tracking" tab
- Find expired offers (candidates who didn't respond in 24 hours)
- Click "Revoke Offer" to free up the seat

**Q: Can I see candidates from other companies?**
- No, each HR account only has access to their company's applications

## Support

For technical issues or questions, contact the system administrator.
