import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '@/constants/colors';

export default function LogsScreen() {
  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.title}>TRANSACTION LOGS</Text>
      </View>
      <View style={styles.empty}>
        <Ionicons name="time-outline" size={48} color={COLORS.lightGray} />
        <Text style={styles.emptyText}>No transactions yet</Text>
        <Text style={styles.emptySubtext}>
          Your transaction history will appear here
        </Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: COLORS.white,
  },
  header: {
    paddingHorizontal: '6%',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#EEE',
  },
  title: {
    color: COLORS.black,
    fontSize: 16,
    fontWeight: '900',
    letterSpacing: 2,
  },
  empty: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: '10%',
  },
  emptyText: {
    color: COLORS.black,
    fontSize: 16,
    fontWeight: '700',
    marginTop: 16,
  },
  emptySubtext: {
    color: COLORS.lightGray,
    fontSize: 13,
    marginTop: 6,
    textAlign: 'center',
  },
});
