'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { ArrowRight, Smile, Frown, Meh, Loader2 } from 'lucide-react'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Skeleton } from '@/components/ui/skeleton'
import { analysisApi } from '@/lib/api'
import { cn, toPersianNumber, formatNumber, formatDateTime } from '@/lib/utils'
import type { Analysis, AnalysisSummary } from '@/types'

export default function AnalysisResultsPage() {
  const params = useParams()
  const router = useRouter()
  const id = Number(params.id)
  
  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [summary, setSummary] = useState<AnalysisSummary | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [analysisData, summaryData] = await Promise.all([
          analysisApi.get(id),
          analysisApi.summary(id),
        ])
        setAnalysis(analysisData)
        setSummary(summaryData)
      } catch (error) {
        console.error('Error fetching analysis:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [id])

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <div className="grid gap-4 md:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-32" />
          ))}
        </div>
        <Skeleton className="h-64" />
      </div>
    )
  }

  if (!analysis || !summary) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">تحلیل یافت نشد</p>
        <Button variant="link" onClick={() => router.back()}>بازگشت</Button>
      </div>
    )
  }

  const total = summary.sentiment_distribution.positive + summary.sentiment_distribution.negative + summary.sentiment_distribution.neutral
  const sentiments = [
    { label: 'مثبت', value: summary.sentiment_distribution.positive, percent: (summary.sentiment_distribution.positive / total) * 100, icon: Smile, color: 'text-green-500' },
    { label: 'منفی', value: summary.sentiment_distribution.negative, percent: (summary.sentiment_distribution.negative / total) * 100, icon: Frown, color: 'text-red-500' },
    { label: 'خنثی', value: summary.sentiment_distribution.neutral, percent: (summary.sentiment_distribution.neutral / total) * 100, icon: Meh, color: 'text-gray-500' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()}>
          <ArrowRight className="h-5 w-5" />
        </Button>
        <div>
          <h2 className="text-2xl font-bold">{analysis.name}</h2>
          <p className="text-muted-foreground">{analysis.description}</p>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        {sentiments.map((s) => (
          <Card key={s.label}>
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center gap-2 text-base">
                <s.icon className={cn("h-5 w-5", s.color)} />
                {s.label}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{toPersianNumber(formatNumber(s.value))}</div>
              <Progress value={s.percent} className="mt-2" />
              <p className="text-sm text-muted-foreground mt-1">{toPersianNumber(s.percent.toFixed(1))}%</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Top Keywords */}
      {summary.top_keywords && summary.top_keywords.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>کلمات کلیدی برتر</CardTitle>
            <CardDescription>پرتکرارترین کلمات در پست‌ها</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {summary.top_keywords.slice(0, 20).map((kw, i) => (
                <Badge key={i} variant="secondary" className="text-sm">
                  {kw.keyword}
                  <span className="mr-1 text-muted-foreground">({toPersianNumber(kw.count)})</span>
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Emotions */}
      {summary.emotion_distribution && Object.keys(summary.emotion_distribution).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>توزیع احساسات</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-5">
              {Object.entries(summary.emotion_distribution).map(([emotion, count]) => (
                <div key={emotion} className="text-center">
                  <div className="text-2xl font-bold">{toPersianNumber(formatNumber(count as number))}</div>
                  <div className="text-sm text-muted-foreground">{emotion}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Info */}
      <Card>
        <CardHeader>
          <CardTitle>اطلاعات تحلیل</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-2">
          <div>
            <p className="text-sm text-muted-foreground">تعداد پست‌ها</p>
            <p className="font-medium">{toPersianNumber(summary.total_posts)}</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">پست‌های پردازش‌شده</p>
            <p className="font-medium">{toPersianNumber(summary.processed_posts)}</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">میانگین امتیاز احساسات</p>
            <p className="font-medium">{toPersianNumber(summary.average_sentiment_score.toFixed(2))}</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">زمان تولید</p>
            <p className="font-medium">{formatDateTime(summary.generated_at)}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
