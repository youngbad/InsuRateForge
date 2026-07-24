import { apiClient } from '@/api/client';
import { computePricingSnapshot, defaultProducts, seedQuotes } from '@/api/mock-data';
import type {
  PricingInput,
  QuoteDetail,
  QuoteListParams,
  QuoteListResponse,
  QuoteSummary,
  QuoteUpsertPayload
} from '@/types/models';

let quoteCache: QuoteDetail[] | null = null;

export function readQuoteStore(): QuoteDetail[] {
  if (!quoteCache) {
    quoteCache = seedQuotes.map((quote) => ({ ...quote, pricing: { ...quote.pricing } }));
  }
  return quoteCache;
}

function writeQuoteStore(quotes: QuoteDetail[]): void {
  quoteCache = quotes;
}

const toSummary = (quote: QuoteDetail): QuoteSummary => ({
  id: quote.id,
  quoteNumber: quote.quoteNumber,
  insuredName: quote.insuredName,
  insuredEmail: quote.insuredEmail,
  broker: quote.broker,
  channel: quote.channel,
  productId: quote.productId,
  productName: quote.productName,
  status: quote.status,
  premium: quote.premium,
  coverageAmount: quote.coverageAmount,
  createdAt: quote.createdAt,
  effectiveDate: quote.effectiveDate,
  assignedUnderwriter: quote.assignedUnderwriter,
  region: quote.region,
  riskScore: quote.riskScore
});

function filterAndPaginate(quotes: QuoteDetail[], params: QuoteListParams): QuoteListResponse {
  const normalizedSearch = params.search?.trim().toLowerCase() ?? '';
  const filtered = quotes.filter((quote) => {
    const matchesSearch =
      !normalizedSearch ||
      [quote.quoteNumber, quote.insuredName, quote.productName, quote.broker, quote.region]
        .join(' ')
        .toLowerCase()
        .includes(normalizedSearch);
    const matchesStatus = !params.status || params.status === 'All' || quote.status === params.status;

    return matchesSearch && matchesStatus;
  });

  const sortBy = params.sortBy ?? 'createdAt';
  const sortDir = params.sortDir ?? 'desc';

  filtered.sort((left, right) => {
    const leftValue = left[sortBy];
    const rightValue = right[sortBy];

    if (typeof leftValue === 'number' && typeof rightValue === 'number') {
      return sortDir === 'asc' ? leftValue - rightValue : rightValue - leftValue;
    }

    return sortDir === 'asc'
      ? String(leftValue).localeCompare(String(rightValue))
      : String(rightValue).localeCompare(String(leftValue));
  });

  const page = Math.max(params.page, 1);
  const pageSize = Math.max(params.pageSize, 1);
  const startIndex = (page - 1) * pageSize;
  const pageItems = filtered.slice(startIndex, startIndex + pageSize).map(toSummary);

  return {
    items: pageItems,
    total: filtered.length,
    page,
    pageSize
  };
}

export async function listQuotes(params: QuoteListParams): Promise<QuoteListResponse> {
  try {
    const response = await apiClient.get<QuoteListResponse>('/quotes', { params });
    return response.data;
  } catch {
    return filterAndPaginate(readQuoteStore(), params);
  }
}

export async function getQuote(quoteId: string): Promise<QuoteDetail> {
  try {
    const response = await apiClient.get<QuoteDetail>(`/quotes/${quoteId}`);
    return response.data;
  } catch {
    const quote = readQuoteStore().find((item) => item.id === quoteId);

    if (!quote) {
      throw new Error(`Quote ${quoteId} not found`);
    }

    return quote;
  }
}

function buildRiskScore(input: PricingInput): number {
  return Math.min(95, Math.round(42 + input.priorClaims * 9 + input.coverageAmount / 300000 + input.termMonths));
}

export async function createQuote(payload: QuoteUpsertPayload): Promise<QuoteDetail> {
  try {
    const response = await apiClient.post<QuoteDetail>('/quotes', payload);
    return response.data;
  } catch {
    const quotes = readQuoteStore();
    const product = defaultProducts.find((item) => item.id === payload.productId) ?? defaultProducts[0];
    const pricing =
      payload.pricing ??
      computePricingSnapshot(
        {
          productId: payload.productId,
          coverageAmount: payload.coverageAmount,
          termMonths: payload.termMonths,
          priorClaims: payload.priorClaims,
          creditTier: payload.creditTier,
          region: payload.region
        },
        product
      );
    const created: QuoteDetail = {
      id: globalThis.crypto?.randomUUID?.() ?? `quote-${Date.now()}`,
      quoteNumber: `Q-2026-${String(quotes.length + 1001).padStart(4, '0')}`,
      insuredName: payload.insuredName,
      insuredEmail: payload.insuredEmail,
      broker: payload.broker,
      channel: payload.channel,
      productId: payload.productId,
      productName: product.name,
      status: payload.status,
      premium: pricing.finalPremium,
      coverageAmount: payload.coverageAmount,
      createdAt: new Date().toISOString(),
      effectiveDate: payload.effectiveDate,
      assignedUnderwriter: payload.assignedUnderwriter,
      region: payload.region,
      riskScore: buildRiskScore({
        productId: payload.productId,
        coverageAmount: payload.coverageAmount,
        termMonths: payload.termMonths,
        priorClaims: payload.priorClaims,
        creditTier: payload.creditTier,
        region: payload.region
      }),
      termMonths: payload.termMonths,
      annualRevenue: payload.annualRevenue,
      employeeCount: payload.employeeCount,
      priorClaims: payload.priorClaims,
      creditTier: payload.creditTier,
      notes: payload.notes,
      pricing
    };

    writeQuoteStore([created, ...quotes]);
    return created;
  }
}

export async function updateQuote(quoteId: string, payload: QuoteUpsertPayload): Promise<QuoteDetail> {
  try {
    const response = await apiClient.put<QuoteDetail>(`/quotes/${quoteId}`, payload);
    return response.data;
  } catch {
    const quotes = readQuoteStore();
    const existing = quotes.find((item) => item.id === quoteId);

    if (!existing) {
      throw new Error(`Quote ${quoteId} not found`);
    }

    const product = defaultProducts.find((item) => item.id === payload.productId) ?? defaultProducts[0];
    const pricing =
      payload.pricing ??
      computePricingSnapshot(
        {
          productId: payload.productId,
          coverageAmount: payload.coverageAmount,
          termMonths: payload.termMonths,
          priorClaims: payload.priorClaims,
          creditTier: payload.creditTier,
          region: payload.region
        },
        product
      );
    const updated: QuoteDetail = {
      ...existing,
      ...payload,
      productName: product.name,
      premium: pricing.finalPremium,
      riskScore: buildRiskScore({
        productId: payload.productId,
        coverageAmount: payload.coverageAmount,
        termMonths: payload.termMonths,
        priorClaims: payload.priorClaims,
        creditTier: payload.creditTier,
        region: payload.region
      }),
      pricing
    };

    writeQuoteStore(quotes.map((item) => (item.id === quoteId ? updated : item)));
    return updated;
  }
}

export async function deleteQuote(quoteId: string): Promise<void> {
  try {
    await apiClient.delete(`/quotes/${quoteId}`);
  } catch {
    const quotes = readQuoteStore();
    writeQuoteStore(quotes.filter((item) => item.id !== quoteId));
  }
}
