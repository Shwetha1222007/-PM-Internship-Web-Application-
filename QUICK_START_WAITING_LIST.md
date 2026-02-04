# 🚀 Quick Start Guide - Waiting List System

## For HR Users

### How to Run Selection Process

```python
from waiting_list_manager import select_candidates_and_create_waiting_list

# Define job requirements
requirements = {
    'skills': 'Python, JavaScript, React',  # Required skills
    'min_cgpa': 7.0                         # Minimum CGPA
}

# Run selection for a specific company and location
result = select_candidates_and_create_waiting_list(
    company='TCS',
    location='Bangalore',
    requirements=requirements
)

# View results
print(f"Selected: {result['selected_count']}")
print(f"Waiting List: {result['waiting_list_count']}")
```

### What Happens Automatically:
1. ✅ All applications are retrieved
2. ✅ Candidates are ranked by AI
3. ✅ Top candidates are selected
4. ✅ Others go to waiting list
5. ✅ Alternative locations are found
6. ✅ Emails sent to everyone
7. ✅ Database updated

## For Candidates

### Check Your Waiting List Status

```python
from waiting_list_manager import get_waiting_list_for_user

# Get your waiting list entries
waiting_entries = get_waiting_list_for_user(user_id=YOUR_USER_ID)

for entry in waiting_entries:
    wl = entry['waiting_list_entry']
    alts = entry['alternatives']
    
    print(f"Company: {wl['company']}")
    print(f"Position: #{wl['rank_position']}")
    print(f"Score: {wl['ai_score']}")
    print(f"Alternatives: {len(alts)}")
```

### Accept an Alternative Location

```python
from waiting_list_manager import accept_alternative_location

# Accept an alternative offer
success = accept_alternative_location(
    alternative_offer_id=123,  # From your dashboard
    user_id=YOUR_USER_ID
)

if success:
    print("✅ Alternative accepted! You are now selected!")
```

### Reject an Alternative Location

```python
from waiting_list_manager import reject_alternative_location

# Reject an alternative offer
success = reject_alternative_location(
    alternative_offer_id=123,
    user_id=YOUR_USER_ID
)

if success:
    print("✅ Alternative rejected. You remain on waiting list.")
```

## Testing & Demo

### Run the Complete Demo

```bash
# This creates sample data and demonstrates the entire system
python demo_waiting_list.py
```

**What the demo does:**
1. Creates 5 sample candidates
2. Creates applications for TCS Bangalore
3. Runs AI ranking
4. Selects top 3 candidates
5. Places 2 on waiting list
6. Finds alternative locations
7. Shows all results

### Clear All Data

```bash
# Remove all users and applications
python clear_all_data.py
```

### Verify Data is Clean

```bash
# Check that all tables are empty
python verify_clean.py
```

### Initialize Database

```bash
# Create tables and seed company locations
python database.py
```

## Common Scenarios

### Scenario 1: First Time Setup
```bash
1. python database.py              # Create tables
2. python demo_waiting_list.py     # Test with sample data
3. python clear_all_data.py        # Clean up test data
4. # Now ready for real applications!
```

### Scenario 2: Running Selection
```bash
1. Candidates apply via Streamlit app
2. HR logs in and clicks "Run Selection"
3. System automatically:
   - Ranks candidates
   - Selects top ones
   - Creates waiting list
   - Sends emails
4. Candidates check dashboard for results
```

### Scenario 3: Candidate on Waiting List
```bash
1. Candidate receives email notification
2. Logs into dashboard
3. Sees waiting list position and score
4. Views alternative locations
5. Clicks "Accept" or "Reject" for each alternative
6. If accepted → Status changes to "Selected"
7. If rejected → Can apply to other companies
```

## API Reference

### Main Functions

#### `select_candidates_and_create_waiting_list(company, location, requirements)`
**Purpose**: Run the complete selection process  
**Parameters**:
- `company` (str): Company name (e.g., "TCS")
- `location` (str): Location name (e.g., "Bangalore")
- `requirements` (dict): Job requirements with 'skills' and 'min_cgpa'

**Returns**: Dictionary with selected and waiting list counts

---

#### `get_waiting_list_for_user(user_id)`
**Purpose**: Get all waiting list entries for a candidate  
**Parameters**:
- `user_id` (int): User's ID

**Returns**: List of waiting list entries with alternatives

---

#### `accept_alternative_location(alternative_offer_id, user_id)`
**Purpose**: Accept an alternative location offer  
**Parameters**:
- `alternative_offer_id` (int): ID of the alternative offer
- `user_id` (int): User's ID

**Returns**: Boolean (True if successful)

---

#### `reject_alternative_location(alternative_offer_id, user_id)`
**Purpose**: Reject an alternative location offer  
**Parameters**:
- `alternative_offer_id` (int): ID of the alternative offer
- `user_id` (int): User's ID

**Returns**: Boolean (True if successful)

---

#### `find_alternative_locations(company, preferred_location, cur)`
**Purpose**: Find alternative locations for a company  
**Parameters**:
- `company` (str): Company name
- `preferred_location` (str): Location to exclude
- `cur`: Database cursor

**Returns**: List of alternative locations with available seats

## Database Queries

### Check Waiting List
```sql
SELECT * FROM waiting_list WHERE user_id = ?
```

### Check Alternative Offers
```sql
SELECT * FROM alternative_offers WHERE user_id = ? AND response = 'Pending'
```

### Check Company Locations
```sql
SELECT * FROM company_locations WHERE company_name = ?
```

### Check Seat Availability
```sql
SELECT 
    company_name, 
    location, 
    (available_seats - allocated_seats) as remaining
FROM company_locations
WHERE (available_seats - allocated_seats) > 0
```

## Troubleshooting

### Issue: No alternatives found
**Solution**: Check if company has multiple locations
```sql
SELECT * FROM company_locations WHERE company_name = 'TCS'
```

### Issue: Selection not working
**Solution**: Check if seats are available
```sql
SELECT available_seats, allocated_seats 
FROM company_locations 
WHERE company_name = 'TCS' AND location = 'Bangalore'
```

### Issue: Emails not sending
**Solution**: Check email configuration in `email_service.py`

## Tips & Best Practices

1. **Always run database.py first** to ensure tables exist
2. **Test with demo_waiting_list.py** before using with real data
3. **Clear test data** with clear_all_data.py before production
4. **Check seat availability** before running selection
5. **Monitor email logs** to ensure notifications are sent

## Next Steps

1. ✅ Run `python database.py` to initialize
2. ✅ Run `python demo_waiting_list.py` to test
3. ✅ Integrate into Streamlit UI
4. ✅ Test with real applications
5. ✅ Monitor and optimize

---

**Need Help?**
- Check `WAITING_LIST_SYSTEM.md` for detailed documentation
- Review `WAITING_LIST_FLOW.md` for visual diagrams
- See `PROJECT_UPDATE_SUMMARY.md` for complete overview

🎉 **Happy Managing!**
