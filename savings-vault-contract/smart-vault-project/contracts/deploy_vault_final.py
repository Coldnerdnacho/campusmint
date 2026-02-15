"""
Deploy Smart Vault to Algorand Testnet
FIXED VERSION - uses correct SDK methods
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import (
    ApplicationCreateTxn,
    StateSchema,
    OnComplete,
    wait_for_confirmation
)
import base64

# ==========================================
# CONFIGURATION (from your .env file)
# ==========================================

CREATOR_MNEMONIC = "firm bar service volcano candy recall delay beach vibrant muffin vault ribbon roof crane bus easily flight connect country witness insane cage purity above wheel"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ALGOD_SERVER = "https://testnet-api.algonode.cloud"


def deploy_vault():
    """Deploy vault contract to testnet"""
    
    print("\n" + "="*70)
    print("🚀 DEPLOYING SMART VAULT TO ALGORAND TESTNET")
    print("="*70 + "\n")
    
    # ==========================================
    # STEP 1: CONNECT TO ALGORAND
    # ==========================================
    
    print("📡 Connecting to Algorand testnet...")
    
    client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_SERVER)
    
    status = client.status()
    print(f"✅ Connected!")
    print(f"   Network: Testnet")
    print(f"   Current round: {status['last-round']}\n")
    
    # ==========================================
    # STEP 2: GET CREATOR ACCOUNT
    # ==========================================
    
    print("👤 Loading creator account...")
    
    creator_private_key = mnemonic.to_private_key(CREATOR_MNEMONIC)
    creator_address = account.address_from_private_key(creator_private_key)
    
    print(f"   Address: {creator_address}")
    
    # Check balance - try both method names for compatibility
    try:
        account_info = client.account_info(creator_address)
    except AttributeError:
        account_info = client.account_information(creator_address)
    
    balance = account_info['amount'] / 1_000_000
    print(f"   Balance: {balance} ALGO\n")
    
    if balance < 0.5:
        print("❌ ERROR: Insufficient balance!")
        print("   You need at least 0.5 ALGO to deploy")
        print(f"\n   Fund your wallet:")
        print(f"   1. Go to: https://bank.testnet.algorand.network/")
        print(f"   2. Paste: {creator_address}")
        print(f"   3. Click 'Dispense'")
        print()
        return
    
    # ==========================================
    # STEP 3: READ AND COMPILE CONTRACT
    # ==========================================
    
    print("📄 Reading contract files...")
    
    try:
        # Read TEAL files
        with open("vault_approval.teal", "r") as f:
            approval_teal = f.read()
            print("   ✅ vault_approval.teal")
        
        with open("vault_clear.teal", "r") as f:
            clear_teal = f.read()
            print("   ✅ vault_clear.teal")
    
    except FileNotFoundError as e:
        print(f"   ❌ File not found: {e}")
        print("\n   Make sure you:")
        print("   1. Are in the contracts/ directory")
        print("   2. Have run: python simple_vault.py")
        return
    
    # Compile to bytecode
    print("\n🔨 Compiling to bytecode...")
    
    try:
        approval_result = client.compile(approval_teal)
        approval_program = base64.b64decode(approval_result['result'])
        
        clear_result = client.compile(clear_teal)
        clear_program = base64.b64decode(clear_result['result'])
        
        print("   ✅ Compilation successful\n")
    
    except Exception as e:
        print(f"   ❌ Compilation failed: {e}")
        return
    
    # ==========================================
    # STEP 4: DEFINE STATE SCHEMA
    # ==========================================
    
    print("📊 Defining state schema...")
    
    # Local schema: variables stored per user
    local_schema = StateSchema(
        num_uints=2,      # amount, unlock_time
        num_byte_slices=1 # owner
    )
    
    # Global schema: variables shared by everyone
    global_schema = StateSchema(
        num_uints=1,      # asset_id
        num_byte_slices=0
    )
    
    print(f"   Local: {local_schema.num_uints} integers, {local_schema.num_byte_slices} strings")
    print(f"   Global: {global_schema.num_uints} integers, {global_schema.num_byte_slices} strings\n")
    
    # ==========================================
    # STEP 5: CREATE DEPLOYMENT TRANSACTION
    # ==========================================
    
    print("📝 Creating deployment transaction...")
    
    params = client.suggested_params()
    
    txn = ApplicationCreateTxn(
        sender=creator_address,
        sp=params,
        on_complete=OnComplete.NoOpOC,
        approval_program=approval_program,
        clear_program=clear_program,
        global_schema=global_schema,
        local_schema=local_schema,
    )
    
    print("   ✅ Transaction created\n")
    
    # ==========================================
    # STEP 6: SIGN TRANSACTION
    # ==========================================
    
    print("✍️  Signing transaction...")
    
    signed_txn = txn.sign(creator_private_key)
    
    print("   ✅ Signed\n")
    
    # ==========================================
    # STEP 7: SEND TO BLOCKCHAIN
    # ==========================================
    
    print("📤 Sending to blockchain...")
    
    try:
        tx_id = client.send_transaction(signed_txn)
        print(f"   Transaction ID: {tx_id}")
    except Exception as e:
        print(f"   ❌ Failed to send: {e}")
        return
    
    # ==========================================
    # STEP 8: WAIT FOR CONFIRMATION
    # ==========================================
    
    print("\n⏳ Waiting for confirmation...")
    print("   (This takes about 4 seconds)")
    
    try:
        confirmed_txn = wait_for_confirmation(client, tx_id, 4)
    except Exception as e:
        print(f"   ❌ Confirmation failed: {e}")
        return
    
    # ==========================================
    # STEP 9: GET APPLICATION ID
    # ==========================================
    
    app_id = confirmed_txn['application-index']
    
    print("\n" + "="*70)
    print("🎉 SUCCESS! SMART VAULT DEPLOYED!")
    print("="*70)
    print(f"\n📍 Application ID: {app_id}")
    print(f"\n🔗 View on AlgoExplorer:")
    print(f"   https://testnet.algoexplorer.io/application/{app_id}")
    print("\n" + "="*70)
    
    # ==========================================
    # STEP 10: SAVE APP ID
    # ==========================================
    
    print(f"\n💾 IMPORTANT: Save this App ID!")
    print(f"\nAdd this to your .env file:")
    print(f"VAULT_APP_ID={app_id}")
    print()
    
    print("="*70)
    print("✨ DEPLOYMENT COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print(f"  1. Update .env file with: VAULT_APP_ID={app_id}")
    print("  2. Test the vault with backend scripts")
    print("  3. Create demo scenarios")
    print("\n")
    
    return app_id


if __name__ == "__main__":
    try:
        app_id = deploy_vault()
        
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user\n")
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        print("\nFull error details:")
        import traceback
        traceback.print_exc()
        print()