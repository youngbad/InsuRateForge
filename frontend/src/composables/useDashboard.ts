import { useQuery } from '@tanstack/vue-query';
import { getAnalyticsSnapshot, getDashboardOverview, getMonitoringSnapshot } from '@/api/dashboard';

export function useDashboardOverview() {
  return useQuery({
    queryKey: ['dashboard'],
    queryFn: getDashboardOverview
  });
}

export function useAnalyticsSnapshot() {
  return useQuery({
    queryKey: ['analytics'],
    queryFn: getAnalyticsSnapshot
  });
}

export function useMonitoringSnapshot() {
  return useQuery({
    queryKey: ['monitoring'],
    queryFn: getMonitoringSnapshot
  });
}
