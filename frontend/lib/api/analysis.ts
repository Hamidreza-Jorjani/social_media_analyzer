import apiClient from './client'
import type { Analysis, AnalysisResult, AnalysisSummary, AnalysisType, AnalysisStatus } from '@/types'

export interface CreateAnalysisRequest {
  name: string
  description?: string
  analysis_type: AnalysisType
  config?: Record<string, unknown>
  query_filters?: Record<string, unknown>
  post_count?: number
}

export const analysisApi = {
  list: async (statusFilter?: AnalysisStatus, typeFilter?: AnalysisType): Promise<Analysis[]> => {
    const response = await apiClient.get<Analysis[]>('/analysis', {
      params: { status_filter: statusFilter, type_filter: typeFilter },
    })
    return response.data
  },

  get: async (id: number): Promise<Analysis> => {
    const response = await apiClient.get<Analysis>(`/analysis/${id}`)
    return response.data
  },

  stats: async (): Promise<{ total: number; by_status: Record<string, number>; by_type: Record<string, number> }> => {
    const response = await apiClient.get('/analysis/stats')
    return response.data
  },

  create: async (data: CreateAnalysisRequest): Promise<Analysis> => {
    const response = await apiClient.post<Analysis>('/analysis', data)
    return response.data
  },

  start: async (id: number, config?: Record<string, unknown>): Promise<{ message: string; success: boolean }> => {
    const response = await apiClient.post(`/analysis/${id}/start`, config || {})
    return response.data
  },

  cancel: async (id: number): Promise<{ message: string; success: boolean }> => {
    const response = await apiClient.post(`/analysis/${id}/cancel`)
    return response.data
  },

  progress: async (id: number): Promise<{ analysis_id: number; status: AnalysisStatus; progress: number }> => {
    const response = await apiClient.get(`/analysis/${id}/progress`)
    return response.data
  },

  results: async (id: number, page?: number, pageSize?: number): Promise<AnalysisResult[]> => {
    const response = await apiClient.get<AnalysisResult[]>(`/analysis/${id}/results`, {
      params: { page, page_size: pageSize },
    })
    return response.data
  },

  summary: async (id: number): Promise<AnalysisSummary> => {
    const response = await apiClient.get<AnalysisSummary>(`/analysis/${id}/summary`)
    return response.data
  },

  update: async (id: number, data: Partial<CreateAnalysisRequest>): Promise<Analysis> => {
    const response = await apiClient.put<Analysis>(`/analysis/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/analysis/${id}`)
  },
}
