'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { 
  Search, 
  Filter, 
  RefreshCw, 
  Eye,
  MessageSquare,
  Heart,
  Share2,
  ExternalLink,
  ChevronRight,
  ChevronLeft
} from 'lucide-react'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import { postsApi } from '@/lib/api'
import { cn, toPersianNumber, formatNumber, formatRelativeTime, truncate } from '@/lib/utils'
import type { Post, Platform } from '@/types'

const platformLabels: Record<Platform, string> = {
  twitter: 'توییتر',
  instagram: 'اینستاگرام',
  telegram: 'تلگرام',
  linkedin: 'لینکدین',
  youtube: 'یوتیوب',
  news: 'خبر',
  forum: 'فروم',
  custom: 'سفارشی',
}

const platformColors: Record<Platform, string> = {
  twitter: 'bg-blue-500',
  instagram: 'bg-pink-500',
  telegram: 'bg-sky-500',
  linkedin: 'bg-blue-700',
  youtube: 'bg-red-500',
  news: 'bg-gray-500',
  forum: 'bg-green-500',
  custom: 'bg-purple-500',
}

export default function PostsPage() {
  const router = useRouter()
  const [posts, setPosts] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [platform, setPlatform] = useState<string>('all')
  const [page, setPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)
  const pageSize = 20

  const fetchPosts = async () => {
    setLoading(true)
    try {
      const params: Record<string, unknown> = {
        page,
        page_size: pageSize,
      }
      if (platform !== 'all') params.platform = platform
      if (search) params.search = search
      
      const data = await postsApi.list(params as Parameters<typeof postsApi.list>[0])
      setPosts(data)
      setHasMore(data.length === pageSize)
    } catch (error) {
      console.error('Error fetching posts:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPosts()
  }, [page, platform])

  const handleSearch = () => {
    setPage(1)
    fetchPosts()
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleSearch()
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">پست‌ها</h2>
          <p className="text-muted-foreground">مشاهده و مدیریت پست‌های جمع‌آوری شده</p>
        </div>
        <Button onClick={fetchPosts} variant="outline" size="sm">
          <RefreshCw className={cn("h-4 w-4 ml-2", loading && "animate-spin")} />
          بروزرسانی
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="جستجو در محتوای پست‌ها..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                onKeyPress={handleKeyPress}
                className="pr-10"
              />
            </div>
            <Select value={platform} onValueChange={(v) => { setPlatform(v); setPage(1); }}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="پلتفرم" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">همه پلتفرم‌ها</SelectItem>
                <SelectItem value="twitter">توییتر</SelectItem>
                <SelectItem value="instagram">اینستاگرام</SelectItem>
                <SelectItem value="telegram">تلگرام</SelectItem>
              </SelectContent>
            </Select>
            <Button onClick={handleSearch}>
              <Filter className="h-4 w-4 ml-2" />
              فیلتر
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Posts Table */}
      <Card>
        <CardHeader>
          <CardTitle>لیست پست‌ها</CardTitle>
          <CardDescription>
            {loading ? 'در حال بارگذاری...' : `${toPersianNumber(posts.length)} پست نمایش داده شده`}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-4">
              {Array.from({ length: 5 }).map((_, i) => (
                <Skeleton key={i} className="h-16 w-full" />
              ))}
            </div>
          ) : posts.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              پستی یافت نشد
            </div>
          ) : (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-16">پلتفرم</TableHead>
                    <TableHead>محتوا</TableHead>
                    <TableHead className="w-32 text-center">تعاملات</TableHead>
                    <TableHead className="w-24 text-center">وضعیت</TableHead>
                    <TableHead className="w-32">زمان</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {posts.map((post) => (
                    <TableRow key={post.id} className="cursor-pointer" onClick={() => {}}>
                      <TableCell>
                        <Badge variant="secondary" className={cn("text-white", platformColors[post.platform])}>
                          {platformLabels[post.platform]}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-1">
                          <p className="font-medium line-clamp-2">{truncate(post.content, 100)}</p>
                          {post.hashtags && post.hashtags.length > 0 && (
                            <div className="flex flex-wrap gap-1">
                              {post.hashtags.slice(0, 3).map((tag) => (
                                <Badge key={tag} variant="outline" className="text-xs">
                                  #{tag}
                                </Badge>
                              ))}
                              {post.hashtags.length > 3 && (
                                <Badge variant="outline" className="text-xs">
                                  +{toPersianNumber(post.hashtags.length - 3)}
                                </Badge>
                              )}
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center justify-center gap-3 text-muted-foreground">
                          <Tooltip>
                            <TooltipTrigger className="flex items-center gap-1">
                              <Heart className="h-3.5 w-3.5" />
                              <span className="text-xs">{toPersianNumber(formatNumber(post.likes_count))}</span>
                            </TooltipTrigger>
                            <TooltipContent>پسند</TooltipContent>
                          </Tooltip>
                          <Tooltip>
                            <TooltipTrigger className="flex items-center gap-1">
                              <MessageSquare className="h-3.5 w-3.5" />
                              <span className="text-xs">{toPersianNumber(formatNumber(post.comments_count))}</span>
                            </TooltipTrigger>
                            <TooltipContent>نظر</TooltipContent>
                          </Tooltip>
                          <Tooltip>
                            <TooltipTrigger className="flex items-center gap-1">
                              <Share2 className="h-3.5 w-3.5" />
                              <span className="text-xs">{toPersianNumber(formatNumber(post.shares_count))}</span>
                            </TooltipTrigger>
                            <TooltipContent>اشتراک</TooltipContent>
                          </Tooltip>
                        </div>
                      </TableCell>
                      <TableCell className="text-center">
                        <Badge variant={post.is_processed ? "default" : "secondary"}>
                          {post.is_processed ? 'پردازش‌شده' : 'در انتظار'}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-muted-foreground text-sm">
                        {post.posted_at ? formatRelativeTime(post.posted_at) : '-'}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              {/* Pagination */}
              <div className="flex items-center justify-between mt-4 pt-4 border-t">
                <div className="text-sm text-muted-foreground">
                  صفحه {toPersianNumber(page)}
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setPage(p => Math.max(1, p - 1))}
                    disabled={page === 1}
                  >
                    <ChevronRight className="h-4 w-4" />
                    قبلی
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setPage(p => p + 1)}
                    disabled={!hasMore}
                  >
                    بعدی
                    <ChevronLeft className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
