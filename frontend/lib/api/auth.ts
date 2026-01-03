import apiClient from './client'
import type { AuthResponse, LoginRequest, User } from '@/types'

export const authApi = {
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/login', data)
    return response.data
  },
  me: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me')
    return response.data
  },
  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout')
  },
}
