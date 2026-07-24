<script setup lang="ts">
import { useRouter } from 'vue-router';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import StatusBadge from '@/components/common/StatusBadge.vue';
import { useProducts } from '@/composables/useProducts';

const router = useRouter();
const productsQuery = useProducts();
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
        <h1>Product workspace</h1>
        <p>Review available insurance products, appetite constraints, and version metadata.</p>
      </div>
    </header>

    <Card class="surface-card table-compact">
      <template #content>
        <DataTable :value="productsQuery.data.value ?? []" responsive-layout="scroll">
          <Column field="code" header="Code" />
          <Column field="name" header="Product" />
          <Column field="lineOfBusiness" header="Line" />
          <Column header="Status">
            <template #body="{ data }">
              <StatusBadge :label="data.status" />
            </template>
          </Column>
          <Column field="version" header="Version" />
          <Column header="Max coverage">
            <template #body="{ data }">
              {{ currency.format(data.maxCoverage) }}
            </template>
          </Column>
          <Column header="Actions" style="width: 8rem">
            <template #body="{ data }">
              <Button
                label="Open"
                size="small"
                outlined
                @click="router.push({ name: 'product-detail', params: { id: data.id } })"
              />
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>
  </div>
</template>
