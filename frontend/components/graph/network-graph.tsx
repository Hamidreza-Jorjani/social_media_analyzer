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
