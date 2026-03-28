# Reading Habit Tracker

## Problem

Reading is one of those habits where the doing is easy but the consistency is hard. Without visibility into patterns — when you read, how much, whether you're trending up or fading out — it's easy to let weeks slip by without picking up a book. Existing tools like Goodreads act as catalogs, not behavior tools. They tell you *what* you read, not *how* you read.

## Goal

A mobile-first app that makes logging a reading session take under 10 seconds and turns that data into visual feedback that motivates consistent reading.

## Audience

A solo reader who reads 20-30 books a year across physical and Kindle formats, typically 2-3 books concurrently. Reads in bed, on the couch, on a commute. Reaches for this tool right after putting a book down, while still on the couch, on their phone.

## Scope

### In Scope

- **Book management:** Add books by title search (Open Library API) with cover art and metadata. Manual fallback for books not found. Track currently-reading, finished, and abandoned states.
- **Session logging:** Tap a current book, enter current page number, done. System calculates pages read by diffing against last entry. One log per day per book is fine — no need for per-session granularity.
- **Streak tracking:** Consecutive-day reading streak displayed prominently on the home screen.
- **Heatmap visualization:** GitHub-contribution-style calendar showing reading activity by day. Color intensity maps to pages read.
- **Trend charts:** Weekly pages-read bar chart showing long-term patterns. Ability to see trends over 1 month, 3 months, 1 year.
- **Book completion:** When marking a book finished, optional 1-5 rating and one-line note.
- **Goodreads CSV import:** Import historical "read" shelf with titles, dates, and ratings. Session-level data not expected from import.
- **Offline support:** Full functionality without network. Syncs when connectivity returns.
- **PWA installable:** Add-to-home-screen on iOS and Android.

### Out of Scope

- **Notes and highlights system** — deferred to v2. The current tool is about the habit, not the knowledge.
- **Social features** — no sharing, no friends, no public profiles. Personal tool.
- **Audiobook tracking** — page-based logging doesn't map to audio. Revisit if the habit tracking proves valuable.
- **Reading goals / reminders / push notifications** — could be valuable but adds complexity. Evaluate after core usage patterns are established.
- **Native iOS/Android app** — PWA first. Native wrapper or rebuild only if PWA limitations become a real pain point.

## Design

### How It Works

```
Home Screen (currently reading)
  |
  ├── Tap book → Log page number → Done (< 10 seconds)
  |
  ├── "+" button → Search/add new book
  |
  └── Tab: Stats
        ├── Streak counter
        ├── Heatmap (year view)
        ├── Pages/week bar chart
        └── Books finished this year
```

The home screen shows 2-3 currently-reading books with cover art, title, and progress (page 120 / 340). Tapping a book opens a minimal logging view: a number input pre-focused, enter the page you're on, submit. The previous page is shown for reference.

Stats live one tab away. The heatmap is the centerpiece — a year of reading at a glance. Below it, a bar chart of pages per week and a count of books finished.

### Key Decisions

- **Page number, not pages read:** The user enters their current page, not how many pages they read. The system diffs against the previous entry. This is faster and less error-prone — you always know what page you're on.
- **Daily granularity, not session-level:** Multiple reading sessions in a day collapse into one data point. This simplifies the data model and matches how the user actually thinks about their reading.
- **PWA over native:** Faster to build, cross-platform by default, and the core interaction (number input + submit) doesn't need native capabilities. Widgets and notifications are the only real loss, and those are deferred features anyway.
- **Open Library API over Google Books:** Free, no API key required for basic lookups, good coverage. Google Books is a fallback option if Open Library coverage is insufficient.
- **Approximate tracking is fine:** The goal is trend data and motivation, not precision. If page numbers don't perfectly add up across sessions, that's acceptable.

### Open Questions

- **Data persistence strategy:** IndexedDB for offline-first local storage, with optional cloud sync (Supabase or similar) for cross-device access? Or start local-only and add sync later?
  *Current thinking:* Start with IndexedDB only. Cloud sync is a v2 concern. Keep the data model sync-friendly so it's not a rewrite later.
- **Streak definition:** Does "reading day" mean any pages logged, or a minimum threshold (e.g., 10 pages)?
  *Current thinking:* Any pages logged counts. Lower the bar to maintain the habit. A 1-page day still counts.

## Constraints

- Logging interaction must complete in under 10 seconds from app open to submission
- Must work offline (reading often happens without connectivity)
- Must be installable as PWA on iOS Safari and Android Chrome
- SvelteKit with Tailwind v4 tech stack
- No account creation required — local-first, single user

## Success Criteria

- **Still in active use after 6 months** — the primary signal that logging friction is low enough
- **Reading consistency improves** — fewer multi-week gaps between reading sessions, visible in the heatmap
- **Books finished increases** — from ~25/year baseline toward 30+
- **The user can answer "what did I read this year?" in 5 seconds** by opening the app

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Logging friction too high, user stops after 2 weeks | Medium | Fatal | Ruthlessly optimize the logging flow. Prototype and time it before building anything else. The "tap book, enter page, done" flow must be tested on a real phone. |
| Stats aren't motivating enough to check regularly | Medium | High | Make the heatmap visually satisfying (D3.js, not a basic grid). Streak counter should feel rewarding. Consider subtle animations on logging. |
| PWA limitations on iOS (no push notifications, limited background sync) | Low | Medium | Core functionality doesn't need push or background sync. These are v2 features that might justify native if needed. |
| Open Library API coverage gaps for niche or new books | Low | Low | Manual book entry as fallback. Good enough for launch. |
| Data loss (no cloud backup, phone dies) | Low | High | Export-to-JSON feature as a stopgap. Cloud sync in v2. |
