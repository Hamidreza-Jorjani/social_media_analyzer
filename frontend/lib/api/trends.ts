import apiClient from './client'
import type { Trend, TrendingItem, SentimentTrend, VolumeTrend } from '@/types'

export const trendsApi = {
  list: async (activeOnly?: boolean): Promise<Trend[]> => {
    const response = await apiClient.get<Trend[]>('/trends', {
      params: { active_only: activeOnly },
    })
    return response.data
  },

  get: async (id: number): Promise<Trend> => {
    const response = await apiClient.get<Trend>(`/trends/${id}`)
    return response.data
  },

  hashtags: async (hours?: number, limit?: number): Promise<TrendingItem[]> => {
    const response = await apiClient.get<TrendingItem[]>('/trends/hashtags', {
      params: { hours, limit },
    })
    return response.data
  },

  keywords: async (hours?: number, limit?: number): Promise<TrendingItem[]> => {
    const response = await apiClient.get<TrendingItem[]>('/trends/keywords', {
      params: { hours, limit },
    })
    return response.data
  },

  sentiment: async (hours?: number, interval?: string): Promise<SentimentTrend[]> => {
    const response = await apiClient.get<SentimentTrend[]>('/trends/sentiment', {
      params: { hours, interval },
    })
    return response.data
  },

  volume: async (hours?: number, interval?: string, platform?: string): Promise<VolumeTrend[]> => {
    const response = await apiClient.get<VolumeTrend[]>('/trends/volume', {
      params: { hours, interval, platform },
    })
    return response.data
  },

  summary: async (hours?: number) => {
    const response = await apiClient.get('/trends/summary', { params: { hours } })
    return response.data
  },

  detect: async (hours?: number, minCount?: number): Promise<{ message: string; success: boolean }> => {
    const response = await apiClient.post('/trends/detect', null, {
      params: { hours, min_count: minCount },
    })
    return response.data
  },
}
