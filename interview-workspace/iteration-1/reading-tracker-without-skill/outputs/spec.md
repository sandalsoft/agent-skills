# Reading Habit Tracker — Specification

## Problem Statement

Existing tools (Goodreads, scattered notes) track book catalogs but not the reading habit itself. The gap between "books I've finished" and "how I actually spend time reading" leaves readers without actionable data to build consistent habits or hit annual goals.

## Product Vision

A fast, mobile-first reading tracker that treats reading as a daily habit, not a social activity. Log sessions in under 15 seconds. See your patterns. Finish more books.

## Target User

Solo reader who wants accountability and self-knowledge. Reads 1-2 books concurrently (mix of physical, ebook, audiobook). Sets annual reading goals but struggles with consistency.

## Tech Stack

- **Frontend**: SvelteKit (Svelte 5), Tailwind CSS v4, shadcn-svelte
- **Database**: PostgreSQL (normalized schema)
- **Deployment**: Vercel
- **Book metadata**: Open Library API
- **Auth**: None for V1 (single-user, private deployment). Add auth when opening to multiple users.

## Core Data Model

### Books
| Field | Type | Notes |
|-------|------|-------|
| id | uuid | PK |
| title | text | Required |
| author | text | |
| isbn | text | For metadata lookup |
| cover_url | text | From Open Library |
| total_pages | int | null for audiobooks |
| total_duration_minutes | int | null for page-based books |
| format | enum | physical, ebook, audiobook |
| category | enum | fiction, nonfiction |
| genre | text | Optional, pulled from metadata |
| status | enum | reading, finished, to-read, abandoned |
| started_at | timestamp | |
| finished_at | timestamp | |
| created_at | timestamp | |

### Reading Sessions
| Field | Type | Notes |
|-------|------|-------|
| id | uuid | PK |
| book_id | uuid | FK to books |
| date | date | When the session occurred |
| duration_minutes | int | How long the session lasted |
| pages_start | int | null for audiobooks |
| pages_end | int | null for audiobooks |
| percent_start | numeric | For audiobooks |
| percent_end | numeric | For audiobooks |
| note | text | Optional journal entry |
| created_at | timestamp | |

Pages read is derived: `pages_end - pages_start`. For audiobooks, progress is percentage-based.

### Goals
| Field | Type | Notes |
|-------|------|-------|
| id | uuid | PK |
| year | int | |
| book_target | int | Annual book count goal |
| daily_minutes_target | int | Daily reading time target |
| streak_grace_days_per_week | int | Default: 1 |

### Derived Metrics (computed, not stored)
- Current streak (consecutive days meeting daily target, with grace allowance)
- Days read this month / total days
- Average reading speed per book (pages/hour)
- Projected finish date for current books
- Books finished this year vs. goal pace

## V1 Features (Priority Order)

### 1. Session Logging
The primary interaction. Must be fast.

- Open app, see current book(s) prominently displayed
- Tap a book to log a session
- Enter duration and current page/percentage (app calculates delta from last session)
- Optional short note (journal-style, not highlight-style)
- Save in one tap
- Support multiple concurrent books

### 2. Progress Tracking
- Per-book progress bar (pages or percentage)
- Projected finish date based on rolling 7-day reading pace
- "At your current pace" messaging: "You'll finish this book in ~8 days"
- Books finished this year vs. annual goal, shown as simple fraction and progress bar

### 3. Stats and Heatmap
- Year heatmap (GitHub contribution graph style) showing reading days and intensity (minutes)
- Time read per day/week/month (bar chart)
- Books finished over time (cumulative line chart)
- Average reading speed by book, with fiction vs. nonfiction comparison
- List of books finished this year with completion dates

### 4. Book Management
- Add books by title search (Open Library API for metadata, cover, page count)
- Manual entry fallback
- To-read list: simple ordered list, drag to reorder
- Mark books as reading, finished, abandoned
- Support for re-reads (separate entry per read)

### 5. Goals and Streaks
- Set annual book target and daily minutes target
- Streak counter with configurable grace (default: 1 miss per week doesn't break streak)
- Monthly summary: days read out of days in month
- Streak displayed on home screen

### 6. Daily Reminder (Optional)
- Evening notification if no session logged today
- User-configurable time
- Can be disabled entirely

## V1 Nice-to-Have
- Goodreads CSV import (bootstrap finished-books history)
- Dark mode (first-class, not afterthought)

## Post-V1 / Future
- User accounts and authentication
- Kindle/Apple Books sync
- Social features (if ever — keep optional)
- Book recommendations based on reading history
- Annual year-in-review shareable summary
- Tags and custom shelves

## Key UX Principles

1. **15-second logging.** If it takes longer, people stop using it. The session log flow is the most important screen in the app.
2. **Visibility changes behavior.** The heatmap and streak aren't gamification for its own sake. They make the invisible (daily reading time) visible.
3. **No guilt.** Grace days on streaks. "26 of 30 days" framing instead of "you missed 4 days." Progress, not perfection.
4. **Catalog is secondary.** This isn't a book database. It's a habit tracker that happens to involve books. Keep book management minimal.
5. **Mobile-first, desktop-friendly.** Daily interaction happens on the phone. Stats review happens on desktop. Design for both, prioritize phone.

## Pages / Routes

| Route | Purpose |
|-------|---------|
| `/` | Home: current books, today's reading status, streak, quick-log buttons |
| `/log/[bookId]` | Session logging form |
| `/books` | Library: reading, finished, to-read tabs |
| `/books/add` | Search + add a book |
| `/books/[id]` | Book detail: progress, sessions, notes, projected finish |
| `/stats` | Heatmap, charts, annual progress |
| `/goals` | Set/edit annual and daily goals |
| `/import` | Goodreads CSV import (nice-to-have) |

## Success Criteria

Six months after launch:
- App used daily (session logged 5+ days/week)
- User has clear, data-backed understanding of reading habits
- More books finished than the previous year
- App is clean and fast enough to show to other people without embarrassment
