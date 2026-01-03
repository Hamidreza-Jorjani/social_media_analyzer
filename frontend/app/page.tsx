import Link from 'next/link'

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="flex flex-col items-center justify-center min-h-[80vh] text-center">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            🚀 سامانه هوشمند
          </h1>
          <h2 className="text-3xl font-bold text-primary mb-8">
            تحلیل شبکه‌های اجتماعی فارسی
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mb-12">
            پلتفرم پیشرفته تحلیل احساسات، روندها و شبکه‌های اجتماعی
          </p>
          <div className="flex gap-4">
            <Link href="/login" className="bg-primary text-white px-8 py-4 rounded-lg text-lg font-medium hover:bg-primary/90">
              ورود به سامانه
            </Link>
            <Link href="/register" className="border border-input bg-background px-8 py-4 rounded-lg text-lg font-medium hover:bg-accent">
              ثبت‌نام
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20 max-w-5xl">
            <div className="bg-card p-6 rounded-xl border shadow-sm">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-semibold mb-2">تحلیل احساسات</h3>
              <p className="text-muted-foreground">تشخیص احساسات در متون فارسی</p>
            </div>
            <div className="bg-card p-6 rounded-xl border shadow-sm">
              <div className="text-4xl mb-4">📈</div>
              <h3 className="text-xl font-semibold mb-2">تحلیل روندها</h3>
              <p className="text-muted-foreground">شناسایی هشتگ‌های ترند</p>
            </div>
            <div className="bg-card p-6 rounded-xl border shadow-sm">
              <div className="text-4xl mb-4">🕸️</div>
              <h3 className="text-xl font-semibold mb-2">تحلیل شبکه</h3>
              <p className="text-muted-foreground">نمایش گراف ارتباطات</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
