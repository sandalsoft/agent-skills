# Component Patterns

Copy-pasteable component code for the clean web design system. These are production-ready primitives that compose together to build complete UIs.

## Table of Contents
1. Card
2. Button
3. Input
4. Select
5. Dialog/Modal
6. Navigation Layout
7. KPI Card
8. Search Bar
9. Filter Bar
10. Person/Entity Card
11. Data List Item
12. Status Badge
13. Avatar
14. Page Layout Template

---

## 1. Card

The foundational surface component. Everything in the UI lives inside a card.

```tsx
import * as React from 'react';
import { cn } from '@/lib/utils';

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('rounded-lg border bg-card text-card-foreground shadow-sm', className)}
      {...props}
    />
  )
);

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} />
  )
);

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn('text-2xl font-semibold leading-none tracking-tight', className)}
      {...props}
    />
  )
);

const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn('text-sm text-muted-foreground', className)} {...props} />
  )
);

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
  )
);

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('flex items-center p-6 pt-0', className)} {...props} />
  )
);

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
```

### Interactive Card Pattern

For clickable cards (list items, directory entries):

```tsx
<Card
  className="hover:bg-muted/50 transition-colors cursor-pointer"
  onClick={handleClick}
>
  <CardContent className="p-4">
    {/* Content */}
  </CardContent>
</Card>
```

### Settings Card Pattern

For form sections with a save action:

```tsx
<Card>
  <CardHeader>
    <div className="flex items-center gap-2">
      <Icon className="h-5 w-5 text-muted-foreground" />
      <CardTitle>Section Title</CardTitle>
    </div>
    <CardDescription>
      Description of what this section controls.
    </CardDescription>
  </CardHeader>
  <CardContent className="space-y-4">
    {/* Form fields */}
  </CardContent>
  <CardFooter className="border-t pt-4">
    <Button>Save</Button>
  </CardFooter>
</Card>
```

---

## 2. Button

Six variants with four sizes. Uses `class-variance-authority` for variant management.

```tsx
import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      ref={ref}
      {...props}
    />
  )
);

export { Button, buttonVariants };
```

### Button with Icon Pattern

```tsx
<Button>
  <Save className="h-4 w-4 mr-2" />
  Save
</Button>

<Button variant="outline" size="icon">
  <X className="h-4 w-4" />
</Button>
```

### Loading Button Pattern

```tsx
<Button disabled={saving}>
  {saving ? (
    <>
      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
      Saving...
    </>
  ) : (
    <>
      <Save className="h-4 w-4 mr-2" />
      Save
    </>
  )}
</Button>
```

---

## 3. Input

```tsx
import * as React from 'react';
import { cn } from '@/lib/utils';

const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, type, ...props }, ref) => (
    <input
      type={type}
      className={cn(
        'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      ref={ref}
      {...props}
    />
  )
);

export { Input };
```

### Form Field Pattern

```tsx
<div>
  <label className="block text-sm font-medium mb-2">
    Field Label
  </label>
  <Input
    type="text"
    value={value}
    onChange={(e) => setValue(e.target.value)}
    placeholder="Placeholder text..."
  />
  <p className="text-xs text-muted-foreground mt-1">
    Help text explaining the field.
  </p>
</div>
```

### Search Input with Icon

```tsx
<div className="relative">
  <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
  <Input
    type="text"
    placeholder="Search..."
    className="pl-9 pr-9"
  />
  {value && (
    <button
      onClick={handleClear}
      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
    >
      <X className="h-4 w-4" />
    </button>
  )}
</div>
```

---

## 4. Select

```tsx
import * as React from 'react';
import { cn } from '@/lib/utils';

const Select = React.forwardRef<HTMLSelectElement, React.SelectHTMLAttributes<HTMLSelectElement>>(
  ({ className, children, ...props }, ref) => (
    <select
      className={cn(
        'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      ref={ref}
      {...props}
    >
      {children}
    </select>
  )
);

export { Select };
```

### Filter Select with Icon

```tsx
<div className="flex items-center gap-2">
  <Users className="h-4 w-4 text-muted-foreground" />
  <Select value={filter} onChange={(e) => setFilter(e.target.value)} className="w-[160px]">
    <option value="">All people</option>
    {options.map((opt) => (
      <option key={opt.value} value={opt.value}>{opt.label}</option>
    ))}
  </Select>
</div>
```

---

## 5. Dialog/Modal

Uses Radix UI Dialog primitive for accessibility:

```tsx
import * as React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

const Dialog = DialogPrimitive.Root;
const DialogTrigger = DialogPrimitive.Trigger;
const DialogPortal = DialogPrimitive.Portal;
const DialogClose = DialogPrimitive.Close;

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      'fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
      className
    )}
    {...props}
  />
));

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        'fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 sm:rounded-lg',
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
));

const DialogHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('flex flex-col space-y-1.5 text-center sm:text-left', className)} {...props} />
);

const DialogFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2', className)} {...props} />
);

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn('text-lg font-semibold leading-none tracking-tight', className)}
    {...props}
  />
));

const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn('text-sm text-muted-foreground', className)}
    {...props}
  />
));

export {
  Dialog, DialogPortal, DialogOverlay, DialogClose, DialogTrigger,
  DialogContent, DialogHeader, DialogFooter, DialogTitle, DialogDescription,
};
```

---

## 6. Navigation Layout

Fixed sidebar with icon + label nav items, theme toggle, and main content area:

```tsx
import { NavLink, Outlet } from 'react-router-dom';
import { LayoutDashboard, Users, Settings, Sun, Moon } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useTheme } from '@/hooks/useTheme';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'People', href: '/people', icon: Users },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export function MainLayout() {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="fixed inset-y-0 left-0 z-50 w-64 border-r bg-card">
        <div className="flex h-16 items-center justify-between border-b px-6">
          <h1 className="text-xl font-semibold">App Name</h1>
          <button
            onClick={toggleTheme}
            className="rounded-md p-2 text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors"
            aria-label={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
          >
            {theme === 'light' ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
          </button>
        </div>
        <nav className="flex flex-col gap-1 p-4">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-accent text-accent-foreground'
                    : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                )
              }
            >
              <item.icon className="h-4 w-4" />
              {item.name}
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* Main content */}
      <main className="pl-64">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
```

---

## 7. KPI Card

A stat card with optional icon, trend indicator, and loading state:

```tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui';
import { cn } from '@/lib/utils';
import { LucideIcon, TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: LucideIcon;
  trend?: { value: number; direction: 'up' | 'down' | 'neutral' };
  loading?: boolean;
}

export function KPICard({ title, value, subtitle, icon: Icon, trend, loading = false }: KPICardProps) {
  const TrendIcon = trend?.direction === 'up' ? TrendingUp
    : trend?.direction === 'down' ? TrendingDown : Minus;

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="h-8 w-24 bg-muted animate-pulse rounded" />
        ) : (
          <div className="text-2xl font-bold">{value}</div>
        )}
        <div className="flex items-center gap-2">
          {trend && !loading && (
            <span className={cn(
              'flex items-center text-xs font-medium',
              trend.direction === 'up' && 'text-green-600',
              trend.direction === 'down' && 'text-red-600',
              trend.direction === 'neutral' && 'text-muted-foreground'
            )}>
              <TrendIcon className="h-3 w-3 mr-0.5" />
              {trend.value > 0 ? '+' : ''}{trend.value}%
            </span>
          )}
          {subtitle && <p className="text-xs text-muted-foreground">{subtitle}</p>}
          {loading && !subtitle && <div className="h-4 w-32 bg-muted animate-pulse rounded mt-1" />}
        </div>
      </CardContent>
    </Card>
  );
}
```

Usage: `<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">` containing multiple KPICards.

---

## 8. Entity Card (Person, Company, etc.)

A versatile card for displaying entity profiles with stats and metadata:

```tsx
<Card className="hover:bg-muted/50 transition-colors cursor-pointer" onClick={onClick}>
  <CardContent className="p-6">
    {/* Header: Avatar + Name + Badge */}
    <div className="flex items-start gap-4">
      <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-primary/10 text-lg font-medium">
        {initials}
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2 flex-wrap">
          <h3 className="font-semibold text-lg">{name}</h3>
          <StatusBadge />
        </div>
        <div className="flex items-center gap-1.5 text-sm text-muted-foreground mt-1">
          <Mail className="h-3.5 w-3.5" />
          <span className="truncate">{email}</span>
        </div>
      </div>
    </div>

    {/* Stats Row */}
    <div className="grid grid-cols-3 gap-4 mt-6">
      <div className="text-center">
        <p className="text-2xl font-bold">{count}</p>
        <p className="text-xs text-muted-foreground">Label</p>
      </div>
      {/* ... more stats */}
    </div>

    {/* Info Section */}
    <div className="mt-4 p-3 bg-muted/50 rounded-lg">
      <div className="flex items-center gap-1.5 text-xs text-muted-foreground mb-1">
        <Calendar className="h-3 w-3" />
        <span>Section label</span>
      </div>
      <p className="text-sm">{info}</p>
    </div>

    {/* Tags */}
    <div className="mt-4">
      <div className="flex flex-wrap gap-1.5">
        {tags.map((tag) => (
          <span key={tag} className="text-xs bg-secondary px-2 py-1 rounded-full">
            {tag}
          </span>
        ))}
      </div>
    </div>

    {/* Related Items with Border Separator */}
    <div className="mt-4 pt-4 border-t">
      <div className="flex items-center gap-1.5 text-xs text-muted-foreground mb-2">
        <Users className="h-3 w-3" />
        <span>Related items</span>
      </div>
      <div className="space-y-2">
        {items.map((item) => (
          <div key={item.id} className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <div className="flex h-6 w-6 items-center justify-center rounded-full bg-muted text-xs">
                {item.initials}
              </div>
              <span>{item.name}</span>
            </div>
            <span className="text-muted-foreground text-xs">{item.count} items</span>
          </div>
        ))}
      </div>
    </div>
  </CardContent>
</Card>
```

### Compact Entity Card Variant

```tsx
<Card className="hover:bg-muted/50 transition-colors cursor-pointer" onClick={onClick}>
  <CardContent className="p-4">
    <div className="flex items-center gap-3">
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/10 text-sm font-medium">
        {initials}
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <p className="font-medium truncate">{name}</p>
          <StatusBadge />
        </div>
        <p className="text-sm text-muted-foreground truncate">{subtitle}</p>
      </div>
      <div className="shrink-0 text-right">
        <p className="text-sm font-medium">{count}</p>
        <p className="text-xs text-muted-foreground">label</p>
      </div>
    </div>
  </CardContent>
</Card>
```

---

## 9. Status Badge

```tsx
function StatusBadge({ status }: { status: 'up' | 'down' | 'stable' }) {
  if (status === 'up') {
    return (
      <span className="inline-flex items-center gap-1 text-xs bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 px-2 py-0.5 rounded">
        <TrendingUp className="h-3 w-3" />
        Growing
      </span>
    );
  }
  if (status === 'down') {
    return (
      <span className="inline-flex items-center gap-1 text-xs bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 px-2 py-0.5 rounded">
        <TrendingDown className="h-3 w-3" />
        Declining
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 text-xs bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200 px-2 py-0.5 rounded">
      <Minus className="h-3 w-3" />
      Stable
    </span>
  );
}
```

---

## 10. List Item Card (Action Items, Tasks, etc.)

```tsx
<Card
  className={cn(
    'transition-colors',
    onClick && 'cursor-pointer hover:bg-muted/50',
    isOverdue && 'border-red-200 dark:border-red-800'
  )}
  onClick={onClick}
>
  <CardContent className="p-4">
    <div className="flex items-start gap-3">
      {/* Status icon */}
      <div className="mt-0.5">
        {isCompleted ? (
          <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400" />
        ) : isOverdue ? (
          <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400" />
        ) : (
          <Circle className="h-5 w-5 text-muted-foreground" />
        )}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <p className={cn('text-sm', isCompleted && 'line-through text-muted-foreground')}>
          {text}
        </p>
        <div className="flex flex-wrap items-center gap-2 mt-2 text-xs text-muted-foreground">
          {assignee && (
            <span className="inline-flex items-center px-2 py-0.5 rounded bg-secondary">
              {assignee}
            </span>
          )}
          {dueDate && (
            <span className={cn(
              'inline-flex items-center gap-1',
              isOverdue && 'text-red-600 dark:text-red-400'
            )}>
              <Clock className="h-3 w-3" />
              {dueDate}
            </span>
          )}
        </div>
      </div>
    </div>
  </CardContent>
</Card>
```

---

## 11. Page Layout Template

Standard page structure used across the app:

```tsx
export function ExamplePage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Page Title</h2>
          <p className="text-muted-foreground">
            Brief description of this page.
          </p>
        </div>
        <Button variant="outline">
          <RefreshCw className="h-4 w-4 mr-2" />
          Action
        </Button>
      </div>

      {/* Search & Filters */}
      <div className="space-y-4">
        <SearchBar value={query} onChange={setQuery} />
        <FilterBar filters={filters} onChange={setFilters} />
      </div>

      {/* Error State */}
      {error && (
        <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-4">
          <p className="text-sm text-destructive">
            Failed to load data: {error.message}
          </p>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <KPICard title="Metric 1" value={42} icon={Calendar} />
        <KPICard title="Metric 2" value="8h" icon={Clock} />
        {/* ... */}
      </div>

      {/* Content Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <EntityCard key={item.id} data={item} />
        ))}
      </div>

      {/* Full-Width Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Chart Title</CardTitle>
        </CardHeader>
        <CardContent className="h-[300px] flex items-center justify-center">
          {loading ? (
            <div className="text-muted-foreground">Loading...</div>
          ) : data.length > 0 ? (
            <Chart data={data} />
          ) : (
            <div className="text-muted-foreground">No data available</div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
```

---

## 12. Loading Skeleton Patterns

### Card List Skeleton

```tsx
{[...Array(5)].map((_, i) => (
  <div key={i} className="flex items-center justify-between">
    <div className="flex items-center gap-3">
      <div className="h-8 w-8 bg-muted animate-pulse rounded-full" />
      <div className="h-4 w-24 bg-muted animate-pulse rounded" />
    </div>
    <div className="h-4 w-12 bg-muted animate-pulse rounded" />
  </div>
))}
```

### Full Page Loading

```tsx
<div className="min-h-screen bg-background flex items-center justify-center">
  <div className="text-center">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto" />
    <p className="mt-4 text-muted-foreground">Loading...</p>
  </div>
</div>
```

### Inline KPI Skeleton

```tsx
<div className="h-8 w-24 bg-muted animate-pulse rounded" />  {/* Value */}
<div className="h-4 w-32 bg-muted animate-pulse rounded mt-1" />  {/* Subtitle */}
```
