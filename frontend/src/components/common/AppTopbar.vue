<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import Menu from 'primevue/menu';
import type { MenuItem } from 'primevue/menuitem';
import { useAuthStore } from '@/stores/auth';
import { useThemeStore } from '@/stores/theme';

defineProps<{
  isMobile: boolean;
}>();

const emit = defineEmits<{
  'toggle-sidebar': [];
}>();

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const themeStore = useThemeStore();
const menu = ref<InstanceType<typeof Menu> | null>(null);

const routeTitle = computed(() => String(route.meta.title ?? 'Workspace'));

const menuItems = computed<MenuItem[]>(() => [
  {
    label: authStore.user?.name ?? 'Signed in',
    items: [
      {
        label: 'Open dashboard',
        icon: 'pi pi-home',
        command: () => router.push({ name: 'dashboard' })
      },
      {
        label: 'Review quotes',
        icon: 'pi pi-file-edit',
        command: () => router.push({ name: 'quotes' })
      }
    ]
  },
  {
    label: 'Session',
    items: [
      {
        label: themeStore.isDark ? 'Switch to light mode' : 'Switch to dark mode',
        icon: themeStore.isDark ? 'pi pi-sun' : 'pi pi-moon',
        command: () => themeStore.toggleTheme()
      },
      {
        label: 'Logout',
        icon: 'pi pi-sign-out',
        command: () => {
          authStore.logout();
          router.push({ name: 'login' });
        }
      }
    ]
  }
]);

const toggleUserMenu = (event: Event) => {
  menu.value?.toggle(event);
};
</script>

<template>
  <header class="topbar surface-card">
    <div class="topbar__left">
      <Button
        icon="pi pi-bars"
        text
        rounded
        severity="secondary"
        aria-label="Toggle navigation"
        @click="emit('toggle-sidebar')"
      />
      <div>
        <span class="topbar__eyebrow">Platform workspace</span>
        <h2>{{ routeTitle }}</h2>
      </div>
    </div>

    <div class="topbar__right">
      <Button
        :icon="themeStore.isDark ? 'pi pi-sun' : 'pi pi-moon'"
        text
        rounded
        severity="secondary"
        :aria-label="themeStore.isDark ? 'Enable light mode' : 'Enable dark mode'"
        @click="themeStore.toggleTheme()"
      />
      <Button icon="pi pi-bell" text rounded severity="secondary" aria-label="Open notifications" />
      <Button class="topbar__profile" text rounded severity="secondary" @click="toggleUserMenu">
        <Avatar :label="authStore.user?.initials ?? 'IF'" shape="circle" class="topbar__avatar" />
        <span class="topbar__profile-copy">
          <strong>{{ authStore.user?.name ?? 'InsuRateForge' }}</strong>
          <small>{{ authStore.user?.role ?? 'Insurance platform' }}</small>
        </span>
        <i class="pi pi-angle-down"></i>
      </Button>
      <Menu ref="menu" :model="menuItems" popup />
    </div>
  </header>
</template>

<style scoped>
.topbar {
  position: fixed;
  top: 1rem;
  right: 1rem;
  left: calc(var(--sidebar-width) + 1rem);
  z-index: 30;
  height: calc(var(--topbar-height) - 1rem);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0 1rem;
  transition: left 0.22s ease;
}

.topbar__left,
.topbar__right {
  display: flex;
  align-items: center;
  gap: 0.9rem;
}

.topbar__eyebrow {
  display: block;
  color: var(--text-muted);
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.topbar h2 {
  margin: 0.1rem 0 0;
  font-size: 1.15rem;
}

.topbar__profile {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding-inline: 0.65rem;
}

.topbar__profile-copy {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.15;
}

.topbar__profile-copy small {
  color: var(--text-muted);
}

.topbar__avatar {
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-accent));
  color: #fff;
}

@media (max-width: 1023px) {
  .topbar {
    left: 1rem;
  }
}

@media (max-width: 768px) {
  .topbar {
    height: auto;
    flex-wrap: wrap;
    align-items: flex-start;
    padding: 0.8rem 0.95rem;
  }

  .topbar__right {
    width: 100%;
    justify-content: flex-end;
  }

  .topbar__profile-copy {
    display: none;
  }
}
</style>
