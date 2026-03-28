# Reading Habit Tracker — Interview Transcript

## Round 1: Understanding the Core Problem

**QUESTION:** What's driving this? Are you trying to read more, read better, or just keep a record of what you've read?

**ANSWER:** A mix. I want to keep a record, but I also want to understand my patterns — like how much I actually read versus how much I think I read. I'll set a goal to read 30 books a year and then realize in November I've only finished 12. I want something that keeps me honest.

**QUESTION:** What are you using right now to track reading, if anything?

**ANSWER:** Goodreads, loosely. I mark books as "read" after I finish them, but I never update progress along the way. So it's more of a finished-books list than a habit tracker. I also sometimes jot notes in Apple Notes but they're scattered and I never go back to them.

**QUESTION:** What specifically bugs you about Goodreads? What would make you reach for a different tool?

**ANSWER:** It's social-media-first. I don't care about reviews or what my friends are reading. The UI is cluttered. And it doesn't track the *habit* — it tracks the *catalog*. I want to know things like: did I read today? How many days in a row? Am I on pace for my goal? Goodreads tells me I'm 5 books behind schedule, but that's not actionable.

## Round 2: Target User and Platform

**QUESTION:** Is this just for you, or do you imagine other people using it too?

**ANSWER:** Starts as just for me, but I think a lot of readers have this same frustration. If it works well I'd want to ship it publicly.

**QUESTION:** Where do you want to use this — phone, desktop, both? And when in your day would you interact with it?

**ANSWER:** Primarily phone. I read before bed and on my commute. I want to log a session quickly — like, I just read for 30 minutes, I'm on page 147. Maybe a quick note if something stood out. Desktop would be nice for reviewing stats and browsing my history, but mobile is where the daily interaction happens.

**QUESTION:** Would you use it as a native app or is a web app fine?

**ANSWER:** Web app is fine if it feels good on mobile. I don't need push notifications or offline support right now. A solid PWA would work.

## Round 3: Core Features and Data Model

**QUESTION:** Walk me through your ideal interaction. You just finished a reading session — what do you do?

**ANSWER:** Open the app. It already knows what book I'm reading. I tap "log session," enter how long I read or what page I'm on now (it should figure out pages read from my last entry), and optionally add a short note. Done. Under 15 seconds. Then maybe once a week I look at my stats — streak, pace, time spent, that kind of thing.

**QUESTION:** What does "pace" mean to you? Pages per day? Books per month? Something else?

**ANSWER:** Both, actually. Pages per day tells me about my daily habit. Books per month (or per year) tells me if I'm hitting my goal. I'd want to see a projected finish date for my current book too — "at your current pace, you'll finish this in 8 days."

**QUESTION:** You mentioned notes. How important is that? Are we talking highlights and annotations, or more like a reading journal?

**ANSWER:** More like a journal. Short thoughts — "this chapter on X changed how I think about Y" or "the pacing dragged here." Not highlights from the text itself. I want to be able to look back at a book and remember what I thought while reading it, not just that I read it.

**QUESTION:** What about tracking books you want to read — a "to read" list?

**ANSWER:** Yeah, but keep it simple. A list I can add to and pull from. No elaborate shelving system. When I finish a book, I want to pick my next one from the list easily.

## Round 4: Goals, Streaks, and Motivation

**QUESTION:** You mentioned streaks and goals. How do you want goals to work — annual book count? Daily reading time? Both?

**ANSWER:** Annual book count as the big goal. But the daily habit is what actually gets me there, so I want a daily target too — something like "read for at least 20 minutes a day." The streak tracks consecutive days meeting that daily target.

**QUESTION:** What happens when you miss a day? Some apps use streak-freezes or grace periods. Others just reset to zero. What feels right?

**ANSWER:** Hard reset feels punishing and makes me want to stop using the app. I'd like a grace day — maybe one miss per week doesn't break the streak. Or show the streak but also show total days read this month, so even if the streak breaks I can see I read 26 out of 30 days and feel good about that.

**QUESTION:** Do you want any kind of reminders or nudges?

**ANSWER:** Maybe a gentle evening reminder if I haven't logged anything that day. But it should be optional and not aggressive. I'm not looking for a guilt machine.

## Round 5: Data and Insights

**QUESTION:** What stats or visualizations would you actually look at? Think about what would make you open the stats page on purpose.

**ANSWER:** A year-in-review style heatmap, like GitHub's contribution graph but for reading. Time read per day. A chart of books finished over time. Average reading speed (pages per hour) per book — I'm curious if I read fiction faster than nonfiction. And a simple list of books finished this year with dates.

**QUESTION:** Would you want to categorize books — genre, fiction vs nonfiction, that kind of thing?

**ANSWER:** Yeah, at least fiction/nonfiction. Genre would be nice but I don't want to spend time classifying things. If the app could pull metadata (genre, page count, author, cover image) from an ISBN or title search, that would save a lot of manual entry.

**QUESTION:** Where would that metadata come from? Are you okay with pulling from a public API like Open Library or Google Books?

**ANSWER:** Absolutely. Open Library is fine. I just don't want to type in page counts manually for every book.

## Round 6: Technical and Scope

**QUESTION:** You mentioned SvelteKit earlier in your stack preferences. Are you thinking SvelteKit for this?

**ANSWER:** Yeah. SvelteKit with Tailwind, deployed on Vercel. PostgreSQL for the database. Standard stack for me.

**QUESTION:** Authentication — do you need user accounts from day one, or is this single-user to start?

**ANSWER:** Single-user to start. I can add auth later if I open it up. For now, maybe just a simple password or even no auth if it's behind a private URL.

**QUESTION:** Any integrations you'd want? Kindle sync, Apple Books, importing from Goodreads?

**ANSWER:** Goodreads CSV import would be huge for bootstrapping. Kindle sync would be a dream but sounds hard. Let's call Goodreads import a V1 nice-to-have and Kindle a future thing.

**QUESTION:** What about the reading-list source — would you ever want to pull from a "want to read" list on Goodreads or is manual entry fine?

**ANSWER:** Manual is fine for the to-read list. It's usually short — maybe 10-20 books at a time.

## Round 7: Edge Cases and Boundaries

**QUESTION:** Do you ever read multiple books at once?

**ANSWER:** Yeah, usually two — one fiction, one nonfiction. The app should handle that. I should be able to log a session for whichever book I was reading.

**QUESTION:** Audiobooks? Or strictly physical/ebook?

**ANSWER:** I listen to audiobooks on walks. I'd want to track those too. The metric shifts from pages to time (or percentage complete). Maybe the session log should support both — pages for physical/ebook, time/percentage for audio.

**QUESTION:** What about re-reads? If you read a book again, is that a separate entry?

**ANSWER:** Yeah, treat it as a new read. Separate entry, separate notes, counts toward the annual goal.

## Final Clarifications

**QUESTION:** If you could only build three features for V1, what are they?

**ANSWER:** Session logging (quick, daily), progress tracking with projected finish dates, and the reading heatmap/stats. Everything else can wait.

**QUESTION:** What does success look like six months from now?

**ANSWER:** I open this app every day. I actually know how much I read. I've finished more books than last year because the visibility changed my behavior. And the app is clean enough that I'd be proud to show it to someone.

---

# Final Specification

See [spec.md](spec.md) for the complete specification derived from this interview.
