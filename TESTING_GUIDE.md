# Testing Guide: Automatic Status Management

## Overview
This guide will help you test the automatic status management feature to ensure it's working correctly.

## Prerequisites
- ✅ App is running: `streamlit run app.py`
- ✅ `schedule` package installed: `pip install schedule`
- ✅ Database has some test data (candidates and applications)
- ✅ Email service is configured (check `email_service.py`)

## Test Scenarios

### Test 1: Verify Scheduler is Running

**Objective:** Confirm the background scheduler starts automatically

**Steps:**
1. Start the Streamlit app: `streamlit run app.py`
2. Check the console output
3. Look for the message: "Background scheduler started - checking every hour"

**Expected Result:**
```
Background scheduler started - checking every hour
```

**Status:** ✅ Pass / ❌ Fail

---

### Test 2: Manual Status Check

**Objective:** Run a one-time status check to see if it works

**Steps:**
1. Open a new terminal
2. Navigate to the project directory
3. Run: `python auto_status_manager.py`
4. Check the output

**Expected Result:**
```
2026-02-04 12:00:00 - INFO - Starting automatic status check...
2026-02-04 12:00:01 - INFO - No expired selections found.
2026-02-04 12:00:02 - INFO - Automatic status check completed.
```

**Status:** ✅ Pass / ❌ Fail

---

### Test 3: Create a Test Expired Selection

**Objective:** Manually create an expired selection to test auto-processing

**Steps:**
1. Login as HR (e.g., `1208_google_HR` / `1234`)
2. Go to AI Filtered Candidates tab
3. Select a candidate
4. Open the database file: `data/internship.db`
5. Manually update the deadline to be in the past:
   ```sql
   UPDATE applications 
   SET response_deadline = datetime('now', '-1 hour')
   WHERE status = 'Selected' 
   LIMIT 1;
   ```
6. Run manual check: `python auto_status_manager.py`
7. Check the log file: `auto_status_manager.log`

**Expected Result:**
- Candidate status changed to "Waiting List"
- Seat freed up
- Next candidate automatically selected
- Emails sent to both candidates
- All operations logged

**Status:** ✅ Pass / ❌ Fail

---

### Test 4: Verify Email Notifications

**Objective:** Ensure emails are sent correctly

**Steps:**
1. Complete Test 3 above
2. Check the email inbox for the expired candidate
3. Check the email inbox for the newly selected candidate

**Expected Result:**

**Email 1 (Expired Candidate):**
- Subject: "OFFICIAL NOTIFICATION: Internship Application Update - [Company]"
- Status: Waiting List (Yellow/Orange background)
- Message: "Your application has been moved to the waiting list..."

**Email 2 (New Candidate):**
- Subject: "OFFICIAL NOTIFICATION: Internship Application Update - [Company]"
- Status: Selected (Green background)
- Message: "Congratulations! You have been shortlisted... Please respond within 48 hours..."

**Status:** ✅ Pass / ❌ Fail

---

### Test 5: Verify UI Updates

**Objective:** Ensure the UI shows the correct status and colors

**Steps:**
1. After completing Test 3, refresh the HR Dashboard
2. Go to "All Applications" tab
3. Check the status of the expired candidate
4. Check the status of the newly selected candidate
5. Go to "⏰ 48-Hour Response Tracking" tab
6. Verify the new candidate appears with countdown timer

**Expected Result:**
- Expired candidate shows "Waiting List" with yellow/orange color
- New candidate shows "Selected" with green color
- New candidate appears in Response Tracking with 48h countdown
- Old candidate removed from Response Tracking

**Status:** ✅ Pass / ❌ Fail

---

### Test 6: Verify Candidate View

**Objective:** Ensure candidates see the correct status

**Steps:**
1. Login as the expired candidate
2. Go to "📊 My Applications"
3. Check the status badge
4. Login as the newly selected candidate
5. Go to "📊 My Applications"
6. Check the status badge

**Expected Result:**
- Expired candidate sees "Waiting List" (Yellow/Orange badge)
- New candidate sees "Selected" (Green badge)

**Status:** ✅ Pass / ❌ Fail

---

### Test 7: Verify Logging

**Objective:** Ensure all operations are logged correctly

**Steps:**
1. After completing Test 3, open `auto_status_manager.log`
2. Check for log entries

**Expected Result:**
```
2026-02-04 12:00:00 - INFO - Starting automatic status check...
2026-02-04 12:00:01 - INFO - Found 1 expired selections to process.
2026-02-04 12:00:02 - INFO - Processing expired selection: John Doe (john@example.com) for Google
2026-02-04 12:00:03 - INFO - Freed up 1 seat for Google
2026-02-04 12:00:04 - INFO - Sent waiting list notification to john@example.com
2026-02-04 12:00:05 - INFO - Promoted candidate: Jane Smith (jane@example.com) for Google
2026-02-04 12:00:06 - INFO - Sent selection notification to jane@example.com
2026-02-04 12:00:07 - INFO - Automatic status check completed.
```

**Status:** ✅ Pass / ❌ Fail

---

### Test 8: Verify Seat Allocation

**Objective:** Ensure seats are properly managed

**Steps:**
1. Before Test 3, note the allocated seats for a company
2. Complete Test 3
3. Check the allocated seats again
4. It should remain the same (freed up, then re-allocated)

**Expected Result:**
- Allocated seats remain constant
- Available seats remain constant
- No seats are lost or duplicated

**Status:** ✅ Pass / ❌ Fail

---

### Test 9: Test with No Waiting List Candidates

**Objective:** Ensure system handles case when no candidates are available

**Steps:**
1. Create a scenario where:
   - A candidate is selected and expires
   - No other candidates are in "Applied" or "Waiting List" status
2. Run manual check: `python auto_status_manager.py`
3. Check the log

**Expected Result:**
- Expired candidate moved to "Waiting List"
- Seat freed up
- Log shows: "No pending candidates to promote for [Company]"
- No errors occur

**Status:** ✅ Pass / ❌ Fail

---

### Test 10: Test Hourly Scheduler

**Objective:** Verify the scheduler runs automatically every hour

**Steps:**
1. Start the app: `streamlit run app.py`
2. Create an expired selection (as in Test 3)
3. Wait for 1 hour (or modify scheduler.py to run every 1 minute for testing)
4. Check `auto_status_manager.log` after the hour

**Expected Result:**
- Log shows automatic check ran at the scheduled time
- Expired selection was processed
- No manual intervention required

**Status:** ✅ Pass / ❌ Fail

---

## Quick Test Checklist

Use this checklist for a quick verification:

- [ ] Scheduler starts automatically with app
- [ ] Manual status check runs without errors
- [ ] Expired selections are detected
- [ ] Status changes to "Waiting List"
- [ ] Seats are freed up correctly
- [ ] Next candidate is selected automatically
- [ ] Emails are sent to both candidates
- [ ] UI shows correct status colors
- [ ] Candidate view shows correct status
- [ ] All operations are logged
- [ ] Seat allocation is correct
- [ ] System handles edge cases (no candidates)

## Troubleshooting

### Issue: Scheduler not starting
**Check:**
- Console output for error messages
- `schedule` package is installed: `pip list | grep schedule`
- No syntax errors in `scheduler.py`

**Fix:**
```bash
pip install schedule
```

### Issue: No expired selections found (but you know there are some)
**Check:**
- Database query is correct
- Timezone issues (use UTC or local time consistently)
- `response_deadline` field is populated

**Fix:**
Manually check the database:
```sql
SELECT id, user_id, company, status, selected_at, response_deadline 
FROM applications 
WHERE status = 'Selected' 
AND response_deadline IS NOT NULL;
```

### Issue: Emails not sending
**Check:**
- Email credentials in `email_service.py`
- SMTP settings are correct
- Internet connection
- Email provider allows SMTP

**Fix:**
Test email sending separately:
```python
from email_service import send_update_to_candidate
send_update_to_candidate("test@example.com", "Selected", "Test Company")
```

### Issue: Next candidate not being selected
**Check:**
- There are candidates with "Applied" or "Waiting List" status
- Company has available seats
- AI engine is working correctly

**Fix:**
Check the log for specific error messages.

## Performance Testing

### Load Test
1. Create 100+ applications for a single company
2. Set 10 of them to "Selected" with expired deadlines
3. Run manual check
4. Measure time taken

**Expected:** Should complete in < 30 seconds

### Concurrent Test
1. Have multiple companies with expired selections
2. Run manual check
3. Verify all are processed correctly

**Expected:** All companies processed, no data corruption

## Database Verification Queries

### Check all statuses
```sql
SELECT status, COUNT(*) as count 
FROM applications 
GROUP BY status;
```

### Check expired selections
```sql
SELECT * FROM applications 
WHERE status = 'Selected' 
AND response_deadline IS NOT NULL 
AND datetime(response_deadline) < datetime('now');
```

### Check waiting list
```sql
SELECT * FROM applications 
WHERE status = 'Waiting List';
```

### Check seat allocation
```sql
SELECT c.name, c.total_seats, c.allocated_seats, 
       (c.total_seats - c.allocated_seats) as available_seats,
       COUNT(a.id) as selected_count
FROM companies c
LEFT JOIN applications a ON c.name = a.company AND a.status = 'Selected'
GROUP BY c.name;
```

## Test Data Setup

If you need to create test data:

```python
# Create test candidates
from database import get_connection
import datetime

conn = get_connection()

# Insert test application
conn.execute("""
    INSERT INTO applications 
    (user_id, company, status, selected_at, response_deadline, skills, sector, cgpa, college_name)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    1,  # user_id
    "Google",
    "Selected",
    datetime.datetime.now().isoformat(),
    (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat(),  # Expired
    "Python, JavaScript",
    "Technology",
    8.5,
    "Test University"
))

conn.commit()
conn.close()
```

## Success Criteria

The feature is working correctly if:

✅ All 10 test scenarios pass
✅ No errors in logs
✅ Emails are sent correctly
✅ UI displays correct information
✅ Database is updated correctly
✅ Seat allocation is accurate
✅ System handles edge cases gracefully

## Reporting Issues

If you find any issues:

1. Check `auto_status_manager.log` for error details
2. Note the exact steps to reproduce
3. Include relevant log entries
4. Check database state before and after
5. Verify email configuration

---

**Happy Testing! 🧪**
