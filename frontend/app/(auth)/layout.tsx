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
