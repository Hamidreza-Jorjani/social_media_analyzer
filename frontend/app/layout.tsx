import type { Metadata } from 'next'
import { Vazirmatn, Inter } from 'next/font/google'
import { Providers } from '@/providers'
import './globals.css'

const vazirmatn = Vazirmatn({ subsets: ['arabic'], variable: '--font-vazirmatn' })
const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

export const metadata: Metadata = {
  title: 'سامانه هوشمند تحلیل اجتماعی',
  description: 'پلتفرم هوشمند تحلیل شبکه‌های اجتماعی فارسی',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fa" dir="rtl" suppressHydrationWarning>
      <body className={`${vazirmatn.variable} ${inter.variable} font-sans antialiased`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
