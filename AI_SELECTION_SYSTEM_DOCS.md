# 🤖 AI-Driven Automatic Candidate Selection System

## Overview
This document describes the comprehensive AI-driven automatic candidate selection and notification system implemented for the PM Internship Web Application.

## System Architecture

### Core Components

1. **`ai_auto_selector.py`** - Main AI processing engine
2. **`ai_engine.py`** - AI scoring and ranking algorithm
3. **`auto_status_manager.py`** - 48-hour deadline monitoring and auto-promotion
4. **`scheduler.py`** - Background task scheduler
5. **`email_service.py`** - Notification system

## Workflow

### Phase 1: AI Filtering & Ranking

When applications are submitted or AI processing is triggered:

1. **AI collects all "Applied" candidates** for each company
2. **AI calculates scores** based on:
   - Skills match (15 points per matching skill)
   - CGPA (up to 50 points: CGPA × 5)
   - Experience (10 points if substantial)
   - Rural priority (20 points)
   - Social category priority (20 points for SC/ST/OBC/MBC)
3. **AI ranks candidates** by total score (highest to lowest)

### Phase 2: Status Assignment

Based on AI ranking:

| Rank | Status | Details |
|------|--------|---------|
| **1st** | **Selected** | 48-hour response deadline set |
| **2nd** | **Shortlisted** | Backup candidate, ready for promotion |
| **3rd+** | **Waiting List** | Ranked position maintained |

### Phase 3: Notification Sequence

Notifications are sent in **reverse order** (3rd → 2nd → 1st):

1. **Waiting List candidates (3rd+)** receive notification first
   - Message: "You are on the waiting list, ranked #X"
   
2. **Shortlisted candidate (2nd)** receives notification
   - Message: "You are shortlisted! If the top candidate doesn't respond within 48 hours, you will be automatically promoted"
   
3. **Selected candidate (1st)** receives notification last
   - Message: "Congratulations! You are selected. You must contact the company within 48 hours"
   - Deadline: Current time + 48 hours

### Phase 4: HR Notification

After all candidate notifications are sent:

- **HR receives a completion email** with:
  - Total candidates processed
  - Top candidate details and AI score
  - Status breakdown (1 Selected, 1 Shortlisted, X Waiting List)
  - Reminder about 48-hour deadline

## Automatic Deadline Monitoring

### 48-Hour Response Tracking

The system automatically monitors selected candidates:

1. **Hourly checks** run via background scheduler
2. If deadline passes without response:
   - Selected candidate → Moved to "Waiting List"
   - Seat is freed up
   - Candidate receives notification about status change
3. **Automatic promotion** of 2nd candidate:
   - Shortlisted → Selected (with new 48-hour deadline)
   - Notification sent to newly selected candidate
   - HR notified of the promotion

## Automation Schedule

| Task | Frequency | Purpose |
|------|-----------|---------|
| **AI Processing** | Every 30 minutes | Process new "Applied" candidates |
| **Deadline Check** | Every 1 hour | Monitor 48-hour deadlines and auto-promote |

## Manual Triggers

### Admin Dashboard
Administrators can manually trigger AI processing:

1. Navigate to **Admin Dashboard**
2. Scroll to **🤖 AI Selection Control Panel**
3. Click **"🚀 Run AI Selection Process for All Companies"**
4. System processes all pending applications immediately

### HR Dashboard
HR can trigger AI processing for their company:

1. Navigate to **HR Dashboard**
2. Go to **"🤖 AI Filtered Candidates"** tab
3. Click **"🚀 Run AI Selection & Ranking Process"**

## Notification Examples

### For Selected Candidate (1st)
```
Subject: OFFICIAL NOTIFICATION: Internship Application Update - [Company]

🎉 Congratulations! You have been SELECTED for the internship at [Company]. 
You must contact the company within 48 hours to confirm your acceptance. 
Deadline: February 7, 2026 at 01:30 PM
```

### For Shortlisted Candidate (2nd)
```
Subject: OFFICIAL NOTIFICATION: Internship Application Update - [Company]

🌟 Great news! You have been SHORTLISTED for the internship at [Company]. 
You are the second-ranked candidate. If the top candidate doesn't respond 
within 48 hours, you will be automatically promoted to Selected status.
```

### For Waiting List Candidates (3rd+)
```
Subject: OFFICIAL NOTIFICATION: Internship Application Update - [Company]

📋 Your application for [Company] has been placed on the Waiting List. 
You are ranked #3. You will be notified if a position becomes available.
```

### For HR (Completion)
```
Subject: ✅ AI FILTERING COMPLETE: [Company] - X Candidates Processed

The AI-driven candidate filtering process has been completed for [Company].

Processing Summary:
- Total Candidates Processed: X
- Status Assignments: 1 Selected, 1 Shortlisted, X Waiting List
- Notifications Sent: All candidates notified (3rd → 2nd → 1st)

Top Selected Candidate:
- Name: [Name]
- AI Score: [Score]
- Response Deadline: 48 hours from selection
```

## AI Scoring Example

### Candidate Profile:
- **Skills**: Python, Java, React (3 skills)
- **CGPA**: 8.5
- **Experience**: "2 years internship at startup"
- **Rural**: Yes
- **Social Category**: OBC

### Score Calculation:
```
Skills Match: 3 × 15 = 45 points
CGPA: 8.5 × 5 = 42.5 points
Experience: 10 points (substantial)
Rural Priority: 20 points
Social Category: 20 points
------------------------
Total AI Score: 137.5 points
```

## Database Updates

### New Fields Added to `applications` table:
- `ai_score` (REAL) - AI-calculated score
- `selected_at` (TIMESTAMP) - When candidate was selected
- `response_deadline` (TIMESTAMP) - 48-hour deadline
- `hr_rejection_reason` (TEXT) - If HR rejects top candidate

## Logging

All AI processing is logged to:
- **`ai_auto_selector.log`** - AI processing events
- **`auto_status_manager.log`** - Deadline monitoring and promotions

## Key Features

✅ **Fully Automated** - Runs every 30 minutes without manual intervention  
✅ **Fair Ranking** - AI considers skills, academics, and social priorities  
✅ **Transparent** - All candidates notified of their status  
✅ **Time-Bound** - 48-hour deadline enforced automatically  
✅ **Auto-Promotion** - Backup candidates promoted if needed  
✅ **HR Oversight** - HR notified at every stage  
✅ **Manual Override** - Admin/HR can trigger processing anytime  

## Testing the System

### Test Scenario 1: New Applications
1. Have 3+ candidates apply for a company
2. Wait for automatic processing (30 min) OR trigger manually
3. Verify:
   - 1st candidate gets "Selected" status with deadline
   - 2nd candidate gets "Shortlisted" status
   - 3rd+ get "Waiting List" status
   - All receive emails in order: 3rd → 2nd → 1st
   - HR receives completion email

### Test Scenario 2: Deadline Expiry
1. Wait for 48 hours after selection (or manually set past deadline)
2. Wait for hourly check OR run `python auto_status_manager.py`
3. Verify:
   - 1st candidate moved to "Waiting List"
   - 2nd candidate promoted to "Selected" with new deadline
   - Both candidates receive notifications
   - Seat allocation updated correctly

## Troubleshooting

### AI Not Processing
- Check `ai_auto_selector.log` for errors
- Verify candidates have "Applied" status
- Ensure scheduler is running (check Streamlit terminal)

### Notifications Not Sent
- Check email credentials in `email_service.py`
- Verify SMTP settings
- Check for email errors in logs

### Deadline Not Triggering
- Verify `auto_status_manager.py` is running
- Check system time is correct
- Review `auto_status_manager.log`

---

**Implementation Date**: February 5, 2026  
**Version**: 1.0  
**Status**: ✅ Active and Operational
