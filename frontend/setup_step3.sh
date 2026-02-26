#!/bin/bash
set -e

echo "🔧 Step 3: Enhancing existing files + Adding missing APIs..."
cd "$(dirname "$0")"

# ============================================================
# 1. Enhance Auth Store (add token getters for API client)
# ============================================================
echo "📝 Enhancing lib/stores/auth-store.ts..."
cat > lib/stores/auth-store.ts << 'STOREEOF'
import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '@/types'

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  
  // Actions
  setAuth: (user: User, accessToken: string, refreshToken: string) => void
  setTokens: (accessToken: string, refreshToken: string) => void
  setUser: (user: User) => void
  setLoading: (loading: boolean) => void
  logout: () => void
  reset: () => void
}

const initialState = {
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: true,
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      ...initialState,

      setAuth: (user, accessToken, refreshToken) => {
        set({
          user,
          accessToken,
          refreshToken,
          isAuthenticated: true,
          isLoading: false,
        })
      },

      setTokens: (accessToken, refreshToken) => {
        set({ accessToken, refreshToken })
      },

      setUser: (user) => {
        set({ user })
      },

      setLoading: (isLoading) => {
        set({ isLoading })
      },

      logout: () => {
        set({
          ...initialState,
          isLoading: false,
        })
      },

      reset: () => {
        set(initialState)
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

// Selector hooks for common patterns
export const useUser = () => useAuthStore((state) => state.user)
export const useIsAuthenticated = () => useAuthStore((state) => state.isAuthenticated)
export const useIsLoading = () => useAuthStore((state) => state.isLoading)
STOREEOF

# ============================================================
# 2. Enhance API Client (use Zustand store)
# ============================================================
echo "📝 Enhancing lib/api/client.ts..."
cat > lib/api/client.ts << 'CLIENTEOF'
import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/lib/stores/auth-store'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:18000/api/v1'

// Create axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = useAuthStore.getState().accessToken
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - handle errors & token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

    // Handle 401 - try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = useAuthStore.getState().refreshToken
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          })

          const { access_token, refresh_token } = response.data
          useAuthStore.getState().setTokens(access_token, refresh_token)

          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access_token}`
          }
          return apiClient(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed - logout
        useAuthStore.getState().logout()
        if (typeof window !== 'undefined') {
          window.location.href = '/login'
        }
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Helper to extract error message
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.detail || error.message || 'An error occurred'
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'An unknown error occurred'
}

export default apiClient
CLIENTEOF

# ============================================================
# 3. Enhance Auth API
# ============================================================
echo "📝 Enhancing lib/api/auth.ts..."
cat > lib/api/auth.ts << 'AUTHEOF'
import apiClient from './client'
import type { AuthResponse, LoginRequest, User } from '@/types'

export interface RegisterRequest {
  email: string
  username: string
  password: string
  full_name?: string
}

export const authApi = {
  /**
   * Login with username/email and password
   */
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/login', data)
    return response.data
  },

  /**
   * Register a new user
   */
  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/register', data)
    return response.data
  },

  /**
   * Refresh access token
   */
  refresh: async (refreshToken: string): Promise<{ access_token: string; refresh_token: string }> => {
    const response = await apiClient.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  },

  /**
   * Get current user
   */
  me: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me')
    return response.data
  },

  /**
   * Logout
   */
  logout: async (): Promise<void> => {
    try {
      await apiClient.post('/auth/logout')
    } catch {
      // Ignore logout errors
    }
  },

  /**
   * Change password
   */
  changePassword: async (currentPassword: string, newPassword: string): Promise<void> => {
    await apiClient.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  },
}
AUTHEOF

# ============================================================
# 4. Add Posts API
# ============================================================
echo "📝 Creating lib/api/posts.ts..."
cat > lib/api/posts.ts << 'POSTSEOF'
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
POSTSEOF

# ============================================================
# 5. Add Analysis API
# ============================================================
echo "📝 Creating lib/api/analysis.ts..."
cat > lib/api/analysis.ts << 'ANALYSISEOF'
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
ANALYSISEOF

# ============================================================
# 6. Add Trends API
# ============================================================
echo "📝 Creating lib/api/trends.ts..."
cat > lib/api/trends.ts << 'TRENDSEOF'
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
TRENDSEOF

# ============================================================
# 7. Add Graph API
# ============================================================
echo "📝 Creating lib/api/graph.ts..."
cat > lib/api/graph.ts << 'GRAPHEOF'
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
GRAPHEOF

# ============================================================
# 8. Enhance Dashboard API
# ============================================================
echo "📝 Enhancing lib/api/dashboard.ts..."
cat > lib/api/dashboard.ts << 'DASHEOF'
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
DASHEOF

# ============================================================
# 9. Update API Index
# ============================================================
echo "📝 Updating lib/api/index.ts..."
cat > lib/api/index.ts << 'INDEXEOF'
export { apiClient, getErrorMessage } from './client'
export { authApi } from './auth'
export { postsApi } from './posts'
export { analysisApi } from './analysis'
export { dashboardApi } from './dashboard'
export { trendsApi } from './trends'
export { graphApi } from './graph'
INDEXEOF

# ============================================================
# 10. Enhance Types
# ============================================================
echo "📝 Enhancing types/index.ts..."
cat > types/index.ts << 'TYPESEOF'
// ============================================================
// Auth Types
// ============================================================

export type UserRole = 'admin' | 'analyst' | 'viewer'

export interface User {
  id: number
  email: string
  username: string
  full_name: string | null
  is_active: boolean
  role: UserRole
  created_at: string
  updated_at: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface LoginRequest {
  username: string
  password: string
}

export interface AuthResponse {
  user: User
  tokens: AuthTokens
}

// ============================================================
// Post Types
// ============================================================

export type Platform = 'twitter' | 'instagram' | 'telegram' | 'linkedin' | 'youtube' | 'news' | 'forum' | 'custom'
export type Language = 'fa' | 'en' | 'ar'

export interface Author {
  id: number
  platform_id: string
  platform: Platform
  username: string
  display_name: string | null
  bio: string | null
  profile_url: string | null
  avatar_url: string | null
  followers_count: number
  following_count: number
  posts_count: number
  influence_score: number | null
  pagerank_score: number | null
  created_at: string
  updated_at: string
}

export interface DataSource {
  id: number
  name: string
  platform: Platform
  description: string | null
  is_active: boolean
  last_sync_at: string | null
  created_at: string
  updated_at: string
}

export interface Post {
  id: number
  platform_id: string
  platform: Platform
  content: string
  content_normalized: string | null
  language: Language
  url: string | null
  media_urls: string[] | null
  likes_count: number
  comments_count: number
  shares_count: number
  views_count: number
  posted_at: string | null
  hashtags: string[] | null
  mentions: string[] | null
  is_processed: boolean
  data_source_id: number | null
  author_id: number | null
  author?: Author
  data_source?: DataSource
  created_at: string
  updated_at: string
}

export interface PostStats {
  total: number
  processed: number
  unprocessed: number
  by_platform: Record<Platform, number>
  by_language: Record<Language, number>
}

// ============================================================
// Analysis Types
// ============================================================

export type AnalysisType = 'sentiment' | 'emotion' | 'summarization' | 'topic_modeling' | 'keyword_extraction' | 'entity_recognition' | 'trend_detection' | 'graph_analysis' | 'full'
export type AnalysisStatus = 'pending' | 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled'

export interface Analysis {
  id: number
  name: string
  description: string | null
  analysis_type: AnalysisType
  config: Record<string, unknown> | null
  query_filters: Record<string, unknown> | null
  post_count: number
  status: AnalysisStatus
  progress: number
  summary: AnalysisSummary | null
  error_message: string | null
  started_at: string | null
  completed_at: string | null
  user_id: number
  created_at: string
  updated_at: string
}

export interface AnalysisResult {
  id: number
  post_id: number
  analysis_id: number
  sentiment_label: 'positive' | 'negative' | 'neutral' | null
  sentiment_score: number | null
  sentiment_confidence: number | null
  emotions: Record<string, number> | null
  dominant_emotion: string | null
  summary: string | null
  keywords: string[] | null
  topics: Array<{ topic: string; score: number }> | null
  entities: Array<{ text: string; type: string }> | null
  created_at: string
  updated_at: string
}

export interface AnalysisSummary {
  total_posts: number
  processed_posts: number
  sentiment_distribution: { positive: number; negative: number; neutral: number }
  emotion_distribution: Record<string, number>
  average_sentiment_score: number
  top_keywords: Array<{ keyword: string; count: number }>
  generated_at: string
}

// ============================================================
// Trend Types
// ============================================================

export type TrendStatus = 'active' | 'declining' | 'ended'

export interface Trend {
  id: number
  name: string
  description: string | null
  volume: number
  growth_rate: number
  velocity: number
  peak_time: string | null
  keywords: string[] | null
  hashtags: string[] | null
  sentiment_distribution: Record<string, number> | null
  is_active: TrendStatus
  created_at: string
  updated_at: string
}

export interface TrendingItem {
  item: string
  count: number
}

export interface SentimentTrend {
  time: string
  positive: number
  negative: number
  neutral: number
}

export interface VolumeTrend {
  time: string
  count: number
}

// ============================================================
// Graph Types
// ============================================================

export type NodeType = 'author' | 'hashtag' | 'topic' | 'keyword' | 'post'
export type EdgeType = 'mentions' | 'replies_to' | 'retweets' | 'follows' | 'co_occurrence'

export interface GraphNode {
  id: number
  node_id: string
  node_type: NodeType
  label: string
  degree: number
  in_degree: number
  out_degree: number
  pagerank: number | null
  betweenness_centrality: number | null
  community_id: number | null
  created_at: string
  updated_at: string
}

export interface GraphData {
  nodes: Array<{ id: string; label: string; type: NodeType; pagerank?: number; degree?: number; community?: number }>
  edges: Array<{ source: string; target: string; type: EdgeType; weight?: number }>
}

export interface GraphStats {
  total_nodes: number
  total_edges: number
  node_types: Record<NodeType, number>
  edge_types: Record<EdgeType, number>
  communities_count: number
  average_degree: number
  density: number
}

// ============================================================
// Dashboard Types
// ============================================================

export interface DashboardOverview {
  posts: { total: number; processed: number; by_platform: Record<Platform, number>; by_language: Record<Language, number> }
  trends: { active: number; total: number }
  graph: { nodes: number; communities: number }
  analyses: { total: number; by_status: Record<AnalysisStatus, number> }
}

export interface SentimentOverview {
  distribution: { positive: number; negative: number; neutral: number }
  percentages: { positive: number; negative: number; neutral: number }
  average_score: number
  total_analyzed: number
}

export interface EmotionOverview {
  distribution: Record<string, number>
  percentages: Record<string, number>
  total_analyzed: number
}

export interface PlatformStats {
  platform: Platform
  post_count: number
  percentage: number
}

export type WidgetType = 'sentiment_chart' | 'emotion_chart' | 'trending_hashtags' | 'trending_keywords' | 'volume_chart' | 'platform_stats' | 'overview' | 'top_authors' | 'recent_analyses'
TYPESEOF

echo ""
echo "✅ Step 3 complete!"
echo ""
echo "Enhanced/Created files:"
echo "  - lib/stores/auth-store.ts (enhanced)"
echo "  - lib/api/client.ts (enhanced)"
echo "  - lib/api/auth.ts (enhanced)"
echo "  - lib/api/posts.ts (new)"
echo "  - lib/api/analysis.ts (new)"
echo "  - lib/api/trends.ts (new)"
echo "  - lib/api/graph.ts (new)"
echo "  - lib/api/dashboard.ts (enhanced)"
echo "  - lib/api/index.ts (updated)"
echo "  - types/index.ts (enhanced)"
echo ""
