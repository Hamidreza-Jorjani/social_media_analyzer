'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { 
  Plus, 
  RefreshCw, 
  Play, 
  Square, 
  Trash2, 
  Eye,
  Clock,
  CheckCircle,
  XCircle,
  Loader2,
  BarChart3
} from 'lucide-react'
import { toast } from 'sonner'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Skeleton } from '@/components/ui/skeleton'
import { analysisApi } from '@/lib/api'
import { cn, toPersianNumber, formatRelativeTime, formatDateTime } from '@/lib/utils'
import type { Analysis, AnalysisStatus, AnalysisType } from '@/types'

const statusConfig: Record<AnalysisStatus, { label: string; color: string; icon: React.ElementType }> = {
  pending: { label: 'در انتظار', color: 'bg-gray-500', icon: Clock },
  queued: { label: 'در صف', color: 'bg-yellow-500', icon: Clock },
  processing: { label: 'در حال پردازش', color: 'bg-blue-500', icon: Loader2 },
  completed: { label: 'تکمیل شده', color: 'bg-green-500', icon: CheckCircle },
  failed: { label: 'خطا', color: 'bg-red-500', icon: XCircle },
  cancelled: { label: 'لغو شده', color: 'bg-gray-400', icon: Square },
}

const typeLabels: Record<AnalysisType, string> = {
  sentiment: 'تحلیل احساسات',
  emotion: 'تشخیص احساسات',
  summarization: 'خلاصه‌سازی',
  topic_modeling: 'مدل‌سازی موضوع',
  keyword_extraction: 'استخراج کلمات',
  entity_recognition: 'شناسایی موجودیت',
  trend_detection: 'تشخیص روند',
  graph_analysis: 'تحلیل گراف',
  full: 'تحلیل کامل',
}

function AnalysisCard({ analysis, onRefresh }: { analysis: Analysis; onRefresh: () => void }) {
  const [starting, setStarting] = useState(false)
  const [progress, setProgress] = useState(analysis.progress)
  const status = statusConfig[analysis.status]
  const StatusIcon = status.icon

  useEffect(() => {
    if (analysis.status === 'processing') {
      const interval = setInterval(async () => {
        try {
          const prog = await analysisApi.progress(analysis.id)
          setProgress(prog.progress)
          if (prog.status === 'completed' || prog.status === 'failed') {
            onRefresh()
          }
        } catch (e) {
          console.error(e)
        }
      }, 2000)
      return () => clearInterval(interval)
    }
  }, [analysis.status, analysis.id, onRefresh])

  const handleStart = async () => {
    setStarting(true)
    try {
      await analysisApi.start(analysis.id)
      toast.success('تحلیل شروع شد')
      onRefresh()
    } catch (error) {
      toast.error('خطا در شروع تحلیل')
    } finally {
      setStarting(false)
    }
  }

  const handleCancel = async () => {
    try {
      await analysisApi.cancel(analysis.id)
      toast.success('تحلیل لغو شد')
      onRefresh()
    } catch (error) {
      toast.error('خطا در لغو تحلیل')
    }
  }

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <CardTitle className="text-lg">{analysis.name}</CardTitle>
            <CardDescription>{analysis.description || 'بدون توضیحات'}</CardDescription>
          </div>
          <Badge className={cn("text-white", status.color)}>
            <StatusIcon className={cn("h-3 w-3 ml-1", analysis.status === 'processing' && "animate-spin")} />
            {status.label}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex flex-wrap gap-2">
          <Badge variant="outline">{typeLabels[analysis.analysis_type]}</Badge>
          <Badge variant="secondary">{toPersianNumber(analysis.post_count)} پست</Badge>
        </div>

        {analysis.status === 'processing' && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>پیشرفت</span>
              <span>{toPersianNumber(progress.toFixed(0))}%</span>
            </div>
            <Progress value={progress} />
          </div>
        )}

        <div className="flex items-center justify-between pt-2 border-t">
          <span className="text-xs text-muted-foreground">
            {formatRelativeTime(analysis.created_at)}
          </span>
          <div className="flex gap-2">
            {analysis.status === 'pending' && (
              <Button size="sm" onClick={handleStart} disabled={starting}>
                {starting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4 ml-1" />}
                شروع
              </Button>
            )}
            {analysis.status === 'processing' && (
              <Button size="sm" variant="destructive" onClick={handleCancel}>
                <Square className="h-4 w-4 ml-1" />
                لغو
              </Button>
            )}
            {analysis.status === 'completed' && (
              <Button size="sm" variant="outline" asChild>
                <Link href={`/dashboard/analysis/${analysis.id}`}>
                  <Eye className="h-4 w-4 ml-1" />
                  نتایج
                </Link>
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default function AnalysisPage() {
  const [analyses, setAnalyses] = useState<Analysis[]>([])
  const [loading, setLoading] = useState(true)

  const fetchAnalyses = async () => {
    setLoading(true)
    try {
      const data = await analysisApi.list()
      setAnalyses(data)
    } catch (error) {
      console.error('Error fetching analyses:', error)
      toast.error('خطا در دریافت تحلیل‌ها')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAnalyses()
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">تحلیل‌ها</h2>
          <p className="text-muted-foreground">ایجاد و مدیریت تحلیل‌های NLP</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={fetchAnalyses} variant="outline" size="sm">
            <RefreshCw className={cn("h-4 w-4 ml-2", loading && "animate-spin")} />
            بروزرسانی
          </Button>
          <Button asChild>
            <Link href="/dashboard/analysis/new">
              <Plus className="h-4 w-4 ml-2" />
              تحلیل جدید
            </Link>
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Card key={i}>
              <CardHeader>
                <Skeleton className="h-5 w-32" />
                <Skeleton className="h-4 w-48" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-20 w-full" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : analyses.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <BarChart3 className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground mb-4">هنوز تحلیلی ایجاد نشده</p>
            <Button asChild>
              <Link href="/dashboard/analysis/new">
                <Plus className="h-4 w-4 ml-2" />
                ایجاد اولین تحلیل
              </Link>
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {analyses.map((analysis) => (
            <AnalysisCard key={analysis.id} analysis={analysis} onRefresh={fetchAnalyses} />
          ))}
        </div>
      )}
    </div>
  )
}
