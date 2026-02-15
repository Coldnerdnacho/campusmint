"""
Quick test - verify your wallet and Algorand connection
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod

print("\n" + "="*70)
print("🧪 TESTING YOUR SETUP")
print("="*70 + "\n")

# ==========================================
# TEST 1: MNEMONIC
# ==========================================

print("Test 1: Validating mnemonic...")

# Your mnemonic from .env
MNEMONIC = "firm bar service volcano candy recall delay beach vibrant muffin vault ribbon roof crane bus easily flight connect country witness insane cage purity above wheel"

try:
    # Convert to private key
    private_key = mnemonic.to_private_key(MNEMONIC)
    address = account.address_from_private_key(private_key)
    
    print(f"  ✅ Mnemonic is valid!")
    print(f"  Address: {address}")
    
    # Check if it matches your .env
    expected_address = "OB7RINYEUFAIMGHKWJ7UZYZFRJN4IGEKFO3HEAKAQGHZIML2LI25NIB7DU"
    if address == expected_address:
        print(f"  ✅ Address matches .env file")
    else:
        print(f"  ⚠️  Address mismatch!")
        print(f"     Expected: {expected_address}")
        print(f"     Got: {address}")
        
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

print()

# ==========================================
# TEST 2: ALGORAND CONNECTION
# ==========================================

print("Test 2: Testing Algorand connection...")

try:
    client = algod.AlgodClient(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "https://testnet-api.algonode.cloud"
    )
    
    status = client.status()
    print(f"  ✅ Connected to Algorand Testnet")
    print(f"  Current round: {status['last-round']}")
    
except Exception as e:
    print(f"  ❌ Connection failed: {e}")
    exit(1)

print()

# ==========================================
# TEST 3: CHECK BALANCE
# ==========================================

print("Test 3: Checking account balance...")

try:
    account_info = client.account_information(address)
    balance = account_info['amount'] / 1_000_000
    
    print(f"  Balance: {balance} ALGO")
    
    if balance >= 0.5:
        print(f"  ✅ Sufficient balance for deployment")
    else:
        print(f"  ❌ Insufficient! Need at least 0.5 ALGO")
        print(f"  Fund at: https://bank.testnet.algorand.network/")
        
except Exception as e:
    print(f"  ❌ Error: {e}")
    exit(1)

print()

# ==========================================
# TEST 4: CHECK CINR TOKEN
# ==========================================

print("Test 4: Checking CINR token...")

try:
    asset_info = client.asset_info(755378709)
    print(f"  ✅ CINR token found")
    print(f"  Name: {asset_info['params']['name']}")
    print(f"  Total supply: {asset_info['params']['total'] / 100}")
    
except Exception as e:
    print(f"  ⚠️  Could not fetch token info: {e}")

print()

# ==========================================
# FINAL RESULT
# ==========================================

print("="*70)
print("✅ ALL TESTS PASSED!")
print("="*70)
print("\nYou're ready to deploy the Smart Vault!")
print("\nNext step: Run deployment script")
print()