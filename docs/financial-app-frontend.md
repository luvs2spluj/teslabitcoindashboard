# Financial App Frontend Architecture

## Next.js 14 Application Structure
```
apps/web/
├── app/                       # App Router pages
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Home page
│   ├── tsla/                 # Tesla dashboard
│   ├── stock/[symbol]/       # Stock analysis pages
│   ├── strategies/           # Strategy builder
│   ├── backtests/[id]/       # Backtest results
│   ├── btc/                  # Bitcoin analysis
│   └── compare/              # Benchmark comparison
├── components/               # Reusable components
│   ├── ui/                   # shadcn/ui components
│   ├── charts/               # Chart components
│   ├── forms/                # Form components
│   └── layout/               # Layout components
├── lib/                      # Utilities and configurations
├── hooks/                    # Custom React hooks
├── types/                    # TypeScript definitions
└── styles/                   # Global styles
```

## UI/UX Design System

### Design Principles
- **Minimal and Intuitive**: Clean, focused interface
- **Data-Driven**: Charts and metrics as primary content
- **Responsive**: Mobile-first design approach
- **Dark Mode**: Built-in dark/light theme support
- **Accessibility**: WCAG 2.1 AA compliance

### Component Library (shadcn/ui)
- **Layout**: Card, Sheet, Tabs, Accordion
- **Forms**: Input, Select, Button, Checkbox, Radio
- **Data Display**: Table, Badge, Progress, Alert
- **Navigation**: Breadcrumb, Pagination, Command
- **Feedback**: Toast, Dialog, Alert Dialog

## Chart Components (Recharts)

### Core Charts
- **PriceChart**: OHLCV candlestick/line charts
- **PercentileBands**: Monte Carlo simulation bands
- **DistributionChart**: Statistical distributions
- **DrawdownChart**: Portfolio drawdown visualization
- **MetricsGrid**: Performance metrics dashboard

### Tesla-Specific Charts
- **TeslaEnergyCharts**: Solar/storage capacity and margins
- **VehicleDeliveryChart**: Quarterly delivery trends
- **MarginAnalysisChart**: Gross margin evolution
- **ScenarioChart**: Regime probability visualization

## Page Architecture

### Tesla Dashboard (/tsla)
- **Overview**: Key metrics and recent performance
- **Vehicles**: Delivery trends and ASP analysis
- **Energy**: Solar/storage business metrics
- **Margins**: Profitability analysis
- **Scenarios**: Game-theory analysis and forecasts

### Stock Analysis (/stock/[symbol])
- **Overview**: Price action and key metrics
- **Fair Value**: Valuation models and percentiles
- **Scenarios**: Regime analysis and Monte Carlo
- **News**: Sentiment analysis and news feed
- **Reddit**: Social sentiment tracking
- **Peers**: Comparative analysis

### Strategy Tools
- **Strategy Builder**: Visual strategy configuration
- **Backtest Runner**: Strategy testing interface
- **Optimizer Panel**: Parameter optimization
- **Results Viewer**: Comprehensive backtest analysis

## Data Management

### State Management
- **Server State**: TanStack Query for API data
- **Client State**: React Context for UI state
- **Form State**: React Hook Form for complex forms
- **Cache Strategy**: Aggressive caching with invalidation

### Data Fetching Patterns
- **Server Actions**: Next.js server actions for mutations
- **Route Handlers**: API routes for data transformation
- **Client Components**: Real-time data updates
- **Static Generation**: Pre-built pages where possible

## Authentication & Authorization

### Supabase Integration
- **Email/Password**: Traditional authentication
- **OAuth**: Google, GitHub, Apple sign-in
- **Row Level Security**: Database-level permissions
- **User Profiles**: Custom user data management

### Security Features
- **CSRF Protection**: Built-in Next.js protection
- **Content Security Policy**: Strict CSP headers
- **Input Validation**: Zod schemas for all inputs
- **Rate Limiting**: Client-side request throttling

## Performance Optimization

### Next.js Features
- **App Router**: Latest routing and layouts
- **Server Components**: Reduced client bundle
- **Streaming**: Progressive page loading
- **Image Optimization**: Next.js Image component

### Bundle Optimization
- **Code Splitting**: Route-based splitting
- **Tree Shaking**: Unused code elimination
- **Dynamic Imports**: Lazy loading of heavy components
- **Bundle Analysis**: Regular bundle size monitoring

## Responsive Design

### Breakpoints (Tailwind)
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px
- **Large**: > 1280px

### Mobile-First Approach
- **Touch-Friendly**: Large tap targets
- **Swipe Gestures**: Chart navigation
- **Responsive Tables**: Horizontal scroll
- **Collapsible Sections**: Space-efficient layouts
