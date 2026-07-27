import { storeToRefs } from 'pinia';
import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

export function useAuth() {
  const authStore = useAuthStore();
  const { user, status } = storeToRefs(authStore);

  return {
    user,
    status,
    isAuthenticated: computed(() => authStore.isAuthenticated),
    expiresSoon: computed(() => authStore.expiresSoon),
    login: authStore.login,
    logout: authStore.logout,
    refreshSession: authStore.refreshSession,
    loadCurrentUser: authStore.loadCurrentUser
  };
}
