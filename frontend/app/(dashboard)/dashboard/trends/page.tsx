'use client'

import { useEffect, useState } from 'react'
import { TrendingUp, Hash, Type, RefreshCw } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { trendsApi } from '@/lib/api'
import { cn, toPersianNumber, formatNumber } from '@/lib/utils'
import type { TrendingItem, SentimentTrend, VolumeTrend } from '@/types'

const COLORS = {
  positive: '#22c55e',
  negative: '#ef4444',
  neutral: '#6b7280',
}

export default function TrendsPage() {
  const [hashtags, setHashtags] = useState<TrendingItem[]>([])
  const [keywords, setKeywords] = useState<TrendingItem[]>([])
  const [sentimentTrends, setSentimentTrends] = useState<SentimentTrend[]>([])
  const [volumeTrends, setVolumeTrends] = useState<VolumeTrend[]>([])
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    setLoading(true)
    try {
      const [hashtagsData, keywordsData, sentimentData, volumeData] = await Promise.all([
        trendsApi.hashtags(24, 10),
        trendsApi.keywords(24, 10),
        trendsApi.sentiment(24, '1h'),
        trendsApi.volume(24, '1h'),
      ])
      setHashtags(hashtagsData)
      setKeywords(keywordsData)
      setSentimentTrends(sentimentData)
      setVolumeTrends(volumeData)
    } catch (error) {
      console.error('Error fetching trends:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const totalSentiment = sentimentTrends.reduce(
    (acc, curr) => ({
      positive: acc.positive + curr.positive,
      negative: acc.negative + curr.negative,
      neutral: acc.neutral + curr.neutral,
    }),
    { positive: 0, negative: 0, neutral: 0 }
  )

  const pieData = [
    { name: 'مثبت', value: totalSentiment.positive, color: COLORS.positive },
    { name: 'منفی', value: totalSentiment.negative, color: COLORS.negative },
    { name: 'خنثی', value: totalSentiment.neutral, color: COLORS.neutral },
  ]

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">روندها</h2>
          <p className="text-muted-foreground">هشتگ‌ها و کلمات کلیدی ترند</p>
        </div>
        <Button onClick={fetchData} variant="outline" size="sm">
          <RefreshCw className={cn('h-4 w-4 ml-2', loading && 'animate-spin')} />
          بروزرسانی
        </Button>
      </div>

      {/* Volume Chart */}
      <Card>
        <CardHeader>
          <CardTitle>حجم پست‌ها در ۲۴ ساعت گذشته</CardTitle>
          <CardDescription>تعداد پست‌ها به تفکیک ساعت</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <Skeleton className="h-64 w-full" />
          ) : (
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={volumeTrends}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                <XAxis dataKey="time" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px',
                    direction: 'rtl',
                  }}
                  formatter={(value: number) => [toPersianNumber(value), 'تعداد']}
                />
                <Area type="monotone" dataKey="count" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.2} />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </CardContent>
      </Card>

      {/* Sentiment Charts */}
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>روند احساسات</CardTitle>
            <CardDescription>تغییرات احساسات در طول زمان</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <Skeleton className="h-64 w-full" />
            ) : (
              <ResponsiveContainer width="100%" height={250}>
                <AreaChart data={sentimentTrends}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                  <XAxis dataKey="time" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'hsl(var(--card))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px',
                      direction: 'rtl',
                    }}
                  />
                  <Area type="monotone" dataKey="positive" stackId="1" stroke={COLORS.positive} fill={COLORS.positive} fillOpacity={0.6} name="مثبت" />
                  <Area type="monotone" dataKey="neutral" stackId="1" stroke={COLORS.neutral} fill={COLORS.neutral} fillOpacity={0.6} name="خنثی" />
                  <Area type="monotone" dataKey="negative" stackId="1" stroke={COLORS.negative} fill={COLORS.negative} fillOpacity={0.6} name="منفی" />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>توزیع احساسات</CardTitle>
            <CardDescription>نسبت احساسات در ۲۴ ساعت</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <Skeleton className="h-64 w-full" />
            ) : (
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={2}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value: number) => toPersianNumber(value)} />
                </PieChart>
              </ResponsiveContainer>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Trending Lists */}
      <Tabs defaultValue="hashtags" className="space-y-4">
        <TabsList>
          <TabsTrigger value="hashtags" className="gap-2">
            <Hash className="h-4 w-4" />
            هشتگ‌ها
          </TabsTrigger>
          <TabsTrigger value="keywords" className="gap-2">
            <Type className="h-4 w-4" />
            کلمات کلیدی
          </TabsTrigger>
        </TabsList>

        <TabsContent value="hashtags">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Hash className="h-5 w-5" />
                هشتگ‌های ترند
              </CardTitle>
              <CardDescription>پرتکرارترین هشتگ‌ها در ۲۴ ساعت گذشته</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="space-y-3">
                  {Array.from({ length: 5 }).map((_, i) => (
                    <Skeleton key={i} className="h-12 w-full" />
                  ))}
                </div>
              ) : hashtags.length === 0 ? (
                <p className="text-center text-muted-foreground py-8">هشتگی یافت نشد</p>
              ) : (
                <div className="space-y-3">
                  {hashtags.map((item, index) => (
                    <div key={item.item} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                      <div className="flex items-center gap-3">
                        <span
                          className={cn(
                            'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold',
                            index === 0 && 'bg-yellow-500 text-white',
                            index === 1 && 'bg-gray-400 text-white',
                            index === 2 && 'bg-amber-600 text-white',
                            index > 2 && 'bg-muted text-muted-foreground'
                          )}
                        >
                          {toPersianNumber(index + 1)}
                        </span>
                        <span className="font-medium text-lg">#{item.item}</span>
                      </div>
                      <Badge variant="secondary" className="text-lg">
                        {toPersianNumber(formatNumber(item.count))}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="keywords">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Type className="h-5 w-5" />
                کلمات کلیدی ترند
              </CardTitle>
              <CardDescription>پرتکرارترین کلمات در ۲۴ ساعت گذشته</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <Skeleton className="h-64 w-full" />
              ) : keywords.length === 0 ? (
                <p className="text-center text-muted-foreground py-8">کلمه‌ای یافت نشد</p>
              ) : (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={keywords.slice(0, 10)} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                    <XAxis type="number" tick={{ fontSize: 12 }} />
                    <YAxis dataKey="item" type="category" tick={{ fontSize: 12 }} width={80} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'hsl(var(--card))',
                        border: '1px solid hsl(var(--border))',
                        borderRadius: '8px',
                        direction: 'rtl',
                      }}
                      formatter={(value: number) => [toPersianNumber(value), 'تعداد']}
                    />
                    <Bar dataKey="count" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
