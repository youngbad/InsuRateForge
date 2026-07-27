<script setup lang="ts">
import { computed } from 'vue';
import Tag from 'primevue/tag';

const props = defineProps<{
  label: string;
  severity?: 'success' | 'info' | 'warn' | 'danger' | 'secondary' | 'contrast';
}>();

const resolvedSeverity = computed(() => {
  if (props.severity) {
    return props.severity;
  }

  const normalized = props.label.toLowerCase();

  if (['bound', 'approved', 'healthy', 'active'].includes(normalized)) {
    return 'success';
  }

  if (['priced', 'pilot', 'open', 'info'].includes(normalized)) {
    return 'info';
  }

  if (['draft', 'degraded', 'paused', 'investigating', 'warn'].includes(normalized)) {
    return 'warn';
  }

  if (['declined', 'offline', 'error'].includes(normalized)) {
    return 'danger';
  }

  return 'secondary';
});
</script>

<template>
  <Tag :value="label" :severity="resolvedSeverity" rounded />
</template>
