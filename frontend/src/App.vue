<script setup lang="ts">
import { watch } from 'vue';
import { RouterView } from 'vue-router';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import GlobalConfirmDialog from '@/components/common/ConfirmDialog.vue';
import { useNotificationsStore } from '@/stores/notifications';

const notifications = useNotificationsStore();
const toast = useToast();

watch(
  () => notifications.pendingToasts,
  (messages) => {
    if (!messages.length) {
      return;
    }

    messages.forEach(({ severity, summary, detail, life }) => {
      toast.add({ severity, summary, detail, life });
    });

    notifications.markDisplayed(messages.map((message) => message.id));
  },
  { deep: true, immediate: true }
);
</script>

<template>
  <RouterView />
  <Toast position="top-right" />
  <GlobalConfirmDialog />
</template>
