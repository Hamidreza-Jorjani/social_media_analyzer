#!/bin/bash
set -e

echo "🔐 Step 4: Creating Auth Pages (Login/Register)..."
cd "$(dirname "$0")"

# ============================================================
# 1. Auth Layout
# ============================================================
echo "📝 Creating app/(auth)/layout.tsx..."
mkdir -p "app/(auth)"
cat > "app/(auth)/layout.tsx" << 'LAYOUTEOF'
import Link from 'next/link'

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex">
      {/* Left Panel - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary via-primary/90 to-primary/80 p-12 flex-col justify-between">
        <div>
          <Link href="/" className="flex items-center gap-3">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
              <span className="text-2xl">🧠</span>
            </div>
            <span className="text-2xl font-bold text-white">سامانه هوشمند</span>
          </Link>
        </div>
        
        <div className="space-y-6">
          <h1 className="text-4xl font-bold text-white leading-relaxed">
            تحلیل هوشمند
            <br />
            شبکه‌های اجتماعی فارسی
          </h1>
          <p className="text-xl text-white/80 leading-relaxed">
            پلتفرم پیشرفته تحلیل احساسات، کشف روندها و نمایش شبکه‌های اجتماعی
          </p>
          
          <div className="grid grid-cols-2 gap-4 pt-8">
            <div className="bg-white/10 backdrop-blur rounded-xl p-4">
              <div className="text-3xl mb-2">📊</div>
              <div className="text-white font-medium">تحلیل احساسات</div>
              <div className="text-white/60 text-sm">تشخیص مثبت، منفی، خنثی</div>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-xl p-4">
              <div className="text-3xl mb-2">📈</div>
              <div className="text-white font-medium">روندها</div>
              <div className="text-white/60 text-sm">هشتگ‌های ترند</div>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-xl p-4">
              <div className="text-3xl mb-2">🕸️</div>
              <div className="text-white font-medium">گراف شبکه</div>
              <div className="text-white/60 text-sm">تحلیل ارتباطات</div>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-xl p-4">
              <div className="text-3xl mb-2">🎭</div>
              <div className="text-white font-medium">احساسات</div>
              <div className="text-white/60 text-sm">شادی، غم، عصبانیت</div>
            </div>
          </div>
        </div>
        
        <div className="text-white/60 text-sm">
          © ۱۴۰۳ تمامی حقوق محفوظ است
        </div>
      </div>
      
      {/* Right Panel - Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-background">
        <div className="w-full max-w-md">
          {children}
        </div>
      </div>
    </div>
  )
}
LAYOUTEOF

# ============================================================
# 2. Login Page
# ============================================================
echo "📝 Creating app/(auth)/login/page.tsx..."
mkdir -p "app/(auth)/login"
cat > "app/(auth)/login/page.tsx" << 'LOGINEOF'
'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'sonner'
import { Eye, EyeOff, Loader2, LogIn } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { authApi } from '@/lib/api'
import { useAuthStore } from '@/lib/stores/auth-store'
import { getErrorMessage } from '@/lib/api/client'

const loginSchema = z.object({
  username: z.string().min(1, 'نام کاربری الزامی است'),
  password: z.string().min(1, 'رمز عبور الزامی است'),
})

type LoginFormData = z.infer<typeof loginSchema>

export default function LoginPage() {
  const router = useRouter()
  const setAuth = useAuthStore((state) => state.setAuth)
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: '',
      password: '',
    },
  })

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true)
    try {
      const response = await authApi.login(data)
      setAuth(response.user, response.tokens.access_token, response.tokens.refresh_token)
      toast.success(`خوش آمدید، ${response.user.full_name || response.user.username}!`)
      router.push('/dashboard')
    } catch (error) {
      toast.error(getErrorMessage(error))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="border-0 shadow-xl">
      <CardHeader className="space-y-1 text-center">
        <div className="lg:hidden flex justify-center mb-4">
          <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center">
            <span className="text-4xl">🧠</span>
          </div>
        </div>
        <CardTitle className="text-2xl font-bold">ورود به سامانه</CardTitle>
        <CardDescription>
          برای دسترسی به داشبورد، وارد حساب کاربری خود شوید
        </CardDescription>
      </CardHeader>
      
      <form onSubmit={handleSubmit(onSubmit)}>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username">نام کاربری یا ایمیل</Label>
            <Input
              id="username"
              type="text"
              placeholder="admin"
              autoComplete="username"
              disabled={isLoading}
              {...register('username')}
              className={errors.username ? 'border-destructive' : ''}
            />
            {errors.username && (
              <p className="text-sm text-destructive">{errors.username.message}</p>
            )}
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="password">رمز عبور</Label>
              <Link 
                href="/forgot-password" 
                className="text-sm text-primary hover:underline"
              >
                فراموشی رمز عبور؟
              </Link>
            </div>
            <div className="relative">
              <Input
                id="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••"
                autoComplete="current-password"
                disabled={isLoading}
                {...register('password')}
                className={errors.password ? 'border-destructive' : ''}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
            {errors.password && (
              <p className="text-sm text-destructive">{errors.password.message}</p>
            )}
          </div>

          {/* Demo credentials hint */}
          <div className="bg-muted/50 rounded-lg p-3 text-sm">
            <p className="text-muted-foreground">
              <span className="font-medium">حساب آزمایشی:</span>
              {' '}admin / Admin123!
            </p>
          </div>
        </CardContent>
        
        <CardFooter className="flex flex-col gap-4">
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                در حال ورود...
              </>
            ) : (
              <>
                <LogIn className="ml-2 h-4 w-4" />
                ورود
              </>
            )}
          </Button>
          
          <p className="text-sm text-center text-muted-foreground">
            حساب کاربری ندارید؟{' '}
            <Link href="/register" className="text-primary font-medium hover:underline">
              ثبت‌نام کنید
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  )
}
LOGINEOF

# ============================================================
# 3. Register Page
# ============================================================
echo "📝 Creating app/(auth)/register/page.tsx..."
mkdir -p "app/(auth)/register"
cat > "app/(auth)/register/page.tsx" << 'REGISTEREOF'
'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'sonner'
import { Eye, EyeOff, Loader2, UserPlus } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { authApi } from '@/lib/api'
import { useAuthStore } from '@/lib/stores/auth-store'
import { getErrorMessage } from '@/lib/api/client'

const registerSchema = z.object({
  full_name: z.string().min(2, 'نام حداقل ۲ کاراکتر باشد'),
  username: z
    .string()
    .min(3, 'نام کاربری حداقل ۳ کاراکتر باشد')
    .max(20, 'نام کاربری حداکثر ۲۰ کاراکتر باشد')
    .regex(/^[a-zA-Z0-9_]+$/, 'فقط حروف انگلیسی، اعداد و _ مجاز است'),
  email: z.string().email('ایمیل نامعتبر است'),
  password: z
    .string()
    .min(8, 'رمز عبور حداقل ۸ کاراکتر باشد')
    .regex(/[A-Z]/, 'حداقل یک حرف بزرگ')
    .regex(/[a-z]/, 'حداقل یک حرف کوچک')
    .regex(/[0-9]/, 'حداقل یک عدد'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'رمز عبور و تکرار آن یکسان نیستند',
  path: ['confirmPassword'],
})

type RegisterFormData = z.infer<typeof registerSchema>

export default function RegisterPage() {
  const router = useRouter()
  const setAuth = useAuthStore((state) => state.setAuth)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  })

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true)
    try {
      const response = await authApi.register({
        email: data.email,
        username: data.username,
        password: data.password,
        full_name: data.full_name,
      })
      setAuth(response.user, response.tokens.access_token, response.tokens.refresh_token)
      toast.success('ثبت‌نام با موفقیت انجام شد!')
      router.push('/dashboard')
    } catch (error) {
      toast.error(getErrorMessage(error))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="border-0 shadow-xl">
      <CardHeader className="space-y-1 text-center">
        <div className="lg:hidden flex justify-center mb-4">
          <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center">
            <span className="text-4xl">🧠</span>
          </div>
        </div>
        <CardTitle className="text-2xl font-bold">ثبت‌نام</CardTitle>
        <CardDescription>
          حساب کاربری جدید ایجاد کنید
        </CardDescription>
      </CardHeader>
      
      <form onSubmit={handleSubmit(onSubmit)}>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="full_name">نام و نام خانوادگی</Label>
            <Input
              id="full_name"
              type="text"
              placeholder="علی محمدی"
              disabled={isLoading}
              {...register('full_name')}
              className={errors.full_name ? 'border-destructive' : ''}
            />
            {errors.full_name && (
              <p className="text-sm text-destructive">{errors.full_name.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="username">نام کاربری</Label>
            <Input
              id="username"
              type="text"
              placeholder="ali_mohammadi"
              autoComplete="username"
              disabled={isLoading}
              {...register('username')}
              className={errors.username ? 'border-destructive' : ''}
              dir="ltr"
            />
            {errors.username && (
              <p className="text-sm text-destructive">{errors.username.message}</p>
            )}
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="email">ایمیل</Label>
            <Input
              id="email"
              type="email"
              placeholder="ali@example.com"
              autoComplete="email"
              disabled={isLoading}
              {...register('email')}
              className={errors.email ? 'border-destructive' : ''}
              dir="ltr"
            />
            {errors.email && (
              <p className="text-sm text-destructive">{errors.email.message}</p>
            )}
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="password">رمز عبور</Label>
            <div className="relative">
              <Input
                id="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••"
                autoComplete="new-password"
                disabled={isLoading}
                {...register('password')}
                className={errors.password ? 'border-destructive' : ''}
                dir="ltr"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
            {errors.password && (
              <p className="text-sm text-destructive">{errors.password.message}</p>
            )}
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">تکرار رمز عبور</Label>
            <div className="relative">
              <Input
                id="confirmPassword"
                type={showConfirmPassword ? 'text' : 'password'}
                placeholder="••••••••"
                autoComplete="new-password"
                disabled={isLoading}
                {...register('confirmPassword')}
                className={errors.confirmPassword ? 'border-destructive' : ''}
                dir="ltr"
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
            {errors.confirmPassword && (
              <p className="text-sm text-destructive">{errors.confirmPassword.message}</p>
            )}
          </div>
        </CardContent>
        
        <CardFooter className="flex flex-col gap-4">
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                در حال ثبت‌نام...
              </>
            ) : (
              <>
                <UserPlus className="ml-2 h-4 w-4" />
                ثبت‌نام
              </>
            )}
          </Button>
          
          <p className="text-sm text-center text-muted-foreground">
            قبلاً ثبت‌نام کرده‌اید؟{' '}
            <Link href="/login" className="text-primary font-medium hover:underline">
              وارد شوید
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  )
}
REGISTEREOF

# ============================================================
# 4. Add missing UI components (if needed)
# ============================================================
echo "📝 Checking/Creating additional UI components..."

# Check if Card component exists, if not create it
if [ ! -f "components/ui/card.tsx" ]; then
  echo "📝 Creating components/ui/card.tsx..."
  cat > "components/ui/card.tsx" << 'CARDEOF'
import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("rounded-xl border bg-card text-card-foreground shadow", className)}
      {...props}
    />
  )
)
Card.displayName = "Card"

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
)
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn("font-semibold leading-none tracking-tight", className)} {...props} />
  )
)
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn("text-sm text-muted-foreground", className)} {...props} />
  )
)
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
)
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex items-center p-6 pt-0", className)} {...props} />
  )
)
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
CARDEOF
fi

# ============================================================
# 5. Update UI index to export Card
# ============================================================
echo "📝 Updating components/ui/index.ts..."
cat > "components/ui/index.ts" << 'UIINDEXEOF'
export { Avatar, AvatarFallback, AvatarImage } from './avatar'
export { Badge, badgeVariants } from './badge'
export { Button, buttonVariants } from './button'
export { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './card'
export { DropdownMenu, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem, DropdownMenuLabel, DropdownMenuPortal, DropdownMenuSeparator, DropdownMenuShortcut, DropdownMenuSub, DropdownMenuSubContent, DropdownMenuSubTrigger, DropdownMenuTrigger } from './dropdown-menu'
export { Input } from './input'
export { Label } from './label'
export { Progress } from './progress'
export { ScrollArea, ScrollBar } from './scroll-area'
export { Separator } from './separator'
export { Skeleton } from './skeleton'
export { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './tooltip'
UIINDEXEOF

echo ""
echo "✅ Step 4 complete!"
echo ""
echo "Created files:"
echo "  - app/(auth)/layout.tsx"
echo "  - app/(auth)/login/page.tsx"
echo "  - app/(auth)/register/page.tsx"
echo "  - components/ui/card.tsx (if missing)"
echo "  - components/ui/index.ts (updated)"
echo ""
echo "🎯 Next: Test by visiting http://localhost:3000/login"
echo ""
