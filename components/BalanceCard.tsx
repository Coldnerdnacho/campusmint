import React from 'react';
import { View, Text, StyleSheet, useWindowDimensions } from 'react-native';
import { COLORS } from '@/constants/colors';
import { MOCK_BALANCE } from '@/constants/mockData';

export default function BalanceCard() {
  const { width } = useWindowDimensions();
  const balanceFontSize = width * 0.13;

  return (
    <View style={styles.container}>
      <Text style={styles.label}>TOTAL BALANCE</Text>
      <View style={styles.balanceRow}>
        <Text style={[styles.currency, { fontSize: balanceFontSize * 0.5 }]}>
          {MOCK_BALANCE.currency}
        </Text>
        <Text style={[styles.amount, { fontSize: balanceFontSize }]}>
          {MOCK_BALANCE.amount}
        </Text>
        <Text style={[styles.decimals, { fontSize: balanceFontSize * 0.35 }]}>
          .{MOCK_BALANCE.decimals}
        </Text>
      </View>
      <View style={styles.statusRow}>
        <View style={styles.statusDot} />
        <Text style={styles.statusText}>{MOCK_BALANCE.statusLabel}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: '6%',
    paddingTop: '6%',
    paddingBottom: '4%',
  },
  label: {
    color: COLORS.black,
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 1.5,
    marginBottom: 4,
  },
  balanceRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
  },
  currency: {
    color: COLORS.neonGreen,
    fontWeight: '900',
    marginBottom: 4,
    marginRight: 2,
  },
  amount: {
    color: COLORS.black,
    fontWeight: '900',
    lineHeight: undefined,
  },
  decimals: {
    color: COLORS.black,
    fontWeight: '700',
    marginBottom: 6,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 6,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: COLORS.neonGreen,
    marginRight: 6,
  },
  statusText: {
    color: COLORS.black,
    fontSize: 10,
    fontWeight: '600',
    letterSpacing: 1.2,
  },
});
