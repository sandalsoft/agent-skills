---
name: clean-web-design
description: "Guide for building clean, modern web front-ends with a professional design system featuring HSL CSS custom properties, Tailwind CSS utility classes, light/dark mode support, and shadcn/ui-inspired component architecture. Use this skill whenever building a web UI, React component, dashboard, landing page, web app, or any front-end that should look polished and professional. Also use when the user mentions wanting a 'clean' or 'modern' design, asks for dark mode support, or needs a consistent design system for their web project. This skill covers typography, color tokens, spacing, component patterns (cards, buttons, inputs, modals, navigation), layout structure, data visualization theming, loading states, and responsive design that avoids generic AI aesthetics."
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

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Commit to a distinct direction: brutally minimal, maximalist chaos, luxury/refined, lo-fi/zine, dark/moody, soft/pastel, editorial/magazine, brutalist/raw, retro-futuristic, handcrafted/artisanal, organic/natural, art deco/geometric, playful/whimsical, industrial/utilitarian, etc. There are infinite varieties to start from and surpass. Use these as inspiration, but the final design should feel singular, with every detail working in service of one cohesive direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?


## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Typography carries the design's singular voice. Choose fonts with interesting personality. Default fonts signal default thinking: skip Arial, Inter, Roboto, system stacks. Font choices should be inseparable from the aesthetic direction. Display type should be expressive, even risky. Body text should be legible, refined. Pair them like actors in a scene. Work the full typographic range: size, weight, case, spacing to establish hierarchy.
- **Color & Theme**: Commit to a cohesive aesthetic. Palettes should take a clear position: bold and saturated, moody and restrained, or high-contrast and minimal. Lead with a dominant color, punctuate with sharp accents. Avoid timid, non-committal distributions. Use CSS variables for consistency.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap and z-depth. Diagonal flow. Grid-breaking elements. Dramatic scale jumps. Full-bleed moments. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise and grain overlays, geometric patterns, layered transparencies and glassmorphism, dramatic or soft shadows and glows, parallax depth, decorative borders and clip-path shapes, print-inspired textures (halftone, duotone, stipple), knockout typography, and custom cursors.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, Space Grotesk, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter designs that lack context-specific character.
INSTEAD: distinctive fonts. Bold, committed palettes. Layouts that surprise. Bespoke details. Every choice rooted in rich context.

Build creatively on the user's intent, and make unexpected choices that feel genuinely designed for the context. Every design should feel distinct. Actively explore the full range: light and dark themes, unexpected font pairings, substantially varied aesthetic directions. Let the specific context drive choices, NOT familiar defaults.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, elegance, and precision. All designs need careful attention to spacing, typography, and subtle details. Excellence comes from executing the vision well.

Remember: Claude is capable of extraordinary, award-worthy creative work. Don't hold back, show what's truly possible, and commit relentlessly to a distinctive and unforgettable vision.

## Quality Checklist

Before delivering any frontend:

### Visual Impact
- [ ] Does it have a clear point of view?
- [ ] Would someone remember this tomorrow?
- [ ] Does it avoid all generic AI patterns?

### Technical Excellence
- [ ] Responsive across all breakpoints?
- [ ] Accessible (ARIA labels, keyboard navigation)?
- [ ] Performance optimized (lazy loading, code splitting)?
- [ ] Cross-browser tested?

### Attention to Detail
- [ ] Custom focus states defined?
- [ ] Loading and error states designed?
- [ ] Micro-interactions enhance usability?
- [ ] Typography hierarchy consistent?

## Tech Stack

The design system is framework-flexible but optimized for:
- **React** with TypeScript
- **Tailwind CSS** with `darkMode: ['class']`
- **Lucide React** for icons (16×16 at `h-4 w-4` default)
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

See `references/design-tokens.md` for exact HSL values and the full CSS setup.

### Status Colors

For semantic indicators outside the token system, use Tailwind colors with dark variants:

- **Success**: `text-green-600 bg-green-100` / `dark:text-green-400 dark:bg-green-900`
- **Error**: `text-red-600 bg-red-100` / `dark:text-red-400 dark:bg-red-900`
- **Warning**: `text-amber-600 bg-amber-100` / `dark:text-amber-400 dark:bg-amber-900`
- **Info**: `text-blue-600 bg-blue-100` / `dark:text-blue-400 dark:bg-blue-900`

Badge pattern: `bg-{color}-100 text-{color}-800 dark:bg-{color}-900 dark:text-{color}-200`

## Typography

System font stack (no custom fonts — keeps things fast and native-feeling).

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

### Buttons
Six variants (`default`, `destructive`, `outline`, `secondary`, `ghost`, `link`) × four sizes (`default`, `sm`, `lg`, `icon`). Icons: `h-4 w-4 mr-2` before text.

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
- Skeleton: `bg-muted animate-pulse rounded` (sized to match content)
- Spinner: `animate-spin rounded-full h-8 w-8 border-b-2 border-primary`
- Inline: `text-muted-foreground` with "Loading..." text

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

Keep animations subtle: `transition-colors` on hover states, `animate-pulse` for skeletons, `animate-spin` for spinners, `duration-200` for modals. No flashy animations — the interface should feel responsive, not performative.
