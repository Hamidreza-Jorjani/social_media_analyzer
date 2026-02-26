'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'sonner'
import { User, Lock, Bell, Palette, Save, Loader2, Moon, Sun } from 'lucide-react'
import { useTheme } from 'next-themes'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Separator } from '@/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { useAuthStore } from '@/lib/stores/auth-store'
import { authApi, getErrorMessage } from '@/lib/api'

const profileSchema = z.object({
  full_name: z.string().min(2, 'نام حداقل ۲ کاراکتر'),
  email: z.string().email('ایمیل نامعتبر'),
})

const passwordSchema = z.object({
  current_password: z.string().min(1, 'رمز فعلی الزامی است'),
  new_password: z.string().min(8, 'رمز جدید حداقل ۸ کاراکتر'),
  confirm_password: z.string(),
}).refine((data) => data.new_password === data.confirm_password, {
  message: 'رمز عبور و تکرار یکسان نیستند',
  path: ['confirm_password'],
})

type ProfileFormData = z.infer<typeof profileSchema>
type PasswordFormData = z.infer<typeof passwordSchema>

export default function SettingsPage() {
  const { user } = useAuthStore()
  const { theme, setTheme } = useTheme()
  const [savingProfile, setSavingProfile] = useState(false)
  const [savingPassword, setSavingPassword] = useState(false)

  const profileForm = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      full_name: user?.full_name || '',
      email: user?.email || '',
    },
  })

  const passwordForm = useForm<PasswordFormData>({
    resolver: zodResolver(passwordSchema),
    defaultValues: {
      current_password: '',
      new_password: '',
      confirm_password: '',
    },
  })

  const onProfileSubmit = async (data: ProfileFormData) => {
    setSavingProfile(true)
    try {
      // API call would go here
      toast.success('پروفایل با موفقیت بروزرسانی شد')
    } catch (error) {
      toast.error(getErrorMessage(error))
    } finally {
      setSavingProfile(false)
    }
  }

  const onPasswordSubmit = async (data: PasswordFormData) => {
    setSavingPassword(true)
    try {
      await authApi.changePassword(data.current_password, data.new_password)
      toast.success('رمز عبور با موفقیت تغییر کرد')
      passwordForm.reset()
    } catch (error) {
      toast.error(getErrorMessage(error))
    } finally {
      setSavingPassword(false)
    }
  }

  const userInitials = user?.full_name
    ? user.full_name.split(' ').map((n) => n[0]).join('').slice(0, 2)
    : user?.username.slice(0, 2).toUpperCase() || 'UN'

  const roleLabels: Record<string, string> = {
    admin: 'مدیر سیستم',
    analyst: 'تحلیلگر',
    viewer: 'مشاهده‌کننده',
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">تنظیمات</h2>
        <p className="text-muted-foreground">مدیریت حساب کاربری و تنظیمات سامانه</p>
      </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList>
          <TabsTrigger value="profile" className="gap-2">
            <User className="h-4 w-4" />
            پروفایل
          </TabsTrigger>
          <TabsTrigger value="security" className="gap-2">
            <Lock className="h-4 w-4" />
            امنیت
          </TabsTrigger>
          <TabsTrigger value="appearance" className="gap-2">
            <Palette className="h-4 w-4" />
            ظاهر
          </TabsTrigger>
          <TabsTrigger value="notifications" className="gap-2">
            <Bell className="h-4 w-4" />
            اعلان‌ها
          </TabsTrigger>
        </TabsList>

        {/* Profile Tab */}
        <TabsContent value="profile">
          <Card>
            <CardHeader>
              <CardTitle>پروفایل کاربری</CardTitle>
              <CardDescription>اطلاعات حساب کاربری خود را مدیریت کنید</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center gap-6">
                <Avatar className="h-20 w-20">
                  <AvatarFallback className="text-2xl bg-primary text-primary-foreground">
                    {userInitials}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <h3 className="text-lg font-medium">{user?.full_name || user?.username}</h3>
                  <p className="text-muted-foreground">{user?.email}</p>
                  <p className="text-sm text-muted-foreground mt-1">
                    نقش: {roleLabels[user?.role || 'viewer']}
                  </p>
                </div>
              </div>

              <Separator />

              <form onSubmit={profileForm.handleSubmit(onProfileSubmit)} className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="full_name">نام و نام خانوادگی</Label>
                    <Input
                      id="full_name"
                      {...profileForm.register('full_name')}
                      className={profileForm.formState.errors.full_name ? 'border-destructive' : ''}
                    />
                    {profileForm.formState.errors.full_name && (
                      <p className="text-sm text-destructive">{profileForm.formState.errors.full_name.message}</p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="email">ایمیل</Label>
                    <Input
                      id="email"
                      type="email"
                      dir="ltr"
                      {...profileForm.register('email')}
                      className={profileForm.formState.errors.email ? 'border-destructive' : ''}
                    />
                    {profileForm.formState.errors.email && (
                      <p className="text-sm text-destructive">{profileForm.formState.errors.email.message}</p>
                    )}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>نام کاربری</Label>
                  <Input value={user?.username || ''} disabled className="bg-muted" dir="ltr" />
                  <p className="text-xs text-muted-foreground">نام کاربری قابل تغییر نیست</p>
                </div>

                <Button type="submit" disabled={savingProfile}>
                  {savingProfile ? (
                    <>
                      <Loader2 className="h-4 w-4 ml-2 animate-spin" />
                      در حال ذخیره...
                    </>
                  ) : (
                    <>
                      <Save className="h-4 w-4 ml-2" />
                      ذخیره تغییرات
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Security Tab */}
        <TabsContent value="security">
          <Card>
            <CardHeader>
              <CardTitle>تغییر رمز عبور</CardTitle>
              <CardDescription>رمز عبور خود را تغییر دهید</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={passwordForm.handleSubmit(onPasswordSubmit)} className="space-y-4 max-w-md">
                <div className="space-y-2">
                  <Label htmlFor="current_password">رمز عبور فعلی</Label>
                  <Input
                    id="current_password"
                    type="password"
                    dir="ltr"
                    {...passwordForm.register('current_password')}
                    className={passwordForm.formState.errors.current_password ? 'border-destructive' : ''}
                  />
                  {passwordForm.formState.errors.current_password && (
                    <p className="text-sm text-destructive">{passwordForm.formState.errors.current_password.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="new_password">رمز عبور جدید</Label>
                  <Input
                    id="new_password"
                    type="password"
                    dir="ltr"
                    {...passwordForm.register('new_password')}
                    className={passwordForm.formState.errors.new_password ? 'border-destructive' : ''}
                  />
                  {passwordForm.formState.errors.new_password && (
                    <p className="text-sm text-destructive">{passwordForm.formState.errors.new_password.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirm_password">تکرار رمز عبور جدید</Label>
                  <Input
                    id="confirm_password"
                    type="password"
                    dir="ltr"
                    {...passwordForm.register('confirm_password')}
                    className={passwordForm.formState.errors.confirm_password ? 'border-destructive' : ''}
                  />
                  {passwordForm.formState.errors.confirm_password && (
                    <p className="text-sm text-destructive">{passwordForm.formState.errors.confirm_password.message}</p>
                  )}
                </div>

                <Button type="submit" disabled={savingPassword}>
                  {savingPassword ? (
                    <>
                      <Loader2 className="h-4 w-4 ml-2 animate-spin" />
                      در حال تغییر...
                    </>
                  ) : (
                    <>
                      <Lock className="h-4 w-4 ml-2" />
                      تغییر رمز عبور
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Appearance Tab */}
        <TabsContent value="appearance">
          <Card>
            <CardHeader>
              <CardTitle>ظاهر سامانه</CardTitle>
              <CardDescription>تنظیمات نمایشی را تغییر دهید</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>حالت تاریک</Label>
                  <p className="text-sm text-muted-foreground">تغییر بین حالت روشن و تاریک</p>
                </div>
                <div className="flex items-center gap-2">
                  <Sun className="h-4 w-4" />
                  <Switch
                    checked={theme === 'dark'}
                    onCheckedChange={(checked) => setTheme(checked ? 'dark' : 'light')}
                  />
                  <Moon className="h-4 w-4" />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notifications Tab */}
        <TabsContent value="notifications">
          <Card>
            <CardHeader>
              <CardTitle>تنظیمات اعلان‌ها</CardTitle>
              <CardDescription>مدیریت اعلان‌های سامانه</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>اعلان ایمیلی</Label>
                  <p className="text-sm text-muted-foreground">دریافت اعلان از طریق ایمیل</p>
                </div>
                <Switch defaultChecked />
              </div>

              <Separator />

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>اعلان تکمیل تحلیل</Label>
                  <p className="text-sm text-muted-foreground">اطلاع‌رسانی هنگام تکمیل تحلیل‌ها</p>
                </div>
                <Switch defaultChecked />
              </div>

              <Separator />

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>اعلان روندهای جدید</Label>
                  <p className="text-sm text-muted-foreground">اطلاع‌رسانی هنگام شناسایی روند جدید</p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
