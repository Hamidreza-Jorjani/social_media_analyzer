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
