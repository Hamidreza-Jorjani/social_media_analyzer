export interface User {
  id: number
  email: string
  username: string
  full_name: string
  is_active: boolean
  role: 'admin' | 'analyst' | 'viewer'
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

export interface Post {
  id: number
  platform_id: string
  platform: string
  content: string
  language: string
  likes_count: number
  comments_count: number
  shares_count: number
  views_count: number
  posted_at: string
  hashtags: string[]
  is_processed: boolean
  created_at: string
}

export interface Analysis {
  id: number
  name: string
  analysis_type: string
  status: string
  progress: number
  post_count: number
  created_at: string
}

export interface DashboardOverview {
  posts: { total: number; processed: number; by_platform: Record<string, number> }
  trends: { active: number; total: number }
  graph: { nodes: number; communities: number }
  analyses: { total: number; by_status: Record<string, number> }
}
