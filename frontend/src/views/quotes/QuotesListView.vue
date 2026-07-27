<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useConfirm } from 'primevue/useconfirm';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import InputText from 'primevue/inputtext';
import Select from 'primevue/select';
import StatusBadge from '@/components/common/StatusBadge.vue';
import { useDeleteQuote, useQuotesList } from '@/composables/useQuotes';
import { useNotificationsStore } from '@/stores/notifications';
import type { QuoteListParams, QuoteStatus, QuoteSummary } from '@/types/models';

const router = useRouter();
const confirm = useConfirm();
const notifications = useNotificationsStore();
const deleteQuoteMutation = useDeleteQuote();

const search = ref('');
const status = ref<QuoteStatus | 'All'>('All');
const page = ref(1);
const rows = ref(5);
const sortField = ref<QuoteListParams['sortBy']>('createdAt');
const sortDir = ref<'asc' | 'desc'>('desc');

const queryParams = computed<QuoteListParams>(() => ({
  page: page.value,
  pageSize: rows.value,
  search: search.value,
  status: status.value,
  sortBy: sortField.value,
  sortDir: sortDir.value
}));

const quotesQuery = useQuotesList(queryParams);

const statusOptions: Array<QuoteStatus | 'All'> = ['All', 'Draft', 'Priced', 'Approved', 'Bound', 'Declined'];
const currency = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0
});

const onPage = (event: { page: number; rows: number }) => {
  page.value = event.page + 1;
  rows.value = event.rows;
};

const onSort = (event: {
  sortField?: string | ((item: QuoteSummary) => string);
  sortOrder?: 1 | -1 | 0 | null;
}) => {
  sortField.value =
    typeof event.sortField === 'string' ? (event.sortField as QuoteListParams['sortBy']) : 'createdAt';
  sortDir.value = event.sortOrder === 1 ? 'asc' : 'desc';
};

const openQuote = (quoteId: string) => {
  router.push({ name: 'quote-detail', params: { id: quoteId } });
};

const archiveQuote = (quote: QuoteSummary) => {
  confirm.require({
    group: 'global',
    header: 'Archive quote',
    message: `Archive ${quote.quoteNumber} for ${quote.insuredName}? This removes it from the local working set.`,
    icon: 'pi pi-inbox',
    acceptLabel: 'Archive',
    acceptClass: 'danger',
    accept: async () => {
      await deleteQuoteMutation.mutateAsync(quote.id);
      notifications.success('Quote archived', `${quote.quoteNumber} has been removed from the active queue.`);
    }
  });
};
</script>

<template>
  <div class="page-shell">
    <header class="page-header">
      <div class="page-header__title">
        <h1>Quote workspace</h1>
        <p>Search, triage, and route pricing submissions across the underwriting queue.</p>
      </div>
      <Button label="Create quote" icon="pi pi-plus" @click="router.push({ name: 'quote-create' })" />
    </header>

    <Card class="surface-card">
      <template #content>
        <div class="quotes-toolbar">
          <span class="p-input-icon-left quotes-toolbar__search">
            <i class="pi pi-search"></i>
            <InputText v-model="search" fluid placeholder="Search by quote, insured, broker, or region" />
          </span>
          <Select v-model="status" :options="statusOptions" placeholder="Filter status" class="quotes-toolbar__status" />
        </div>

        <DataTable
          class="table-compact"
          :value="quotesQuery.data.value?.items ?? []"
          lazy
          paginator
          responsive-layout="scroll"
          :rows="rows"
          :first="(page - 1) * rows"
          :total-records="quotesQuery.data.value?.total ?? 0"
          :loading="quotesQuery.isLoading.value || deleteQuoteMutation.isPending.value"
          sort-mode="single"
          :sort-field="sortField"
          :sort-order="sortDir === 'asc' ? 1 : -1"
          @page="onPage"
          @sort="onSort"
        >
          <Column field="quoteNumber" header="Quote" sortable>
            <template #body="{ data }">
              <button class="quotes-link" type="button" @click="openQuote(data.id)">
                {{ data.quoteNumber }}
              </button>
            </template>
          </Column>
          <Column field="insuredName" header="Insured" sortable />
          <Column field="productName" header="Product" sortable />
          <Column field="region" header="Region" sortable />
          <Column header="Status">
            <template #body="{ data }">
              <StatusBadge :label="data.status" />
            </template>
          </Column>
          <Column field="premium" header="Premium" sortable>
            <template #body="{ data }">
              {{ currency.format(data.premium) }}
            </template>
          </Column>
          <Column field="effectiveDate" header="Effective" sortable>
            <template #body="{ data }">
              {{ new Date(data.effectiveDate).toLocaleDateString() }}
            </template>
          </Column>
          <Column header="Actions" :exportable="false" style="width: 9rem">
            <template #body="{ data }">
              <div class="quotes-actions">
                <Button icon="pi pi-pencil" text rounded severity="secondary" @click="openQuote(data.id)" />
                <Button icon="pi pi-archive" text rounded severity="danger" @click="archiveQuote(data)" />
              </div>
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>
  </div>
</template>

<style scoped>
.quotes-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.quotes-toolbar__search {
  flex: 1 1 22rem;
}

.quotes-toolbar__status {
  width: 14rem;
}

.quotes-link {
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--brand-primary);
  cursor: pointer;
  font-weight: 600;
}

.quotes-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.25rem;
}
</style>
