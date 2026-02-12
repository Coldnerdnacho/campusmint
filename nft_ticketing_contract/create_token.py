from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import AssetConfigTxn, wait_for_confirmation
import os
from dotenv import load_dotenv

load_dotenv()

def create_campus_token():
    # Connect to Algorand
    algod_client = algod.AlgodClient(
        os.getenv("ALGOD_TOKEN"),
        os.getenv("ALGOD_SERVER")
    )
    
    # Get creator account
    wallet_mnemonic = os.getenv("CREATOR_MNEMONIC")
    private_key = mnemonic.to_private_key(wallet_mnemonic)
    creator_address = account.address_from_private_key(private_key)
    
    print("\n" + "="*70)
    print("🪙 CREATING CAMPUS INR TOKEN")
    print("="*70)
    print(f"\nCreator Address: {creator_address}")
    
    # Check balance first
    account_info = algod_client.account_info(creator_address)
    balance = account_info['amount'] / 1_000_000
    print(f"Balance: {balance} ALGO")
    
    if balance < 0.5:
        print("❌ Insufficient balance. Need at least 0.5 ALGO")
        return
    
    # Get suggested params
    params = algod_client.suggested_params()
    
    # Create ASA transaction
    print("\n⏳ Creating token transaction...")
    txn = AssetConfigTxn(
        sender=creator_address,
        sp=params,
        total=100000000,  # 1 million tokens with 2 decimals = ₹10,00,000
        default_frozen=False,
        unit_name="CINR",
        asset_name="Campus INR",
        manager=creator_address,
        reserve=creator_address,
        freeze=creator_address,  # Set to creator, not None
        clawback=creator_address,  # Set to creator, not None
        url="https://campusmint.xyz",
        decimals=2,
        strict_empty_address_check=False  # Allow empty addresses
    )
    
    # Sign transaction
    print("🔐 Signing transaction...")
    signed_txn = txn.sign(private_key)
    
    # Send transaction
    print("📤 Sending to blockchain...")
    tx_id = algod_client.send_transaction(signed_txn)
    print(f"Transaction ID: {tx_id}")
    
    # Wait for confirmation
    print("⏳ Waiting for confirmation (this takes ~4 seconds)...")
    confirmed_txn = wait_for_confirmation(algod_client, tx_id, 4)
    
    # Get asset ID
    asset_id = confirmed_txn['asset-index']
    
    print("\n" + "="*70)
    print("🎉 SUCCESS! CAMPUS INR TOKEN CREATED!")
    print("="*70)
    print(f"\n📋 TOKEN DETAILS:")
    print(f"   Asset ID: {asset_id}")
    print(f"   Token Name: Campus INR")
    print(f"   Unit Name: CINR")
    print(f"   Total Supply: 1,000,000 CINR (₹10,00,000)")
    print(f"   Decimals: 2 (₹1 = 100 units)")
    print(f"\n🔗 View on AlgoExplorer:")
    print(f"   https://testnet.algoexplorer.io/asset/{asset_id}")
    print("\n" + "="*70)
    
    # Save asset ID to file
    with open("ASSET_ID.txt", "w") as f:
        f.write(f"Campus INR Token - CampusMint Hackathon\n")
        f.write(f"="*50 + "\n\n")
        f.write(f"Asset ID: {asset_id}\n\n")
        f.write(f"AlgoExplorer Link:\n")
        f.write(f"https://testnet.algoexplorer.io/asset/{asset_id}\n\n")
        f.write(f"Token Details:\n")
        f.write(f"- Name: Campus INR\n")
        f.write(f"- Unit: CINR\n")
        f.write(f"- Supply: 1,000,000 CINR\n")
        f.write(f"- Decimals: 2\n\n")
        f.write(f"="*50 + "\n")
        f.write(f"🚨 SHARE THIS ASSET ID WITH YOUR ENTIRE TEAM!\n")
    
    # Save to .env as well
    with open(".env", "a") as f:
        f.write(f"\nASSET_ID={asset_id}\n")
    
    print("\n💾 Asset ID saved to:")
    print("   - ASSET_ID.txt")
    print("   - .env file")
    print("\n🚨 IMPORTANT: Share this Asset ID with Person 1, 3, and 4!")
    print("="*70 + "\n")
    
    return asset_id

if __name__ == "__main__":
    try:
        asset_id = create_campus_token()
        print("✅ Day 1 Task Complete: Campus INR token created!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure .env file exists (run setup_env.py)")
        print("2. Check your balance (should have ~9.99 ALGO)")
        print("3. Verify internet connection")
        print("4. Try again in a few seconds\n")