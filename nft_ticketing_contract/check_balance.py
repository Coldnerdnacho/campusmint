from algosdk.v2client import algod

# Testnet connection
algod_address = "https://testnet-api.algonode.cloud"
algod_token = "a" * 64  # Testnet uses dummy token
algod_client = algod.AlgodClient(algod_token, algod_address)

# Read wallet address from file
with open("NEW_WALLET_INFO.txt", "r") as f:
    lines = f.readlines()

# Find the address (comes after "Address:" line)
address = None
for i, line in enumerate(lines):
    if "Address:" in line:
        # Next non-empty line is the address
        address = lines[i + 1].strip()
        break

if not address:
    print("❌ Could not find address in NEW_WALLET_INFO.txt")
    print("\nManually check the file:")
    print("Open NEW_WALLET_INFO.txt and copy the address\n")
    exit()

print("\n" + "="*70)
print("🔍 CHECKING WALLET BALANCE")
print("="*70)
print(f"\n📍 Address: {address}\n")

# Get account info
try:
    account_info = algod_client.account_info(address)
    balance = account_info['amount'] / 1_000_000  # Convert microAlgos to ALGO
    
    print(f"💰 Current Balance: {balance} ALGO")
    
    if balance >= 9:
        print("\n✅ Transfer successful! Ready to build.")
        print("="*70 + "\n")
    else:
        print(f"\n⏳ Balance is low ({balance} ALGO)")
        print("Please transfer from Pera Wallet:")
        print("1. Open Pera Wallet")
        print(f"2. Send 9.5 ALGO to: {address}")
        print("3. Wait ~5 seconds")
        print("4. Run this script again")
        print("="*70 + "\n")
        
except Exception as e:
    print(f"❌ Error: {e}\n")
    print("This means either:")
    print("1. You haven't transferred ALGO yet (account doesn't exist)")
    print("2. There's a connection issue\n")
    print("To transfer:")
    print(f"Address: {address}")
    print("="*70 + "\n")