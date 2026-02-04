# Automatic Status Management - Visual Flow

## Process Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                  AUTOMATIC STATUS MANAGEMENT FLOW                    │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────┐
    │  HR Manager Selects  │
    │     Candidate        │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Status: "Selected"  │
    │  Deadline: 48 hours  │
    │  Seat: Allocated     │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │  📧 Email Sent to    │
    │     Candidate        │
    │  "You're Selected!"  │
    └──────────┬───────────┘
               │
               ▼
         ┌─────────────┐
         │  Wait for   │
         │  Response   │
         └──────┬──────┘
                │
                ▼
    ╔═══════════════════════════╗
    ║ Response within 48 hours? ║
    ╚═══════════╦═══════════════╝
                │
        ┌───────┴────────┐
        │                │
       YES              NO
        │                │
        ▼                ▼
┌───────────────┐  ┌──────────────────────┐
│  Candidate    │  │  ⏰ Hourly Scheduler │
│  Confirmed    │  │  Detects Expiration  │
│   ✅ END      │  └──────────┬───────────┘
└───────────────┘             │
                              ▼
                   ┌──────────────────────┐
                   │ Status: "Waiting     │
                   │         List"        │
                   │ Deadline: Cleared    │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  Seat Freed Up       │
                   │  (allocated_seats-1) │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  📧 Email Sent to    │
                   │     Candidate        │
                   │  "Moved to Waiting   │
                   │      List"           │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  🤖 AI Engine Finds  │
                   │  Next Best Candidate │
                   │  (Ranked by Score)   │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  Next Candidate      │
                   │  Status: "Selected"  │
                   │  Deadline: 48 hours  │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  📧 Email Sent to    │
                   │  New Candidate       │
                   │  "You're Selected!"  │
                   └──────────┬───────────┘
                              │
                              ▼
                        (Loop back to
                         "Wait for Response")
```

## Timeline View

```
Hour 0:  ┌─────────────────────────────────────────────┐
         │ Candidate Selected by HR                    │
         │ Status: Selected                            │
         │ Email: Selection notification sent          │
         └─────────────────────────────────────────────┘

Hour 1:  ┌─────────────────────────────────────────────┐
         │ Scheduler Check #1                          │
         │ Status: Still Selected (47h remaining)      │
         │ Action: None                                │
         └─────────────────────────────────────────────┘

Hour 2:  ┌─────────────────────────────────────────────┐
         │ Scheduler Check #2                          │
         │ Status: Still Selected (46h remaining)      │
         │ Action: None                                │
         └─────────────────────────────────────────────┘

  ...    (Scheduler checks every hour)

Hour 48: ┌─────────────────────────────────────────────┐
         │ Scheduler Check #48                         │
         │ Status: Still Selected (0h remaining)       │
         │ Action: None (deadline just reached)        │
         └─────────────────────────────────────────────┘

Hour 49: ┌─────────────────────────────────────────────┐
         │ Scheduler Check #49                         │
         │ Status: EXPIRED! (-1h)                      │
         │ Action: AUTOMATIC PROCESSING                │
         │   1. Status → "Waiting List"                │
         │   2. Seat freed up                          │
         │   3. Email sent (Waiting List)              │
         │   4. Next candidate selected                │
         │   5. Email sent (Selection)                 │
         └─────────────────────────────────────────────┘
```

## Status Transition Diagram

```
┌──────────┐
│ Applied  │ ◄─────────────────────────────┐
└────┬─────┘                                │
     │                                      │
     │ HR Accepts                           │
     ▼                                      │
┌──────────┐                                │
│ Selected │                                │
│ (48h)    │                                │
└────┬─────┘                                │
     │                                      │
     ├─────► Candidate Responds ──► Confirmed
     │
     │ 48h Pass, No Response
     ▼
┌──────────────┐
│ Waiting List │
└──────┬───────┘
       │
       │ Seat Available
       │ (Auto-promotion)
       ▼
   ┌──────────┐
   │ Selected │
   │ (48h)    │
   └──────────┘
```

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         SYSTEM COMPONENTS                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  Streamlit   │         │  Background  │         │   Database   │
│     App      │◄───────►│  Scheduler   │◄───────►│   (SQLite)   │
│   (app.py)   │         │(scheduler.py)│         │              │
└──────┬───────┘         └──────┬───────┘         └──────────────┘
       │                        │
       │                        │
       │                        ▼
       │                 ┌──────────────┐
       │                 │ Auto Status  │
       │                 │   Manager    │
       │                 │(auto_status_ │
       │                 │ manager.py)  │
       │                 └──────┬───────┘
       │                        │
       │                        │
       ▼                        ▼
┌──────────────┐         ┌──────────────┐
│    Email     │         │  AI Engine   │
│   Service    │         │ (ai_engine.  │
│(email_service│         │     py)      │
│    .py)      │         │              │
└──────────────┘         └──────────────┘
       │                        │
       │                        │
       ▼                        ▼
┌──────────────┐         ┌──────────────┐
│  Candidate   │         │  Candidate   │
│    Email     │         │   Ranking    │
│ Notifications│         │  & Selection │
└──────────────┘         └──────────────┘
```

## Data Flow

```
1. HR Action:
   HR Dashboard → app.py → Database (UPDATE status='Selected')
                        → Email Service (Send selection email)

2. Scheduler (Every Hour):
   scheduler.py → auto_status_manager.py → Database (SELECT expired)
                                         → Database (UPDATE to Waiting List)
                                         → Email Service (Send waiting list email)
                                         → AI Engine (Rank candidates)
                                         → Database (UPDATE next candidate)
                                         → Email Service (Send selection email)

3. Candidate View:
   Candidate Login → app.py → Database (SELECT applications)
                           → Display status with color coding
```

## Color Coding Legend

```
┌─────────────────────────────────────────────────────────┐
│                    STATUS COLORS                        │
├─────────────────────────────────────────────────────────┤
│  🟢 Selected       │ #28a745 (Green)                    │
│  🟡 Waiting List   │ #ffc107 (Yellow/Orange)            │
│  🟠 Applied        │ #ffb703 (Orange)                   │
│  🔴 Rejected       │ #dc3545 (Red)                      │
└─────────────────────────────────────────────────────────┘
```

## Key Metrics

```
┌─────────────────────────────────────────────────────────┐
│                   SYSTEM METRICS                        │
├─────────────────────────────────────────────────────────┤
│  Check Frequency:     Every 1 hour                     │
│  Response Deadline:   48 hours                         │
│  Auto-promotion:      Immediate (on next check)        │
│  Email Notifications: 3 types (Selection, Waiting,     │
│                       Auto-promotion)                   │
│  Logging:            All operations logged              │
└─────────────────────────────────────────────────────────┘
```

---

**Note:** All diagrams are simplified representations. Actual implementation includes error handling, logging, and additional validation steps.
