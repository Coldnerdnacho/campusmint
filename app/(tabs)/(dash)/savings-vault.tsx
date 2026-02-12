import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  useWindowDimensions,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { COLORS } from '@/constants/colors';
import { MOCK_VAULT } from '@/constants/mockData';

export default function SavingsVaultScreen() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const ringSize = width * 0.55;
  const timerFontSize = width * 0.15;

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <Pressable style={styles.backButton} onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={20} color={COLORS.white} />
          </Pressable>
          <Text style={styles.headerTitle}>SAVINGS VAULT</Text>
        </View>

        {/* Lock ring */}
        <View style={styles.ringContainer}>
          <View
            style={[
              styles.ring,
              {
                width: ringSize,
                height: ringSize,
                borderRadius: ringSize / 2,
              },
            ]}
          >
            <Ionicons
              name="lock-closed-outline"
              size={24}
              color={COLORS.white}
              style={styles.lockIcon}
            />
            <Text style={styles.lockedLabel}>LOCKED FOR</Text>
            <Text style={[styles.daysNumber, { fontSize: timerFontSize }]}>
              {MOCK_VAULT.daysRemaining}
            </Text>
            <Text style={styles.daysLabel}>DAYS</Text>
          </View>
        </View>

        {/* Info card */}
        <View style={styles.infoCard}>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>LOCKED AMOUNT</Text>
            <Text style={styles.infoValue}>{MOCK_VAULT.lockedAmount}</Text>
          </View>
          <View style={styles.divider} />
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>UNLOCK DATE</Text>
            <Text style={styles.infoValue}>{MOCK_VAULT.unlockDate}</Text>
          </View>
        </View>

        {/* Blockchain note */}
        <View style={styles.noteRow}>
          <Ionicons
            name="checkmark-circle"
            size={18}
            color={COLORS.neonGreen}
            style={{ marginRight: 8 }}
          />
          <Text style={styles.noteText}>
            Funds are secured on the{' '}
            <Text style={styles.noteLink}>Algorand blockchain</Text> and cannot
            be withdrawn until the unlock date.
          </Text>
        </View>

        {/* Withdraw button */}
        <Pressable
          style={[
            styles.withdrawButton,
            MOCK_VAULT.isLocked && styles.withdrawDisabled,
          ]}
          disabled={MOCK_VAULT.isLocked}
        >
          <Text
            style={[
              styles.withdrawText,
              MOCK_VAULT.isLocked && styles.withdrawTextDisabled,
            ]}
          >
            WITHDRAW
          </Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: COLORS.black,
  },
  scrollContent: {
    flexGrow: 1,
    paddingBottom: 40,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: '6%',
    paddingVertical: 16,
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 6,
    borderWidth: 1,
    borderColor: COLORS.borderGray,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitle: {
    color: COLORS.white,
    fontSize: 16,
    fontWeight: '900',
    letterSpacing: 2,
    marginLeft: 14,
  },
  ringContainer: {
    alignItems: 'center',
    marginTop: '8%',
    marginBottom: '8%',
  },
  ring: {
    borderWidth: 2,
    borderColor: COLORS.white,
    justifyContent: 'center',
    alignItems: 'center',
  },
  lockIcon: {
    marginBottom: 8,
  },
  lockedLabel: {
    color: COLORS.lightGray,
    fontSize: 11,
    fontWeight: '600',
    letterSpacing: 1.5,
  },
  daysNumber: {
    color: COLORS.white,
    fontWeight: '900',
    marginVertical: 2,
  },
  daysLabel: {
    color: COLORS.white,
    fontSize: 14,
    fontWeight: '700',
    letterSpacing: 3,
  },
  infoCard: {
    marginHorizontal: '6%',
    borderWidth: 1,
    borderColor: COLORS.borderGray,
    borderRadius: 4,
    paddingVertical: 18,
    paddingHorizontal: 20,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
  },
  infoLabel: {
    color: COLORS.lightGray,
    fontSize: 12,
    fontWeight: '600',
    letterSpacing: 1,
  },
  infoValue: {
    color: COLORS.white,
    fontSize: 18,
    fontWeight: '900',
  },
  divider: {
    height: StyleSheet.hairlineWidth,
    backgroundColor: COLORS.borderGray,
  },
  noteRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    paddingHorizontal: '6%',
    marginTop: 24,
    marginBottom: 30,
  },
  noteText: {
    flex: 1,
    color: COLORS.lightGray,
    fontSize: 12,
    lineHeight: 18,
  },
  noteLink: {
    textDecorationLine: 'underline',
    color: COLORS.white,
  },
  withdrawButton: {
    marginHorizontal: '6%',
    borderWidth: 1.5,
    borderColor: COLORS.white,
    borderRadius: 4,
    paddingVertical: 16,
    alignItems: 'center',
  },
  withdrawDisabled: {
    borderColor: COLORS.borderGray,
    opacity: 0.4,
  },
  withdrawText: {
    color: COLORS.white,
    fontSize: 14,
    fontWeight: '800',
    letterSpacing: 3,
  },
  withdrawTextDisabled: {
    color: COLORS.lightGray,
  },
});
