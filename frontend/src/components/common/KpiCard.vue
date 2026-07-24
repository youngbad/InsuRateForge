<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  title: string;
  value: string;
  subtitle: string;
  trend: string;
  icon: string;
  tone?: 'primary' | 'success' | 'warning' | 'danger';
}>();

const toneClass = computed(() => `kpi-card--${props.tone ?? 'primary'}`);
</script>

<template>
  <article class="kpi-card surface-card surface-card--padded" :class="toneClass">
    <div class="kpi-card__header">
      <div>
        <p>{{ title }}</p>
        <h3>{{ value }}</h3>
      </div>
      <span class="kpi-card__icon">
        <i :class="icon"></i>
      </span>
    </div>
    <div class="kpi-card__footer">
      <strong>{{ trend }}</strong>
      <span>{{ subtitle }}</span>
    </div>
  </article>
</template>

<style scoped>
.kpi-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.kpi-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.kpi-card p,
.kpi-card h3 {
  margin: 0;
}

.kpi-card p {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.kpi-card h3 {
  margin-top: 0.35rem;
  font-size: 1.7rem;
  line-height: 1.15;
}

.kpi-card__icon {
  width: 2.8rem;
  height: 2.8rem;
  display: grid;
  place-items: center;
  border-radius: 0.95rem;
  font-size: 1.15rem;
}

.kpi-card__footer {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.kpi-card__footer strong {
  font-size: 0.95rem;
}

.kpi-card__footer span {
  color: var(--text-muted);
  font-size: 0.92rem;
}

.kpi-card--primary .kpi-card__icon {
  background: var(--info-soft);
  color: var(--brand-primary);
}

.kpi-card--success .kpi-card__icon {
  background: var(--success-soft);
  color: #15803d;
}

.kpi-card--warning .kpi-card__icon {
  background: var(--warning-soft);
  color: #b45309;
}

.kpi-card--danger .kpi-card__icon {
  background: var(--danger-soft);
  color: #dc2626;
}
</style>
