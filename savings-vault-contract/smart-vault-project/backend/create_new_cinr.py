"""
Create NEW CINR Token
Use this when you lost access to the old token creator wallet
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import (
    AssetConfigTxn,
    wait_for_confirmation
)

# ==========================================
# CONFIGURATION
# ==========================================

# Your current wallet
YOUR_MNEMONIC = "firm bar service volcano candy recall delay beach vibrant muffin vault ribbon roof crane bus easily flight connect country witness insane cage purity above wheel"

# Algorand Connection
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ALGOD_SERVER = "https://testnet-api.algonode.cloud"


def create_new_cinr_token():
    """Create a brand new CINR token"""
    
    print("\n" + "="*70)
    print("🪙 CREATING NEW CINR TOKEN")
    print("="*70 + "\n")
    
    print("ℹ️  Since you lost access to the old wallet, we're creating")
    print("   a fresh CINR token with your current wallet.\n")
    
    # Connect to Algorand
    client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_SERVER)
    
    # Get your account
    private_key = mnemonic.to_private_key(YOUR_MNEMONIC)
    creator_address = account.address_from_private_key(private_key)
    
    print(f"Creator (You): {creator_address}\n")
    
    # Check balance
    try:
        account_info = client.account_info(creator_address)
    except AttributeError:
        account_info = client.account_information(creator_address)
    
    balance = account_info['amount'] / 1_000_000
    print(f"Your ALGO balance: {balance} ALGO\n")
    
    if balance < 0.2:
        print("❌ ERROR: Insufficient balance!")
        print(f"   You need at least 0.2 ALGO to create a token")
        print(f"\n   Fund your wallet:")
        print(f"   1. Go to: https://bank.testnet.algorand.network/")
        print(f"   2. Paste: {creator_address}")
        print(f"   3. Get testnet ALGO\n")
        return
    
    # ==========================================
    # CREATE TOKEN
    # ==========================================
    
    print("Creating CINR token...")
    print("  Token specifications:")
    print("  - Name: Campus INR")
    print("  - Unit: CINR")
    print("  - Total: 1,000,000 (10 lakh)")
    print("  - Decimals: 2 (₹1 = 100 units)")
    print("  - Symbol: ₹\n")
    
    params = client.suggested_params()
    
    # Create token transaction
    txn = AssetConfigTxn(
        sender=creator_address,
        sp=params,
        total=100000000,        # 1 million * 100 (2 decimals)
        default_frozen=False,
        unit_name="CINR",
        asset_name="Campus INR",
        manager=creator_address,
        reserve=creator_address,
        freeze=creator_address,
        clawback=creator_address,
        url="https://campusmint.io",
        decimals=2
    )
    
    # Sign transaction
    signed_txn = txn.sign(private_key)
    
    # Send transaction
    print("📤 Sending to blockchain...")
    tx_id = client.send_transaction(signed_txn)
    
    print(f"   Transaction ID: {tx_id}")
    print(f"   Waiting for confirmation (4 seconds)...")
    
    # Wait for confirmation
    confirmed_txn = wait_for_confirmation(client, tx_id, 4)
    
    # Get asset ID
    asset_id = confirmed_txn['asset-index']
    
    print("\n" + "="*70)
    print("🎉 SUCCESS! NEW CINR TOKEN CREATED!")
    print("="*70)
    print(f"\n📍 NEW Asset ID: {asset_id}")
    print(f"\n🔗 View on AlgoExplorer:")
    print(f"   https://testnet.algoexplorer.io/asset/{asset_id}")
    print("\n" + "="*70)
    
    # ==========================================
    # UPDATE INSTRUCTIONS
    # ==========================================
    
    print("\n💾 IMPORTANT: Update your configuration!\n")
    
    print("1. Update .env file:")
    print(f"   Change: ASSET_ID=755378709")
    print(f"   To:     ASSET_ID={asset_id}")
    print()
    
    print("2. Your wallet now has 1,000,000 CINR tokens!")
    print(f"   You can use them for vault testing\n")
    
    print("3. Next steps:")
    print(f"   a. Update .env with new ASSET_ID={asset_id}")
    print(f"   b. Run: python vault_service_fixed.py")
    print(f"   c. Choose option 1 (Opt-in to vault)")
    print(f"   d. Choose option 2 (Deposit to vault)")
    print()
    
    print("="*70)
    print("✅ All set! Fresh CINR token ready to use!")
    print("="*70 + "\n")
    
    return asset_id


if __name__ == "__main__":
    print("\n⚠️  This will create a BRAND NEW CINR token")
    print("The old token (755378709) will remain, but you can't access it.\n")
    
    response = input("Create new CINR token? (y/n): ")
    
    if response.lower() == 'y':
        try:
            asset_id = create_new_cinr_token()
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            print()
    else:
        print("\nCancelled. No token created.\n")