import { defineStore } from 'pinia';
import { getCurrentUser, loginUser, refreshAuthToken } from '@/api/auth';
import { clearPersistedAuthState, getPersistedAuthState, persistAuthState } from '@/api/client';
import type { AuthLoginPayload, PersistedAuthState } from '@/types/models';

type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'error';

const initialState = (): PersistedAuthState => getPersistedAuthState();

export const useAuthStore = defineStore('auth', {
  state: () => ({
    ...initialState(),
    status: initialState().accessToken ? ('authenticated' as AuthStatus) : ('idle' as AuthStatus)
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.accessToken),
    expiresSoon: (state) => {
      if (!state.expiresAt) {
        return false;
      }

      return new Date(state.expiresAt).getTime() - Date.now() < 5 * 60 * 1000;
    }
  },
  actions: {
    persist() {
      persistAuthState({
        accessToken: this.accessToken,
        refreshToken: this.refreshToken,
        expiresAt: this.expiresAt,
        user: this.user
      });
    },
    hydrate() {
      const persisted = getPersistedAuthState();
      this.accessToken = persisted.accessToken;
      this.refreshToken = persisted.refreshToken;
      this.expiresAt = persisted.expiresAt;
      this.user = persisted.user;
      this.status = persisted.accessToken ? 'authenticated' : 'idle';
    },
    async login(payload: AuthLoginPayload) {
      this.status = 'loading';

      try {
        const session = await loginUser(payload);
        const user = session.user ?? (await getCurrentUser());
        this.accessToken = session.accessToken;
        this.refreshToken = session.refreshToken;
        this.expiresAt = session.expiresAt;
        this.user = user;
        this.status = 'authenticated';
        this.persist();
        return user;
      } catch (error) {
        this.status = 'error';
        throw error;
      }
    },
    async refreshSession() {
      if (!this.refreshToken) {
        this.logout();
        return null;
      }

      const refreshed = await refreshAuthToken(this.refreshToken);
      this.accessToken = refreshed.accessToken;
      this.refreshToken = refreshed.refreshToken;
      this.expiresAt = refreshed.expiresAt;
      this.user = refreshed.user ?? this.user;
      this.status = 'authenticated';
      this.persist();
      return refreshed;
    },
    async loadCurrentUser() {
      if (!this.accessToken) {
        return null;
      }

      const user = await getCurrentUser();
      this.user = user;
      this.persist();
      return user;
    },
    logout() {
      this.accessToken = null;
      this.refreshToken = null;
      this.expiresAt = null;
      this.user = null;
      this.status = 'idle';
      clearPersistedAuthState();
    }
  }
});
