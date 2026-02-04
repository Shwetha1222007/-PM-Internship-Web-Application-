# Automatic Status Management Feature

## Overview
This feature implements an **automatic status management system** that handles candidate selections that expire after 48 hours without a response. When a candidate doesn't respond within the deadline, the system automatically:

1. ✅ Moves the candidate from "Selected" to "Waiting List" status
2. ✅ Frees up the allocated seat
3. ✅ Sends notification email to the candidate
4. ✅ Automatically promotes the next best candidate from the waiting list
5. ✅ Sends selection notification to the newly promoted candidate

## How It Works

### 48-Hour Response Window
When an HR manager selects a candidate:
- The candidate's status is set to "Selected"
- A `selected_at` timestamp is recorded
- A `response_deadline` is set to 48 hours from selection time
- The candidate receives an email notification

### Automatic Processing
A background scheduler runs **every hour** and:
1. Checks for all "Selected" candidates whose `response_deadline` has passed
2. For each expired selection:
   - Changes status from "Selected" to "Waiting List"
   - Clears the `selected_at` and `response_deadline` fields
   - Decrements the company's allocated seat count
   - Sends a "Waiting List" notification email to the candidate
   - Automatically selects the next best candidate using AI ranking
   - Sends a "Selected" notification to the newly promoted candidate

### AI-Based Candidate Promotion
When promoting the next candidate, the system:
- Retrieves all candidates with "Applied" or "Waiting List" status for that company
- Prioritizes "Waiting List" candidates over "Applied" candidates
- Uses the AI ranking algorithm to score candidates based on:
  - Skills match
  - CGPA
  - Experience
  - Rural area priority (+20 points)
  - Reserved category priority (+20 points)
- Selects the highest-ranked candidate
- Sets a new 48-hour deadline for the promoted candidate

## Files Created

### 1. `auto_status_manager.py`
The core module that handles:
- `check_and_update_expired_selections()`: Main function that finds and processes expired selections
- `promote_next_candidate()`: Promotes the next best candidate from waiting list
- `run_status_check()`: Entry point for the scheduled task
- Logging to `auto_status_manager.log` file

### 2. `scheduler.py`
Background scheduler that:
- Runs the status check every hour
- Operates in a separate daemon thread
- Starts automatically when the app launches
- Can be run standalone for testing

### 3. Updated Files
- **`app.py`**: Integrated the scheduler to start on app launch, updated all references from 24 to 48 hours
- **`email_service.py`**: Added support for "Waiting List" status and custom messages
- **`database.py`**: Already has the necessary fields (`selected_at`, `response_deadline`)

## Usage

### For HR Managers
1. **Select a Candidate**: Click "✅ Accept" on a candidate in the AI Filtered Candidates tab
2. **Monitor Deadline**: View the "⏰ 48-Hour Response Tracking" tab to see time remaining
3. **Automatic Processing**: If 48 hours pass, the system automatically handles everything
4. **Manual Override**: You can manually process an expired selection using "🗑️ Manually Process Now"

### For Candidates
1. **Selection Notification**: Receive email when selected with 48-hour deadline
2. **Waiting List Notification**: Receive email if moved to waiting list due to no response
3. **Automatic Promotion**: If you're next in line, you'll be automatically selected and notified

### For Administrators
1. **View Logs**: Check `auto_status_manager.log` for all automatic processing activities
2. **Monitor Status**: All status changes are logged with timestamps
3. **Email Tracking**: All email notifications are logged

## Running the Scheduler

### Automatic (Recommended)
The scheduler starts automatically when you run the Streamlit app:
```bash
streamlit run app.py
```

### Manual Testing
To test the scheduler independently:
```bash
python scheduler.py
```

To run a one-time status check:
```bash
python auto_status_manager.py
```

## Status Flow Diagram

```
Applied → Selected (48h deadline) → [No Response] → Waiting List
                                  → [Response] → Confirmed
                                  
Waiting List → [Seat Available] → Selected (48h deadline)
```

## Email Notifications

### Selection Email
- **Subject**: "OFFICIAL NOTIFICATION: Internship Application Update - [Company]"
- **Status**: Selected (Green)
- **Message**: Congratulations with 48-hour response deadline

### Waiting List Email
- **Subject**: "OFFICIAL NOTIFICATION: Internship Application Update - [Company]"
- **Status**: Waiting List (Yellow/Warning)
- **Message**: Explanation that they're still being considered

### Automatic Promotion Email
- **Subject**: "OFFICIAL NOTIFICATION: Internship Application Update - [Company]"
- **Status**: Selected (Green)
- **Message**: Congratulations with 48-hour response deadline

## Logging

All automatic operations are logged to `auto_status_manager.log`:
```
2026-02-04 12:00:00 - INFO - Starting automatic status check...
2026-02-04 12:00:01 - INFO - Found 2 expired selections to process.
2026-02-04 12:00:02 - INFO - Processing expired selection: John Doe (john@example.com) for Google
2026-02-04 12:00:03 - INFO - Freed up 1 seat for Google
2026-02-04 12:00:04 - INFO - Sent waiting list notification to john@example.com
2026-02-04 12:00:05 - INFO - Promoted candidate: Jane Smith (jane@example.com) for Google
2026-02-04 12:00:06 - INFO - Sent selection notification to jane@example.com
2026-02-04 12:00:07 - INFO - Automatic status check completed.
```

## Configuration

### Change Check Frequency
Edit `scheduler.py` line 24:
```python
# Check every hour (default)
schedule.every(1).hours.do(run_status_check)

# Or check every 30 minutes
schedule.every(30).minutes.do(run_status_check)
```

### Change Response Deadline
Edit `app.py` line 2216 and `auto_status_manager.py` line 117:
```python
# 48 hours (default)
deadline = selected_time + datetime.timedelta(hours=48)

# Or 72 hours
deadline = selected_time + datetime.timedelta(hours=72)
```

## Troubleshooting

### Scheduler Not Starting
- Check console for error messages
- Verify `schedule` package is installed: `pip install schedule`
- Check `auto_status_manager.log` for errors

### Emails Not Sending
- Verify email credentials in `email_service.py`
- Check spam folder
- Review logs for SMTP errors

### Candidates Not Being Promoted
- Ensure there are candidates in "Applied" or "Waiting List" status
- Check that the company has available seats
- Review `auto_status_manager.log` for details

## Benefits

1. **Fully Automated**: No manual intervention required
2. **Fair Process**: Next best candidate automatically gets the opportunity
3. **Transparent**: All actions are logged and candidates are notified
4. **Efficient**: Seats don't remain blocked by non-responsive candidates
5. **Scalable**: Handles multiple companies and candidates simultaneously

## Future Enhancements

Possible improvements:
- Add SMS notifications in addition to email
- Implement candidate response confirmation system
- Add dashboard widget showing upcoming expirations
- Create detailed analytics on response rates
- Add configurable deadlines per company
