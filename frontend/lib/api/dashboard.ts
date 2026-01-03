import apiClient from './client'
import type { DashboardOverview } from '@/types'

export const dashboardApi = {
  getOverview: async (): Promise<DashboardOverview> => {
    const response = await apiClient.get<DashboardOverview>('/dashboard/overview')
    return response.data
  },
}
