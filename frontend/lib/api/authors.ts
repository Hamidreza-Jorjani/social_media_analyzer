import apiClient from './client'
import type { Author, Platform } from '@/types'

export interface AuthorsParams {
  page?: number
  page_size?: number
  platform?: Platform
  search?: string
}

export const authorsApi = {
  list: async (params?: AuthorsParams): Promise<Author[]> => {
    const response = await apiClient.get<Author[]>('/authors', { params })
    return response.data
  },

  get: async (id: number): Promise<Author> => {
    const response = await apiClient.get<Author>(`/authors/${id}`)
    return response.data
  },

  topByFollowers: async (platform?: Platform, limit?: number): Promise<Author[]> => {
    const response = await apiClient.get<Author[]>('/authors/top/followers', {
      params: { platform, limit },
    })
    return response.data
  },

  topByPagerank: async (platform?: Platform, limit?: number): Promise<Author[]> => {
    const response = await apiClient.get<Author[]>('/authors/top/pagerank', {
      params: { platform, limit },
    })
    return response.data
  },

  topByInfluence: async (platform?: Platform, limit?: number): Promise<Author[]> => {
    const response = await apiClient.get<Author[]>('/authors/top/influence', {
      params: { platform, limit },
    })
    return response.data
  },

  stats: async (): Promise<{ total: number; by_platform: Record<string, number> }> => {
    const response = await apiClient.get('/authors/stats')
    return response.data
  },
}
