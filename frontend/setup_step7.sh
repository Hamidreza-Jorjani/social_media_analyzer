#!/bin/bash
set -e

echo "🔬 Step 7: Creating Analysis Page..."
cd "$(dirname "$0")"

# ============================================================
# 1. Add Dialog UI Component
# ============================================================
echo "📝 Creating components/ui/dialog.tsx..."
cat > "components/ui/dialog.tsx" << 'DIALOGEOF'
"use client"

import * as React from "react"
import * as DialogPrimitive from "@radix-ui/react-dialog"
import { X } from "lucide-react"
import { cn } from "@/lib/utils"

const Dialog = DialogPrimitive.Root
const DialogTrigger = DialogPrimitive.Trigger
const DialogPortal = DialogPrimitive.Portal
const DialogClose = DialogPrimitive.Close

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
  />
))
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute left-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
))
DialogContent.displayName = DialogPrimitive.Content.displayName

const DialogHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col space-y-1.5 text-center sm:text-right", className)} {...props} />
)
DialogHeader.displayName = "DialogHeader"

const DialogFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2 sm:space-x-reverse", className)} {...props} />
)
DialogFooter.displayName = "DialogFooter"

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title ref={ref} className={cn("text-lg font-semibold leading-none tracking-tight", className)} {...props} />
))
DialogTitle.displayName = DialogPrimitive.Title.displayName

const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
))
DialogDescription.displayName = DialogPrimitive.Description.displayName

export { Dialog, DialogPortal, DialogOverlay, DialogTrigger, DialogClose, DialogContent, DialogHeader, DialogFooter, DialogTitle, DialogDescription }
DIALOGEOF

# ============================================================
# 2. Add Textarea UI Component
# ============================================================
echo "📝 Creating components/ui/textarea.tsx..."
cat > "components/ui/textarea.tsx" << 'TEXTAREAEOF'
import * as React from "react"
import { cn } from "@/lib/utils"

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Textarea.displayName = "Textarea"

export { Textarea }
TEXTAREAEOF

# ============================================================
# 3. Add Switch UI Component
# ============================================================
echo "📝 Creating components/ui/switch.tsx..."
cat > "components/ui/switch.tsx" << 'SWITCHEOF'
"use client"

import * as React from "react"
import * as SwitchPrimitives from "@radix-ui/react-switch"
import { cn } from "@/lib/utils"

const Switch = React.forwardRef<
  React.ElementRef<typeof SwitchPrimitives.Root>,
  React.ComponentPropsWithoutRef<typeof SwitchPrimitives.Root>
>(({ className, ...props }, ref) => (
  <SwitchPrimitives.Root
    className={cn(
      "peer inline-flex h-5 w-9 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=unchecked]:bg-input",
      className
    )}
    {...props}
    ref={ref}
  >
    <SwitchPrimitives.Thumb
      className={cn(
        "pointer-events-none block h-4 w-4 rounded-full bg-background shadow-lg ring-0 transition-transform data-[state=checked]:translate-x-4 data-[state=unchecked]:translate-x-0 rtl:data-[state=checked]:-translate-x-4"
      )}
    />
  </SwitchPrimitives.Root>
))
Switch.displayName = SwitchPrimitives.Root.displayName

export { Switch }
SWITCHEOF

# ============================================================
# 4. Analysis List Page
# ============================================================
echo "📝 Creating app/(dashboard)/dashboard/analysis/page.tsx..."
cat > "app/(dashboard)/dashboard/analysis/page.tsx" << 'ANALYSISPAGEEOF'
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
ANALYSISPAGEEOF

# ============================================================
# 5. New Analysis Page (Create Form)
# ============================================================
echo "📝 Creating app/(dashboard)/dashboard/analysis/new/page.tsx..."
mkdir -p "app/(dashboard)/dashboard/analysis/new"
cat > "app/(dashboard)/dashboard/analysis/new/page.tsx" << 'NEWANALYSISEOF'
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'sonner'
import { ArrowRight, Loader2, Sparkles } from 'lucide-react'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { analysisApi } from '@/lib/api'
import { getErrorMessage } from '@/lib/api/client'
import type { AnalysisType } from '@/types'

const schema = z.object({
  name: z.string().min(1, 'نام الزامی است'),
  description: z.string().optional(),
  analysis_type: z.string().min(1, 'نوع تحلیل را انتخاب کنید'),
  platform: z.string().optional(),
  sentiment_enabled: z.boolean(),
  emotion_enabled: z.boolean(),
  keyword_extraction_enabled: z.boolean(),
})

type FormData = z.infer<typeof schema>

const analysisTypes: { value: AnalysisType; label: string; description: string }[] = [
  { value: 'full', label: 'تحلیل کامل', description: 'شامل همه تحلیل‌ها' },
  { value: 'sentiment', label: 'تحلیل احساسات', description: 'مثبت، منفی، خنثی' },
  { value: 'emotion', label: 'تشخیص احساسات', description: 'شادی، غم، عصبانیت، ترس' },
  { value: 'keyword_extraction', label: 'استخراج کلمات کلیدی', description: 'کلمات مهم متن' },
  { value: 'topic_modeling', label: 'مدل‌سازی موضوع', description: 'موضوعات اصلی' },
]

export default function NewAnalysisPage() {
  const router = useRouter()
  const [isSubmitting, setIsSubmitting] = useState(false)

  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      name: '',
      description: '',
      analysis_type: 'full',
      platform: 'all',
      sentiment_enabled: true,
      emotion_enabled: true,
      keyword_extraction_enabled: true,
    },
  })

  const onSubmit = async (data: FormData) => {
    setIsSubmitting(true)
    try {
      const analysis = await analysisApi.create({
        name: data.name,
        description: data.description,
        analysis_type: data.analysis_type as AnalysisType,
        config: {
          sentiment_enabled: data.sentiment_enabled,
          emotion_enabled: data.emotion_enabled,
          keyword_extraction_enabled: data.keyword_extraction_enabled,
        },
        query_filters: data.platform !== 'all' ? { platform: data.platform } : undefined,
      })
      toast.success('تحلیل با موفقیت ایجاد شد')
      router.push('/dashboard/analysis')
    } catch (error) {
      toast.error(getErrorMessage(error))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()}>
          <ArrowRight className="h-5 w-5" />
        </Button>
        <div>
          <h2 className="text-2xl font-bold">تحلیل جدید</h2>
          <p className="text-muted-foreground">ایجاد تحلیل NLP جدید</p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>اطلاعات پایه</CardTitle>
            <CardDescription>نام و توضیحات تحلیل را وارد کنید</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">نام تحلیل *</Label>
              <Input
                id="name"
                placeholder="مثال: تحلیل احساسات فروردین"
                {...register('name')}
                className={errors.name ? 'border-destructive' : ''}
              />
              {errors.name && <p className="text-sm text-destructive">{errors.name.message}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">توضیحات</Label>
              <Textarea
                id="description"
                placeholder="توضیحات اختیاری درباره این تحلیل..."
                {...register('description')}
              />
            </div>

            <div className="space-y-2">
              <Label>نوع تحلیل *</Label>
              <Select value={watch('analysis_type')} onValueChange={(v) => setValue('analysis_type', v)}>
                <SelectTrigger>
                  <SelectValue placeholder="انتخاب نوع تحلیل" />
                </SelectTrigger>
                <SelectContent>
                  {analysisTypes.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      <div>
                        <div className="font-medium">{type.label}</div>
                        <div className="text-xs text-muted-foreground">{type.description}</div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>پلتفرم</Label>
              <Select value={watch('platform')} onValueChange={(v) => setValue('platform', v)}>
                <SelectTrigger>
                  <SelectValue placeholder="انتخاب پلتفرم" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">همه پلتفرم‌ها</SelectItem>
                  <SelectItem value="twitter">توییتر</SelectItem>
                  <SelectItem value="instagram">اینستاگرام</SelectItem>
                  <SelectItem value="telegram">تلگرام</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>تنظیمات تحلیل</CardTitle>
            <CardDescription>انتخاب ویژگی‌های تحلیل</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label>تحلیل احساسات</Label>
                <p className="text-sm text-muted-foreground">تشخیص مثبت، منفی، خنثی</p>
              </div>
              <Switch
                checked={watch('sentiment_enabled')}
                onCheckedChange={(v) => setValue('sentiment_enabled', v)}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label>تشخیص احساسات</Label>
                <p className="text-sm text-muted-foreground">شادی، غم، عصبانیت، ترس، تعجب</p>
              </div>
              <Switch
                checked={watch('emotion_enabled')}
                onCheckedChange={(v) => setValue('emotion_enabled', v)}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label>استخراج کلمات کلیدی</Label>
                <p className="text-sm text-muted-foreground">کلمات مهم هر متن</p>
              </div>
              <Switch
                checked={watch('keyword_extraction_enabled')}
                onCheckedChange={(v) => setValue('keyword_extraction_enabled', v)}
              />
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-end gap-4">
          <Button type="button" variant="outline" onClick={() => router.back()}>
            انصراف
          </Button>
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 ml-2 animate-spin" />
                در حال ایجاد...
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4 ml-2" />
                ایجاد تحلیل
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  )
}
NEWANALYSISEOF

# ============================================================
# 6. Analysis Results Page
# ============================================================
echo "📝 Creating app/(dashboard)/dashboard/analysis/[id]/page.tsx..."
mkdir -p "app/(dashboard)/dashboard/analysis/[id]"
cat > "app/(dashboard)/dashboard/analysis/[id]/page.tsx" << 'RESULTSEOF'
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
RESULTSEOF

echo ""
echo "✅ Step 7 complete! Analysis pages created."
