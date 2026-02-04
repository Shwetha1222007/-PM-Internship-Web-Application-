# Quick Start Guide: Automatic Status Management

## What's New? 🎉

Your PM Internship application now has **automatic status management**! When a selected candidate doesn't respond within **48 hours**, the system automatically:

1. Moves them to the **Waiting List**
2. Frees up the seat
3. Selects the **next best candidate** automatically
4. Sends email notifications to both candidates

## For HR Managers

### How to Use

1. **Select Candidates as Usual**
   - Go to HR Dashboard → AI Filtered Candidates tab
   - Click "✅ Accept" on your preferred candidate
   - They now have 48 hours to respond

2. **Monitor Response Deadlines**
   - Go to "⏰ 48-Hour Response Tracking" tab
   - See countdown timers for each selected candidate
   - Green = plenty of time, Yellow = getting close, Red = almost expired

3. **Automatic Processing**
   - The system checks every hour
   - Expired selections are automatically moved to waiting list
   - Next best candidate is automatically selected
   - All parties are notified via email

4. **Manual Override (Optional)**
   - If you see an expired selection, you can click "🗑️ Manually Process Now"
   - This immediately processes it instead of waiting for the next hourly check

### What You'll See

**Before Expiry:**
```
Time Remaining: 23h 45m (Green)
```

**After Expiry:**
```
⏰ EXPIRED: John Doe
Candidate did not respond within 48 hours
This will be automatically moved to waiting list and the next candidate 
will be selected in the next hourly check.
```

## For Candidates

### What to Expect

1. **When Selected:**
   - You receive an email: "OFFICIAL NOTIFICATION: Internship Application Update"
   - Status shows: **Selected** (Green)
   - Message: "Please respond within 48 hours to confirm your acceptance"

2. **If You Don't Respond in 48 Hours:**
   - You receive another email
   - Status changes to: **Waiting List** (Yellow/Orange)
   - Message: "You're still being considered. If a seat becomes available, you'll be automatically selected"

3. **If You're Next in Line:**
   - You automatically get selected when a seat opens up
   - You receive a selection email
   - You get another 48 hours to respond

### Viewing Your Status

1. Login to your account
2. Go to "📊 My Applications"
3. Check the status badge:
   - 🟢 **Selected** = You're in! Respond within 48 hours
   - 🟡 **Waiting List** = Still being considered
   - 🟠 **Applied** = Under review
   - 🔴 **Rejected** = Not selected this time

## For Administrators

### Monitoring the System

1. **Check Logs**
   - File: `auto_status_manager.log`
   - Shows all automatic operations
   - Includes timestamps and details

2. **View Statistics**
   - Admin Dashboard shows all statuses
   - Filter by "Waiting List" to see candidates in queue
   - Monitor seat allocation per company

### Log Example
```
2026-02-04 12:00:00 - INFO - Starting automatic status check...
2026-02-04 12:00:01 - INFO - Found 2 expired selections to process.
2026-02-04 12:00:02 - INFO - Processing expired selection: John Doe for Google
2026-02-04 12:00:03 - INFO - Freed up 1 seat for Google
2026-02-04 12:00:04 - INFO - Promoted candidate: Jane Smith for Google
2026-02-04 12:00:05 - INFO - Automatic status check completed.
```

## Status Colors Reference

| Status | Color | Meaning |
|--------|-------|---------|
| Selected | 🟢 Green | Candidate selected, awaiting response |
| Waiting List | 🟡 Yellow/Orange | Candidate in queue, may be auto-selected |
| Applied | 🟠 Orange | Application under review |
| Rejected | 🔴 Red | Not selected |

## Frequently Asked Questions

### Q: How often does the system check for expired selections?
**A:** Every hour, automatically.

### Q: Can I change the 48-hour deadline?
**A:** Yes! Edit the code in `app.py` (line 2216) and `auto_status_manager.py` (line 117). Change `hours=48` to your preferred duration.

### Q: What if I want to manually process an expired selection?
**A:** Go to the "⏰ 48-Hour Response Tracking" tab and click "🗑️ Manually Process Now" on the expired selection.

### Q: Will candidates be notified?
**A:** Yes! All status changes trigger automatic email notifications.

### Q: What happens if there are no candidates in the waiting list?
**A:** The system will check for "Applied" candidates and select the best one using AI ranking.

### Q: Can I see who's in the waiting list?
**A:** Yes! In the HR Dashboard, filter by status "Waiting List" or check the "Waiting List" section in the AI Filtered Candidates tab.

### Q: Is the scheduler running?
**A:** Check the console output when you start the app. You should see: "Background scheduler started - checking every hour"

## Troubleshooting

### Issue: Scheduler not starting
**Solution:** 
```bash
pip install schedule
```
Then restart the app.

### Issue: Emails not being sent
**Solution:** Check `email_service.py` for correct email credentials and SMTP settings.

### Issue: Candidates not being auto-promoted
**Solution:** 
1. Check if there are available seats
2. Verify there are candidates with "Applied" or "Waiting List" status
3. Review `auto_status_manager.log` for errors

## Need Help?

- Check the detailed documentation: `AUTO_STATUS_MANAGEMENT.md`
- Review the logs: `auto_status_manager.log`
- Contact the system administrator

---

**Remember:** The system works automatically in the background. You don't need to do anything special - just select candidates as usual, and the system handles the rest! 🚀
