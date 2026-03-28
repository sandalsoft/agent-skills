# Interview Transcript: Reading Habit Tracker

**Date:** 2026-03-23
**Initial prompt:** "I want to build a tool that helps me track my reading habits"

---

## Phase 1: Intake

**Hypothesis:** The user likely reads regularly but lacks visibility into patterns — what they read, how much, how consistently. The stated goal is "tracking," but the real goal is probably behavior change: reading more, reading more intentionally, or finishing more of what they start. The word "habits" (not "books" or "reading list") suggests they care about the behavioral pattern, not just a catalog.

**Gaps and ambiguities identified:**
1. "Reading" — books? Articles? Papers? RSS feeds? All of the above?
2. "Track" — logging what you've read, or tracking progress through things you're currently reading? Or both?
3. "Habits" — does this mean frequency/consistency (like a streak tracker), or is it about understanding patterns over time?
4. No mention of platform, which suggests the user hasn't decided yet
5. No mention of data source — manual entry? Integrations? Import from Goodreads?

**Domain assessment:** Greenfield personal tool. Solo developer, personal use (likely). Software project.

**Acknowledgment:**

So you want something that gives you visibility into your reading behavior — not just a list of books, but the habit itself. There's an interesting tension between making this easy enough that you actually log things vs. rich enough that the data tells you something useful. Let me dig into what you're really after.

---

## Phase 2: Investigation

Greenfield project, no existing codebase. Skipping this phase.

---

## Phase 3: Interview Loop

### Round 1 — Intent & Real Goals

*You said "habits," not "books" or "reading list." That word choice tells me something about what you're actually after.*

**QUESTION:** What are you doing today to keep track of your reading? Spreadsheet, Goodreads, notes app, nothing at all?

**ANSWER:** I use Goodreads but I hate it. The interface is terrible and it's really just a catalog — it tells me what I've read but nothing about how I read. I also have a notes app where I sometimes jot down quotes or thoughts, but it's completely disconnected from the tracking. So it's fragmented: Goodreads for the list, Apple Notes for reflections, and my memory for everything else.

**QUESTION:** What specifically would change in your reading behavior if this tool worked perfectly? Paint me the picture of what "better" looks like six months from now.

**ANSWER:** I'd actually finish more books. Right now I start a lot and abandon them halfway through. I'd also read more consistently — like, I go through weeks where I read every day and then drop off for a month. If I could see those patterns I think I'd be more motivated to stay consistent. And I want my notes and highlights to live with the book, not scattered across apps.

---

**Clarity tracking (internal):**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Intent | 60% | Behavior change + consolidation, not just logging |
| Outcome | 40% | "Finish more books, read consistently" — still vague on specifics |
| Scope | 20% | Very open still |
| Constraints | 10% | Nothing discussed yet |
| Audience | 50% | Personal tool, solo user, uses Goodreads currently |
| Criteria | 10% | Not discussed |

**Overall: ~32%**

---

### Round 2 — Digging Into the Real Problem

*Two distinct problems are emerging here: one is about consistency and motivation (the habit side), and the other is about consolidating notes and reflections (the knowledge side). Those pull in different design directions.*

**QUESTION:** If you had to pick one — the habit/consistency tracking OR the notes/reflections living with each book — which one would you build first?

**ANSWER:** The habit tracking. The notes thing is a nice-to-have, but the real pain is that I have no idea what my reading patterns look like. I want to see streaks, pages per day, time spent — that kind of thing. The notes can come later.

**QUESTION:** When you imagine logging a reading session, what does that interaction look like? Do you sit down and type "read 30 pages of X," or are you thinking more passive — like a timer you start and stop?

**ANSWER:** I think a quick manual log after I finish a session. Like I put the book down and open the app and say "read pages 45 to 78 of this book." Maybe 10 seconds to log it. If it takes longer than that I won't do it. A timer feels like overkill and I'd forget to stop it.

---

**Clarity tracking (internal):**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Intent | 80% | Behavior visibility and motivation through data |
| Outcome | 55% | Streaks, pages/day, time patterns |
| Scope | 35% | Habit tracking first, notes deferred |
| Constraints | 25% | Must be <10 seconds to log |
| Audience | 55% | Personal, mobile-first likely |
| Criteria | 15% | Implicit: "I finish more books" |

**Overall: ~47%**

---

### Round 3 — Platform & Data Shape

*The 10-second logging constraint is the most important thing you've said so far. That basically rules out anything that requires too many taps or typed input. It also means the book selection needs to be fast — you can't be searching a database every time.*

**QUESTION:** Where are you when you finish a reading session — mostly phone, or sometimes at a desk with a laptop? This determines whether we're building a mobile app, a web app, or a CLI.

**ANSWER:** Phone almost always. I read in bed, on the couch, on the train. I'd want an iOS app ideally, but I know that's a bigger lift. A really good mobile web app would work too. I don't want to open a laptop to log that I just read for 20 minutes.

**QUESTION:** What types of reading do you want to track? Just physical books? Kindle? Audiobooks? Articles?

**ANSWER:** Mostly physical books and Kindle. I do audiobooks occasionally but tracking "pages" doesn't make sense there. Let's focus on books for now. I read maybe 2-3 books at a time, finish about 20-25 a year.

---

**Clarity tracking (internal):**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Intent | 80% | Stable |
| Outcome | 60% | Clearer on metrics wanted |
| Scope | 50% | Mobile-first, books only, 2-3 concurrent |
| Constraints | 45% | iOS/mobile web, <10s logging, physical + Kindle |
| Audience | 65% | Solo, reads 20-25 books/year, multi-format |
| Criteria | 20% | Still implicit |

**Overall: ~55%**

**Progress note to user:** We've got a clear picture of the core problem — you want visibility into reading patterns, fast logging from your phone, focused on books. The main gaps now are around what the data visualization looks like, how you get books into the system, and what "success" actually means in measurable terms.

---

### Round 4 — Data Model & UX Flow

*You're reading 2-3 books concurrently and finishing ~25 a year. That's a manageable catalog size, which means we don't need anything fancy for search or organization. But the concurrent reading adds a wrinkle: when you open the app, you need to pick which book you're logging against, and that needs to be instant.*

**QUESTION:** For adding a new book to track, would you want to search by title/ISBN (pulling cover art and metadata from an API), or are you fine typing in a title and maybe the page count manually?

**ANSWER:** Searching by title would be great — I like having the cover art, it makes it feel real. But I don't want it to be a blocker. If the search doesn't find it, I should be able to just type a title and total pages and get going. Open Library or Google Books API would probably work.

**QUESTION:** When you open the app, what do you want to see first? Your currently-reading books with a "log session" button? A dashboard with stats? A daily check-in prompt?

**ANSWER:** My current books front and center with a big obvious way to log a session. I want the stats but they're secondary — the primary action is logging. Maybe the stats are one swipe or tab away. The daily flow is: open app, tap the book I was reading, enter the page I'm on now, done.

---

### Round 5 — Visualization & Motivation

*The interaction model is getting clear: a home screen with your active books, tap-to-log, stats behind a tab. The visualization piece is where this either becomes motivating or just another chore.*

**QUESTION:** When you say you want to see "streaks" and "pages per day," are you thinking something like GitHub's contribution graph (green squares showing daily activity), or more like charts showing trends over weeks and months?

**ANSWER:** The GitHub contribution graph is exactly what I had in mind. That visual is motivating — you don't want to break the chain. But I'd also want a simple line chart or bar chart showing pages per week over time, so I can see if I'm trending up or down. Both, basically. The heatmap for daily motivation, the charts for longer-term trends.

**QUESTION:** What happens when you finish a book? Is there anything you'd want to capture — a rating, a one-line reaction, whether you'd recommend it — or do you just want it moved to a "finished" list?

**ANSWER:** A quick rating (1-5 stars or something) and maybe a one-line note. Nothing heavy. I want to be able to look back and remember if I liked something. But this should be optional and fast — two taps and a sentence max.

---

**Clarity tracking (internal):**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Intent | 85% | Solid |
| Outcome | 75% | Heatmap + trend charts, finish tracking |
| Scope | 65% | Core features clear, notes/reflections deferred |
| Constraints | 55% | Mobile-first, speed-critical, optional enrichment |
| Audience | 70% | Well understood |
| Criteria | 30% | Still needs concrete definition |

**Overall: ~66%**

---

### Round 6 — Data Portability & Technical Shape

*You mentioned hating Goodreads. Part of that frustration is probably vendor lock-in — years of data trapped in a platform you don't control. Worth thinking about whether this tool avoids that same trap.*

**QUESTION:** Do you want to import your existing Goodreads data (they have a CSV export), or start fresh?

**ANSWER:** Importing would be amazing, but only for the "finished" list. I don't need session-level data for old books — just knowing I read them and when I finished. Starting fresh for the active tracking is fine. The CSV import would save me from having to re-enter 150+ books.

**QUESTION:** For the technical stack, two options worth considering. First: a SvelteKit progressive web app (PWA) — installable on your phone home screen, works offline, data syncs when you're back online, and you own the database. Second: a native iOS app with SwiftUI, which gives better OS integration (widgets, notifications for streak reminders) but is a bigger build. Given the 10-second logging priority, which direction appeals to you?

**ANSWER:** The PWA route sounds right. I want to build this relatively quickly and I'm more comfortable with web tech. Native iOS would be nice for widgets and stuff but that's scope creep. A PWA that I can install on my home screen and that works offline covers the core need. If I really want native features later I can wrap it or rebuild.

---

**Progress note to user:** The shape of this is solidifying. SvelteKit PWA, offline-capable, with a fast logging flow, GitHub-style heatmap, trend charts, and Goodreads CSV import for historical data. Two areas still need attention: what the data model looks like under the hood, and how we'll know this actually changed your reading behavior.

---

### Round 7 — Success Criteria & Risks

*We've been focused on what this thing does. Let's talk about whether it'll actually work.*

**QUESTION:** Be honest — what would make you stop using this after two weeks? What's the most likely way this dies?

**ANSWER:** Friction. If it's even slightly annoying to log a session, I'll stop. The other thing is if the stats aren't motivating — if I open the dashboard and it's just numbers that don't make me feel anything, I won't bother looking. It needs to feel rewarding to log, not like homework.

**QUESTION:** Six months from now, how would you measure whether this was worth building? Is it just "I'm reading more consistently" or is there something more concrete?

**ANSWER:** If I'm still using it after six months, that's the main test. More concretely: if I can see that my reading consistency improved — fewer week-long gaps, more books finished vs. abandoned. If I finished 30 books instead of my usual 25, I'd call that a win. Also if I actually know what I read this year without having to think hard about it.

---

**Clarity tracking (internal):**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Intent | 90% | Crystal clear |
| Outcome | 80% | Concrete metrics defined |
| Scope | 70% | Core well-defined, v2 items identified |
| Constraints | 65% | PWA, offline, <10s, web stack |
| Audience | 75% | Well understood |
| Criteria | 60% | "Still using at 6 months," books finished, consistency |

**Overall: ~76%**

---

## Phase 4: Challenge

### Simplifier Challenge

*You've described a heatmap, trend charts, book search API, Goodreads import, offline support, and a polished logging UX. That's a real feature set. Let me push on this.*

**QUESTION:** If you had exactly one weekend to ship a version you'd actually use on Monday morning, what survives the cut? Forget the heatmap, forget the import, forget the charts. What's the absolute minimum that makes you open this app instead of doing nothing?

**ANSWER:** A list of my current books with page count, tap to update my current page, and a simple streak counter — "you've read 5 days in a row." That's it. The heatmap and charts are what make it compelling long-term, but the bare minimum is just "log that I read today and show me my streak." If I built just that, I'd use it. The rest makes it better but isn't day-one essential.

### Edge Finder Challenge

*Here's the scenario that worries me: you're reading a physical book and you don't remember what page you were on last time. Or you read 50 pages across two sessions but only logged once. How precise does this tracking actually need to be?*

**QUESTION:** When the page numbers don't quite add up — you logged page 120 yesterday and today you're at page 185 but you read in two sessions — does that bother you? Or is approximate good enough for the patterns you care about?

**ANSWER:** Approximate is fine. I'm not trying to track to the page. If I log once at the end of the day with my current page number, that's enough. The system can figure out I read 65 pages that day. I don't need per-session precision. The trend data is what matters, not the exact page-by-page timeline.

---

## Phase 5: Crystallize

**Final clarity scores:**

| Dimension | Score |
|-----------|-------|
| Intent | 90% |
| Outcome | 82% |
| Scope | 75% |
| Constraints | 70% |
| Audience | 78% |
| Criteria | 65% |

**Overall: ~80%** — Meets readiness threshold.

---

The spec follows in the next section and is also saved separately to `spec.md`.

---

# Final Spec

See `spec.md` for the standalone version.
