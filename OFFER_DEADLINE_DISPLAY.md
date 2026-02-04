# Offer Deadline Display Feature

## Overview
Candidates can now see the **exact date, time, and countdown** for when their internship offer expires when they view their application details.

## What Was Added

### 1. **Application Detail View**
When a candidate clicks "View Details" on a selected application, they will see:

- **📅 Offer End Date**: Full date (e.g., "February 04, 2026")
- **🕐 Offer End Time**: Exact time (e.g., "11:52 PM")
- **⏰ Time Remaining**: Live countdown (e.g., "47h 30m")
- **📊 Days Remaining**: Number of days left

### 2. **My Applications List View**
In the "My Applications" page, selected candidates see:
- **Compact countdown timer** showing hours and minutes remaining
- **Expiration date and time** in a compact format
- **Color-coded urgency**:
  - 🟢 Green: More than 24 hours remaining
  - 🟡 Yellow: 12-24 hours remaining
  - 🔴 Red: Less than 12 hours remaining

### 3. **Expired Offer Indication**
If the deadline has passed:
- Shows "⏰ Offer Expired" message
- Displays when the deadline was
- Informs candidate that the application will be moved to waiting list

## Visual Examples

### Detail View - Active Offer
```
┌─────────────────────────────────────────────────────────┐
│ ✅ Internship Offer Deadline                           │
│                                                         │
│ You must respond to this offer before the deadline     │
│ expires                                                 │
│                                                         │
│ ┌──────────────────┐  ┌──────────────────┐            │
│ │ Offer Ends On    │  │ Time Remaining   │            │
│ │ 📅 February 06,  │  │ 47h 30m          │            │
│ │    2026          │  │                  │            │
│ │ 🕐 11:52 PM      │  │ (1 days          │            │
│ │                  │  │  remaining)      │            │
│ └──────────────────┘  └──────────────────┘            │
└─────────────────────────────────────────────────────────┘
```

### List View - Active Offer
```
┌─────────────────────────────────────────────────────────┐
│ Technology Internship                          Selected │
│                                                         │
│ 📅 Applied: 2026-02-04 10:00:00                        │
│ 🏢 Company: Google                                     │
│ 📍 Location: Bangalore                                 │
│                                                         │
│ ┌─────────────────────────────────────────────────┐   │
│ │ ✅ Offer Deadline                               │   │
│ │ 47h 30m remaining                               │   │
│ │ Expires: Feb 06, 2026 at 11:52 PM              │   │
│ └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Expired Offer
```
┌─────────────────────────────────────────────────────────┐
│ ⏰ Offer Deadline Expired                              │
│                                                         │
│ The offer deadline was: February 04, 2026 at 11:52 PM  │
│                                                         │
│ This application will be moved to the waiting list in  │
│ the next automatic check.                              │
└─────────────────────────────────────────────────────────┘
```

## Color Coding

The deadline display uses color coding to indicate urgency:

| Time Remaining | Color | Icon | Meaning |
|----------------|-------|------|---------|
| > 24 hours | 🟢 Green (#28a745) | ✅ | Plenty of time |
| 12-24 hours | 🟡 Yellow (#ffc107) | ⚠️ | Getting close |
| < 12 hours | 🔴 Red (#dc3545) | ⏰ | Urgent! |
| Expired | 🔴 Red (#dc3545) | ⏰ | Deadline passed |

## Where It Appears

### For Candidates
1. **My Applications** page (list view)
   - Shows compact countdown for selected applications
   
2. **Application Detail** page
   - Shows full deadline information with date, time, and countdown

### Not Shown For
- Applications with status "Applied" (no deadline yet)
- Applications with status "Rejected" (no longer relevant)
- Applications with status "Waiting List" (deadline was cleared)
- Applications without a `response_deadline` set

## Technical Details

### Data Source
- **Field**: `response_deadline` in the `applications` table
- **Format**: ISO format datetime string (e.g., "2026-02-06T23:52:00")
- **Set When**: HR selects a candidate (48 hours from selection time)

### Calculation
```python
deadline = datetime.datetime.fromisoformat(app['response_deadline'])
now = datetime.datetime.now()
time_left = deadline - now

hours_left = int(time_left.total_seconds() // 3600)
minutes_left = int((time_left.total_seconds() % 3600) // 60)
days_left = time_left.days
```

### Display Format
- **Full Date**: `%B %d, %Y` (e.g., "February 06, 2026")
- **Time**: `%I:%M %p` (e.g., "11:52 PM")
- **Compact Date**: `%b %d, %Y` (e.g., "Feb 06, 2026")

## User Experience Flow

1. **Candidate is selected by HR**
   - `response_deadline` is set to 48 hours from now
   - Status changes to "Selected"

2. **Candidate logs in**
   - Sees "Selected" status on "My Applications" page
   - Sees countdown timer showing time remaining
   - Can click "View Details" for full information

3. **Candidate views details**
   - Sees prominent deadline box with:
     - Exact end date and time
     - Countdown timer
     - Number of days remaining
   - Color changes based on urgency

4. **Deadline approaches**
   - Timer color changes from green → yellow → red
   - Icon changes to indicate urgency

5. **Deadline passes**
   - Shows "Offer Expired" message
   - Informs about automatic waiting list move
   - Next hourly check will process the expiration

## Benefits

1. **Transparency**: Candidates know exactly when they need to respond
2. **Urgency**: Color coding creates appropriate sense of urgency
3. **Clarity**: Shows both absolute time (date/time) and relative time (countdown)
4. **Accessibility**: Information visible in both list and detail views
5. **Real-time**: Countdown updates when page is refreshed

## Files Modified

- **`app.py`**: 
  - Updated `view_applications()` function to show deadline in list view
  - Updated `application_detail()` function to show full deadline information

## Testing

To test this feature:

1. **As HR**: Select a candidate
2. **As Candidate**: 
   - Login and go to "My Applications"
   - Check if countdown appears for selected application
   - Click "View Details"
   - Verify full deadline information is displayed
3. **Test color changes**: Manually adjust deadline in database to test different time ranges
4. **Test expiration**: Set deadline to past time and verify "Expired" message appears

## Future Enhancements

Possible improvements:
- Add auto-refresh to update countdown without page reload
- Add browser notifications when deadline is approaching
- Add "Respond to Offer" button directly on the page
- Show deadline in email notifications
- Add calendar export option (iCal/Google Calendar)

---

**Feature Status**: ✅ Complete and Active

**Added**: February 4, 2026

**Impact**: All selected candidates now see their offer deadline clearly
