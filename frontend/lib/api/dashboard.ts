import apiClient from './client'
import type { DashboardOverview, SentimentOverview, EmotionOverview, PlatformStats, WidgetType } from '@/types'

export const dashboardApi = {
  overview: async (): Promise<DashboardOverview> => {
    const response = await apiClient.get<DashboardOverview>('/dashboard/overview')
    return response.data
  },

  sentiment: async (): Promise<SentimentOverview> => {
    const response = await apiClient.get<SentimentOverview>('/dashboard/sentiment')
    return response.data
  },

  emotions: async (): Promise<EmotionOverview> => {
    const response = await apiClient.get<EmotionOverview>('/dashboard/emotions')
    return response.data
  },

  platforms: async (): Promise<PlatformStats[]> => {
    const response = await apiClient.get<PlatformStats[]>('/dashboard/platforms')
    return response.data
  },

  widget: async (type: WidgetType, params?: { hours?: number; limit?: number; interval?: string }) => {
    const response = await apiClient.get(`/dashboard/widget/${type}`, { params })
    return response.data
  },
}
