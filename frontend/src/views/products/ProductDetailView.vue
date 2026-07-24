<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Card from 'primevue/card';
import Chip from 'primevue/chip';
import ProgressBar from 'primevue/progressbar';
import StatusBadge from '@/components/common/StatusBadge.vue';
import { useProduct } from '@/composables/useProducts';

const route = useRoute();
const productId = computed(() => route.params.id as string | undefined);
const productQuery = useProduct(productId);
const product = computed(() => productQuery.data.value);

const currency = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0
});
</script>

<template>
  <div class="page-shell" v-if="product">
    <header class="page-header">
      <div class="page-header__title">
        <h1>{{ product.name }}</h1>
        <p>{{ product.description }}</p>
      </div>
      <div class="metric-strip">
        <StatusBadge :label="product.status" />
        <span class="metric-chip"><i class="pi pi-tag"></i> {{ product.code }}</span>
        <span class="metric-chip"><i class="pi pi-sitemap"></i> {{ product.lineOfBusiness }}</span>
      </div>
    </header>

    <section class="grid-3">
      <Card class="surface-card">
        <template #title>Base rate</template>
        <template #content>
          <h2>{{ currency.format(product.baseRate) }}</h2>
          <p class="section-note">Per $1,000 of insured exposure before modifiers.</p>
        </template>
      </Card>
      <Card class="surface-card">
        <template #title>Binding authority</template>
        <template #content>
          <h2>{{ currency.format(product.bindingAuthority) }}</h2>
          <p class="section-note">Maximum premium authority per delegated underwriter.</p>
        </template>
      </Card>
      <Card class="surface-card">
        <template #title>Target loss ratio</template>
        <template #content>
          <ProgressBar :value="Math.round(product.targetLossRatio * 100)" />
          <p class="section-note">Pricing guardrail used by portfolio management.</p>
        </template>
      </Card>
    </section>

    <section class="grid-2">
      <Card class="surface-card">
        <template #title>Covered regions</template>
        <template #content>
          <div class="product-chips">
            <Chip v-for="region in product.regions" :key="region" :label="region" />
          </div>
        </template>
      </Card>
      <Card class="surface-card">
        <template #title>Key capabilities</template>
        <template #content>
          <ul class="product-features">
            <li v-for="feature in product.features" :key="feature">{{ feature }}</li>
          </ul>
        </template>
      </Card>
    </section>
  </div>
</template>

<style scoped>
.product-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
}

.product-features {
  margin: 0;
  padding-left: 1.25rem;
  color: var(--text-muted);
}
</style>
