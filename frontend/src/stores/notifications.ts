import { defineStore } from 'pinia';
import type { AppNotification, NotificationSeverity } from '@/types/models';

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    messages: [] as AppNotification[]
  }),
  getters: {
    pendingToasts: (state) => state.messages.filter((message) => !message.displayed)
  },
  actions: {
    push(severity: NotificationSeverity, summary: string, detail: string, life = 4000) {
      this.messages.push({
        id: globalThis.crypto?.randomUUID?.() ?? `toast-${Date.now()}-${this.messages.length}`,
        severity,
        summary,
        detail,
        life,
        displayed: false
      });
    },
    success(summary: string, detail: string, life?: number) {
      this.push('success', summary, detail, life);
    },
    info(summary: string, detail: string, life?: number) {
      this.push('info', summary, detail, life);
    },
    warn(summary: string, detail: string, life?: number) {
      this.push('warn', summary, detail, life);
    },
    error(summary: string, detail: string, life?: number) {
      this.push('error', summary, detail, life);
    },
    markDisplayed(ids: string[]) {
      this.messages = this.messages.map((message) =>
        ids.includes(message.id) ? { ...message, displayed: true } : message
      );
    },
    clear() {
      this.messages = [];
    }
  }
});
