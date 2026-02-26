import apiClient from './client'
import type { Post, PostStats, Platform, Language } from '@/types'

export interface PostsParams {
  page?: number
  page_size?: number
  platform?: Platform
  language?: Language
  data_source_id?: number
  author_id?: number
  is_processed?: boolean
  date_from?: string
  date_to?: string
  search?: string
}

export const postsApi = {
  list: async (params?: PostsParams): Promise<Post[]> => {
    const response = await apiClient.get<Post[]>('/posts', { params })
    return response.data
  },

  get: async (id: number): Promise<Post> => {
    const response = await apiClient.get<Post>(`/posts/${id}`)
    return response.data
  },

  stats: async (): Promise<PostStats> => {
    const response = await apiClient.get<PostStats>('/posts/stats')
    return response.data
  },

  search: async (query: string, platform?: Platform): Promise<Post[]> => {
    const response = await apiClient.get<Post[]>('/posts/search', {
      params: { q: query, platform },
    })
    return response.data
  },

  byHashtag: async (hashtag: string): Promise<Post[]> => {
    const response = await apiClient.get<Post[]>(`/posts/by-hashtag/${hashtag}`)
    return response.data
  },

  create: async (data: Partial<Post>): Promise<Post> => {
    const response = await apiClient.post<Post>('/posts', data)
    return response.data
  },

  bulkCreate: async (posts: Partial<Post>[]): Promise<{ total: number; created: number; existing: number }> => {
    const response = await apiClient.post('/posts/bulk', { posts })
    return response.data
  },

  update: async (id: number, data: Partial<Post>): Promise<Post> => {
    const response = await apiClient.put<Post>(`/posts/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/posts/${id}`)
  },
}
