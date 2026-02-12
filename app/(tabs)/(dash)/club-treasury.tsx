import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  ScrollView,
  useWindowDimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { COLORS } from '@/constants/colors';
import { MOCK_TREASURY } from '@/constants/mockData';
import TreasuryProgressBar from '@/components/TreasuryProgressBar';

export default function ClubTreasuryScreen() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const titleFontSize = width * 0.11;

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      {/* Fixed header */}
      <View style={styles.header}>
        <Pressable onPress={() => router.back()}>
          <Ionicons name="chevron-back" size={24} color={COLORS.white} />
        </Pressable>
        <Text style={styles.headerTitle}>CLUB TREASURY</Text>
        <View style={{ width: 24 }} />
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        {/* Event banner */}
        <View style={styles.bannerContainer}>
          <View style={styles.bannerPlaceholder}>
            <Ionicons name="people" size={48} color={COLORS.lightGray} />
            <Text style={styles.bannerOverlay}>TECH FEST 2026</Text>
          </View>
        </View>

        {/* Event title */}
        <View style={styles.contentPadding}>
          <Text style={[styles.eventTitle, { fontSize: titleFontSize }]}>
            {MOCK_TREASURY.eventName}
          </Text>
          <View style={styles.poolIdRow}>
            <View style={styles.poolIdBar} />
            <Text style={styles.poolIdText}>{MOCK_TREASURY.poolId}</Text>
          </View>

          {/* Progress */}
          <TreasuryProgressBar
            raised={MOCK_TREASURY.raised}
            goal={MOCK_TREASURY.goal}
          />

          {/* Contributors */}
          <View style={styles.contribSection}>
            <Text style={styles.contribHeader}>RECENT CONTRIBUTORS</Text>
            <View style={styles.contribDivider} />
            {MOCK_TREASURY.contributors.map((c, i) => (
              <View key={i} style={styles.contribRow}>
                <Text style={styles.contribAddress}>{c.address}</Text>
                <View style={styles.contribLine} />
                <Text style={styles.contribAmount}>
                  ₹{c.amount.toLocaleString('en-IN')}
                </Text>
              </View>
            ))}
          </View>

          <Pressable style={styles.viewAllButton}>
            <Text style={styles.viewAllText}>VIEW ALL TRANSACTIONS</Text>
          </Pressable>
        </View>
      </ScrollView>

      {/* Sticky CTA */}
      <Pressable style={styles.ctaButton}>
        <Text style={styles.ctaText}>CONTRIBUTE NOW</Text>
        <Ionicons
          name="arrow-forward"
          size={18}
          color={COLORS.black}
          style={{ marginLeft: 8 }}
        />
      </Pressable>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: COLORS.black,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: '5%',
    paddingVertical: 14,
  },
  headerTitle: {
    color: COLORS.white,
    fontSize: 13,
    fontWeight: '800',
    letterSpacing: 2,
  },
  scrollContent: {
    flexGrow: 1,
    paddingBottom: 20,
  },
  bannerContainer: {
    paddingHorizontal: '8%',
    marginBottom: 16,
  },
  bannerPlaceholder: {
    width: '100%',
    aspectRatio: 2.2,
    backgroundColor: COLORS.darkGray,
    borderRadius: 4,
    justifyContent: 'center',
    alignItems: 'center',
  },
  bannerOverlay: {
    color: COLORS.lightGray,
    fontSize: 10,
    fontWeight: '600',
    letterSpacing: 1,
    marginTop: 6,
  },
  contentPadding: {
    paddingHorizontal: '8%',
  },
  eventTitle: {
    color: COLORS.white,
    fontWeight: '900',
    lineHeight: undefined,
    letterSpacing: -1,
  },
  poolIdRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  poolIdBar: {
    width: 3,
    height: 16,
    backgroundColor: COLORS.white,
    marginRight: 10,
  },
  poolIdText: {
    color: COLORS.lightGray,
    fontSize: 12,
    fontWeight: '600',
    letterSpacing: 1.5,
  },
  contribSection: {
    marginTop: 30,
  },
  contribHeader: {
    color: COLORS.white,
    fontSize: 13,
    fontWeight: '800',
    letterSpacing: 1,
    marginBottom: 10,
  },
  contribDivider: {
    height: StyleSheet.hairlineWidth,
    backgroundColor: COLORS.borderGray,
    marginBottom: 6,
  },
  contribRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
  },
  contribAddress: {
    color: COLORS.white,
    fontSize: 13,
    fontWeight: '500',
    fontFamily: undefined, // mono if available
  },
  contribLine: {
    flex: 1,
    height: StyleSheet.hairlineWidth,
    backgroundColor: COLORS.borderGray,
    marginHorizontal: 12,
  },
  contribAmount: {
    color: COLORS.white,
    fontSize: 13,
    fontWeight: '700',
  },
  viewAllButton: {
    alignItems: 'center',
    marginTop: 16,
    marginBottom: 10,
  },
  viewAllText: {
    color: COLORS.lightGray,
    fontSize: 11,
    fontWeight: '600',
    letterSpacing: 1.5,
    textDecorationLine: 'underline',
  },
  ctaButton: {
    backgroundColor: COLORS.white,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 18,
    marginHorizontal: '6%',
    marginBottom: 14,
    borderRadius: 4,
  },
  ctaText: {
    color: COLORS.black,
    fontSize: 14,
    fontWeight: '900',
    letterSpacing: 2,
  },
});
