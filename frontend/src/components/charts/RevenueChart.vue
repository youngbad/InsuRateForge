<script setup lang="ts">
import { computed } from 'vue';
import type { ApexOptions } from 'apexcharts';
import type { RevenuePoint } from '@/types/models';
import { useThemeStore } from '@/stores/theme';

const props = defineProps<{
  series: RevenuePoint[];
}>();

const themeStore = useThemeStore();

const chartSeries = computed(() => [
  {
    name: 'Written premium',
    data: props.series.map((point) => point.writtenPremium)
  },
  {
    name: 'Earned premium',
    data: props.series.map((point) => point.earnedPremium)
  }
]);

const chartOptions = computed<ApexOptions>(() => ({
  chart: {
    toolbar: { show: false },
    background: 'transparent',
    foreColor: themeStore.isDark ? '#e2e8f0' : '#334155'
  },
  stroke: {
    width: 3,
    curve: 'smooth'
  },
  colors: ['#2563eb', '#7c3aed'],
  markers: {
    size: 4,
    hover: { size: 6 }
  },
  xaxis: {
    categories: props.series.map((point) => point.month),
    labels: {
      style: {
        colors: themeStore.isDark ? '#94a3b8' : '#64748b'
      }
    }
  },
  yaxis: {
    labels: {
      formatter: (value: number) => `$${Math.round(value / 1000)}k`
    }
  },
  grid: {
    borderColor: themeStore.isDark ? 'rgba(148, 163, 184, 0.12)' : 'rgba(15, 23, 42, 0.08)'
  },
  tooltip: {
    y: {
      formatter: (value: number) =>
        new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          maximumFractionDigits: 0
        }).format(value)
    }
  },
  legend: {
    position: 'top'
  }
}));
</script>

<template>
  <ApexChart type="line" height="320" :options="chartOptions" :series="chartSeries" />
</template>
