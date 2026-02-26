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
