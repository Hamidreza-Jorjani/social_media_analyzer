import apiClient from './client'
import type { GraphData, GraphStats, GraphNode, NodeType } from '@/types'

export const graphApi = {
  data: async (nodeType?: NodeType, limit?: number): Promise<GraphData> => {
    const response = await apiClient.get<GraphData>('/graph/data', {
      params: { node_type: nodeType, limit },
    })
    return response.data
  },

  stats: async (): Promise<GraphStats> => {
    const response = await apiClient.get<GraphStats>('/graph/stats')
    return response.data
  },

  topByPagerank: async (nodeType?: NodeType, limit?: number): Promise<GraphNode[]> => {
    const response = await apiClient.get<GraphNode[]>('/graph/nodes/top/pagerank', {
      params: { node_type: nodeType, limit },
    })
    return response.data
  },

  topByDegree: async (nodeType?: NodeType, limit?: number): Promise<GraphNode[]> => {
    const response = await apiClient.get<GraphNode[]>('/graph/nodes/top/degree', {
      params: { node_type: nodeType, limit },
    })
    return response.data
  },

  community: async (communityId: number): Promise<GraphNode[]> => {
    const response = await apiClient.get<GraphNode[]>(`/graph/nodes/community/${communityId}`)
    return response.data
  },

  buildAuthorNetwork: async (): Promise<{ message: string; success: boolean }> => {
    const response = await apiClient.post('/graph/build/author-network')
    return response.data
  },

  buildHashtagNetwork: async (): Promise<{ message: string; success: boolean }> => {
    const response = await apiClient.post('/graph/build/hashtag-network')
    return response.data
  },

  calculatePagerank: async (): Promise<{ message: string; success: boolean }> => {
    const response = await apiClient.post('/graph/calculate/pagerank')
    return response.data
  },

  detectCommunities: async () => {
    const response = await apiClient.post('/graph/detect/communities')
    return response.data
  },
}
