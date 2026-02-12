export const MOCK_BALANCE = {
  amount: '12,450',
  decimals: '00',
  currency: '₹',
  statusLabel: 'CINR LIVE STATUS',
};

export const MOCK_INSTRUMENTS = [
  {
    id: 'savings-vault',
    icon: 'lock-closed-outline' as const,
    title: 'Savings Vault',
    subtitle: 'HIGH YIELD • 4.5% APY',
    route: '/savings-vault' as const,
  },
  {
    id: 'event-tickets',
    icon: 'ticket-outline' as const,
    title: 'Event Tickets',
    subtitle: 'ACTIVE: 2 • UPCOMING',
    route: null,
  },
  {
    id: 'ngo-pool',
    icon: 'globe-outline' as const,
    title: 'NGO Pool',
    subtitle: 'MONTHLY CONTRIBUTION',
    route: '/club-treasury' as const,
  },
];

export const MOCK_VAULT = {
  isLocked: true,
  daysRemaining: 42,
  lockedAmount: '₹15,000',
  unlockDate: 'MAY 2026',
  blockchainNote:
    'Funds are secured on the Algorand blockchain and cannot be withdrawn until the unlock date.',
};

export const MOCK_TREASURY = {
  eventName: 'TECH\nFEST\n2026',
  poolId: 'FUNDRAISING POOL #8821',
  raised: 50000,
  goal: 100000,
  contributors: [
    { address: '0x4f...2a', amount: 5000 },
    { address: '0x9c...1b', amount: 2500 },
    { address: '0xa1...88', amount: 10000 },
    { address: '0xbb...4c', amount: 1200 },
    { address: '0xde...99', amount: 7500 },
  ],
};
