import { apiClient } from '@/api/client';
import { defaultProducts } from '@/api/mock-data';
import type { Product } from '@/types/models';

export async function listProducts(): Promise<Product[]> {
  try {
    const response = await apiClient.get<Product[]>('/products');
    return response.data;
  } catch {
    return defaultProducts;
  }
}

export async function getProduct(productId: string): Promise<Product> {
  try {
    const response = await apiClient.get<Product>(`/products/${productId}`);
    return response.data;
  } catch {
    const matched = defaultProducts.find((item) => item.id === productId);

    if (!matched) {
      throw new Error(`Product ${productId} not found`);
    }

    return matched;
  }
}
