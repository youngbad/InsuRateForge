<script setup lang="ts">
import { computed } from 'vue';
import type { ApexOptions } from 'apexcharts';
import Card from 'primevue/card';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import StatusBadge from '@/components/common/StatusBadge.vue';
import { useMonitoringSnapshot } from '@/composables/useDashboard';
import { useThemeStore } from '@/stores/theme';

const monitoringQuery = useMonitoringSnapshot();
const themeStore = useThemeStore();

const latencyChartOptions = computed<ApexOptions>(() => ({
  chart: {
    type: 'bar',
    toolbar: { show: false },
    background: 'transparent',
    foreColor: themeStore.isDark ? '#e2e8f0' : '#334155'
  },
  colors: ['#2563eb'],
  xaxis: {
    categories: (monitoringQuery.data.value?.quoteLatencySeries ?? []).map((point) => point.interval)
  },
  yaxis: {
    labels: {
      formatter: (value: number) => `${Math.round(value)} ms`
    }
  },
  plotOptions: {
    bar: {
      borderRadius: 8,
      columnWidth: '45%'
    }
  },
  grid: {
    borderColor: themeStore.isDark ? 'rgba(148, 163, 184, 0.12)' : 'rgba(15, 23, 42, 0.08)'
  }
}));

const latencyChartSeries = computed(() => [
  {
    name: 'Quote latency',
    data: (monitoringQuery.data.value?.quoteLatencySeries ?? []).map((point) => point.latencyMs)
  }
]);
</script>

<template>
  <div class="page-shell">
    <header class="page-header">
      <div class="page-header__title">
        <h1>Monitoring</h1>
        <p>Track service health, pricing latency, and live incident activity.</p>
      </div>
    </header>

    <section class="grid-2">
      <Card class="surface-card">
        <template #title>Quote engine latency</template>
        <template #subtitle>Average response time across the intraday quote burst</template>
        <template #content>
          <ApexChart type="bar" height="320" :options="latencyChartOptions" :series="latencyChartSeries" />
        </template>
      </Card>
      <Card class="surface-card">
        <template #title>Service health</template>
        <template #subtitle>Current platform dependencies and uptime profile</template>
        <template #content>
          <div class="monitoring-services">
            <article
              v-for="service in monitoringQuery.data.value?.services ?? []"
              :key="service.id"
              class="monitoring-services__item"
            >
              <div>
                <div class="monitoring-services__header">
                  <h3>{{ service.name }}</h3>
                  <StatusBadge :label="service.status" />
                </div>
                <p>{{ service.owner }}</p>
              </div>
              <div class="monitoring-services__meta">
                <strong>{{ service.latencyMs }} ms</strong>
                <small>{{ service.uptimePercentage.toFixed(2) }}% uptime</small>
              </div>
            </article>
          </div>
        </template>
      </Card>
    </section>

    <section>
      <Card class="surface-card table-compact">
        <template #title>Open alerts</template>
        <template #subtitle>Current operational follow-up list</template>
        <template #content>
          <DataTable :value="monitoringQuery.data.value?.alerts ?? []" responsive-layout="scroll">
            <Column field="service" header="Service" />
            <Column header="Severity">
              <template #body="{ data }">
                <StatusBadge :label="data.severity" />
              </template>
            </Column>
            <Column field="message" header="Alert" />
            <Column header="State">
              <template #body="{ data }">
                <StatusBadge :label="data.state" />
              </template>
            </Column>
            <Column header="Opened">
              <template #body="{ data }">
                {{ new Date(data.openedAt).toLocaleString() }}
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>
    </section>
  </div>
</template>

<style scoped>
.monitoring-services {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.monitoring-services__item {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  border-radius: 1rem;
  background: var(--surface-muted);
  border: 1px solid var(--surface-border);
}

.monitoring-services__header {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.monitoring-services__header h3,
.monitoring-services__item p,
.monitoring-services__meta strong,
.monitoring-services__meta small {
  margin: 0;
}

.monitoring-services__item p,
.monitoring-services__meta small {
  color: var(--text-muted);
}

.monitoring-services__meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
</style>
