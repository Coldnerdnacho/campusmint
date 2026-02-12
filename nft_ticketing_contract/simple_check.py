from algosdk.v2client import algod

# PASTE YOUR ADDRESS HERE (from NEW_WALLET_INFO.txt)
YOUR_ADDRESS = "LPM55WTEFFP6UGM7JHKMIFC5GXHJOFQLDKOFSAPQRMHRCAHYLQCHQJBY6I"

# Connect to testnet
algod_client = algod.AlgodClient(
    "a" * 64,
    "https://testnet-api.algonode.cloud"
)

print(f"\n📍 Checking: {YOUR_ADDRESS}\n")

try:
    account_info = algod_client.account_info(YOUR_ADDRESS)
    balance = account_info['amount'] / 1_000_000
    print(f"💰 Balance: {balance} ALGO\n")
    
    if balance >= 9:
        print("✅ Funded! Ready to create token.\n")
    else:
        print("⏳ Transfer ALGO from Pera Wallet to this address.\n")
except Exception as e:
    print("❌ Account not found. Transfer ALGO first.\n")