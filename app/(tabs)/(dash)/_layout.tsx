import { Stack } from 'expo-router';

export default function DashLayout() {
  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="index" />
      <Stack.Screen name="savings-vault" />
      <Stack.Screen name="club-treasury" />
    </Stack>
  );
}
