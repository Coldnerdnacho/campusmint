import React from 'react';
import { ScrollView, View, Text, StyleSheet, Pressable } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '@/constants/colors';
import BalanceCard from '@/components/BalanceCard';
import ActionButtons from '@/components/ActionButtons';
import InstrumentList from '@/components/InstrumentList';

export default function DashScreen() {
  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.logoRow}>
          <View style={styles.logoSquare} />
          <Text style={styles.logoText}>CAMPUSMINT</Text>
        </View>
        <View style={styles.avatar}>
          <Ionicons name="person-circle-outline" size={32} color={COLORS.black} />
        </View>
      </View>

      {/* Blue accent line */}
      <View style={styles.accentLine} />

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <BalanceCard />
        <InstrumentList />
        <ActionButtons />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: COLORS.white,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: '6%',
    paddingVertical: 12,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoSquare: {
    width: 16,
    height: 16,
    backgroundColor: COLORS.neonGreen,
    borderRadius: 2,
    marginRight: 8,
  },
  logoText: {
    color: COLORS.black,
    fontSize: 16,
    fontWeight: '900',
    letterSpacing: 2,
  },
  avatar: {
    width: 34,
    height: 34,
    borderRadius: 17,
    overflow: 'hidden',
    justifyContent: 'center',
    alignItems: 'center',
  },
  accentLine: {
    height: 3,
    backgroundColor: '#2979FF',
    width: '2%',
    marginLeft: '1%',
  },
  scroll: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: 30,
  },
});
