<script setup lang="ts">
import Card from 'primevue/card';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import Skeleton from 'primevue/skeleton';
import KpiCard from '@/components/common/KpiCard.vue';
import StatusBadge from '@/components/common/StatusBadge.vue';
import ProductMixChart from '@/components/charts/ProductMixChart.vue';
import RevenueChart from '@/components/charts/RevenueChart.vue';
import { useDashboardOverview } from '@/composables/useDashboard';

const dashboardQuery = useDashboardOverview();
const currency = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0
});
</script>

<template>
  <div class="page-shell">
    <header class="page-header">
      <div class="page-header__title">
        <h1>Pricing command center</h1>
        <p>Monitor performance, pipeline movement, and underwriting alerts in one view.</p>
      </div>
      <div class="metric-strip">
        <span class="metric-chip"><i class="pi pi-calendar"></i> Updated every 15 minutes</span>
        <span class="metric-chip"><i class="pi pi-shield"></i> Operational status: 99.95% uptime</span>
      </div>
    </header>

    <section v-if="dashboardQuery.isLoading.value" class="grid-4">
      <Skeleton v-for="item in 4" :key="item" height="10rem" borderRadius="1rem" />
    </section>
    <section v-else class="grid-4">
      <KpiCard
        v-for="kpi in dashboardQuery.data.value?.kpis ?? []"
        :key="kpi.title"
        :title="kpi.title"
        :value="kpi.value"
        :subtitle="kpi.subtitle"
        :trend="kpi.delta"
        :icon="kpi.icon"
        :tone="kpi.tone"
      />
    </section>

    <section class="grid-2">
      <Card class="surface-card">
        <template #title>Revenue trend</template>
        <template #subtitle>Written versus earned premium for the last six months</template>
        <template #content>
          <RevenueChart :series="dashboardQuery.data.value?.revenueSeries ?? []" />
        </template>
      </Card>

      <Card class="surface-card">
        <template #title>Product mix</template>
        <template #subtitle>Quote volume concentration across active products</template>
        <template #content>
          <ProductMixChart :items="dashboardQuery.data.value?.productMix ?? []" />
        </template>
      </Card>
    </section>

    <section class="grid-2">
      <Card class="surface-card table-compact">
        <template #title>Pipeline spotlight</template>
        <template #subtitle>Highest premium submissions that need attention</template>
        <template #content>
          <DataTable :value="dashboardQuery.data.value?.pipeline ?? []" responsive-layout="scroll">
            <Column field="quoteNumber" header="Quote" />
            <Column field="insuredName" header="Insured" />
            <Column field="region" header="Region" />
            <Column header="Status">
              <template #body="{ data }">
                <StatusBadge :label="data.status" />
              </template>
            </Column>
            <Column header="Premium">
              <template #body="{ data }">
                {{ currency.format(data.premium) }}
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>

      <Card class="surface-card">
        <template #title>Operational alerts</template>
        <template #subtitle>Recent exceptions surfaced from platform monitoring</template>
        <template #content>
          <div class="dashboard-alerts">
            <article
              v-for="alert in dashboardQuery.data.value?.alerts ?? []"
              :key="alert.id"
              class="dashboard-alerts__item"
            >
              <div>
                <StatusBadge :label="alert.severity" />
                <h4>{{ alert.title }}</h4>
                <p>{{ alert.description }}</p>
              </div>
              <small>{{ new Date(alert.timestamp).toLocaleString() }}</small>
            </article>
          </div>
        </template>
      </Card>
    </section>
  </div>
</template>

<style scoped>
.dashboard-alerts {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.dashboard-alerts__item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  border-radius: 1rem;
  background: var(--surface-muted);
  border: 1px solid var(--surface-border);
}

.dashboard-alerts__item h4,
.dashboard-alerts__item p {
  margin: 0;
}

.dashboard-alerts__item h4 {
  margin-top: 0.65rem;
  margin-bottom: 0.35rem;
}

.dashboard-alerts__item p,
.dashboard-alerts__item small {
  color: var(--text-muted);
}
</style>
