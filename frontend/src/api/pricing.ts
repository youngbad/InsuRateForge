import { apiClient } from '@/api/client';
import { computePricingSnapshot, defaultProducts } from '@/api/mock-data';
import type { PricingInput, PricingResponse } from '@/types/models';

export async function calculatePricing(payload: PricingInput): Promise<PricingResponse> {
  try {
    const response = await apiClient.post<PricingResponse>('/pricing/quote', payload);
    return response.data;
  } catch {
    const product = defaultProducts.find((item) => item.id === payload.productId);
    return computePricingSnapshot(payload, product);
  }
}
