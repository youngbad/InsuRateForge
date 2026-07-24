import { useQuery } from '@tanstack/vue-query';
import { computed, toValue, type MaybeRefOrGetter } from 'vue';
import { getProduct, listProducts } from '@/api/products';

export function useProducts() {
  return useQuery({
    queryKey: ['products'],
    queryFn: listProducts
  });
}

export function useProduct(productId: MaybeRefOrGetter<string | undefined>) {
  return useQuery({
    queryKey: computed(() => ['product', toValue(productId)]),
    queryFn: () => getProduct(toValue(productId) as string),
    enabled: computed(() => Boolean(toValue(productId)))
  });
}
