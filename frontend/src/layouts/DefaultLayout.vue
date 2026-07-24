<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue';
import { RouterView } from 'vue-router';
import AppSidebar from '@/components/common/AppSidebar.vue';
import AppTopbar from '@/components/common/AppTopbar.vue';

const sidebarCollapsed = ref(false);
const mobileSidebarOpen = ref(false);
const isMobile = ref(false);

const syncViewport = () => {
  if (typeof window === 'undefined') {
    return;
  }

  isMobile.value = window.innerWidth < 1024;
  if (!isMobile.value) {
    mobileSidebarOpen.value = false;
  }
};

const toggleSidebar = () => {
  if (isMobile.value) {
    mobileSidebarOpen.value = !mobileSidebarOpen.value;
    return;
  }

  sidebarCollapsed.value = !sidebarCollapsed.value;
};

onMounted(() => {
  syncViewport();
  window.addEventListener('resize', syncViewport);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', syncViewport);
});
</script>

<template>
  <div class="layout-shell">
    <AppSidebar
      :collapsed="sidebarCollapsed"
      :is-mobile="isMobile"
      :mobile-open="mobileSidebarOpen"
      @close="mobileSidebarOpen = false"
    />
    <div
      v-if="isMobile && mobileSidebarOpen"
      class="layout-shell__overlay"
      @click="mobileSidebarOpen = false"
    ></div>
    <div class="layout-shell__main" :class="{ 'layout-shell__main--collapsed': sidebarCollapsed }">
      <AppTopbar :is-mobile="isMobile" @toggle-sidebar="toggleSidebar" />
      <main class="layout-shell__content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.layout-shell {
  min-height: 100vh;
  background: var(--app-bg);
}

.layout-shell__main {
  min-height: 100vh;
  margin-left: var(--sidebar-width);
  transition: margin-left 0.22s ease;
}

.layout-shell__main--collapsed {
  margin-left: var(--sidebar-collapsed-width);
}

.layout-shell__content {
  padding: calc(var(--topbar-height) + 1.5rem) 1.5rem 1.75rem;
}

.layout-shell__overlay {
  position: fixed;
  inset: 0;
  z-index: 45;
  background: rgba(2, 6, 23, 0.52);
  backdrop-filter: blur(4px);
}

@media (max-width: 1023px) {
  .layout-shell__main,
  .layout-shell__main--collapsed {
    margin-left: 0;
  }

  .layout-shell__content {
    padding: calc(var(--topbar-height) + 1rem) 1rem 1.25rem;
  }
}
</style>
