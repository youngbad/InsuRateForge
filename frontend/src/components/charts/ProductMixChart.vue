<script setup lang="ts">
import { computed } from 'vue';
import type { ApexOptions } from 'apexcharts';
import type { ProductMixItem } from '@/types/models';
import { useThemeStore } from '@/stores/theme';

const props = defineProps<{
  items: ProductMixItem[];
}>();

const themeStore = useThemeStore();

const chartSeries = computed(() => props.items.map((item) => item.value));
const chartOptions = computed<ApexOptions>(() => ({
  labels: props.items.map((item) => item.label),
  colors: ['#2563eb', '#7c3aed', '#14b8a6', '#f59e0b', '#ef4444'],
  chart: {
    background: 'transparent',
    foreColor: themeStore.isDark ? '#e2e8f0' : '#334155'
  },
  legend: {
    position: 'bottom'
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    colors: [themeStore.isDark ? '#07111f' : '#ffffff']
  },
  plotOptions: {
    pie: {
      donut: {
        size: '70%',
        labels: {
          show: true,
          total: {
            show: true,
            label: 'Quotes'
          }
        }
      }
    }
  }
}));
</script>

<template>
  <ApexChart type="donut" height="320" :options="chartOptions" :series="chartSeries" />
</template>
