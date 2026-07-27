<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Button from 'primevue/button';

const props = defineProps<{
  collapsed: boolean;
  isMobile: boolean;
  mobileOpen: boolean;
}>();

const emit = defineEmits<{
  close: [];
}>();

const route = useRoute();

interface NavigationItem {
  label: string;
  icon: string;
  routeName: string;
  to: { name: string };
}

const navigationItems: NavigationItem[] = [
  { label: 'Dashboard', icon: 'pi pi-home', routeName: 'dashboard', to: { name: 'dashboard' } },
  { label: 'Quotes', icon: 'pi pi-file-edit', routeName: 'quotes', to: { name: 'quotes' } },
  { label: 'Portfolio', icon: 'pi pi-briefcase', routeName: 'portfolio', to: { name: 'portfolio' } },
  { label: 'Products', icon: 'pi pi-box', routeName: 'products', to: { name: 'products' } },
  { label: 'Administration', icon: 'pi pi-cog', routeName: 'admin', to: { name: 'admin' } },
  { label: 'Analytics', icon: 'pi pi-chart-bar', routeName: 'analytics', to: { name: 'analytics' } },
  { label: 'Monitoring', icon: 'pi pi-wave-pulse', routeName: 'monitoring', to: { name: 'monitoring' } }
];

const sidebarClasses = computed(() => ({
  'sidebar--collapsed': props.collapsed && !props.isMobile,
  'sidebar--mobile-open': props.mobileOpen,
  'sidebar--mobile': props.isMobile
}));

const isItemActive = (item: NavigationItem) => {
  if (item.routeName === 'quotes') {
    return ['quotes', 'quote-detail', 'quote-create'].includes(String(route.name));
  }

  if (item.routeName === 'products') {
    return ['products', 'product-detail'].includes(String(route.name));
  }

  return route.name === item.routeName;
};
</script>

<template>
  <aside class="sidebar surface-card" :class="sidebarClasses">
    <div class="sidebar__brand">
      <div class="sidebar__logo">IF</div>
      <div v-if="!collapsed || isMobile" class="sidebar__brand-copy">
        <span>InsuRateForge</span>
        <small>Pricing Platform</small>
      </div>
      <Button
        v-if="isMobile"
        icon="pi pi-times"
        severity="secondary"
        text
        rounded
        aria-label="Close navigation"
        @click="emit('close')"
      />
    </div>

    <nav class="sidebar__nav">
      <RouterLink
        v-for="item in navigationItems"
        :key="item.routeName"
        :to="item.to"
        class="sidebar__link"
        :class="{ 'sidebar__link--active': isItemActive(item) }"
        @click="isMobile && emit('close')"
      >
        <i :class="item.icon"></i>
        <span v-if="!collapsed || isMobile">{{ item.label }}</span>
      </RouterLink>
    </nav>

    <div class="sidebar__footer" :class="{ 'sidebar__footer--compact': collapsed && !isMobile }">
      <span class="sidebar__footer-chip">
        <i class="pi pi-sparkles"></i>
        <span v-if="!collapsed || isMobile">Release 2026.3</span>
      </span>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  position: fixed;
  inset: 1rem auto 1rem 1rem;
  z-index: 50;
  width: calc(var(--sidebar-width) - 1rem);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.1rem;
  overflow: hidden;
  transition: width 0.22s ease, transform 0.22s ease;
}

.sidebar--collapsed {
  width: calc(var(--sidebar-collapsed-width) - 1rem);
}

.sidebar--mobile {
  transform: translateX(calc(-100% - 1rem));
  inset: 0 auto 0 0;
  width: min(320px, 88vw);
  border-radius: 0 1.5rem 1.5rem 0;
}

.sidebar--mobile-open {
  transform: translateX(0);
}

.sidebar__brand {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding-bottom: 0.5rem;
}

.sidebar__logo {
  width: 2.75rem;
  height: 2.75rem;
  display: grid;
  place-items: center;
  border-radius: 0.9rem;
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-accent));
  color: white;
  font-weight: 700;
  letter-spacing: 0.06em;
  flex-shrink: 0;
}

.sidebar__brand-copy {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 0.1rem;
}

.sidebar__brand-copy span {
  font-size: 1rem;
  font-weight: 700;
}

.sidebar__brand-copy small {
  color: var(--text-muted);
}

.sidebar__nav {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 0.35rem;
}

.sidebar__link {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.85rem 0.95rem;
  border-radius: 0.95rem;
  color: var(--text-muted);
  font-weight: 500;
  transition: background 0.18s ease, color 0.18s ease, transform 0.18s ease;
}

.sidebar__link i {
  font-size: 1rem;
  min-width: 1rem;
}

.sidebar__link:hover {
  background: var(--surface-muted);
  color: var(--surface-strong);
  transform: translateX(2px);
}

.sidebar__link--active {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.18), rgba(124, 58, 237, 0.14));
  color: var(--surface-strong);
  border: 1px solid rgba(37, 99, 235, 0.18);
}

.sidebar__footer {
  display: flex;
}

.sidebar__footer--compact {
  justify-content: center;
}

.sidebar__footer-chip {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 0.8rem 0.9rem;
  border-radius: 0.95rem;
  background: var(--surface-muted);
  border: 1px solid var(--surface-border);
  color: var(--text-muted);
}
</style>
