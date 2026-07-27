export type QuoteStatus = 'Draft' | 'Priced' | 'Approved' | 'Bound' | 'Declined';
export type ProductStatus = 'Active' | 'Pilot' | 'Paused';
export type CreditTier = 'A' | 'B' | 'C' | 'D';
export type DistributionChannel = 'Broker' | 'Direct' | 'Partner';
export type NotificationSeverity = 'success' | 'info' | 'warn' | 'error' | 'secondary' | 'contrast';

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: 'Platform Admin' | 'Underwriter' | 'Actuary' | 'Operations Lead';
  team: string;
  initials: string;
  lastLogin: string;
}

export interface AuthLoginPayload {
  email: string;
  password: string;
  rememberMe: boolean;
}

export interface AuthTokenBundle {
  accessToken: string;
  refreshToken: string;
  expiresAt: string;
  user?: UserProfile;
}

export interface PersistedAuthState {
  accessToken: string | null;
  refreshToken: string | null;
  expiresAt: string | null;
  user: UserProfile | null;
}

export interface Product {
  id: string;
  code: string;
  name: string;
  lineOfBusiness: string;
  status: ProductStatus;
  version: string;
  description: string;
  baseRate: number;
  targetLossRatio: number;
  maxCoverage: number;
  bindingAuthority: number;
  regions: string[];
  features: string[];
}

export interface PricingFactor {
  label: string;
  value: string;
  impact: number;
}

export interface PricingResponse {
  basePremium: number;
  technicalPremium: number;
  expenses: number;
  taxes: number;
  brokerCommission: number;
  finalPremium: number;
  ratePerThousand: number;
  factors: PricingFactor[];
}

export interface PricingInput {
  productId: string;
  coverageAmount: number;
  termMonths: number;
  priorClaims: number;
  creditTier: CreditTier;
  region: string;
}

export interface QuoteSummary {
  id: string;
  quoteNumber: string;
  insuredName: string;
  insuredEmail: string;
  broker: string;
  channel: DistributionChannel;
  productId: string;
  productName: string;
  status: QuoteStatus;
  premium: number;
  coverageAmount: number;
  createdAt: string;
  effectiveDate: string;
  assignedUnderwriter: string;
  region: string;
  riskScore: number;
}

export interface QuoteDetail extends QuoteSummary {
  termMonths: number;
  annualRevenue: number;
  employeeCount: number;
  priorClaims: number;
  creditTier: CreditTier;
  notes: string;
  pricing: PricingResponse;
}

export interface QuoteUpsertPayload {
  insuredName: string;
  insuredEmail: string;
  broker: string;
  channel: DistributionChannel;
  productId: string;
  status: QuoteStatus;
  coverageAmount: number;
  termMonths: number;
  annualRevenue: number;
  employeeCount: number;
  priorClaims: number;
  creditTier: CreditTier;
  effectiveDate: string;
  region: string;
  assignedUnderwriter: string;
  notes: string;
  pricing?: PricingResponse;
}

export interface QuoteListParams {
  page: number;
  pageSize: number;
  search?: string;
  status?: QuoteStatus | 'All';
  sortBy?: keyof QuoteSummary;
  sortDir?: 'asc' | 'desc';
}

export interface QuoteListResponse {
  items: QuoteSummary[];
  page: number;
  pageSize: number;
  total: number;
}

export interface DashboardKpi {
  title: string;
  value: string;
  delta: string;
  subtitle: string;
  icon: string;
  tone: 'primary' | 'success' | 'warning' | 'danger';
}

export interface RevenuePoint {
  month: string;
  writtenPremium: number;
  earnedPremium: number;
}

export interface ProductMixItem {
  label: string;
  value: number;
}

export interface PipelineQuote {
  quoteNumber: string;
  insuredName: string;
  status: QuoteStatus;
  premium: number;
  region: string;
}

export interface DashboardAlert {
  id: string;
  title: string;
  severity: NotificationSeverity;
  description: string;
  timestamp: string;
}

export interface DashboardOverview {
  kpis: DashboardKpi[];
  revenueSeries: RevenuePoint[];
  productMix: ProductMixItem[];
  pipeline: PipelineQuote[];
  alerts: DashboardAlert[];
}

export interface AnalyticsChannelPerformance {
  channel: DistributionChannel;
  quoteCount: number;
  hitRatio: number;
  averagePremium: number;
  averageCycleDays: number;
}

export interface AnalyticsSnapshot {
  hitRatioSeries: Array<{ month: string; hitRatio: number }>;
  lossRatioByProduct: Array<{ product: string; lossRatio: number }>;
  channelPerformance: AnalyticsChannelPerformance[];
  regionalConversion: Array<{ region: string; conversionRate: number }>;
}

export interface MonitoringService {
  id: string;
  name: string;
  status: 'Healthy' | 'Degraded' | 'Offline';
  latencyMs: number;
  uptimePercentage: number;
  lastCheckedAt: string;
  owner: string;
}

export interface MonitoringAlert {
  id: string;
  service: string;
  severity: NotificationSeverity;
  message: string;
  openedAt: string;
  state: 'Open' | 'Investigating' | 'Mitigated';
}

export interface MonitoringSnapshot {
  quoteLatencySeries: Array<{ interval: string; latencyMs: number }>;
  services: MonitoringService[];
  alerts: MonitoringAlert[];
}

export interface AppNotification {
  id: string;
  severity: NotificationSeverity;
  summary: string;
  detail: string;
  life: number;
  displayed: boolean;
}
