---
name: clean-web-design
description: "Guide for building clean, modern web front-ends with a professional design system featuring HSL CSS custom properties, Tailwind CSS utility classes, light/dark mode support, and shadcn/ui-inspired component architecture. Use this skill whenever building a web UI, React component, dashboard, landing page, web app, or any front-end that should look polished and professional. Also use when the user mentions wanting a 'clean' or 'modern' design, asks for dark mode support, needs a consistent design system, or wants to avoid vibecoded / generic AI SaaS aesthetics. This skill covers typography, color tokens, spacing, component patterns (cards, buttons, inputs, modals, navigation), layout structure, data visualization theming, loading states, copy and trust, and responsive design that avoids generic AI aesthetics."
---

# Clean Web Design System

This skill captures a professional, minimal design aesthetic for web front-ends. The style is characterized by restrained use of color, generous whitespace, crisp typography, and seamless light/dark mode transitions — the kind of design you'd see in a well-crafted SaaS dashboard or modern productivity tool.

The system is built on three pillars:
1. **HSL CSS custom properties** as a semantic color token layer
2. **Tailwind CSS** for utility-first styling
3. **Component composition** with small, reusable UI primitives (shadcn/ui style)

Read `references/design-tokens.md` for the complete color token system and CSS/Tailwind setup.
Read `references/component-patterns.md` for copy-pasteable component code.

## Design Philosophy

Every pixel of border, shadow, and color should serve a purpose. The palette is intentionally narrow — mostly neutrals with a single primary accent — so the user's *content* takes center stage. Dark mode is a first-class citizen achieved by swapping CSS custom property values, not by overriding individual styles.

If something doesn't need to be colorful, it shouldn't be. Text is the primary communicator. Color is reserved for status indicators (green = good, red = bad, amber = caution) and interactive affordances (primary buttons, active nav items, focus rings).

Product UI (dashboards, settings, data tools) and marketing surfaces share tokens but not costumes. A utility app should feel native and quiet. A marketing page should feel specific to the product. Neither should look like the default "AI SaaS" landing page.

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Commit to a distinct direction: brutally minimal, maximalist chaos, luxury/refined, lo-fi/zine, dark/moody, soft/pastel, editorial/magazine, brutalist/raw, retro-futuristic, handcrafted/artisanal, organic/natural, art deco/geometric, playful/whimsical, industrial/utilitarian, etc. There are infinite varieties to start from and surpass. Use these as inspiration, but the final design should feel singular, with every detail working in service of one cohesive direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?


## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Typography carries the design's singular voice. Font choices should be inseparable from the aesthetic direction. Display type should be expressive, even risky. Body text should be legible, refined. Pair them like actors in a scene. Work the full typographic range: size, weight, case, spacing to establish hierarchy. Inter, Geist, and Space Grotesk are the current "I picked a modern font" defaults — do not use them as the personality. System stacks are fine for utility/dashboard UIs (native, fast). Marketing and branded surfaces need a distinctive pairing, not Arial/Roboto and not the Inter/Geist/Space Grotesk trio.
- **Color & Theme**: Commit to a cohesive aesthetic. Palettes should take a clear position: bold and saturated, moody and restrained, or high-contrast and minimal. Lead with a dominant color, punctuate with sharp accents. Avoid timid, non-committal distributions. Use CSS variables for consistency. Do not default to purple-on-black, neon-on-navy, rainbow-per-card, or a wash of basic pastels — those read as uncommitted AI palettes, not a direction.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Hover should confirm affordance (`transition-colors`, opacity, a quiet border shift) — not scale, glow, bounce, or an animated arrow on every interactive element.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap and z-depth. Diagonal flow. Grid-breaking elements. Dramatic scale jumps. Full-bleed moments. Generous negative space OR controlled density. Do not default a landing page to a bento mosaic or a row of three identical feature cards. Those layouts can exist when the content actually wants them; they are not the starting template.
- **Backgrounds & Visual Details**: Create atmosphere and depth when the direction calls for it — not as default decoration. Noise, grain, print texture, or a tinted canvas can serve a committed look. Do not start from the vibecode hero: harsh multi-stop gradients, floating radial orbs, dot-grid wallpaper, liquid-glass chrome, or stacked drop shadows. Glass, gradients, and glow are tools for a specific material story, not the costume you put on every SaaS page.

NEVER ship the generic AI SaaS costume: Inter / Geist / Space Grotesk as the "designed" typeface; purple-and-black or neon/pastel filler palettes; harsh gradients and radial orbs; decorative liquid glass; sparkle icons and emoji-as-UI; a colored left stripe on every card; fake terminal windows; three feature cards / three pricing tiers / a bento grid as the automatic landing-page structure. Several of these tells are from UiSavior's "30 reasons your site looks vibecoded" (Saved #35): https://x.com/uisavior/status/2094368948452016305
INSTEAD: type that matches the context (system stack for tools, distinctive pairing for brand). A committed palette. Layouts that follow the content. Real product evidence. Bespoke details. Every choice rooted in rich context.

Build creatively on the user's intent, and make unexpected choices that feel genuinely designed for the context. Every design should feel distinct. Actively explore the full range: light and dark themes, unexpected font pairings, substantially varied aesthetic directions. Let the specific context drive choices, NOT familiar defaults.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, elegance, and precision. All designs need careful attention to spacing, typography, and subtle details. Excellence comes from executing the vision well.

Remember: Claude is capable of extraordinary, award-worthy creative work. Don't hold back, show what's truly possible, and commit relentlessly to a distinctive and unforgettable vision.

## Quality Checklist

Before delivering any frontend:

### Visual Impact
- [ ] Does it have a clear point of view?
- [ ] Would someone remember this tomorrow?
- [ ] Does it avoid the generic AI SaaS costume (see Frontend Aesthetics Guidelines) — not just "purple gradients"?

### Technical Excellence
- [ ] Responsive across all breakpoints?
- [ ] Accessible (ARIA labels, keyboard navigation)?
- [ ] Performance optimized (lazy loading, code splitting)?
- [ ] Cross-browser tested?

### Attention to Detail
- [ ] Custom focus states defined?
- [ ] Async views use skeleton loaders that match the real layout (not a blank page or a lone spinner)?
- [ ] Hover and motion confirm affordance without performing (no decorative scale/glow/animated arrows)?
- [ ] Typography hierarchy consistent, and the typeface is not Inter / Geist / Space Grotesk used as "personality"?
- [ ] Marketing/product pages show a real demo or screenshot — not a fake terminal or abstract cards in place of the product?

### Copy & Trust
- [ ] Copy avoids em-dash stacks and the "it's not X, it's Y" pivot?
- [ ] No invented testimonials, logos, or social proof?
- [ ] Public product/marketing surfaces link to Terms and a Privacy Policy (real pages, even if stubbed for the user to fill)?

## Tech Stack

The design system is framework-flexible but optimized for:
- **React** with TypeScript
- **Tailwind CSS** with `darkMode: ['class']`
- **Icons**: Lucide React is fine as a quiet utility set in product UI (16×16 at `h-4 w-4` default). Do not treat Lucide — or any single default set — as the marketing-page aesthetic. When personality matters, pick a distinctive family (Phosphor, Radix Icons, a custom subset) or draw a few marks; never decorate with sparkles, emoji, or animated arrows.
- **clsx + tailwind-merge** via a `cn()` utility for conditional class merging
- **Radix UI** for accessible unstyled primitives (dialogs, dropdowns)
- **D3.js** or **Recharts** for data visualization

For other frameworks (Vue, Svelte, plain HTML), adapt the patterns but keep the same visual language. The color tokens, spacing, and typography choices transfer directly.

## Color System

Colors are HSL values (without the `hsl()` wrapper) in CSS custom properties on `:root` and `.dark`. This lets Tailwind apply opacity modifiers like `bg-primary/10`.

There's no "blue-500" or "gray-300" here. Every color has a *semantic name* describing its purpose. This makes dark mode trivial — swap the variable values and every component updates automatically.

### Core Tokens

| Token | Purpose | Light | Dark |
|---|---|---|---|
| `--background` | Page background | white | near-black navy |
| `--foreground` | Primary text | near-black navy | near-white |
| `--card` / `--card-foreground` | Card surfaces & text | white / dark | dark / light |
| `--primary` / `--primary-foreground` | Primary actions, emphasis | dark navy / near-white | near-white / dark navy |
| `--secondary` / `--secondary-foreground` | Secondary surfaces | pale blue-gray / dark | dark blue-gray / light |
| `--muted` / `--muted-foreground` | Muted backgrounds, subdued text | pale / medium gray | dark / lighter gray |
| `--accent` / `--accent-foreground` | Hover states, active nav | pale / dark | dark / light |
| `--destructive` / `--destructive-foreground` | Error, danger | red / white | muted red / white |
| `--border` | All borders | light gray | dark blue-gray |
| `--input` | Input borders | light gray | dark blue-gray |
| `--ring` | Focus rings | dark navy | light gray |
| `--radius` | Border radius base | 0.5rem | 0.5rem |

`--background` in the default tokens is pure white. That is a dashboard canvas, not a rule that every page must be `#FFFFFF`. Prefer a slightly tinted canvas (warm paper, cool gray, or the dark navy) unless high-contrast white is the committed look. Soft-everywhere radius (`rounded-2xl` / `rounded-3xl` on cards, buttons, and inputs) is the other default tell — keep the token at `0.5rem` for product UI, or pick a sharper/mixed radius for brand surfaces. Do not "round everything a little" as decoration.

See `references/design-tokens.md` for exact HSL values and the full CSS setup.

### Status Colors

For semantic indicators outside the token system, use Tailwind colors with dark variants:

- **Success**: `text-green-600 bg-green-100` / `dark:text-green-400 dark:bg-green-900`
- **Error**: `text-red-600 bg-red-100` / `dark:text-red-400 dark:bg-red-900`
- **Warning**: `text-amber-600 bg-amber-100` / `dark:text-amber-400 dark:bg-amber-900`
- **Info**: `text-blue-600 bg-blue-100` / `dark:text-blue-400 dark:bg-blue-900`

Badge pattern: `bg-{color}-100 text-{color}-800 dark:bg-{color}-900 dark:text-{color}-200`

These colors are semantic status only. Do not paint each feature, pricing tier, or bento cell a different bright hue — that rainbow-per-card look is a vibecode tell.

## Typography

**Product / dashboard UI:** use a system font stack (no webfont) so the tool feels native and stays fast.

**Marketing / branded surfaces:** load a distinctive pairing that matches the direction. Do not "upgrade" a page by switching to Inter, Geist, or Space Grotesk — that is the current vibecode default, not a design choice. Arial and Roboto are equally generic.

| Element | Classes | When to use |
|---|---|---|
| Page title | `text-3xl font-bold tracking-tight` | Top of each page |
| Page subtitle | `text-muted-foreground` | Below page title |
| Card/section title | `text-2xl font-semibold leading-none tracking-tight` | CardTitle component |
| Subsection header | `text-lg font-semibold` | Detail panel headers |
| Section label | `text-base font-medium` | Smaller headings |
| Body text | `text-sm` | Default content size |
| Small/metadata | `text-xs text-muted-foreground` | Labels, timestamps, captions |
| KPI / hero number | `text-2xl font-bold` | Statistics, large values |

Key rules: body text is always `text-sm`. Metadata and secondary info is always `text-xs text-muted-foreground`. Statistics are `text-2xl font-bold`. Small section labels within cards pair an icon with `text-xs text-muted-foreground`.

## Spacing & Layout

### Page Structure
```
Sidebar (fixed w-64, border-r, bg-card) | Main (pl-64, p-8 inner)
                                         | └─ space-y-6 between sections
```

### Grid Patterns
- KPI cards: `grid gap-4 md:grid-cols-2 lg:grid-cols-4`
- Content grid: `grid gap-4 md:grid-cols-2 lg:grid-cols-3`
- Stat row in card: `grid grid-cols-3 gap-4`
- Card directory: `grid gap-4 md:grid-cols-2 lg:grid-cols-3`

These grids are for *real* content density (KPIs, directories, settings). Do not auto-build a marketing "Features" section as three icon cards in a row, a bento of rounded tiles, or a Free / Pro / Enterprise pricing trio unless that is the actual product. Vary count, rhythm, and structure with the content.

### Spacing Scale
- Card padding: `p-6` (standard) / `p-4` (compact)
- Between sections: `space-y-6`
- Between items in list: `space-y-2` or `space-y-3`
- Icon-to-label gap: `gap-1.5` (tight) / `gap-2` (normal) / `gap-3` (spacious)
- Tag wrapping: `flex flex-wrap gap-1.5`
- Filter chips: `gap-3`

## Components

See `references/component-patterns.md` for full component code. Quick reference:

### Cards
The foundational surface — everything lives in a card.
- Base: `rounded-lg border bg-card text-card-foreground shadow-sm`
- Interactive: add `hover:bg-muted/50 transition-colors cursor-pointer`
- Structure: `Card > CardHeader > CardTitle + CardDescription > CardContent > CardFooter`
- `shadow-sm` is structural elevation, not decoration. Do not stack large or colored drop shadows. Do not add a colored left stripe as a "feature/testimonial" accent — that pattern is a vibecode tell. Separate sections with space, a hairline `border-t`, or typography.

### Buttons
Six variants (`default`, `destructive`, `outline`, `secondary`, `ghost`, `link`) × four sizes (`default`, `sm`, `lg`, `icon`). Icons: `h-4 w-4 mr-2` before text. Do not use emoji or sparkle marks as button icons.

### Icons
In product chrome, one consistent set at `h-4 w-4` (Lucide is acceptable here). On marketing pages, Lucide-as-default reads as "AI built this" — choose a distinctive set or a few custom marks. Never use sparkles, emoji, or checkmark-bullet rows as visual identity.

### Inputs
`h-10 rounded-md border border-input bg-background px-3 py-2 text-sm` with focus ring and disabled states. Labels: `block text-sm font-medium mb-2`. Help text: `text-xs text-muted-foreground mt-1`.

### Navigation
Sidebar items: `flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors`. Active: `bg-accent text-accent-foreground`. Inactive: `text-muted-foreground hover:bg-accent hover:text-accent-foreground`.

### Badges & Pills
- Status: `inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded`
- Topic: `text-xs bg-secondary px-2 py-1 rounded-full`
- Tag: `text-xs bg-primary/10 text-primary px-2 py-1 rounded-full`

### Avatars (Initials)
`flex items-center justify-center shrink-0 rounded-full bg-primary/10 font-medium`
Sizes: `h-6 w-6 text-xs` / `h-8 w-8 text-sm` / `h-10 w-10 text-sm` / `h-14 w-14 text-lg`

### Loading States
Async UI must reserve space. A blank page or a lone centered spinner is the "no skeleton loaders" tell.
- Skeleton: `bg-muted animate-pulse rounded` (sized to match the real content — KPI value, avatar row, chart block)
- Spinner: `animate-spin rounded-full h-8 w-8 border-b-2 border-primary` (inline actions, not full-page substitutes)
- Inline: `text-muted-foreground` with "Loading..." text only when there is no layout to skeletonize

### Empty States
`flex items-center justify-center h-32 text-muted-foreground` with a simple message.

### Error States
Container: `rounded-lg border border-destructive/50 bg-destructive/10 p-4`, text: `text-sm text-destructive`

## Data Visualization

Charts use the CSS custom properties for automatic theme integration:

- **Line/area stroke**: `hsl(var(--primary))`
- **Area fill**: `hsl(var(--primary) / 0.2)`
- **Bar fill**: `hsl(var(--primary))`, hover: `hsl(var(--primary) / 0.8)`
- **Bar corners**: `rx: 4`
- **Axis text**: CSS class `fill-muted-foreground text-xs`
- **Grid lines**: `stroke: currentColor`, `stroke-opacity: 0.1`
- **Tooltips**: `background: hsl(var(--popover))`, `color: hsl(var(--popover-foreground))`, `border: 1px solid hsl(var(--border))`, `border-radius: 6px`, `padding: 8px 12px`, `font-size: 12px`, `box-shadow: 0 2px 8px rgba(0,0,0,0.1)`
- **Sparkline bars**: `flex items-end gap-1 h-8`, each bar `flex-1 bg-primary/20 rounded-t`

## Copy & Trust

Visual tokens cannot fix copy that sounds generated. Keep this short and specific:

- **Punctuation:** Do not lean on em dashes. Prefer commas, periods, or a shorter sentence.
- **Pivots:** Do not write "it's not X, it's Y" (or "this isn't just…"). Say the thing.
- **Lists:** Feature lists are sentences or short labels, not a column of checkmarks.
- **Social proof:** Never invent testimonials, names, logos, or star ratings. If there are no real quotes, omit the section.
- **Product evidence:** Show the actual UI (screenshot, clip, interactive preview). A decorative macOS terminal window is not a demo.
- **Legal:** Shipping a public product or marketing site? Include footer links to Terms of Service and a Privacy Policy. Stub the pages if the user must fill them — do not leave them off.

## Dark Mode Implementation

Toggle via `.dark` class on `<html>` using Tailwind's `darkMode: ['class']`. Store preference in localStorage. Toggle button in sidebar header using `Moon`/`Sun` lucide icons.

Use the `dark:` prefix only for colors outside the token system (status colors). For everything else — backgrounds, text, borders, cards, inputs — semantic token classes handle it automatically.

## Accessibility

- Focus rings: `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2`
- Semantic HTML: `<nav>`, `<main>`, `<aside>`, `<button>`, proper heading hierarchy
- Screen reader text: `<span className="sr-only">` for icon-only buttons
- Aria labels on icon buttons
- Disabled: `disabled:pointer-events-none disabled:opacity-50`

## Transitions

Keep animations subtle: `transition-colors` on hover states, `animate-pulse` for skeletons, `animate-spin` for spinners, `duration-200` for modals. Hover is an affordance, not a show — skip scale/glow/bounce and animated arrows. The interface should feel responsive, not performative.
