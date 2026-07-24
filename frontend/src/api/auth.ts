import { apiClient, getPersistedAuthState } from '@/api/client';
import { defaultUsers } from '@/api/mock-data';
import type { AuthLoginPayload, AuthTokenBundle, UserProfile } from '@/types/models';

const createDemoSession = (email: string): AuthTokenBundle => {
  const matchedUser =
    defaultUsers.find((user) => user.email.toLowerCase() === email.toLowerCase()) ?? defaultUsers[1];
  const user: UserProfile = matchedUser.email === email ? matchedUser : { ...matchedUser, email };

  return {
    accessToken: `demo-access-${Date.now()}`,
    refreshToken: `demo-refresh-${Date.now()}`,
    expiresAt: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
    user
  };
};

export async function loginUser(payload: AuthLoginPayload): Promise<AuthTokenBundle> {
  try {
    const response = await apiClient.post<AuthTokenBundle>('/auth/login', payload);
    return response.data;
  } catch (error) {
    if (!payload.email.includes('@') || payload.password.length < 8) {
      throw error;
    }

    return createDemoSession(payload.email);
  }
}

export async function refreshAuthToken(refreshToken: string): Promise<AuthTokenBundle> {
  try {
    const response = await apiClient.post<AuthTokenBundle>('/auth/refresh', { refreshToken });
    return response.data;
  } catch {
    return {
      accessToken: `demo-access-${Date.now()}`,
      refreshToken: `demo-refresh-${Date.now()}`,
      expiresAt: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
      user: getPersistedAuthState().user ?? defaultUsers[0]
    };
  }
}

export async function getCurrentUser(): Promise<UserProfile> {
  try {
    const response = await apiClient.get<UserProfile>('/auth/me');
    return response.data;
  } catch {
    return getPersistedAuthState().user ?? defaultUsers[0];
  }
}
