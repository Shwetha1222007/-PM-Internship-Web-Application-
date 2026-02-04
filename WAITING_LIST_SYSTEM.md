# Smart Waiting List & Location-Based Alternatives System

## Overview
This system implements an intelligent candidate selection process with automatic waiting list management and location-based alternative offers.

## Features

### 1. **AI-Based Candidate Selection**
- When multiple candidates apply for the same position, the system uses AI scoring to rank them
- Top candidates (based on available seats) are automatically selected
- Remaining candidates are placed on a waiting list

### 2. **Waiting List Management**
- Candidates not selected for their preferred location are automatically added to a waiting list
- Each candidate receives their rank position and AI score
- Waiting list candidates receive email notifications with their status

### 3. **Location-Based Alternatives**
- If a candidate doesn't get selected for their preferred location, the system automatically finds:
  - Same company, different locations with available seats
  - Alternatives are ranked by number of available seats
- Candidates can view and accept alternative locations from their dashboard

### 4. **Re-Application Option**
- If candidates are not satisfied with alternative locations, they can:
  - Reject the alternatives
  - Apply to different companies
  - Keep their waiting list status active

## Database Schema

### New Tables

#### `company_locations`
Stores location-specific seat availability for each company.
```sql
- id: Primary key
- company_name: Company name
- location: City/location name
- available_seats: Total seats at this location
- allocated_seats: Currently allocated seats
- created_at: Timestamp
```

#### `waiting_list`
Tracks candidates on waiting lists.
```sql
- id: Primary key
- application_id: Reference to application
- user_id: Reference to user
- company: Company name
- preferred_location: Candidate's preferred location
- rank_position: Position in waiting list
- ai_score: AI-calculated score
- status: 'Waiting', 'Accepted Alternative', 'Promoted'
- notified_at: When candidate was notified
- created_at: Timestamp
```

#### `alternative_offers`
Tracks alternative location offers to waiting list candidates.
```sql
- id: Primary key
- waiting_list_id: Reference to waiting_list entry
- user_id: Reference to user
- company: Company name
- alternative_location: Alternative location offered
- offered_at: When offer was made
- response: 'Pending', 'Accepted', 'Rejected'
- responded_at: When candidate responded
```

## Workflow

### Step 1: Application Submission
1. Candidate applies for Company X, Location Y
2. Application is stored with status "Applied"

### Step 2: HR Selection Process
1. HR initiates selection for a specific company and location
2. System retrieves all "Applied" applications for that company-location
3. AI engine ranks candidates based on:
   - Skills match (15 points per matching skill)
   - CGPA (up to 50 points)
   - Experience (10 points)
   - Rural priority (20 points)
   - Social category priority (20 points)

### Step 3: Selection & Waiting List Creation
1. Top N candidates (based on available seats) are selected
2. Selected candidates:
   - Status updated to "Selected"
   - Receive congratulatory email
   - Allocated seats counter incremented
3. Remaining candidates:
   - Status updated to "Waiting List"
   - Added to waiting_list table with rank position
   - System searches for alternative locations

### Step 4: Alternative Location Offers
1. For each waiting list candidate:
   - System finds same company, different locations with available seats
   - Creates alternative_offer records
   - Sends email with:
     - Waiting list position
     - AI score
     - List of alternative locations
     - Option to accept/reject alternatives

### Step 5: Candidate Response
Candidates can:
- **Accept Alternative**: 
  - Application updated to "Selected" with new location
  - Waiting list status changed to "Accepted Alternative"
  - Seats allocated at alternative location
- **Reject Alternative**:
  - Alternative offer marked as "Rejected"
  - Candidate remains on waiting list
  - Can apply to other companies
- **Wait**:
  - Stay on waiting list
  - May be promoted if selected candidate declines

## Email Notifications

### Selection Email
```
Subject: 🎉 Congratulations! You have been SELECTED for [Company], [Location]

Content:
- Congratulations message
- Company and location details
- AI score and rank
- 24-hour acceptance deadline
- Link to dashboard
```

### Waiting List Email
```
Subject: 📋 You are on the Waiting List for [Company], [Location]

Content:
- Waiting list notification
- Position in queue
- AI score
- List of alternative locations with available seats
- Option to accept alternatives or apply elsewhere
- Note about potential promotion
```

## API Functions

### `process_applications_for_position(company, location, requirements)`
- Retrieves and ranks all applications for a specific position
- Returns: (selected_candidates, waiting_list_candidates)

### `select_candidates_and_create_waiting_list(company, location, requirements)`
- Selects top candidates
- Creates waiting list entries
- Sends email notifications
- Creates alternative offers
- Returns: Selection summary

### `find_alternative_locations(company, preferred_location, cur)`
- Finds alternative locations for the same company
- Excludes preferred location
- Returns locations with available seats

### `get_waiting_list_for_user(user_id)`
- Retrieves all waiting list entries for a user
- Includes alternative offers
- Returns: List of waiting list entries with alternatives

### `accept_alternative_location(alternative_offer_id, user_id)`
- Accepts an alternative location offer
- Updates application status to "Selected"
- Allocates seat at alternative location
- Returns: Success boolean

### `reject_alternative_location(alternative_offer_id, user_id)`
- Rejects an alternative location offer
- Keeps waiting list status active
- Returns: Success boolean

## Usage Example

### HR Initiates Selection
```python
from waiting_list_manager import select_candidates_and_create_waiting_list

requirements = {
    'skills': 'python, javascript, react',
    'min_cgpa': 7.0
}

result = select_candidates_and_create_waiting_list(
    company='TCS',
    location='Bangalore',
    requirements=requirements
)

print(f"Selected: {result['selected_count']}")
print(f"Waiting List: {result['waiting_list_count']}")
```

### Candidate Views Waiting List
```python
from waiting_list_manager import get_waiting_list_for_user

waiting_entries = get_waiting_list_for_user(user_id=123)

for entry in waiting_entries:
    print(f"Company: {entry['waiting_list_entry']['company']}")
    print(f"Position: #{entry['waiting_list_entry']['rank_position']}")
    print(f"Alternatives: {len(entry['alternatives'])}")
```

### Candidate Accepts Alternative
```python
from waiting_list_manager import accept_alternative_location

success = accept_alternative_location(
    alternative_offer_id=456,
    user_id=123
)

if success:
    print("Alternative location accepted!")
```

## Benefits

1. **Fair Selection**: AI-based ranking ensures objective candidate evaluation
2. **Transparency**: Candidates know their exact position and score
3. **Flexibility**: Alternative locations provide more opportunities
4. **Efficiency**: Automated process reduces HR workload
5. **Better Matching**: Candidates can choose locations that suit them
6. **Reduced Wastage**: Seats are filled efficiently across locations

## Future Enhancements

1. **Automatic Promotion**: When a selected candidate declines, automatically promote from waiting list
2. **Multi-Company Alternatives**: Suggest similar positions in other companies
3. **Location Preferences**: Allow candidates to rank multiple locations
4. **Skill-Based Matching**: Suggest positions matching candidate's skill set
5. **Deadline Management**: Automatic status updates based on response deadlines
