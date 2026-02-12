from algosdk import account, mnemonic

print("🔐 CREATING NEW ALGORAND TESTNET WALLET")
print("="*70)

# Generate new account
private_key, address = account.generate_account()

# Get the mnemonic (25 words)
wallet_mnemonic = mnemonic.from_private_key(private_key)

print("\n✅ NEW WALLET CREATED!")
print("="*70)

print("\n📋 SAVE THESE DETAILS:\n")
print("Address:")
print(address)
print("\nPrivate Key:")
print(private_key)
print("\n25-Word Mnemonic:")
print(wallet_mnemonic)

print("\n" + "="*70)
print("⚠️  IMPORTANT:")
print("1. Copy the Address and Private Key to your .env file")
print("2. Save the 25-word mnemonic somewhere safe (for recovery)")
print("3. Fund this address with testnet ALGO")
print("="*70)

# Also save to file
with open("NEW_WALLET_INFO.txt", "w") as f:
    f.write("ALGORAND TESTNET WALLET\n")
    f.write("="*70 + "\n\n")
    f.write(f"Address:\n{address}\n\n")
    f.write(f"Private Key:\n{private_key}\n\n")
    f.write(f"25-Word Mnemonic:\n{wallet_mnemonic}\n\n")
    f.write("="*70 + "\n")
    f.write("⚠️ TESTNET ONLY - DO NOT USE FOR REAL FUNDS\n")

print("\n💾 Wallet info also saved to: NEW_WALLET_INFO.txt")