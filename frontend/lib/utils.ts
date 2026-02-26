import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

/**
 * Merge Tailwind classes with clsx
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Format number with Persian numerals
 */
export function toPersianNumber(num: number | string): string {
  const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
  return String(num).replace(/[0-9]/g, (d) => persianDigits[parseInt(d)])
}

/**
 * Format large numbers (1000 -> 1K, 1000000 -> 1M)
 */
export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  }
  return num.toString()
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text: string, length: number): string {
  if (!text) return ''
  if (text.length <= length) return text
  return text.slice(0, length) + '...'
}

/**
 * Format date relative to now (Persian)
 */
export function formatRelativeTime(date: string | Date): string {
  const now = new Date()
  const then = new Date(date)
  const diffMs = now.getTime() - then.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'همین الان'
  if (diffMins < 60) return `${toPersianNumber(diffMins)} دقیقه پیش`
  if (diffHours < 24) return `${toPersianNumber(diffHours)} ساعت پیش`
  if (diffDays < 7) return `${toPersianNumber(diffDays)} روز پیش`
  if (diffDays < 30) return `${toPersianNumber(Math.floor(diffDays / 7))} هفته پیش`
  return `${toPersianNumber(Math.floor(diffDays / 30))} ماه پیش`
}

/**
 * Format date to Persian format
 */
export function formatDate(date: string | Date): string {
  const d = new Date(date)
  return d.toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

/**
 * Format datetime to Persian format
 */
export function formatDateTime(date: string | Date): string {
  const d = new Date(date)
  return d.toLocaleString('fa-IR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * Format percentage
 */
export function formatPercent(value: number, decimals: number = 1): string {
  return `${(value * 100).toFixed(decimals)}%`
}

/**
 * Get sentiment color class
 */
export function getSentimentColor(sentiment: 'positive' | 'negative' | 'neutral'): string {
  const colors = {
    positive: 'text-green-500',
    negative: 'text-red-500',
    neutral: 'text-gray-500',
  }
  return colors[sentiment]
}

/**
 * Get platform color class
 */
export function getPlatformColor(platform: string): string {
  const colors: Record<string, string> = {
    twitter: 'bg-blue-500',
    instagram: 'bg-pink-500',
    telegram: 'bg-sky-500',
  }
  return colors[platform] || 'bg-gray-500'
}
