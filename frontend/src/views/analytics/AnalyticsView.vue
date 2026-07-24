<script setup lang="ts">
import { computed } from 'vue';
import type { ApexOptions } from 'apexcharts';
import Card from 'primevue/card';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import ProgressBar from 'primevue/progressbar';
import ProductMixChart from '@/components/charts/ProductMixChart.vue';
import { useAnalyticsSnapshot, useDashboardOverview } from '@/composables/useDashboard';
import { useThemeStore } from '@/stores/theme';

const analyticsQuery = useAnalyticsSnapshot();
const dashboardQuery = useDashboardOverview();
const themeStore = useThemeStore();

const hitRatioOptions = computed<ApexOptions>(() => ({
  chart: {
    type: 'area',
    toolbar: { show: false },
    background: 'transparent',
    foreColor: themeStore.isDark ? '#e2e8f0' : '#334155'
  },
  dataLabels: { enabled: false },
  stroke: { width: 3, curve: 'smooth' },
  colors: ['#14b8a6'],
  xaxis: {
    categories: (analyticsQuery.data.value?.hitRatioSeries ?? []).map((point) => point.month)
  },
  yaxis: {
    labels: {
      formatter: (value: number) => `${Math.round(value * 100)}%`
    }
  },
  fill: {
    type: 'gradient',
    gradient: {
      opacityFrom: 0.28,
      opacityTo: 0.02
    }
  },
  grid: {
    borderColor: themeStore.isDark ? 'rgba(148, 163, 184, 0.12)' : 'rgba(15, 23, 42, 0.08)'
  }
}));

const hitRatioSeries = computed(() => [
  {
    name: 'Hit ratio',
    data: (analyticsQuery.data.value?.hitRatioSeries ?? []).map((point) => point.hitRatio)
  }
]);
</script>

<template>
  <div class="page-shell">
    <header class="page-header">
      <div class="page-header__title">
        <h1>Analytics</h1>
        <p>Measure channel performance, regional conversion, and product-level profitability signals.</p>
      </div>
    </header>

    <section class="grid-2">
      <Card class="surface-card">
        <template #title>Hit ratio trend</template>
        <template #subtitle>Trailing six-month bind conversion performance</template>
        <template #content>
          <ApexChart type="area" height="320" :options="hitRatioOptions" :series="hitRatioSeries" />
        </template>
      </Card>
      <Card class="surface-card">
        <template #title>Quote mix by product</template>
        <template #subtitle>Cross-reference demand against performance controls</template>
        <template #content>
          <ProductMixChart :items="dashboardQuery.data.value?.productMix ?? []" />
        </template>
      </Card>
    </section>

    <section class="grid-2">
      <Card class="surface-card table-compact">
        <template #title>Channel performance</template>
        <template #subtitle>Average premium and cycle time by submission channel</template>
        <template #content>
          <DataTable :value="analyticsQuery.data.value?.channelPerformance ?? []" responsive-layout="scroll">
            <Column field="channel" header="Channel" />
            <Column field="quoteCount" header="Quotes" />
            <Column header="Hit ratio">
              <template #body="{ data }">
                <ProgressBar :value="Math.round(data.hitRatio * 100)" />
              </template>
            </Column>
            <Column header="Avg premium">
              <template #body="{ data }">
                {{
                  new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: 'USD',
                    maximumFractionDigits: 0
                  }).format(data.averagePremium)
                }}
              </template>
            </Column>
            <Column field="averageCycleDays" header="Cycle days" />
          </DataTable>
        </template>
      </Card>

      <Card class="surface-card table-compact">
        <template #title>Regional conversion</template>
        <template #subtitle>Benchmark which territories convert the fastest</template>
        <template #content>
          <DataTable :value="analyticsQuery.data.value?.regionalConversion ?? []" responsive-layout="scroll">
            <Column field="region" header="Region" />
            <Column header="Conversion rate">
              <template #body="{ data }">
                <ProgressBar :value="Math.round(data.conversionRate * 100)" />
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>
    </section>
  </div>
</template>
