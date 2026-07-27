import type {
  AnalyticsSnapshot,
  CreditTier,
  MonitoringSnapshot,
  PricingInput,
  PricingResponse,
  Product,
  QuoteDetail,
  QuoteStatus,
  UserProfile
} from '@/types/models';

const currency = (value: number) => Number(value.toFixed(2));

const creditFactorMap: Record<CreditTier, number> = {
  A: 0.92,
  B: 1,
  C: 1.11,
  D: 1.24
};

const regionFactorMap: Record<string, number> = {
  Midwest: 0.97,
  Northeast: 1.04,
  Southeast: 1.08,
  Southwest: 1.06,
  West: 1.02
};

export const defaultUsers: UserProfile[] = [
  {
    id: 'user-admin',
    name: 'Amelia Grant',
    email: 'admin@insurateforge.com',
    role: 'Platform Admin',
    team: 'Platform Operations',
    initials: 'AG',
    lastLogin: '2026-07-24T14:42:00.000Z'
  },
  {
    id: 'user-underwriter',
    name: 'Jordan Patel',
    email: 'jordan.patel@insurateforge.com',
    role: 'Underwriter',
    team: 'Commercial Lines',
    initials: 'JP',
    lastLogin: '2026-07-24T13:18:00.000Z'
  },
  {
    id: 'user-actuary',
    name: 'Nina Brooks',
    email: 'nina.brooks@insurateforge.com',
    role: 'Actuary',
    team: 'Pricing Science',
    initials: 'NB',
    lastLogin: '2026-07-24T12:05:00.000Z'
  },
  {
    id: 'user-ops',
    name: 'Marcus Lee',
    email: 'marcus.lee@insurateforge.com',
    role: 'Operations Lead',
    team: 'Shared Services',
    initials: 'ML',
    lastLogin: '2026-07-24T15:07:00.000Z'
  }
];

export const defaultProducts: Product[] = [
  {
    id: 'prod-cyber-flex',
    code: 'CYB-FLEX',
    name: 'Cyber Flex',
    lineOfBusiness: 'Cyber Liability',
    status: 'Active',
    version: '2026.3',
    description: 'Mid-market cyber coverage with incident response and ransomware expense modules.',
    baseRate: 4.85,
    targetLossRatio: 0.53,
    maxCoverage: 10000000,
    bindingAuthority: 5000000,
    regions: ['Midwest', 'Northeast', 'Southeast', 'West'],
    features: ['Primary + excess layers', 'Panel breach counsel', 'Vendor dependency scoring']
  },
  {
    id: 'prod-property-midmarket',
    code: 'PROP-MID',
    name: 'Property MidMarket',
    lineOfBusiness: 'Commercial Property',
    status: 'Active',
    version: '2026.2',
    description: 'Property package tuned for regional portfolios with CAT corridor modifiers.',
    baseRate: 3.95,
    targetLossRatio: 0.58,
    maxCoverage: 25000000,
    bindingAuthority: 8000000,
    regions: ['Midwest', 'Northeast', 'Southwest', 'West'],
    features: ['Scheduled values upload', 'CAT scenario overlays', 'Coinsurance diagnostics']
  },
  {
    id: 'prod-workers-comp-plus',
    code: 'WC-PLUS',
    name: 'Workers Comp Plus',
    lineOfBusiness: 'Workers Compensation',
    status: 'Pilot',
    version: '2026.1',
    description: 'Workers comp digital bind flow with wage inflation and class code benchmarking.',
    baseRate: 5.1,
    targetLossRatio: 0.61,
    maxCoverage: 5000000,
    bindingAuthority: 2500000,
    regions: ['Midwest', 'Southeast', 'Southwest'],
    features: ['Class code validation', 'Payroll drift monitoring', 'Risk engineering referrals']
  },
  {
    id: 'prod-auto-fleet',
    code: 'AUTO-FLT',
    name: 'Fleet Guard',
    lineOfBusiness: 'Commercial Auto',
    status: 'Active',
    version: '2026.4',
    description: 'Fleet portfolio pricing with telematics ingestion and segment-based rate plans.',
    baseRate: 4.35,
    targetLossRatio: 0.56,
    maxCoverage: 15000000,
    bindingAuthority: 4000000,
    regions: ['Northeast', 'Southeast', 'Southwest', 'West'],
    features: ['Telematics scoring', 'Accident trend overlays', 'Jurisdiction surcharges']
  }
];

export function computePricingSnapshot(input: PricingInput, product?: Product): PricingResponse {
  const selectedProduct = product ?? defaultProducts.find((item) => item.id === input.productId);
  const baseRate = selectedProduct?.baseRate ?? 4.25;
  const exposureUnits = input.coverageAmount / 1000;
  const termFactor = Math.max(input.termMonths / 12, 0.5);
  const claimFactor = 1 + input.priorClaims * 0.08;
  const creditFactor = creditFactorMap[input.creditTier] ?? 1;
  const regionFactor = regionFactorMap[input.region] ?? 1.01;
  const basePremium = exposureUnits * baseRate * termFactor;
  const technicalPremium = basePremium * claimFactor * creditFactor * regionFactor;
  const expenses = technicalPremium * 0.14;
  const taxes = technicalPremium * 0.0325;
  const brokerCommission = technicalPremium * 0.1;
  const finalPremium = technicalPremium + expenses + taxes + brokerCommission;

  return {
    basePremium: currency(basePremium),
    technicalPremium: currency(technicalPremium),
    expenses: currency(expenses),
    taxes: currency(taxes),
    brokerCommission: currency(brokerCommission),
    finalPremium: currency(finalPremium),
    ratePerThousand: currency(finalPremium / Math.max(exposureUnits, 1)),
    factors: [
      { label: 'Term factor', value: `${input.termMonths} months`, impact: currency(termFactor) },
      { label: 'Claims experience', value: `${input.priorClaims} prior claims`, impact: currency(claimFactor) },
      { label: 'Credit tier', value: input.creditTier, impact: currency(creditFactor) },
      { label: 'Territory', value: input.region, impact: currency(regionFactor) }
    ]
  };
}

const makeQuote = (
  id: string,
  quoteNumber: string,
  insuredName: string,
  insuredEmail: string,
  broker: string,
  channel: QuoteDetail['channel'],
  productId: string,
  status: QuoteStatus,
  coverageAmount: number,
  termMonths: number,
  priorClaims: number,
  creditTier: CreditTier,
  region: string,
  assignedUnderwriter: string,
  effectiveDate: string,
  annualRevenue: number,
  employeeCount: number,
  notes: string,
  createdAt: string,
  riskScore: number
): QuoteDetail => {
  const product = defaultProducts.find((item) => item.id === productId) ?? defaultProducts[0];
  const pricing = computePricingSnapshot(
    {
      productId,
      coverageAmount,
      termMonths,
      priorClaims,
      creditTier,
      region
    },
    product
  );

  return {
    id,
    quoteNumber,
    insuredName,
    insuredEmail,
    broker,
    channel,
    productId,
    productName: product.name,
    status,
    premium: pricing.finalPremium,
    coverageAmount,
    createdAt,
    effectiveDate,
    assignedUnderwriter,
    region,
    riskScore,
    termMonths,
    annualRevenue,
    employeeCount,
    priorClaims,
    creditTier,
    notes,
    pricing
  };
};

export const seedQuotes: QuoteDetail[] = [
  makeQuote(
    'quote-1001',
    'Q-2026-1001',
    'Northwind Logistics',
    'risk@northwindlogistics.com',
    'Horizon Risk Partners',
    'Broker',
    'prod-auto-fleet',
    'Approved',
    3200000,
    12,
    1,
    'B',
    'Southeast',
    'Jordan Patel',
    '2026-08-01',
    24000000,
    180,
    'Fleet growth plan submitted with telematics participation.',
    '2026-07-10T09:30:00.000Z',
    71
  ),
  makeQuote(
    'quote-1002',
    'Q-2026-1002',
    'Lattice Health Systems',
    'ops@latticehealth.io',
    'Apex Specialty',
    'Partner',
    'prod-cyber-flex',
    'Priced',
    5000000,
    12,
    0,
    'A',
    'Northeast',
    'Jordan Patel',
    '2026-08-15',
    54000000,
    420,
    'SOC 2 and endpoint security controls validated.',
    '2026-07-12T11:10:00.000Z',
    64
  ),
  makeQuote(
    'quote-1003',
    'Q-2026-1003',
    'Juniper Commerce Group',
    'finance@junipercommerce.com',
    'Beacon Brokerage',
    'Broker',
    'prod-property-midmarket',
    'Bound',
    9000000,
    12,
    2,
    'B',
    'Midwest',
    'Marcus Lee',
    '2026-09-01',
    115000000,
    860,
    'Multi-location schedule includes cold storage occupancy.',
    '2026-07-05T08:45:00.000Z',
    79
  ),
  makeQuote(
    'quote-1004',
    'Q-2026-1004',
    'Everstream Manufacturing',
    'captiverisk@everstreammfg.com',
    'Direct Bind Desk',
    'Direct',
    'prod-workers-comp-plus',
    'Draft',
    1800000,
    12,
    1,
    'C',
    'Southwest',
    'Nina Brooks',
    '2026-09-10',
    68000000,
    510,
    'Awaiting updated payroll audit before bind recommendation.',
    '2026-07-18T10:20:00.000Z',
    74
  ),
  makeQuote(
    'quote-1005',
    'Q-2026-1005',
    'Summit Retail Labs',
    'treasury@summitretail.ai',
    'Horizon Risk Partners',
    'Broker',
    'prod-cyber-flex',
    'Approved',
    2500000,
    12,
    0,
    'A',
    'West',
    'Amelia Grant',
    '2026-08-20',
    33000000,
    240,
    'Strong MFA posture and vendor dependency report attached.',
    '2026-07-09T13:40:00.000Z',
    58
  ),
  makeQuote(
    'quote-1006',
    'Q-2026-1006',
    'Atlas Civil Group',
    'insurance@atlascivil.net',
    'Beacon Brokerage',
    'Broker',
    'prod-workers-comp-plus',
    'Declined',
    2200000,
    12,
    4,
    'D',
    'Southeast',
    'Marcus Lee',
    '2026-08-05',
    47000000,
    320,
    'Loss history exceeded pilot product appetite threshold.',
    '2026-07-03T16:55:00.000Z',
    91
  ),
  makeQuote(
    'quote-1007',
    'Q-2026-1007',
    'Blue Harbor Hospitality',
    'controller@blueharborhotels.com',
    'Apex Specialty',
    'Partner',
    'prod-property-midmarket',
    'Priced',
    12000000,
    12,
    1,
    'B',
    'West',
    'Jordan Patel',
    '2026-10-01',
    82000000,
    610,
    'CAT model attachment shows coastal property buffering plan.',
    '2026-07-17T12:05:00.000Z',
    76
  ),
  makeQuote(
    'quote-1008',
    'Q-2026-1008',
    'Copper Oak Energy',
    'risk@copperoakenergy.com',
    'Direct Bind Desk',
    'Direct',
    'prod-auto-fleet',
    'Draft',
    4100000,
    12,
    2,
    'C',
    'Southwest',
    'Amelia Grant',
    '2026-09-15',
    128000000,
    290,
    'Driver turnover is trending higher than portfolio median.',
    '2026-07-21T09:05:00.000Z',
    83
  )
];

export const defaultAnalytics: AnalyticsSnapshot = {
  hitRatioSeries: [
    { month: 'Jan', hitRatio: 0.28 },
    { month: 'Feb', hitRatio: 0.31 },
    { month: 'Mar', hitRatio: 0.36 },
    { month: 'Apr', hitRatio: 0.34 },
    { month: 'May', hitRatio: 0.38 },
    { month: 'Jun', hitRatio: 0.42 }
  ],
  lossRatioByProduct: [
    { product: 'Cyber Flex', lossRatio: 0.49 },
    { product: 'Property MidMarket', lossRatio: 0.57 },
    { product: 'Workers Comp Plus', lossRatio: 0.63 },
    { product: 'Fleet Guard', lossRatio: 0.55 }
  ],
  channelPerformance: [
    { channel: 'Broker', quoteCount: 412, hitRatio: 0.41, averagePremium: 42280, averageCycleDays: 6.1 },
    { channel: 'Partner', quoteCount: 188, hitRatio: 0.47, averagePremium: 50940, averageCycleDays: 4.8 },
    { channel: 'Direct', quoteCount: 133, hitRatio: 0.34, averagePremium: 31210, averageCycleDays: 3.9 }
  ],
  regionalConversion: [
    { region: 'Northeast', conversionRate: 0.44 },
    { region: 'Southeast', conversionRate: 0.36 },
    { region: 'Midwest', conversionRate: 0.48 },
    { region: 'Southwest', conversionRate: 0.33 },
    { region: 'West', conversionRate: 0.39 }
  ]
};

export const defaultMonitoring: MonitoringSnapshot = {
  quoteLatencySeries: [
    { interval: '08:00', latencyMs: 240 },
    { interval: '10:00', latencyMs: 228 },
    { interval: '12:00', latencyMs: 252 },
    { interval: '14:00', latencyMs: 308 },
    { interval: '16:00', latencyMs: 261 },
    { interval: '18:00', latencyMs: 239 }
  ],
  services: [
    {
      id: 'svc-pricing',
      name: 'Pricing API',
      status: 'Healthy',
      latencyMs: 228,
      uptimePercentage: 99.98,
      lastCheckedAt: '2026-07-24T18:30:00.000Z',
      owner: 'Pricing Science'
    },
    {
      id: 'svc-rating',
      name: 'Rating Engine',
      status: 'Healthy',
      latencyMs: 176,
      uptimePercentage: 99.95,
      lastCheckedAt: '2026-07-24T18:30:00.000Z',
      owner: 'Platform Core'
    },
    {
      id: 'svc-portfolio',
      name: 'Portfolio Warehouse',
      status: 'Degraded',
      latencyMs: 412,
      uptimePercentage: 99.41,
      lastCheckedAt: '2026-07-24T18:29:00.000Z',
      owner: 'Data Platform'
    },
    {
      id: 'svc-auth',
      name: 'Identity Gateway',
      status: 'Healthy',
      latencyMs: 96,
      uptimePercentage: 100,
      lastCheckedAt: '2026-07-24T18:29:00.000Z',
      owner: 'Platform Operations'
    }
  ],
  alerts: [
    {
      id: 'alert-1',
      service: 'Portfolio Warehouse',
      severity: 'warn',
      message: 'Warehouse refresh is 11 minutes behind the SLA threshold.',
      openedAt: '2026-07-24T18:06:00.000Z',
      state: 'Investigating'
    },
    {
      id: 'alert-2',
      service: 'Pricing API',
      severity: 'info',
      message: 'Auto-scaling added one replica due to quote surge in the Southeast region.',
      openedAt: '2026-07-24T17:42:00.000Z',
      state: 'Open'
    },
    {
      id: 'alert-3',
      service: 'Identity Gateway',
      severity: 'success',
      message: 'Refresh token error rate returned to baseline after edge cache purge.',
      openedAt: '2026-07-24T16:55:00.000Z',
      state: 'Mitigated'
    }
  ]
};
