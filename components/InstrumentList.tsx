import React from 'react';
import { View, Text, StyleSheet, Pressable, FlatList } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { COLORS } from '@/constants/colors';
import { MOCK_INSTRUMENTS } from '@/constants/mockData';

export default function InstrumentList() {
  const router = useRouter();

  const handlePress = (route: string | null) => {
    if (route) {
      router.push(route as any);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>ACTIVE INSTRUMENTS</Text>
        <View style={styles.badge}>
          <Text style={styles.badgeText}>
            {String(MOCK_INSTRUMENTS.length).padStart(2, '0')}
          </Text>
        </View>
      </View>

      {MOCK_INSTRUMENTS.map((item) => (
        <Pressable
          key={item.id}
          style={styles.row}
          onPress={() => handlePress(item.route)}
        >
          <View style={styles.iconBox}>
            <Ionicons name={item.icon as any} size={22} color={COLORS.black} />
          </View>
          <View style={styles.textCol}>
            <Text style={styles.rowTitle}>{item.title}</Text>
            <Text style={styles.rowSubtitle}>{item.subtitle}</Text>
          </View>
          <Ionicons name="chevron-forward" size={20} color={COLORS.black} />
        </Pressable>
      ))}

      <Pressable style={styles.addButton}>
        <Text style={styles.addLabel}>+ ADD INSTRUMENT</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: '6%',
    marginTop: '2%',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 16,
    borderBottomWidth: 2,
    borderBottomColor: COLORS.black,
    paddingBottom: 10,
  },
  title: {
    color: COLORS.black,
    fontSize: 16,
    fontWeight: '900',
    letterSpacing: 1,
  },
  badge: {
    backgroundColor: COLORS.black,
    borderRadius: 4,
    paddingHorizontal: 8,
    paddingVertical: 3,
  },
  badgeText: {
    color: COLORS.white,
    fontSize: 12,
    fontWeight: '800',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 16,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#DDD',
  },
  iconBox: {
    width: 40,
    height: 40,
    borderRadius: 8,
    borderWidth: 1.5,
    borderColor: COLORS.black,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 14,
  },
  textCol: {
    flex: 1,
  },
  rowTitle: {
    color: COLORS.black,
    fontSize: 15,
    fontWeight: '800',
  },
  rowSubtitle: {
    color: COLORS.lightGray,
    fontSize: 10,
    fontWeight: '600',
    letterSpacing: 1,
    marginTop: 2,
  },
  addButton: {
    borderWidth: 1.5,
    borderColor: COLORS.black,
    borderRadius: 4,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 16,
  },
  addLabel: {
    color: COLORS.black,
    fontSize: 12,
    fontWeight: '800',
    letterSpacing: 2,
  },
});
