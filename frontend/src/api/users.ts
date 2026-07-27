import { apiClient } from '@/api/client';
import { defaultUsers } from '@/api/mock-data';
import type { UserProfile } from '@/types/models';

export async function listUsers(): Promise<UserProfile[]> {
  try {
    const response = await apiClient.get<UserProfile[]>('/users');
    return response.data;
  } catch {
    return defaultUsers;
  }
}
