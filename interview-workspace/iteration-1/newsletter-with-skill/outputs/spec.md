# The Monday AI Briefing — Newsletter Spec

## Problem

Mid-level managers at non-technical companies are caught between AI hype and AI dismissal. They hear about tools constantly but have no practical guidance on what to actually use, for what, and how to start. Existing AI newsletters either target developers or deal in abstract strategy. Nobody is writing the "here's what to do Monday morning" version for a Director of Customer Success or a VP of Marketing.

## Goal

A weekly email newsletter that gives non-technical managers one practical AI tool walkthrough per issue -- specific enough to act on immediately, plain enough that no technical background is required.

## Audience

Mid-level managers (directors, senior managers, VPs) at mid-market companies (200-2000 employees). They manage teams of 5-20 people. They're responsible for operational output -- customer success, marketing, operations, sales, HR. They're curious about AI, have tried ChatGPT a few times, and want to do more but feel overwhelmed by the options. They don't read tech blogs. They spend time on LinkedIn.

**Key persona:** Sarah, Director of Customer Success. Manages 12 people. Wants her team to write better QBR summaries and triage tickets faster. Got overwhelmed by "top 10 AI tools" listicles. Needs someone to say: "Use this tool. Here's how. Here's a template."

**Anti-persona:** CTOs evaluating enterprise AI platforms. Developers comparing model architectures. Anyone who knows what "fine-tuning" means.

## Scope

### In Scope

- **One deep tool walkthrough per issue** -- a specific tool, a specific use case, a real scenario, and a copy-paste prompt template or setup guide
- **Short "what I'm watching" section** -- 2-3 links with one-line takes (secondary to the walkthrough; can be dropped in time-constrained weeks)
- **Weekly cadence** on Beehiiv, with 2-3 pre-written evergreen issues as buffer for busy weeks
- **LinkedIn as primary distribution channel** -- repurpose newsletter content into LinkedIn posts to drive subscriptions
- **Free tier only at launch** -- no paid content for at least 6 months
- **Honest coverage of limitations** -- every tool recommendation includes where it falls short and when not to use it

### Out of Scope

- Comprehensive tool comparison roundups (not actionable, impossible to maintain)
- Enterprise AI strategy content (too broad, different audience)
- Technical deep dives on how models work (violates the core premise)
- Paid tier or premium content (deferred until audience is established)
- Podcast, video, or other media formats (deferred; newsletter is the product)
- Affiliate links or sponsored content (deferred until 5,000+ subscribers minimum)

## Design

### How It Works

```
Weekly cycle (3-4 hours total):

Mon-Tue: Identify tool/use case from own workflow or reader suggestions (30 min)
Wed-Thu: Test tool, document the walkthrough, draft issue (2 hrs)
Fri:     Edit, add "watching" links, schedule send (1 hr)
Sat AM:  Newsletter sends
Mon:     Repurpose core walkthrough as LinkedIn post
```

**Issue structure:**
1. One-line hook (what the reader will be able to do after reading)
2. Tool walkthrough (400-600 words) -- scenario, step-by-step, screenshot-friendly
3. Copy-paste template (prompt, configuration, or setup snippet)
4. Honest limitations (when not to use this, what to watch for)
5. "What I'm watching" (2-3 links, one line each) -- optional section

**Buffer system:** Maintain 2-3 pre-written evergreen issues (tool setups that don't date) for vacation weeks, product launches, or low-energy periods. Sending a lighter issue beats skipping a week.

### Key Decisions

- **Beehiiv over Substack**: Better growth tools (referral program, recommendation network), full email list ownership. Substack has more organic discovery but locks you in.
- **Weekly over biweekly**: Builds habit and momentum faster. Sustainable at 3-4 hours/week given the author already uses AI tools daily and the core content (one tool, one walkthrough) is tightly scoped.
- **One tool per issue, not roundups**: Depth beats breadth. A single actionable walkthrough is worth more than five shallow mentions. This is the core differentiator.
- **Free at launch**: Splitting attention between free and paid content too early will hurt quality and growth. Monetize through sponsorships once audience is established (5K+ subscribers).
- **LinkedIn-first distribution**: The target audience lives on LinkedIn. The newsletter content naturally repurposes into LinkedIn posts. This is the lowest-friction growth channel given an existing 2,200-connection network.

### Open Questions

- **LinkedIn content strategy**: How to repurpose newsletter content into LinkedIn posts that drive subscriptions without giving away the whole issue. Proposed approach: share the "hook" and one insight from the walkthrough, link to the full issue.
- **Liability framing**: When recommending tools that managers apply to real business output, need a standard disclaimer and a consistent editorial practice of noting limitations. Not solved yet -- worth consulting similar newsletters for their approach.
- **Growth beyond LinkedIn**: Once LinkedIn organic reaches its ceiling, what's next? Paid ads, cross-promotions with adjacent newsletters, guest posts? Defer this decision until month 3-4 when baseline growth rate is understood.

## Constraints

- **Time budget**: 3-4 hours per week maximum, author has a full-time PM role
- **Solo operation**: No editor, no contributors, no design help (at least initially)
- **Platform**: Beehiiv (free tier to start, upgrade as needed)
- **Tone**: Conversational, opinionated, practical. Never reads like a tech blog. Reader should feel like getting advice from a smart friend, not reading documentation.
- **Tool coverage**: Only tools the author has personally tested. No secondhand recommendations.

## Success Criteria

**6-month checkpoint (working):**
- 2,000+ subscribers
- 45%+ open rate (industry average for newsletters this size is ~35-40%)
- Inbound reader messages weekly saying the content helped them do something specific
- No missed weeks (buffer system working)
- At least 2-3 sponsorship inquiries from relevant companies

**6-month checkpoint (not working):**
- Under 500 subscribers
- Open rate below 30%
- No qualitative feedback from readers
- Multiple missed weeks or declining motivation

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Writer burnout from weekly cadence + full-time job | Medium | High | Evergreen buffer system, tightly scoped format (one tool only), permission to send lighter issues |
| Crowded AI newsletter space, hard to stand out | High | Medium | Differentiation is the practical, non-technical angle. Most AI newsletters target developers or executives, not operational managers. Lean into specificity. |
| Tool recommendations age poorly as AI landscape shifts | Medium | Medium | Date-stamp recommendations, revisit popular ones quarterly, be transparent about when advice is stale |
| Distribution plateau after exhausting LinkedIn network | Medium | Medium | Cross-promotion with adjacent newsletters, repurpose into LinkedIn carousel/video formats, explore Beehiiv recommendation network |
| Reader applies recommendation poorly, blames newsletter | Low | Medium | Standard disclaimer, honest limitations section in every issue, frame as "how I use this" not "you should do this" |

---

**Next step:** Write issue #1. Pick the tool walkthrough that's closest to done (the ChatGPT custom instructions use case for customer success came up naturally during this interview -- start there). Set up the Beehiiv account, publish the first issue to the 15 existing internal readers as a soft launch, then open it up on LinkedIn.
