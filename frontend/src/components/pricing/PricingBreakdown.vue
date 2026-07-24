<script setup lang="ts">
import Divider from 'primevue/divider';
import type { PricingResponse } from '@/types/models';

defineProps<{
  pricing: PricingResponse | null;
}>();

const currency = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0
});
</script>

<template>
  <div class="pricing-breakdown surface-card surface-card--padded">
    <div class="pricing-breakdown__header">
      <div>
        <span class="section-note">Pricing model</span>
        <h3>Indicative premium</h3>
      </div>
      <strong>{{ pricing ? currency.format(pricing.finalPremium) : '—' }}</strong>
    </div>

    <template v-if="pricing">
      <div class="pricing-breakdown__metrics">
        <div>
          <span>Base premium</span>
          <strong>{{ currency.format(pricing.basePremium) }}</strong>
        </div>
        <div>
          <span>Technical premium</span>
          <strong>{{ currency.format(pricing.technicalPremium) }}</strong>
        </div>
        <div>
          <span>Rate / $1k</span>
          <strong>{{ currency.format(pricing.ratePerThousand) }}</strong>
        </div>
      </div>

      <Divider />

      <div class="pricing-breakdown__line-items">
        <div class="pricing-breakdown__line-item">
          <span>Expenses</span>
          <strong>{{ currency.format(pricing.expenses) }}</strong>
        </div>
        <div class="pricing-breakdown__line-item">
          <span>Taxes & fees</span>
          <strong>{{ currency.format(pricing.taxes) }}</strong>
        </div>
        <div class="pricing-breakdown__line-item">
          <span>Broker commission</span>
          <strong>{{ currency.format(pricing.brokerCommission) }}</strong>
        </div>
      </div>

      <Divider />

      <div class="pricing-breakdown__factors">
        <div v-for="factor in pricing.factors" :key="factor.label" class="pricing-breakdown__factor">
          <div>
            <strong>{{ factor.label }}</strong>
            <span>{{ factor.value }}</span>
          </div>
          <small>{{ factor.impact.toFixed(2) }}x</small>
        </div>
      </div>
    </template>
    <p v-else class="section-note">
      Run the pricing engine to calculate premium, loadings, and exposure factors.
    </p>
  </div>
</template>

<style scoped>
.pricing-breakdown {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pricing-breakdown__header,
.pricing-breakdown__line-item,
.pricing-breakdown__factor {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.pricing-breakdown__header h3,
.pricing-breakdown__header strong {
  margin: 0;
}

.pricing-breakdown__metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.75rem;
}

.pricing-breakdown__metrics div,
.pricing-breakdown__factor div {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.pricing-breakdown span,
.pricing-breakdown small {
  color: var(--text-muted);
}

.pricing-breakdown__factors {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

@media (max-width: 768px) {
  .pricing-breakdown__metrics {
    grid-template-columns: 1fr;
  }
}
</style>
