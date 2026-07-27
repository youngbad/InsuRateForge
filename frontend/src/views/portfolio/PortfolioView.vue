<script setup lang="ts">
import { computed } from 'vue';
import Card from 'primevue/card';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import ProgressBar from 'primevue/progressbar';
import StatusBadge from '@/components/common/StatusBadge.vue';
import { useProducts } from '@/composables/useProducts';
import { useQuotesList } from '@/composables/useQuotes';
import type { Product } from '@/types/models';

const productsQuery = useProducts();
const quotesQuery = useQuotesList(() => ({
  page: 1,
  pageSize: 100,
  search: '',
  status: 'All',
  sortBy: 'premium',
  sortDir: 'desc'
}));

interface PortfolioRollup {
  productId: string;
  productName: string;
  quoteCount: number;
  premium: number;
  bindRatio: number;
}

const currency = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0
});

const totalPremium = computed(() =>
  (quotesQuery.data.value?.items ?? []).reduce((sum, quote) => sum + quote.premium, 0)
);

const boundCount = computed(
  () => (quotesQuery.data.value?.items ?? []).filter((quote) => quote.status === 'Bound').length
);

const portfolioByProduct = computed<PortfolioRollup[]>(() => {
  const quotes = quotesQuery.data.value?.items ?? [];
  const products = productsQuery.data.value ?? [];

  return products.map((product: Product) => {
    const productQuotes = quotes.filter((quote) => quote.productId === product.id);
    const premium = productQuotes.reduce((sum, quote) => sum + quote.premium, 0);
    const bound = productQuotes.filter((quote) => quote.status === 'Bound').length;

    return {
      productId: product.id,
      productName: product.name,
      quoteCount: productQuotes.length,
      premium,
      bindRatio: productQuotes.length ? bound / productQuotes.length : 0
    };
  });
});

const renewalPipeline = computed(() =>
  (quotesQuery.data.value?.items ?? [])
    .slice()
    .sort((left, right) => new Date(left.effectiveDate).getTime() - new Date(right.effectiveDate).getTime())
    .slice(0, 5)
);
</script>

<template>
  <div class="page-shell">
    <header class="page-header">
      <div class="page-header__title">
        <h1>Portfolio workspace</h1>
        <p>Track premium concentration, binding performance, and upcoming renewals.</p>
      </div>
      <div class="metric-strip">
        <span class="metric-chip"><i class="pi pi-wallet"></i> {{ currency.format(totalPremium) }} total premium</span>
        <span class="metric-chip"><i class="pi pi-verified"></i> {{ boundCount }} bound policies</span>
      </div>
    </header>

    <section class="grid-3">
      <Card class="surface-card">
        <template #title>Premium at risk</template>
        <template #content>
          <h2>{{ currency.format(totalPremium * 0.41) }}</h2>
          <p class="section-note">Premium tied to CAT and inflation-sensitive exposures.</p>
        </template>
      </Card>
      <Card class="surface-card">
        <template #title>Average bind ratio</template>
        <template #content>
          <h2>
            {{
              Math.round(
                (portfolioByProduct.reduce((sum, item) => sum + item.bindRatio, 0) /
                  Math.max(portfolioByProduct.length, 1)) *
                  100
              )
            }}%
          </h2>
          <p class="section-note">Across current product shelf participation.</p>
        </template>
      </Card>
      <Card class="surface-card">
        <template #title>Renewals due in 45 days</template>
        <template #content>
          <h2>{{ renewalPipeline.length }}</h2>
          <p class="section-note">Use the list below to coordinate outreach and pricing refreshes.</p>
        </template>
      </Card>
    </section>

    <section class="grid-2">
      <Card class="surface-card table-compact">
        <template #title>Portfolio by product</template>
        <template #subtitle>Premium concentration and bind effectiveness</template>
        <template #content>
          <DataTable :value="portfolioByProduct" responsive-layout="scroll">
            <Column field="productName" header="Product" />
            <Column field="quoteCount" header="Quotes" />
            <Column header="Premium">
              <template #body="{ data }">
                {{ currency.format(data.premium) }}
              </template>
            </Column>
            <Column header="Bind ratio">
              <template #body="{ data }">
                <ProgressBar :value="Math.round(data.bindRatio * 100)" />
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>

      <Card class="surface-card table-compact">
        <template #title>Upcoming renewals</template>
        <template #subtitle>Sorted by effective date</template>
        <template #content>
          <DataTable :value="renewalPipeline" responsive-layout="scroll">
            <Column field="quoteNumber" header="Quote" />
            <Column field="insuredName" header="Insured" />
            <Column field="productName" header="Product" />
            <Column header="Status">
              <template #body="{ data }">
                <StatusBadge :label="data.status" />
              </template>
            </Column>
            <Column header="Effective">
              <template #body="{ data }">
                {{ new Date(data.effectiveDate).toLocaleDateString() }}
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>
    </section>
  </div>
</template>
