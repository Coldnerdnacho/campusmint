import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '@/constants/colors';

interface Props {
  raised: number;
  goal: number;
}

export default function TreasuryProgressBar({ raised, goal }: Props) {
  const ratio = Math.min(raised / goal, 1);
  const percent = Math.round(ratio * 100);

  return (
    <View style={styles.container}>
      <View style={styles.labelRow}>
        <Text style={styles.label}>TARGET</Text>
        <Text style={styles.label}>{percent}% COMPLETE</Text>
      </View>
      <View style={styles.trackOuter}>
        <View style={[styles.trackFill, { width: `${percent}%` }]}>
          <View style={styles.thumb} />
        </View>
      </View>
      <View style={styles.amountRow}>
        <Text style={styles.amountText}>₹{raised.toLocaleString('en-IN')}</Text>
        <Text style={styles.divider}>/</Text>
        <Text style={styles.amountText}>
          ₹{goal.toLocaleString('en-IN')} raised
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: 20,
    width: '100%',
  },
  labelRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  label: {
    color: COLORS.lightGray,
    fontSize: 11,
    fontWeight: '600',
    letterSpacing: 1,
  },
  trackOuter: {
    height: 14,
    borderRadius: 2,
    backgroundColor: COLORS.mediumGray,
    overflow: 'hidden',
    justifyContent: 'center',
  },
  trackFill: {
    height: '100%',
    backgroundColor: COLORS.white,
    borderRadius: 2,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-end',
  },
  thumb: {
    width: 12,
    height: 12,
    borderRadius: 2,
    borderWidth: 1.5,
    borderColor: COLORS.white,
    backgroundColor: COLORS.black,
    marginRight: 1,
  },
  amountRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  divider: {
    color: COLORS.lightGray,
    fontSize: 14,
  },
  amountText: {
    color: COLORS.white,
    fontSize: 13,
    fontWeight: '600',
  },
});
