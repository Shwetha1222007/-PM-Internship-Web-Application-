# 🔄 AI-Driven Selection System - Visual Flow Diagram

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CANDIDATES APPLY FOR INTERNSHIPS                  │
│                    (Status: "Applied")                               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AUTOMATIC TRIGGER (Every 30 min)                  │
│                           OR                                         │
│                    MANUAL TRIGGER (Admin/HR Button)                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🤖 AI FILTERING & RANKING                         │
│                                                                      │
│  1. Collect all "Applied" candidates for each company               │
│  2. Calculate AI scores:                                            │
│     • Skills Match: 15 pts per skill                                │
│     • CGPA: CGPA × 5 (max 50 pts)                                   │
│     • Experience: 10 pts if substantial                             │
│     • Rural Priority: +20 pts                                       │
│     • Social Category: +20 pts (SC/ST/OBC/MBC)                      │
│  3. Rank candidates by total score (highest first)                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    📊 STATUS ASSIGNMENT                              │
│                                                                      │
│  Rank #1 → "Selected"      (48-hour deadline set)                   │
│  Rank #2 → "Shortlisted"   (backup candidate)                       │
│  Rank #3+ → "Waiting List" (ranked position maintained)             │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    📧 NOTIFICATION SEQUENCE                          │
│                    (Reverse Order: 3rd → 2nd → 1st)                 │
│                                                                      │
│  Step 1: Notify Waiting List (3rd, 4th, 5th...)                     │
│          "You are on waiting list, ranked #X"                       │
│          ↓ (2 second delay)                                         │
│  Step 2: Notify Shortlisted (2nd)                                   │
│          "You are shortlisted! Backup for promotion"                │
│          ↓ (2 second delay)                                         │
│  Step 3: Notify Selected (1st)                                      │
│          "Congratulations! Contact company within 48 hours"         │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    📨 HR NOTIFICATION                                │
│                                                                      │
│  Subject: ✅ AI FILTERING COMPLETE                                  │
│  Content:                                                           │
│    • Total candidates processed                                     │
│    • Status breakdown (1 Selected, 1 Shortlisted, X Waiting)        │
│    • Top candidate details & AI score                               │
│    • Reminder: 48-hour deadline active                              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ⏰ 48-HOUR MONITORING BEGINS                      │
│                    (Automatic Check Every Hour)                      │
│                                                                      │
│  Selected Candidate has 48 hours to respond                         │
│  Deadline: [Current Time + 48 hours]                                │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
        ┌───────────────────┐  ┌──────────────────┐
        │  CANDIDATE         │  │  DEADLINE        │
        │  RESPONDS          │  │  EXPIRES         │
        │  (Within 48hrs)    │  │  (No Response)   │
        └─────────┬──────────┘  └────────┬─────────┘
                  │                      │
                  ▼                      ▼
        ┌───────────────────┐  ┌──────────────────────────────────┐
        │  ✅ CONFIRMED     │  │  🔄 AUTO-PROMOTION TRIGGERED     │
        │                   │  │                                  │
        │  Status: Selected │  │  1. Move 1st → "Waiting List"   │
        │  Process Complete │  │  2. Free up seat                │
        │                   │  │  3. Notify 1st candidate        │
        └───────────────────┘  │  4. Promote 2nd → "Selected"    │
                               │  5. Set new 48hr deadline       │
                               │  6. Notify 2nd candidate        │
                               │  7. Update seat allocation      │
                               └──────────┬───────────────────────┘
                                          │
                                          ▼
                               ┌──────────────────────┐
                               │  CYCLE REPEATS       │
                               │  for 2nd candidate   │
                               │  (48-hour deadline)  │
                               └──────────────────────┘
```

## Automation Schedule

```
┌─────────────────────────────────────────────────────────────┐
│                    BACKGROUND SCHEDULER                      │
│                    (Runs Automatically)                      │
└─────────────────────────────────────────────────────────────┘

Every 30 Minutes:
├─ Run AI Processing
│  └─ Process all "Applied" candidates
│     └─ Assign statuses & send notifications

Every 1 Hour:
└─ Check 48-Hour Deadlines
   └─ Find expired selections
      └─ Move to waiting list & promote next candidate
```

## Manual Trigger Points

```
┌──────────────────────────────────────────────────────────────┐
│                    ADMIN DASHBOARD                            │
│                                                               │
│  🤖 AI Selection Control Panel                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 🚀 Run AI Selection Process for All Companies         │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  Triggers: Immediate AI processing for ALL companies         │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    HR DASHBOARD                               │
│                                                               │
│  Tab: 🤖 AI Filtered Candidates                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 🚀 Run AI Selection & Ranking Process                 │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  Triggers: AI processing for SPECIFIC company                │
└──────────────────────────────────────────────────────────────┘
```

## Notification Timeline Example

```
Time: 00:00 - AI Processing Starts
         │
         ├─ Candidate Analysis Complete
         │
Time: 00:01 - Notification to Waiting List (Rank #5)
         │     "You are ranked #5 on waiting list"
         │
Time: 00:03 - Notification to Waiting List (Rank #4)
         │     "You are ranked #4 on waiting list"
         │
Time: 00:05 - Notification to Waiting List (Rank #3)
         │     "You are ranked #3 on waiting list"
         │
Time: 00:07 - Notification to Shortlisted (Rank #2)
         │     "You are shortlisted! Backup candidate"
         │
Time: 00:09 - Notification to Selected (Rank #1)
         │     "Congratulations! 48-hour deadline"
         │     Deadline: Time 48:09
         │
Time: 00:11 - HR Notification
              "AI filtering complete for [Company]"

Time: 48:09 - Deadline Expires (if no response)
         │
         ├─ Auto-promotion triggered
         │
Time: 48:10 - Rank #1 → Waiting List notification
         │     "Moved to waiting list (no response)"
         │
Time: 48:12 - Rank #2 → Selected notification
              "Promoted to Selected! New 48hr deadline"
              New Deadline: Time 96:12
```

## Status Flow Diagram

```
┌─────────────┐
│   Applied   │ ← Initial status when candidate applies
└──────┬──────┘
       │
       │ AI Processing
       │
       ▼
┌──────────────────────────────────────────┐
│  AI Ranking & Status Assignment          │
└──────┬───────────────────────────────────┘
       │
       ├─────────────────┬─────────────────┐
       ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌──────────────┐
│  Selected   │   │ Shortlisted │   │ Waiting List │
│  (Rank #1)  │   │  (Rank #2)  │   │  (Rank #3+)  │
│ 48hr deadline│   │   Backup    │   │   Ranked     │
└──────┬──────┘   └──────┬──────┘   └──────────────┘
       │                 │
       │ Responds        │ If #1 expires
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Confirmed  │   │  Selected   │
│             │   │ (Promoted)  │
└─────────────┘   │ 48hr deadline│
                  └──────┬──────┘
                         │
                         │ Expires
                         ▼
                  ┌──────────────┐
                  │ Waiting List │
                  └──────────────┘
```

---

**Created**: February 5, 2026  
**Version**: 1.0  
**Status**: ✅ Active System
