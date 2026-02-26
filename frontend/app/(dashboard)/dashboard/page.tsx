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
