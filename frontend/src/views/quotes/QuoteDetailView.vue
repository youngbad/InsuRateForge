<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Button from 'primevue/button';
import Card from 'primevue/card';
import DatePicker from 'primevue/datepicker';
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import Select from 'primevue/select';
import Textarea from 'primevue/textarea';
import StatusBadge from '@/components/common/StatusBadge.vue';
import PricingBreakdown from '@/components/pricing/PricingBreakdown.vue';
import { useProducts } from '@/composables/useProducts';
import { useCreateQuote, usePriceQuote, useQuote, useUpdateQuote } from '@/composables/useQuotes';
import { useNotificationsStore } from '@/stores/notifications';
import type { CreditTier, DistributionChannel, QuoteStatus, QuoteUpsertPayload } from '@/types/models';

interface QuoteFormState {
  insuredName: string;
  insuredEmail: string;
  broker: string;
  channel: DistributionChannel;
  productId: string;
  status: QuoteStatus;
  coverageAmount: number | null;
  termMonths: number | null;
  annualRevenue: number | null;
  employeeCount: number | null;
  priorClaims: number | null;
  creditTier: CreditTier;
  effectiveDate: Date | null;
  region: string;
  assignedUnderwriter: string;
  notes: string;
}

const route = useRoute();
const router = useRouter();
const notifications = useNotificationsStore();
const quoteId = computed(() => route.params.id as string | undefined);
const isCreateMode = computed(() => !quoteId.value);
const productsQuery = useProducts();
const quoteQuery = useQuote(quoteId);
const createQuoteMutation = useCreateQuote();
const updateQuoteMutation = useUpdateQuote();
const pricingMutation = usePriceQuote();

const form = reactive<QuoteFormState>({
  insuredName: '',
  insuredEmail: '',
  broker: '',
  channel: 'Broker',
  productId: '',
  status: 'Draft',
  coverageAmount: 1000000,
  termMonths: 12,
  annualRevenue: 5000000,
  employeeCount: 50,
  priorClaims: 0,
  creditTier: 'B',
  effectiveDate: new Date(),
  region: 'Northeast',
  assignedUnderwriter: 'Jordan Patel',
  notes: ''
});

const productOptions = computed(() => productsQuery.data.value ?? []);
const statusOptions: QuoteStatus[] = ['Draft', 'Priced', 'Approved', 'Bound', 'Declined'];
const channelOptions: DistributionChannel[] = ['Broker', 'Partner', 'Direct'];
const creditOptions: CreditTier[] = ['A', 'B', 'C', 'D'];
const regionOptions = ['Midwest', 'Northeast', 'Southeast', 'Southwest', 'West'];

const validationErrors = computed<Record<string, string>>(() => ({
  insuredName: form.insuredName.trim() ? '' : 'Insured name is required.',
  insuredEmail: /^\S+@\S+\.\S+$/.test(form.insuredEmail) ? '' : 'Valid insured email required.',
  broker: form.broker.trim() ? '' : 'Broker or submission source is required.',
  productId: form.productId ? '' : 'Select a product.',
  coverageAmount: form.coverageAmount && form.coverageAmount > 0 ? '' : 'Coverage amount must be greater than zero.',
  termMonths: form.termMonths && form.termMonths > 0 ? '' : 'Term must be at least one month.'
}));
const submitted = ref(false);
const isFormValid = computed(() => Object.values(validationErrors.value).every((value) => !value));

watch(
  () => quoteQuery.data.value,
  (quote) => {
    if (!quote) {
      return;
    }

    form.insuredName = quote.insuredName;
    form.insuredEmail = quote.insuredEmail;
    form.broker = quote.broker;
    form.channel = quote.channel;
    form.productId = quote.productId;
    form.status = quote.status;
    form.coverageAmount = quote.coverageAmount;
    form.termMonths = quote.termMonths;
    form.annualRevenue = quote.annualRevenue;
    form.employeeCount = quote.employeeCount;
    form.priorClaims = quote.priorClaims;
    form.creditTier = quote.creditTier;
    form.effectiveDate = new Date(quote.effectiveDate);
    form.region = quote.region;
    form.assignedUnderwriter = quote.assignedUnderwriter;
    form.notes = quote.notes;
  },
  { immediate: true }
);

const currentPricing = computed(() => pricingMutation.data.value ?? quoteQuery.data.value?.pricing ?? null);

const buildPayload = (): QuoteUpsertPayload => ({
  insuredName: form.insuredName.trim(),
  insuredEmail: form.insuredEmail.trim(),
  broker: form.broker.trim(),
  channel: form.channel,
  productId: form.productId,
  status: form.status,
  coverageAmount: Number(form.coverageAmount),
  termMonths: Number(form.termMonths),
  annualRevenue: Number(form.annualRevenue ?? 0),
  employeeCount: Number(form.employeeCount ?? 0),
  priorClaims: Number(form.priorClaims ?? 0),
  creditTier: form.creditTier,
  effectiveDate: (form.effectiveDate ?? new Date()).toISOString(),
  region: form.region,
  assignedUnderwriter: form.assignedUnderwriter.trim(),
  notes: form.notes.trim(),
  pricing: currentPricing.value ?? undefined
});

async function runPricing() {
  submitted.value = true;
  if (!isFormValid.value) {
    return;
  }

  await pricingMutation.mutateAsync({
    productId: form.productId,
    coverageAmount: Number(form.coverageAmount),
    termMonths: Number(form.termMonths),
    priorClaims: Number(form.priorClaims ?? 0),
    creditTier: form.creditTier,
    region: form.region
  });

  notifications.info('Pricing refreshed', 'Indicative premium recalculated from the latest inputs.');
}

async function save(statusOverride?: QuoteStatus) {
  submitted.value = true;
  if (!isFormValid.value) {
    return;
  }

  if (!currentPricing.value) {
    await runPricing();
  }

  const payload = buildPayload();
  if (statusOverride) {
    payload.status = statusOverride;
  }

  if (isCreateMode.value) {
    const created = await createQuoteMutation.mutateAsync(payload);
    notifications.success('Quote created', `${created.quoteNumber} has been added to the submission queue.`);
    await router.replace({ name: 'quote-detail', params: { id: created.id } });
    return;
  }

  const updated = await updateQuoteMutation.mutateAsync({ quoteId: quoteId.value as string, payload });
  notifications.success('Quote updated', `${updated.quoteNumber} has been saved.`);
}
</script>

<template>
  <div class="page-shell">
    <header class="page-header">
      <div class="page-header__title">
        <h1>{{ isCreateMode ? 'Create quote' : quoteQuery.data.value?.quoteNumber ?? 'Quote detail' }}</h1>
        <p>
          Capture insured exposure, adjust pricing inputs, and promote the submission through
          underwriting review.
        </p>
      </div>
      <div class="metric-strip" v-if="quoteQuery.data.value && !isCreateMode">
        <span class="metric-chip"><i class="pi pi-briefcase"></i> {{ quoteQuery.data.value.productName }}</span>
        <span class="metric-chip"><i class="pi pi-map-marker"></i> {{ quoteQuery.data.value.region }}</span>
        <StatusBadge :label="quoteQuery.data.value.status" />
      </div>
    </header>

    <div class="quote-detail-grid">
      <Card class="surface-card">
        <template #content>
          <form class="quote-form" @submit.prevent="save()">
            <section>
              <h3>Submission details</h3>
              <div class="quote-form__grid quote-form__grid--2">
                <div class="quote-form__field">
                  <label for="insured-name">Insured name</label>
                  <InputText id="insured-name" v-model="form.insuredName" fluid />
                  <small v-if="submitted && validationErrors.insuredName" class="quote-form__error">
                    {{ validationErrors.insuredName }}
                  </small>
                </div>
                <div class="quote-form__field">
                  <label for="insured-email">Insured email</label>
                  <InputText id="insured-email" v-model="form.insuredEmail" fluid />
                  <small v-if="submitted && validationErrors.insuredEmail" class="quote-form__error">
                    {{ validationErrors.insuredEmail }}
                  </small>
                </div>
                <div class="quote-form__field">
                  <label for="broker">Broker / source</label>
                  <InputText id="broker" v-model="form.broker" fluid />
                  <small v-if="submitted && validationErrors.broker" class="quote-form__error">
                    {{ validationErrors.broker }}
                  </small>
                </div>
                <div class="quote-form__field">
                  <label for="channel">Distribution channel</label>
                  <Select id="channel" v-model="form.channel" :options="channelOptions" fluid />
                </div>
                <div class="quote-form__field">
                  <label for="product">Product</label>
                  <Select
                    id="product"
                    v-model="form.productId"
                    option-label="name"
                    option-value="id"
                    :options="productOptions"
                    fluid
                  />
                  <small v-if="submitted && validationErrors.productId" class="quote-form__error">
                    {{ validationErrors.productId }}
                  </small>
                </div>
                <div class="quote-form__field">
                  <label for="status">Quote status</label>
                  <Select id="status" v-model="form.status" :options="statusOptions" fluid />
                </div>
              </div>
            </section>

            <section>
              <h3>Exposure inputs</h3>
              <div class="quote-form__grid quote-form__grid--3">
                <div class="quote-form__field">
                  <label for="coverage">Coverage amount</label>
                  <InputNumber
                    id="coverage"
                    v-model="form.coverageAmount"
                    mode="currency"
                    currency="USD"
                    locale="en-US"
                    fluid
                  />
                  <small v-if="submitted && validationErrors.coverageAmount" class="quote-form__error">
                    {{ validationErrors.coverageAmount }}
                  </small>
                </div>
                <div class="quote-form__field">
                  <label for="term">Term (months)</label>
                  <InputNumber id="term" v-model="form.termMonths" :min="1" fluid />
                  <small v-if="submitted && validationErrors.termMonths" class="quote-form__error">
                    {{ validationErrors.termMonths }}
                  </small>
                </div>
                <div class="quote-form__field">
                  <label for="effective-date">Effective date</label>
                  <DatePicker id="effective-date" v-model="form.effectiveDate" showIcon fluid />
                </div>
                <div class="quote-form__field">
                  <label for="annual-revenue">Annual revenue</label>
                  <InputNumber
                    id="annual-revenue"
                    v-model="form.annualRevenue"
                    mode="currency"
                    currency="USD"
                    locale="en-US"
                    fluid
                  />
                </div>
                <div class="quote-form__field">
                  <label for="employees">Employee count</label>
                  <InputNumber id="employees" v-model="form.employeeCount" :min="1" fluid />
                </div>
                <div class="quote-form__field">
                  <label for="prior-claims">Prior claims</label>
                  <InputNumber id="prior-claims" v-model="form.priorClaims" :min="0" fluid />
                </div>
                <div class="quote-form__field">
                  <label for="credit-tier">Credit tier</label>
                  <Select id="credit-tier" v-model="form.creditTier" :options="creditOptions" fluid />
                </div>
                <div class="quote-form__field">
                  <label for="region">Region</label>
                  <Select id="region" v-model="form.region" :options="regionOptions" fluid />
                </div>
                <div class="quote-form__field">
                  <label for="underwriter">Assigned underwriter</label>
                  <InputText id="underwriter" v-model="form.assignedUnderwriter" fluid />
                </div>
              </div>
            </section>

            <section>
              <h3>Underwriting notes</h3>
              <div class="quote-form__field">
                <label for="notes">Notes</label>
                <Textarea id="notes" v-model="form.notes" autoResize rows="5" fluid />
              </div>
            </section>

            <div class="quote-form__actions">
              <Button
                type="button"
                label="Run pricing"
                icon="pi pi-calculator"
                severity="secondary"
                outlined
                :loading="pricingMutation.isPending.value"
                @click="runPricing"
              />
              <Button
                type="button"
                label="Save draft"
                severity="secondary"
                :loading="createQuoteMutation.isPending.value || updateQuoteMutation.isPending.value"
                @click="save('Draft')"
              />
              <Button
                type="submit"
                label="Save changes"
                icon="pi pi-save"
                :loading="createQuoteMutation.isPending.value || updateQuoteMutation.isPending.value"
              />
            </div>
          </form>
        </template>
      </Card>

      <PricingBreakdown :pricing="currentPricing" />
    </div>
  </div>
</template>

<style scoped>
.quote-detail-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.65fr) minmax(320px, 0.9fr);
  gap: 1.5rem;
  align-items: start;
}

.quote-form {
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
}

.quote-form section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.quote-form h3 {
  margin: 0;
}

.quote-form__grid {
  display: grid;
  gap: 1rem;
}

.quote-form__grid--2 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.quote-form__grid--3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.quote-form__field {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.quote-form__error {
  color: #dc2626;
}

.quote-form__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.75rem;
}

@media (max-width: 1200px) {
  .quote-detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .quote-form__grid--2,
  .quote-form__grid--3 {
    grid-template-columns: 1fr;
  }
}
</style>
