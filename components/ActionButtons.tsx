import React from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '@/constants/colors';

export default function ActionButtons() {
  return (
    <View style={styles.container}>
      <Pressable style={styles.button}>
        <Ionicons name="arrow-forward" size={28} color={COLORS.white} style={{ transform: [{ rotate: '-45deg' }] }} />
        <Text style={styles.label}>SEND</Text>
      </Pressable>
      <View style={styles.spacer} />
      <Pressable style={styles.button}>
        <Ionicons name="arrow-back" size={28} color={COLORS.white} style={{ transform: [{ rotate: '45deg' }] }} />
        <Text style={styles.label}>REQUEST</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    paddingHorizontal: '6%',
    marginTop: '4%',
    marginBottom: '2%',
  },
  button: {
    flex: 1,
    backgroundColor: COLORS.black,
    borderRadius: 4,
    paddingVertical: '8%',
    paddingHorizontal: '6%',
    justifyContent: 'flex-end',
    aspectRatio: 1.3,
  },
  spacer: {
    width: '4%',
  },
  label: {
    color: COLORS.white,
    fontSize: 14,
    fontWeight: '800',
    letterSpacing: 2,
    marginTop: 10,
  },
});
