'use client'

import { useEffect, useState } from 'react'
import { Users, Search, RefreshCw, Trophy, TrendingUp, UserCheck, ExternalLink } from 'lucide-react'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { authorsApi } from '@/lib/api'
import { cn, toPersianNumber, formatNumber } from '@/lib/utils'
import type { Author, Platform } from '@/types'

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

function AuthorCard({ author, rank }: { author: Author; rank?: number }) {
  const initials = author.display_name
    ? author.display_name.split(' ').map((n) => n[0]).join('').slice(0, 2)
    : author.username.slice(0, 2).toUpperCase()

  return (
    <div className="flex items-center gap-4 p-4 rounded-lg bg-muted/50 hover:bg-muted transition-colors">
      {rank && (
        <span
          className={cn(
            'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0',
            rank === 1 && 'bg-yellow-500 text-white',
            rank === 2 && 'bg-gray-400 text-white',
            rank === 3 && 'bg-amber-600 text-white',
            rank > 3 && 'bg-muted text-muted-foreground'
          )}
        >
          {toPersianNumber(rank)}
        </span>
      )}
      <Avatar className="h-12 w-12">
        <AvatarFallback className={cn('text-white', platformColors[author.platform])}>
          {initials}
        </AvatarFallback>
      </Avatar>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <p className="font-medium truncate">{author.display_name || author.username}</p>
          <Badge variant="secondary" className={cn('text-white text-xs', platformColors[author.platform])}>
            {platformLabels[author.platform]}
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground">@{author.username}</p>
      </div>
      <div className="text-left flex-shrink-0">
        <p className="font-bold text-lg">{toPersianNumber(formatNumber(author.followers_count))}</p>
        <p className="text-xs text-muted-foreground">دنبال‌کننده</p>
      </div>
    </div>
  )
}

export default function AuthorsPage() {
  const [authors, setAuthors] = useState<Author[]>([])
  const [topByFollowers, setTopByFollowers] = useState<Author[]>([])
  const [topByPagerank, setTopByPagerank] = useState<Author[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [platform, setPlatform] = useState<string>('all')

  const fetchData = async () => {
    setLoading(true)
    try {
      const [authorsData, followersData, pagerankData] = await Promise.all([
        authorsApi.list({
          page_size: 50,
          platform: platform !== 'all' ? (platform as Platform) : undefined,
          search: search || undefined,
        }),
        authorsApi.topByFollowers(undefined, 10),
        authorsApi.topByPagerank(undefined, 10),
      ])
      setAuthors(authorsData)
      setTopByFollowers(followersData)
      setTopByPagerank(pagerankData)
    } catch (error) {
      console.error('Error fetching authors:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [platform])

  const handleSearch = () => {
    fetchData()
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">نویسندگان</h2>
          <p className="text-muted-foreground">مشاهده و تحلیل نویسندگان</p>
        </div>
        <Button onClick={fetchData} variant="outline" size="sm">
          <RefreshCw className={cn('h-4 w-4 ml-2', loading && 'animate-spin')} />
          بروزرسانی
        </Button>
      </div>

      {/* Top Authors */}
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Trophy className="h-5 w-5 text-yellow-500" />
              برترین بر اساس دنبال‌کننده
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {loading ? (
              Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-16 w-full" />)
            ) : topByFollowers.length === 0 ? (
              <p className="text-center text-muted-foreground py-4">نویسنده‌ای یافت نشد</p>
            ) : (
              topByFollowers.slice(0, 5).map((author, index) => (
                <AuthorCard key={author.id} author={author} rank={index + 1} />
              ))
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-blue-500" />
              برترین بر اساس PageRank
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {loading ? (
              Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-16 w-full" />)
            ) : topByPagerank.length === 0 ? (
              <p className="text-center text-muted-foreground py-4">نویسنده‌ای یافت نشد</p>
            ) : (
              topByPagerank.slice(0, 5).map((author, index) => (
                <AuthorCard key={author.id} author={author} rank={index + 1} />
              ))
            )}
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="جستجوی نویسنده..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="pr-10"
              />
            </div>
            <Select value={platform} onValueChange={setPlatform}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="پلتفرم" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">همه</SelectItem>
                <SelectItem value="twitter">توییتر</SelectItem>
                <SelectItem value="instagram">اینستاگرام</SelectItem>
                <SelectItem value="telegram">تلگرام</SelectItem>
              </SelectContent>
            </Select>
            <Button onClick={handleSearch}>جستجو</Button>
          </div>
        </CardContent>
      </Card>

      {/* Authors Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            لیست نویسندگان
          </CardTitle>
          <CardDescription>
            {loading ? 'در حال بارگذاری...' : `${toPersianNumber(authors.length)} نویسنده`}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-4">
              {Array.from({ length: 5 }).map((_, i) => (
                <Skeleton key={i} className="h-16 w-full" />
              ))}
            </div>
          ) : authors.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">نویسنده‌ای یافت نشد</div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>نویسنده</TableHead>
                  <TableHead>پلتفرم</TableHead>
                  <TableHead className="text-center">دنبال‌کننده</TableHead>
                  <TableHead className="text-center">دنبال‌شونده</TableHead>
                  <TableHead className="text-center">پست‌ها</TableHead>
                  <TableHead className="text-center">امتیاز نفوذ</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {authors.map((author) => (
                  <TableRow key={author.id}>
                    <TableCell>
                      <div className="flex items-center gap-3">
                        <Avatar className="h-8 w-8">
                          <AvatarFallback className={cn('text-white text-xs', platformColors[author.platform])}>
                            {author.username.slice(0, 2).toUpperCase()}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="font-medium">{author.display_name || author.username}</p>
                          <p className="text-xs text-muted-foreground">@{author.username}</p>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="secondary" className={cn('text-white', platformColors[author.platform])}>
                        {platformLabels[author.platform]}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-center">{toPersianNumber(formatNumber(author.followers_count))}</TableCell>
                    <TableCell className="text-center">{toPersianNumber(formatNumber(author.following_count))}</TableCell>
                    <TableCell className="text-center">{toPersianNumber(formatNumber(author.posts_count))}</TableCell>
                    <TableCell className="text-center">
                      {author.influence_score ? toPersianNumber((author.influence_score * 100).toFixed(0)) + '%' : '-'}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
