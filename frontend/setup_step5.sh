#!/bin/bash
set -e

echo "📊 Step 5: Creating Dashboard Layout..."
cd "$(dirname "$0")"

# ============================================================
# 1. Dashboard Layout with Sidebar
# ============================================================
echo "📝 Creating app/(dashboard)/layout.tsx..."
mkdir -p "app/(dashboard)"
cat > "app/(dashboard)/layout.tsx" << 'LAYOUTEOF'
'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import Link from 'next/link'
import { 
  LayoutDashboard, 
  FileText, 
  BarChart3, 
  TrendingUp, 
  Network, 
  Users, 
  Settings,
  LogOut,
  Menu,
  X,
  ChevronLeft,
  Moon,
  Sun,
  Bell
} from 'lucide-react'
import { useTheme } from 'next-themes'

import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Separator } from '@/components/ui/separator'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuLabel, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu'
import { useAuthStore } from '@/lib/stores/auth-store'
import { authApi } from '@/lib/api'

const navigation = [
  { name: 'داشبورد', href: '/dashboard', icon: LayoutDashboard },
  { name: 'پست‌ها', href: '/dashboard/posts', icon: FileText },
  { name: 'تحلیل‌ها', href: '/dashboard/analysis', icon: BarChart3 },
  { name: 'روندها', href: '/dashboard/trends', icon: TrendingUp },
  { name: 'گراف شبکه', href: '/dashboard/graph', icon: Network },
  { name: 'نویسندگان', href: '/dashboard/authors', icon: Users },
]

const bottomNavigation = [
  { name: 'تنظیمات', href: '/dashboard/settings', icon: Settings },
]

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const pathname = usePathname()
  const { theme, setTheme } = useTheme()
  const { user, isAuthenticated, isLoading, logout, setLoading } = useAuthStore()
  
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  // Check auth on mount
  useEffect(() => {
    const checkAuth = async () => {
      if (!isAuthenticated) {
        router.push('/login')
        return
      }
      
      try {
        const currentUser = await authApi.me()
        useAuthStore.getState().setUser(currentUser)
      } catch {
        logout()
        router.push('/login')
      } finally {
        setLoading(false)
      }
    }
    
    checkAuth()
  }, [isAuthenticated, router, logout, setLoading])

  const handleLogout = async () => {
    try {
      await authApi.logout()
    } finally {
      logout()
      router.push('/login')
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
          <p className="text-muted-foreground">در حال بارگذاری...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated || !user) {
    return null
  }

  const userInitials = user.full_name
    ? user.full_name.split(' ').map(n => n[0]).join('').slice(0, 2)
    : user.username.slice(0, 2).toUpperCase()

  return (
    <TooltipProvider delayDuration={0}>
      <div className="min-h-screen bg-background">
        {/* Mobile sidebar backdrop */}
        {sidebarOpen && (
          <div 
            className="fixed inset-0 z-40 bg-black/50 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Sidebar */}
        <aside
          className={cn(
            "fixed inset-y-0 right-0 z-50 flex flex-col bg-sidebar border-l transition-all duration-300",
            sidebarCollapsed ? "w-16" : "w-64",
            sidebarOpen ? "translate-x-0" : "translate-x-full lg:translate-x-0"
          )}
        >
          {/* Logo */}
          <div className={cn(
            "flex items-center h-16 px-4 border-b",
            sidebarCollapsed ? "justify-center" : "justify-between"
          )}>
            {!sidebarCollapsed && (
              <Link href="/dashboard" className="flex items-center gap-2">
                <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                  <span className="text-lg">🧠</span>
                </div>
                <span className="font-bold text-sidebar-foreground">سامانه هوشمند</span>
              </Link>
            )}
            {sidebarCollapsed && (
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <span className="text-lg">🧠</span>
              </div>
            )}
            <Button
              variant="ghost"
              size="icon"
              className="hidden lg:flex h-8 w-8"
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            >
              <ChevronLeft className={cn(
                "h-4 w-4 transition-transform",
                sidebarCollapsed && "rotate-180"
              )} />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden h-8 w-8"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Navigation */}
          <ScrollArea className="flex-1 py-4">
            <nav className="space-y-1 px-2">
              {navigation.map((item) => {
                const isActive = pathname === item.href || pathname.startsWith(item.href + '/')
                const NavLink = (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setSidebarOpen(false)}
                    className={cn(
                      "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                      isActive
                        ? "bg-sidebar-accent text-sidebar-accent-foreground"
                        : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-accent-foreground",
                      sidebarCollapsed && "justify-center px-2"
                    )}
                  >
                    <item.icon className="h-5 w-5 flex-shrink-0" />
                    {!sidebarCollapsed && <span>{item.name}</span>}
                  </Link>
                )

                if (sidebarCollapsed) {
                  return (
                    <Tooltip key={item.name}>
                      <TooltipTrigger asChild>{NavLink}</TooltipTrigger>
                      <TooltipContent side="left">{item.name}</TooltipContent>
                    </Tooltip>
                  )
                }
                return NavLink
              })}
            </nav>
          </ScrollArea>

          {/* Bottom Navigation */}
          <div className="border-t p-2 space-y-1">
            {bottomNavigation.map((item) => {
              const isActive = pathname === item.href
              const NavLink = (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setSidebarOpen(false)}
                  className={cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-sidebar-accent text-sidebar-accent-foreground"
                      : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-accent-foreground",
                    sidebarCollapsed && "justify-center px-2"
                  )}
                >
                  <item.icon className="h-5 w-5 flex-shrink-0" />
                  {!sidebarCollapsed && <span>{item.name}</span>}
                </Link>
              )

              if (sidebarCollapsed) {
                return (
                  <Tooltip key={item.name}>
                    <TooltipTrigger asChild>{NavLink}</TooltipTrigger>
                    <TooltipContent side="left">{item.name}</TooltipContent>
                  </Tooltip>
                )
              }
              return NavLink
            })}
          </div>

          {/* User Section */}
          <div className={cn(
            "border-t p-3",
            sidebarCollapsed && "flex justify-center"
          )}>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className={cn(
                  "flex items-center gap-3 w-full rounded-lg p-2 hover:bg-sidebar-accent/50 transition-colors",
                  sidebarCollapsed && "justify-center"
                )}>
                  <Avatar className="h-8 w-8">
                    <AvatarFallback className="bg-primary text-primary-foreground text-xs">
                      {userInitials}
                    </AvatarFallback>
                  </Avatar>
                  {!sidebarCollapsed && (
                    <div className="flex-1 text-right">
                      <p className="text-sm font-medium text-sidebar-foreground">
                        {user.full_name || user.username}
                      </p>
                      <p className="text-xs text-sidebar-foreground/60">{user.role}</p>
                    </div>
                  )}
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>
                  <div className="flex flex-col">
                    <span>{user.full_name || user.username}</span>
                    <span className="text-xs text-muted-foreground font-normal">{user.email}</span>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild>
                  <Link href="/dashboard/settings">
                    <Settings className="ml-2 h-4 w-4" />
                    تنظیمات
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout} className="text-destructive">
                  <LogOut className="ml-2 h-4 w-4" />
                  خروج
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </aside>

        {/* Main Content */}
        <div className={cn(
          "transition-all duration-300",
          sidebarCollapsed ? "lg:mr-16" : "lg:mr-64"
        )}>
          {/* Header */}
          <header className="sticky top-0 z-30 h-16 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="flex h-full items-center justify-between px-4">
              <div className="flex items-center gap-4">
                <Button
                  variant="ghost"
                  size="icon"
                  className="lg:hidden"
                  onClick={() => setSidebarOpen(true)}
                >
                  <Menu className="h-5 w-5" />
                </Button>
                <h1 className="text-lg font-semibold">
                  {navigation.find(n => pathname === n.href || pathname.startsWith(n.href + '/'))?.name || 'داشبورد'}
                </h1>
              </div>
              
              <div className="flex items-center gap-2">
                <Button variant="ghost" size="icon">
                  <Bell className="h-5 w-5" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                >
                  {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
                </Button>
              </div>
            </div>
          </header>

          {/* Page Content */}
          <main className="p-4 lg:p-6">
            {children}
          </main>
        </div>
      </div>
    </TooltipProvider>
  )
}
LAYOUTEOF

# ============================================================
# 2. Dashboard Home Page
# ============================================================
echo "📝 Creating app/(dashboard)/dashboard/page.tsx..."
mkdir -p "app/(dashboard)/dashboard"
cat > "app/(dashboard)/dashboard/page.tsx" << 'DASHPAGEEOF'
'use client'

import { useEffect, useState } from 'react'
import { 
  FileText, 
  BarChart3, 
  TrendingUp, 
  Network,
  Smile,
  Frown,
  Meh,
  ArrowUpRight,
  ArrowDownRight,
  Loader2
} from 'lucide-react'
import CountUp from 'react-countup'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { dashboardApi, trendsApi } from '@/lib/api'
import { cn, toPersianNumber, formatNumber } from '@/lib/utils'
import type { DashboardOverview, SentimentOverview, TrendingItem } from '@/types'

interface StatsCardProps {
  title: string
  value: number
  icon: React.ElementType
  description?: string
  trend?: { value: number; positive: boolean }
  loading?: boolean
}

function StatsCard({ title, value, icon: Icon, description, trend, loading }: StatsCardProps) {
  if (loading) {
    return (
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-8 w-8 rounded" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-8 w-32 mb-1" />
          <Skeleton className="h-4 w-20" />
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
        <div className="p-2 bg-primary/10 rounded-lg">
          <Icon className="h-5 w-5 text-primary" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold">
          <CountUp end={value} duration={1} separator="," formattingFn={(n) => toPersianNumber(formatNumber(n))} />
        </div>
        {description && (
          <p className="text-xs text-muted-foreground mt-1">{description}</p>
        )}
        {trend && (
          <div className={cn(
            "flex items-center text-xs mt-2",
            trend.positive ? "text-green-600" : "text-red-600"
          )}>
            {trend.positive ? <ArrowUpRight className="h-3 w-3 ml-1" /> : <ArrowDownRight className="h-3 w-3 ml-1" />}
            {toPersianNumber(trend.value)}% نسبت به دیروز
          </div>
        )}
      </CardContent>
    </Card>
  )
}

function SentimentCard({ data, loading }: { data?: SentimentOverview; loading: boolean }) {
  if (loading || !data) {
    return (
      <Card className="col-span-full lg:col-span-2">
        <CardHeader>
          <Skeleton className="h-5 w-32" />
          <Skeleton className="h-4 w-48" />
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-12 w-full" />
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  const sentiments = [
    { label: 'مثبت', value: data.distribution.positive, percent: data.percentages.positive, icon: Smile, color: 'bg-green-500' },
    { label: 'منفی', value: data.distribution.negative, percent: data.percentages.negative, icon: Frown, color: 'bg-red-500' },
    { label: 'خنثی', value: data.distribution.neutral, percent: data.percentages.neutral, icon: Meh, color: 'bg-gray-500' },
  ]

  return (
    <Card className="col-span-full lg:col-span-2">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="h-5 w-5" />
          تحلیل احساسات
        </CardTitle>
        <CardDescription>
          توزیع احساسات در {toPersianNumber(formatNumber(data.total_analyzed))} پست تحلیل‌شده
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {sentiments.map((sentiment) => (
            <div key={sentiment.label} className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <sentiment.icon className={cn(
                    "h-4 w-4",
                    sentiment.label === 'مثبت' && "text-green-500",
                    sentiment.label === 'منفی' && "text-red-500",
                    sentiment.label === 'خنثی' && "text-gray-500"
                  )} />
                  <span className="text-sm font-medium">{sentiment.label}</span>
                </div>
                <span className="text-sm text-muted-foreground">
                  {toPersianNumber(sentiment.percent.toFixed(1))}% ({toPersianNumber(formatNumber(sentiment.value))})
                </span>
              </div>
              <Progress value={sentiment.percent} className={cn("h-2", sentiment.color)} />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

function TrendingCard({ data, loading }: { data?: TrendingItem[]; loading: boolean }) {
  if (loading) {
    return (
      <Card>
        <CardHeader>
          <Skeleton className="h-5 w-32" />
          <Skeleton className="h-4 w-24" />
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <Skeleton key={i} className="h-8 w-full" />
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TrendingUp className="h-5 w-5" />
          هشتگ‌های ترند
        </CardTitle>
        <CardDescription>۲۴ ساعت گذشته</CardDescription>
      </CardHeader>
      <CardContent>
        {data && data.length > 0 ? (
          <div className="space-y-3">
            {data.slice(0, 5).map((item, index) => (
              <div key={item.item} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className={cn(
                    "w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold",
                    index === 0 && "bg-yellow-500 text-white",
                    index === 1 && "bg-gray-400 text-white",
                    index === 2 && "bg-amber-600 text-white",
                    index > 2 && "bg-muted text-muted-foreground"
                  )}>
                    {toPersianNumber(index + 1)}
                  </span>
                  <span className="font-medium">#{item.item}</span>
                </div>
                <Badge variant="secondary">
                  {toPersianNumber(formatNumber(item.count))}
                </Badge>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center text-muted-foreground py-4">هشتگی یافت نشد</p>
        )}
      </CardContent>
    </Card>
  )
}

export default function DashboardPage() {
  const [overview, setOverview] = useState<DashboardOverview | null>(null)
  const [sentiment, setSentiment] = useState<SentimentOverview | null>(null)
  const [hashtags, setHashtags] = useState<TrendingItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const [overviewData, sentimentData, hashtagsData] = await Promise.all([
          dashboardApi.overview(),
          dashboardApi.sentiment(),
          trendsApi.hashtags(24, 10),
        ])
        setOverview(overviewData)
        setSentiment(sentimentData)
        setHashtags(hashtagsData)
      } catch (err) {
        console.error('Dashboard fetch error:', err)
        setError('خطا در دریافت اطلاعات')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <p className="text-destructive mb-4">{error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="text-primary hover:underline"
        >
          تلاش مجدد
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome */}
      <div>
        <h2 className="text-2xl font-bold">خوش آمدید! 👋</h2>
        <p className="text-muted-foreground">نمای کلی از وضعیت سامانه</p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="کل پست‌ها"
          value={overview?.posts.total || 0}
          icon={FileText}
          description={`${toPersianNumber(overview?.posts.processed || 0)} پردازش‌شده`}
          loading={loading}
        />
        <StatsCard
          title="تحلیل‌ها"
          value={overview?.analyses.total || 0}
          icon={BarChart3}
          loading={loading}
        />
        <StatsCard
          title="روندهای فعال"
          value={overview?.trends.active || 0}
          icon={TrendingUp}
          loading={loading}
        />
        <StatsCard
          title="گره‌های شبکه"
          value={overview?.graph.nodes || 0}
          icon={Network}
          description={`${toPersianNumber(overview?.graph.communities || 0)} جامعه`}
          loading={loading}
        />
      </div>

      {/* Charts Row */}
      <div className="grid gap-4 lg:grid-cols-3">
        <SentimentCard data={sentiment || undefined} loading={loading} />
        <TrendingCard data={hashtags} loading={loading} />
      </div>
    </div>
  )
}
DASHPAGEEOF

# ============================================================
# 3. Create Placeholder Pages
# ============================================================
echo "📝 Creating placeholder pages..."

# Posts page
mkdir -p "app/(dashboard)/dashboard/posts"
cat > "app/(dashboard)/dashboard/posts/page.tsx" << 'POSTSEOF'
'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { FileText } from 'lucide-react'

export default function PostsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">پست‌ها</h2>
        <p className="text-muted-foreground">مدیریت و مشاهده پست‌های جمع‌آوری شده</p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            لیست پست‌ها
          </CardTitle>
          <CardDescription>به زودی...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12 text-muted-foreground">
            در حال توسعه...
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
POSTSEOF

# Analysis page
mkdir -p "app/(dashboard)/dashboard/analysis"
cat > "app/(dashboard)/dashboard/analysis/page.tsx" << 'ANALYSISEOF'
'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart3 } from 'lucide-react'

export default function AnalysisPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">تحلیل‌ها</h2>
        <p className="text-muted-foreground">ایجاد و مدیریت تحلیل‌های NLP</p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            لیست تحلیل‌ها
          </CardTitle>
          <CardDescription>به زودی...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12 text-muted-foreground">
            در حال توسعه...
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
ANALYSISEOF

# Trends page
mkdir -p "app/(dashboard)/dashboard/trends"
cat > "app/(dashboard)/dashboard/trends/page.tsx" << 'TRENDSEOF'
'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { TrendingUp } from 'lucide-react'

export default function TrendsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">روندها</h2>
        <p className="text-muted-foreground">هشتگ‌ها و کلمات کلیدی ترند</p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            روندهای فعال
          </CardTitle>
          <CardDescription>به زودی...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12 text-muted-foreground">
            در حال توسعه...
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
TRENDSEOF

# Graph page
mkdir -p "app/(dashboard)/dashboard/graph"
cat > "app/(dashboard)/dashboard/graph/page.tsx" << 'GRAPHEOF'
'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Network } from 'lucide-react'

export default function GraphPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">گراف شبکه</h2>
        <p className="text-muted-foreground">نمایش ارتباطات و تحلیل شبکه</p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Network className="h-5 w-5" />
            نمایش گراف
          </CardTitle>
          <CardDescription>به زودی...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12 text-muted-foreground">
            در حال توسعه...
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
GRAPHEOF

# Authors page
mkdir -p "app/(dashboard)/dashboard/authors"
cat > "app/(dashboard)/dashboard/authors/page.tsx" << 'AUTHORSEOF'
'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Users } from 'lucide-react'

export default function AuthorsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">نویسندگان</h2>
        <p className="text-muted-foreground">مشاهده و تحلیل نویسندگان</p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            لیست نویسندگان
          </CardTitle>
          <CardDescription>به زودی...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12 text-muted-foreground">
            در حال توسعه...
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
AUTHORSEOF

# Settings page
mkdir -p "app/(dashboard)/dashboard/settings"
cat > "app/(dashboard)/dashboard/settings/page.tsx" << 'SETTINGSEOF'
'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Settings } from 'lucide-react'

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">تنظیمات</h2>
        <p className="text-muted-foreground">تنظیمات حساب کاربری و سامانه</p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            تنظیمات
          </CardTitle>
          <CardDescription>به زودی...</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12 text-muted-foreground">
            در حال توسعه...
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
SETTINGSEOF

# ============================================================
# 4. Redirect root dashboard
# ============================================================
echo "📝 Creating app/(dashboard)/page.tsx redirect..."
cat > "app/(dashboard)/page.tsx" << 'REDIRECTEOF'
import { redirect } from 'next/navigation'

export default function DashboardRoot() {
  redirect('/dashboard')
}
REDIRECTEOF

echo ""
echo "✅ Step 5 complete!"
echo ""
echo "Created files:"
echo "  - app/(dashboard)/layout.tsx"
echo "  - app/(dashboard)/page.tsx (redirect)"
echo "  - app/(dashboard)/dashboard/page.tsx (main dashboard)"
echo "  - app/(dashboard)/dashboard/posts/page.tsx"
echo "  - app/(dashboard)/dashboard/analysis/page.tsx"
echo "  - app/(dashboard)/dashboard/trends/page.tsx"
echo "  - app/(dashboard)/dashboard/graph/page.tsx"
echo "  - app/(dashboard)/dashboard/authors/page.tsx"
echo "  - app/(dashboard)/dashboard/settings/page.tsx"
echo ""
echo "🎯 Test flow:"
echo "  1. Go to http://localhost:3000/login"
echo "  2. Login with: admin / Admin123!"
echo "  3. You should be redirected to /dashboard"
echo ""
