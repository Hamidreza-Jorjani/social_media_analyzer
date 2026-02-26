#!/bin/bash
set -e

echo "🕸️ Step 9: Creating Graph Page with Network Visualization..."
cd "$(dirname "$0")"

# ============================================================
# 1. Graph Network Component
# ============================================================
echo "📝 Creating components/graph/network-graph.tsx..."
mkdir -p "components/graph"
cat > "components/graph/network-graph.tsx" << 'GRAPHCOMPEOF'
'use client'

import { useEffect, useRef, useState } from 'react'
import { Network, Options } from 'vis-network'
import { DataSet } from 'vis-data'
import { Loader2 } from 'lucide-react'
import type { GraphData } from '@/types'

interface NetworkGraphProps {
  data: GraphData
  onNodeClick?: (nodeId: string) => void
  className?: string
}

const nodeColors: Record<string, string> = {
  author: '#3b82f6',
  hashtag: '#8b5cf6',
  topic: '#f59e0b',
  keyword: '#10b981',
  post: '#6b7280',
}

export function NetworkGraph({ data, onNodeClick, className }: NetworkGraphProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const networkRef = useRef<Network | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!containerRef.current || !data.nodes.length) {
      setLoading(false)
      return
    }

    const nodes = new DataSet(
      data.nodes.map((node) => ({
        id: node.id,
        label: node.label,
        title: `${node.label}\nنوع: ${node.type}${node.pagerank ? `\nPageRank: ${node.pagerank.toFixed(4)}` : ''}`,
        color: {
          background: nodeColors[node.type] || '#6b7280',
          border: nodeColors[node.type] || '#6b7280',
          highlight: {
            background: nodeColors[node.type] || '#6b7280',
            border: '#fff',
          },
        },
        size: node.pagerank ? Math.max(10, node.pagerank * 500) : node.degree ? Math.max(10, node.degree * 2) : 15,
        font: {
          color: '#fff',
          size: 12,
          face: 'Vazirmatn, sans-serif',
        },
        shape: node.type === 'author' ? 'dot' : node.type === 'hashtag' ? 'diamond' : 'dot',
      }))
    )

    const edges = new DataSet(
      data.edges.map((edge, index) => ({
        id: index,
        from: edge.source,
        to: edge.target,
        width: edge.weight ? Math.max(1, edge.weight) : 1,
        color: {
          color: 'rgba(156, 163, 175, 0.5)',
          highlight: '#3b82f6',
        },
        smooth: {
          type: 'continuous',
        },
      }))
    )

    const options: Options = {
      nodes: {
        borderWidth: 2,
        shadow: true,
      },
      edges: {
        arrows: {
          to: { enabled: false },
        },
        smooth: {
          enabled: true,
          type: 'continuous',
        },
      },
      physics: {
        enabled: true,
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          gravitationalConstant: -50,
          centralGravity: 0.01,
          springLength: 100,
          springConstant: 0.08,
          damping: 0.4,
        },
        stabilization: {
          enabled: true,
          iterations: 200,
          updateInterval: 25,
        },
      },
      interaction: {
        hover: true,
        tooltipDelay: 100,
        zoomView: true,
        dragView: true,
      },
    }

    const network = new Network(containerRef.current, { nodes, edges }, options)
    networkRef.current = network

    network.on('stabilizationIterationsDone', () => {
      setLoading(false)
      network.setOptions({ physics: { enabled: false } })
    })

    network.on('click', (params) => {
      if (params.nodes.length > 0 && onNodeClick) {
        onNodeClick(params.nodes[0] as string)
      }
    })

    return () => {
      network.destroy()
    }
  }, [data, onNodeClick])

  if (!data.nodes.length) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        داده‌ای برای نمایش وجود ندارد
      </div>
    )
  }

  return (
    <div className={`relative ${className}`}>
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-background/80 z-10">
          <div className="flex flex-col items-center gap-2">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <span className="text-sm text-muted-foreground">در حال رندر گراف...</span>
          </div>
        </div>
      )}
      <div ref={containerRef} className="w-full h-full" />
    </div>
  )
}
GRAPHCOMPEOF

# ============================================================
# 2. Graph Page
# ============================================================
echo "📝 Creating app/(dashboard)/dashboard/graph/page.tsx..."
cat > "app/(dashboard)/dashboard/graph/page.tsx" << 'GRAPHPAGEEOF'
'use client'

import { useEffect, useState } from 'react'
import { Network, RefreshCw, Play, Users, Hash, Loader2, Info } from 'lucide-react'
import { toast } from 'sonner'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { NetworkGraph } from '@/components/graph/network-graph'
import { graphApi } from '@/lib/api'
import { cn, toPersianNumber, formatNumber } from '@/lib/utils'
import type { GraphData, GraphStats, NodeType } from '@/types'

export default function GraphPage() {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], edges: [] })
  const [stats, setStats] = useState<GraphStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [building, setBuilding] = useState(false)
  const [nodeType, setNodeType] = useState<string>('all')
  const [selectedNode, setSelectedNode] = useState<string | null>(null)

  const fetchData = async () => {
    setLoading(true)
    try {
      const [graphDataRes, statsRes] = await Promise.all([
        graphApi.data(nodeType !== 'all' ? (nodeType as NodeType) : undefined, 500),
        graphApi.stats(),
      ])
      setGraphData(graphDataRes)
      setStats(statsRes)
    } catch (error) {
      console.error('Error fetching graph data:', error)
      toast.error('خطا در دریافت داده‌های گراف')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [nodeType])

  const handleBuildAuthorNetwork = async () => {
    setBuilding(true)
    try {
      await graphApi.buildAuthorNetwork()
      toast.success('ساخت شبکه نویسندگان در صف قرار گرفت')
      setTimeout(fetchData, 2000)
    } catch (error) {
      toast.error('خطا در ساخت شبکه')
    } finally {
      setBuilding(false)
    }
  }

  const handleBuildHashtagNetwork = async () => {
    setBuilding(true)
    try {
      await graphApi.buildHashtagNetwork()
      toast.success('ساخت شبکه هشتگ‌ها در صف قرار گرفت')
      setTimeout(fetchData, 2000)
    } catch (error) {
      toast.error('خطا در ساخت شبکه')
    } finally {
      setBuilding(false)
    }
  }

  const handleCalculatePagerank = async () => {
    setBuilding(true)
    try {
      await graphApi.calculatePagerank()
      toast.success('محاسبه PageRank در صف قرار گرفت')
      setTimeout(fetchData, 2000)
    } catch (error) {
      toast.error('خطا در محاسبه PageRank')
    } finally {
      setBuilding(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">گراف شبکه</h2>
          <p className="text-muted-foreground">نمایش ارتباطات و تحلیل شبکه</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={fetchData} variant="outline" size="sm">
            <RefreshCw className={cn('h-4 w-4 ml-2', loading && 'animate-spin')} />
            بروزرسانی
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">کل گره‌ها</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? <Skeleton className="h-8 w-16" /> : toPersianNumber(formatNumber(stats?.total_nodes || 0))}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">کل یال‌ها</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? <Skeleton className="h-8 w-16" /> : toPersianNumber(formatNumber(stats?.total_edges || 0))}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">جوامع</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? <Skeleton className="h-8 w-16" /> : toPersianNumber(stats?.communities_count || 0)}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">میانگین درجه</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? <Skeleton className="h-8 w-16" /> : toPersianNumber((stats?.average_degree || 0).toFixed(1))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Controls */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-wrap gap-4 items-center justify-between">
            <div className="flex gap-4 items-center">
              <Select value={nodeType} onValueChange={setNodeType}>
                <SelectTrigger className="w-40">
                  <SelectValue placeholder="نوع گره" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">همه</SelectItem>
                  <SelectItem value="author">نویسندگان</SelectItem>
                  <SelectItem value="hashtag">هشتگ‌ها</SelectItem>
                </SelectContent>
              </Select>
              
              <div className="flex gap-2">
                <Badge variant="outline" className="gap-1">
                  <div className="w-3 h-3 rounded-full bg-blue-500" />
                  نویسنده
                </Badge>
                <Badge variant="outline" className="gap-1">
                  <div className="w-3 h-3 rounded-full bg-purple-500" />
                  هشتگ
                </Badge>
              </div>
            </div>

            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={handleBuildAuthorNetwork} disabled={building}>
                {building ? <Loader2 className="h-4 w-4 ml-2 animate-spin" /> : <Users className="h-4 w-4 ml-2" />}
                شبکه نویسندگان
              </Button>
              <Button variant="outline" size="sm" onClick={handleBuildHashtagNetwork} disabled={building}>
                {building ? <Loader2 className="h-4 w-4 ml-2 animate-spin" /> : <Hash className="h-4 w-4 ml-2" />}
                شبکه هشتگ‌ها
              </Button>
              <Button variant="outline" size="sm" onClick={handleCalculatePagerank} disabled={building}>
                {building ? <Loader2 className="h-4 w-4 ml-2 animate-spin" /> : <Play className="h-4 w-4 ml-2" />}
                PageRank
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Graph Visualization */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Network className="h-5 w-5" />
            نمایش گراف
          </CardTitle>
          <CardDescription>
            {graphData.nodes.length > 0
              ? `${toPersianNumber(graphData.nodes.length)} گره و ${toPersianNumber(graphData.edges.length)} یال`
              : 'برای ساخت گراف از دکمه‌های بالا استفاده کنید'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <Skeleton className="h-[500px] w-full" />
          ) : graphData.nodes.length === 0 ? (
            <div className="h-[500px] flex flex-col items-center justify-center text-muted-foreground">
              <Network className="h-16 w-16 mb-4 opacity-20" />
              <p className="text-lg mb-2">گرافی برای نمایش وجود ندارد</p>
              <p className="text-sm">ابتدا شبکه نویسندگان یا هشتگ‌ها را بسازید</p>
            </div>
          ) : (
            <div className="h-[500px] border rounded-lg overflow-hidden">
              <NetworkGraph
                data={graphData}
                onNodeClick={(nodeId) => setSelectedNode(nodeId)}
                className="h-full"
              />
            </div>
          )}
        </CardContent>
      </Card>

      {/* Node Info */}
      {selectedNode && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Info className="h-5 w-5" />
              اطلاعات گره انتخاب‌شده
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-lg font-medium">{selectedNode}</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
GRAPHPAGEEOF

echo ""
echo "✅ Step 9 complete! Graph page with vis-network created."
