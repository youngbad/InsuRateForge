import { apiClient } from '@/api/client';
import { defaultAnalytics, defaultMonitoring } from '@/api/mock-data';
import { readQuoteStore } from '@/api/quotes';
import type {
  AnalyticsSnapshot,
  DashboardOverview,
  MonitoringSnapshot,
  ProductMixItem,
  RevenuePoint
} from '@/types/models';

const currency = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0
});

function buildRevenueSeries(): RevenuePoint[] {
  return [
    { month: 'Jan', writtenPremium: 810000, earnedPremium: 742000 },
    { month: 'Feb', writtenPremium: 845000, earnedPremium: 768000 },
    { month: 'Mar', writtenPremium: 912000, earnedPremium: 801000 },
    { month: 'Apr', writtenPremium: 954000, earnedPremium: 832000 },
    { month: 'May', writtenPremium: 1018000, earnedPremium: 888000 },
    { month: 'Jun', writtenPremium: 1086000, earnedPremium: 924000 }
  ];
}

function buildProductMix(): ProductMixItem[] {
  const quotes = readQuoteStore();
  const counts = quotes.reduce<Record<string, number>>((accumulator, quote) => {
    accumulator[quote.productName] = (accumulator[quote.productName] ?? 0) + 1;
    return accumulator;
  }, {});

  return Object.entries(counts).map(([label, value]) => ({ label, value }));
}

export async function getDashboardOverview(): Promise<DashboardOverview> {
  try {
    const response = await apiClient.get<DashboardOverview>('/dashboard/overview');
    return response.data;
  } catch {
    const quotes = readQuoteStore();
    const totalPremium = quotes.reduce((sum, quote) => sum + quote.premium, 0);
    const averagePremium = totalPremium / Math.max(quotes.length, 1);
    const approvedQuotes = quotes.filter((quote) => ['Approved', 'Bound'].includes(quote.status)).length;
    const approvalRate = approvedQuotes / Math.max(quotes.length, 1);
    const averageRiskScore = quotes.reduce((sum, quote) => sum + quote.riskScore, 0) / Math.max(quotes.length, 1);

    return {
      kpis: [
        {
          title: 'Written premium',
          value: currency.format(totalPremium),
          delta: '+12.8%',
          subtitle: 'Compared with prior 30 days',
          icon: 'pi pi-dollar',
          tone: 'primary'
        },
        {
          title: 'Average premium',
          value: currency.format(averagePremium),
          delta: '+4.2%',
          subtitle: 'Across active submissions',
          icon: 'pi pi-chart-line',
          tone: 'success'
        },
        {
          title: 'Approval rate',
          value: `${Math.round(approvalRate * 100)}%`,
          delta: '+2 pts',
          subtitle: 'Quote-to-bind trajectory',
          icon: 'pi pi-check-circle',
          tone: 'warning'
        },
        {
          title: 'Average risk score',
          value: `${Math.round(averageRiskScore)}`,
          delta: '-3 pts',
          subtitle: 'Lower score indicates better fit',
          icon: 'pi pi-shield',
          tone: 'danger'
        }
      ],
      revenueSeries: buildRevenueSeries(),
      productMix: buildProductMix(),
      pipeline: quotes
        .slice()
        .sort((left, right) => right.premium - left.premium)
        .slice(0, 5)
        .map((quote) => ({
          quoteNumber: quote.quoteNumber,
          insuredName: quote.insuredName,
          status: quote.status,
          premium: quote.premium,
          region: quote.region
        })),
      alerts: defaultMonitoring.alerts.map((alert) => ({
        id: alert.id,
        title: alert.service,
        severity: alert.severity,
        description: alert.message,
        timestamp: alert.openedAt
      }))
    };
  }
}

export async function getAnalyticsSnapshot(): Promise<AnalyticsSnapshot> {
  try {
    const response = await apiClient.get<AnalyticsSnapshot>('/analytics/overview');
    return response.data;
  } catch {
    return defaultAnalytics;
  }
}

export async function getMonitoringSnapshot(): Promise<MonitoringSnapshot> {
  try {
    const response = await apiClient.get<MonitoringSnapshot>('/monitoring/overview');
    return response.data;
  } catch {
    return defaultMonitoring;
  }
}
