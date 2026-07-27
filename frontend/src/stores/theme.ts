import { defineStore } from 'pinia';

const THEME_STORAGE_KEY = 'insurateforge-theme';

type ThemeMode = 'light' | 'dark';

const resolvePersistedTheme = (): ThemeMode => {
  if (typeof window === 'undefined') {
    return 'light';
  }

  return window.localStorage.getItem(THEME_STORAGE_KEY) === 'dark' ? 'dark' : 'light';
};

export const useThemeStore = defineStore('theme', {
  state: () => ({
    mode: resolvePersistedTheme() as ThemeMode
  }),
  getters: {
    isDark: (state) => state.mode === 'dark'
  },
  actions: {
    applyTheme() {
      if (typeof document === 'undefined') {
        return;
      }

      document.documentElement.classList.toggle('app-dark', this.mode === 'dark');
    },
    initializeTheme() {
      this.mode = resolvePersistedTheme();
      this.applyTheme();
    },
    setTheme(mode: ThemeMode) {
      this.mode = mode;
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(THEME_STORAGE_KEY, mode);
      }
      this.applyTheme();
    },
    toggleTheme() {
      this.setTheme(this.mode === 'dark' ? 'light' : 'dark');
    }
  }
});
