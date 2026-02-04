# 📊 Waiting List System - Visual Flow Diagram

## 🔄 Complete System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CANDIDATE APPLICATION PHASE                       │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    Multiple Candidates Apply
                                  │
                                  ▼
        ┌──────────────────────────────────────────────┐
        │  Candidate A → TCS Bangalore (CGPA: 9.0)     │
        │  Candidate B → TCS Bangalore (CGPA: 8.5)     │
        │  Candidate C → TCS Bangalore (CGPA: 8.2)     │
        │  Candidate D → TCS Bangalore (CGPA: 7.8)     │
        │  Candidate E → TCS Bangalore (CGPA: 7.5)     │
        └──────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      HR SELECTION PROCESS                            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    HR Clicks "Run Selection"
                                  │
                                  ▼
        ┌──────────────────────────────────────────────┐
        │         AI RANKING ENGINE                     │
        │  • Skills Match (15 pts per skill)           │
        │  • CGPA Score (up to 50 pts)                 │
        │  • Experience (10 pts)                       │
        │  • Rural Priority (20 pts)                   │
        │  • Social Category (20 pts)                  │
        └──────────────────────────────────────────────┘
                                  │
                                  ▼
        ┌──────────────────────────────────────────────┐
        │           RANKED CANDIDATES                   │
        │  1. Candidate B → Score: 95.5                │
        │  2. Candidate A → Score: 92.0                │
        │  3. Candidate C → Score: 88.5                │
        │  4. Candidate D → Score: 85.0                │
        │  5. Candidate E → Score: 82.0                │
        └──────────────────────────────────────────────┘
                                  │
                    Check Available Seats (3 seats)
                                  │
                                  ▼
        ┌──────────────────────────────────────────────┐
        │  Top 3 → SELECTED                            │
        │  Remaining 2 → WAITING LIST                  │
        └──────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
    ┌───────────────────────┐     ┌───────────────────────┐
    │   SELECTED (Top 3)    │     │  WAITING LIST (2)     │
    │  • Candidate B        │     │  • Candidate D (#1)   │
    │  • Candidate A        │     │  • Candidate E (#2)   │
    │  • Candidate C        │     │                       │
    └───────────────────────┘     └───────────────────────┘
                │                              │
                │                              │
                ▼                              ▼
    ┌───────────────────────┐     ┌───────────────────────┐
    │  📧 Selection Email   │     │ 📧 Waiting List Email │
    │  • Congratulations!   │     │  • Your Position: #1  │
    │  • 24hr to Accept     │     │  • Your Score: 85.0   │
    │  • Dashboard Link     │     │  • Alternatives:      │
    └───────────────────────┘     │    - Chennai (4 seats)│
                                  │    - Mumbai (3 seats) │
                                  │    - Hyderabad (2)    │
                                  └───────────────────────┘
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  ALTERNATIVE LOCATION SYSTEM                         │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    System Searches for Alternatives
                                  │
                                  ▼
        ┌──────────────────────────────────────────────┐
        │  Same Company, Different Locations           │
        │  • TCS Chennai → 4 seats available           │
        │  • TCS Mumbai → 3 seats available            │
        │  • TCS Hyderabad → 2 seats available         │
        └──────────────────────────────────────────────┘
                                  │
                    Alternative Offers Created
                                  │
                                  ▼
        ┌──────────────────────────────────────────────┐
        │      CANDIDATE DASHBOARD VIEW                │
        │                                              │
        │  📋 Waiting List Status                      │
        │  Company: TCS                                │
        │  Preferred: Bangalore                        │
        │  Position: #1                                │
        │  Score: 85.0                                 │
        │                                              │
        │  🌍 Alternative Locations:                   │
        │  ┌────────────────────────────────┐          │
        │  │ TCS Chennai (4 seats)          │          │
        │  │ [Accept] [Reject]              │          │
        │  └────────────────────────────────┘          │
        │  ┌────────────────────────────────┐          │
        │  │ TCS Mumbai (3 seats)           │          │
        │  │ [Accept] [Reject]              │          │
        │  └────────────────────────────────┘          │
        └──────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
        ┌───────────────────┐       ┌───────────────────┐
        │  ACCEPT           │       │  REJECT           │
        │  Alternative      │       │  Alternative      │
        └───────────────────┘       └───────────────────┘
                    │                           │
                    ▼                           ▼
        ┌───────────────────┐       ┌───────────────────┐
        │  Status: SELECTED │       │  Status: WAITING  │
        │  Location: Chennai│       │  Can Apply to     │
        │  Seat Allocated   │       │  Other Companies  │
        └───────────────────┘       └───────────────────┘
                    │                           │
                    ▼                           ▼
        ┌───────────────────┐       ┌───────────────────┐
        │ 📧 Confirmation   │       │  🔄 Re-apply      │
        │ Email Sent        │       │  to New Companies │
        └───────────────────┘       └───────────────────┘
```

## 📊 Database Relationships

```
┌─────────────┐
│   users     │
│  (id, name, │
│   email)    │
└──────┬──────┘
       │
       │ 1:N
       │
       ▼
┌─────────────────┐
│  applications   │
│  (id, user_id,  │
│   company,      │
│   location_pref,│
│   status)       │
└────────┬────────┘
         │
         │ 1:1
         │
         ▼
┌──────────────────┐
│  waiting_list    │
│  (id, app_id,    │
│   user_id,       │
│   company,       │
│   rank_position, │
│   ai_score)      │
└────────┬─────────┘
         │
         │ 1:N
         │
         ▼
┌───────────────────────┐
│  alternative_offers   │
│  (id, waiting_list_id,│
│   user_id,            │
│   alternative_location│
│   response)           │
└───────────────────────┘
```

## 🎯 Decision Tree for Candidates

```
                    Application Submitted
                            │
                            ▼
                    ┌───────────────┐
                    │ AI Evaluation │
                    └───────┬───────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        ┌───────────┐           ┌─────────────┐
        │ SELECTED  │           │ WAITING LIST│
        └───────────┘           └──────┬──────┘
                │                      │
                ▼                      ▼
        ┌───────────┐           ┌─────────────┐
        │ Accept?   │           │ Alternatives│
        └─┬───────┬─┘           │ Available?  │
          │       │             └──────┬──────┘
        Yes       No                   │
          │       │         ┌──────────┴──────────┐
          ▼       ▼         │                     │
      ┌─────┐ ┌─────┐      Yes                   No
      │DONE │ │LOST │       │                     │
      └─────┘ └─────┘       ▼                     ▼
                      ┌─────────────┐      ┌──────────┐
                      │ View Alts   │      │ Re-apply │
                      └──────┬──────┘      │ or Wait  │
                             │             └──────────┘
                    ┌────────┴────────┐
                    │                 │
                  Accept            Reject
                    │                 │
                    ▼                 ▼
              ┌──────────┐      ┌──────────┐
              │ SELECTED │      │ Re-apply │
              │ New Loc  │      │ or Wait  │
              └──────────┘      └──────────┘
```

## 📈 Status Transitions

```
Applied → Selected (Top Ranked)
   │
   └→ Waiting List → Accepted Alternative → Selected
         │
         ├→ Rejected Alternative → Still Waiting
         │
         └→ Promoted (if selected declines) → Selected
```

## 🔔 Notification Flow

```
Selection Process Triggered
         │
         ├─→ Selected Candidates
         │   └─→ 📧 Congratulations Email
         │       └─→ Dashboard Updated
         │
         └─→ Waiting List Candidates
             └─→ 📧 Waiting List Email
                 ├─→ Position & Score
                 ├─→ Alternative Locations
                 └─→ Dashboard Updated
                     └─→ Alternative Offers Visible
```

## 💡 Key Benefits Visualization

```
┌────────────────────────────────────────────────────────┐
│                    BENEFITS                             │
├────────────────────────────────────────────────────────┤
│                                                         │
│  🎯 Fair Selection                                     │
│     └─→ AI-based objective ranking                     │
│                                                         │
│  📊 Transparency                                       │
│     └─→ Candidates see exact scores & positions        │
│                                                         │
│  🌍 Flexibility                                        │
│     └─→ Multiple location options                      │
│                                                         │
│  ⚡ Efficiency                                         │
│     └─→ Automated notifications & processing           │
│                                                         │
│  🔄 Choice                                             │
│     └─→ Accept, reject, or re-apply                    │
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

**This visual guide helps understand the complete flow of the waiting list system!**
