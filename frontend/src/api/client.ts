import axios, {
  AxiosError,
  AxiosHeaders,
  type InternalAxiosRequestConfig,
} from 'axios';
import type { AuthTokenBundle, PersistedAuthState } from '@/types/models';

export const AUTH_STORAGE_KEY = 'insurateforge-auth';

const baseURL = import.meta.env.VITE_API_BASE_URL ?? '/api';

interface RetriableRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

export const apiClient = axios.create({
  baseURL,
  timeout: 12_000,
  headers: {
    'Content-Type': 'application/json'
  }
});

const refreshClient = axios.create({
  baseURL,
  timeout: 12_000,
  headers: {
    'Content-Type': 'application/json'
  }
});

let refreshPromise: Promise<AuthTokenBundle> | null = null;

const emptyAuthState = (): PersistedAuthState => ({
  accessToken: null,
  refreshToken: null,
  expiresAt: null,
  user: null
});

export function getPersistedAuthState(): PersistedAuthState {
  if (typeof window === 'undefined') {
    return emptyAuthState();
  }

  const serialized = window.localStorage.getItem(AUTH_STORAGE_KEY);

  if (!serialized) {
    return emptyAuthState();
  }

  try {
    return JSON.parse(serialized) as PersistedAuthState;
  } catch {
    window.localStorage.removeItem(AUTH_STORAGE_KEY);
    return emptyAuthState();
  }
}

export function persistAuthState(payload: PersistedAuthState): void {
  if (typeof window === 'undefined') {
    return;
  }

  window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(payload));
}

export function clearPersistedAuthState(): void {
  if (typeof window === 'undefined') {
    return;
  }

  window.localStorage.removeItem(AUTH_STORAGE_KEY);
}

function applyAuthHeader(config: InternalAxiosRequestConfig, accessToken: string | null) {
  if (!accessToken) {
    return config;
  }

  const headers = AxiosHeaders.from(config.headers);
  headers.set('Authorization', 'Bearer ' + accessToken);
  config.headers = headers;
  return config;
}

async function refreshTokens(refreshToken: string): Promise<AuthTokenBundle> {
  const response = await refreshClient.post<AuthTokenBundle>('/auth/refresh', { refreshToken });
  return response.data;
}

apiClient.interceptors.request.use((config) => {
  const { accessToken } = getPersistedAuthState();
  return applyAuthHeader(config, accessToken);
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as RetriableRequestConfig | undefined;
    const status = error.response?.status;
    const requestUrl = originalRequest?.url ?? '';

    if (
      !originalRequest ||
      status !== 401 ||
      originalRequest._retry ||
      requestUrl.includes('/auth/login') ||
      requestUrl.includes('/auth/refresh')
    ) {
      return Promise.reject(error);
    }

    const persisted = getPersistedAuthState();

    if (!persisted.refreshToken) {
      clearPersistedAuthState();
      return Promise.reject(error);
    }

    originalRequest._retry = true;
    refreshPromise ??= refreshTokens(persisted.refreshToken).finally(() => {
      refreshPromise = null;
    });

    try {
      const refreshed = await refreshPromise;
      const nextState: PersistedAuthState = {
        accessToken: refreshed.accessToken,
        refreshToken: refreshed.refreshToken,
        expiresAt: refreshed.expiresAt,
        user: refreshed.user ?? persisted.user
      };

      persistAuthState(nextState);
      applyAuthHeader(originalRequest, refreshed.accessToken);
      return apiClient(originalRequest);
    } catch (refreshError) {
      clearPersistedAuthState();

      if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
        window.location.assign('/login');
      }

      return Promise.reject(refreshError);
    }
  }
);
