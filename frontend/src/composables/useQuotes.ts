import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient
} from '@tanstack/vue-query';
import { computed, toValue, type MaybeRefOrGetter } from 'vue';
import { calculatePricing } from '@/api/pricing';
import { createQuote, deleteQuote, getQuote, listQuotes, updateQuote } from '@/api/quotes';
import type { PricingInput, QuoteListParams, QuoteUpsertPayload } from '@/types/models';

export function useQuotesList(params: MaybeRefOrGetter<QuoteListParams>) {
  return useQuery({
    queryKey: computed(() => ['quotes', { ...toValue(params) }]),
    queryFn: () => listQuotes(toValue(params)),
    placeholderData: keepPreviousData
  });
}

export function useQuote(quoteId: MaybeRefOrGetter<string | undefined>) {
  return useQuery({
    queryKey: computed(() => ['quote', toValue(quoteId)]),
    queryFn: () => getQuote(toValue(quoteId) as string),
    enabled: computed(() => Boolean(toValue(quoteId)))
  });
}

export function useCreateQuote() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: QuoteUpsertPayload) => createQuote(payload),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ['quotes'] }),
        queryClient.invalidateQueries({ queryKey: ['dashboard'] }),
        queryClient.invalidateQueries({ queryKey: ['analytics'] })
      ]);
    }
  });
}

export function useUpdateQuote() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ quoteId, payload }: { quoteId: string; payload: QuoteUpsertPayload }) =>
      updateQuote(quoteId, payload),
    onSuccess: async (_, variables) => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ['quotes'] }),
        queryClient.invalidateQueries({ queryKey: ['quote', variables.quoteId] }),
        queryClient.invalidateQueries({ queryKey: ['dashboard'] }),
        queryClient.invalidateQueries({ queryKey: ['analytics'] })
      ]);
    }
  });
}

export function useDeleteQuote() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (quoteId: string) => deleteQuote(quoteId),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ['quotes'] }),
        queryClient.invalidateQueries({ queryKey: ['dashboard'] }),
        queryClient.invalidateQueries({ queryKey: ['analytics'] })
      ]);
    }
  });
}

export function usePriceQuote() {
  return useMutation({
    mutationFn: (payload: PricingInput) => calculatePricing(payload)
  });
}
