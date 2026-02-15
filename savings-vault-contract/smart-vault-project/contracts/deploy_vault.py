"""
Deploy Smart Vault to Algorand Testnet
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
import os
import sys

# Add parent directory to path to import from root .env
sys.path.append('..')
from dotenv import load_dotenv
load_dotenv('../.env')


def deploy_vault():
    """Deploy vault contract to testnet"""
    
    print("\n" + "="*70)
    print("🚀 DEPLOYING SMART VAULT TO ALGORAND TESTNET")
    print("="*70 + "\n")
    
    # ==========================================
    # STEP 1: CONNECT TO ALGORAND
    # ==========================================
    
    print("📡 Connecting to Algorand testnet...")
    
    algod_token = os.getenv("ALGOD_TOKEN")
    algod_server = os.getenv("ALGOD_SERVER")
    
    client = algod.AlgodClient(algod_token, algod_server)
    
    # Test connection
    status = client.status()
    print(f"✅ Connected!")
    print(f"   Network: Testnet")
    print(f"   Current round: {status['last-round']}\n")
    
    # ==========================================
    # STEP 2: GET CREATOR ACCOUNT
    # ==========================================
    
    print("👤 Loading creator account...")
    
    creator_mnemonic = os.getenv("CREATOR_MNEMONIC")
    creator_private_key = mnemonic.to_private_key(creator_mnemonic)
    creator_address = account.address_from_private_key(creator_private_key)
    
    print(f"   Address: {creator_address}")
    
    # Check balance
    account_info = client.account_information(creator_address)
    balance = account_info['amount'] / 1_000_000
    print(f"   Balance: {balance} ALGO\n")
    
    if balance < 0.5:
        print("❌ ERROR: Insufficient balance!")
        print("   You need at least 0.5 ALGO to deploy")
        print("   Fund your wallet: https://bank.testnet.algorand.network/")
        return
    
    # ==========================================
    # STEP 3: READ AND COMPILE CONTRACT
    # ==========================================
    
    print("📄 Reading contract files...")
    
    # Read TEAL files
    with open("vault_approval.teal", "r") as f:
        approval_teal = f.read()
        print("   ✅ vault_approval.teal")
    
    with open("vault_clear.teal", "r") as f:
        clear_teal = f.read()
        print("   ✅ vault_clear.teal")
    
    # Compile to bytecode
    print("\n🔨 Compiling to bytecode...")
    
    approval_result = client.compile(approval_teal)
    approval_program = base64.b64decode(approval_result['result'])
    
    clear_result = client.compile(clear_teal)
    clear_program = base64.b64decode(clear_result['result'])
    
    print("   ✅ Compilation successful\n")
    
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
    
    tx_id = client.send_transaction(signed_txn)
    print(f"   Transaction ID: {tx_id}")
    
    # ==========================================
    # STEP 8: WAIT FOR CONFIRMATION
    # ==========================================
    
    print("\n⏳ Waiting for confirmation...")
    print("   (This takes about 4 seconds)")
    
    confirmed_txn = wait_for_confirmation(client, tx_id, 4)
    
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
    # STEP 10: SAVE APP ID TO .ENV
    # ==========================================
    
    print("\n💾 Saving App ID to .env file...")
    
    # Read current .env
    with open("../.env", "r") as f:
        env_content = f.read()
    
    # Update VAULT_APP_ID
    if "VAULT_APP_ID=" in env_content:
        # Replace existing
        lines = env_content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("VAULT_APP_ID="):
                lines[i] = f"VAULT_APP_ID={app_id}"
        env_content = '\n'.join(lines)
    else:
        # Add new
        env_content += f"\nVAULT_APP_ID={app_id}\n"
    
    # Save
    with open("../.env", "w") as f:
        f.write(env_content)
    
    print("   ✅ Saved!\n")
    
    print("="*70)
    print("✨ DEPLOYMENT COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Test the vault with backend scripts")
    print("  2. Create demo scenarios")
    print("  3. Build frontend UI")
    print("\n")
    
    return app_id


if __name__ == "__main__":
    try:
        app_id = deploy_vault()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("  1. Check .env file has CREATOR_MNEMONIC")
        print("  2. Ensure balance > 0.5 ALGO")
        print("  3. Verify contract compiled (run simple_vault.py first)")
        print("\n")