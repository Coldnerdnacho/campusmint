"""
Deploy Smart Vault to Algorand Testnet
FIXED VERSION with better error handling
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
from pathlib import Path

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

def load_env_file():
    """Load .env file with proper error handling"""
    
    # Find .env file (check multiple locations)
    possible_paths = [
        Path(__file__).parent.parent / '.env',  # Parent directory
        Path(__file__).parent / '.env',          # Current directory
        Path.cwd() / '.env',                     # Working directory
        Path.home() / 'smart-vault-project' / '.env'  # Home directory
    ]
    
    env_path = None
    for path in possible_paths:
        if path.exists():
            env_path = path
            break
    
    if not env_path:
        print("❌ ERROR: Cannot find .env file!")
        print("\nSearched in:")
        for p in possible_paths:
            print(f"  - {p}")
        print("\nPlease create .env file in your project root")
        exit(1)
    
    print(f"✅ Found .env file: {env_path}")
    
    # Read .env file manually (more reliable than python-dotenv)
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # Remove quotes if present
                value = value.strip().strip('"').strip("'")
                env_vars[key] = value
    
    return env_vars


def deploy_vault():
    """Deploy vault contract to testnet"""
    
    print("\n" + "="*70)
    print("🚀 DEPLOYING SMART VAULT TO ALGORAND TESTNET")
    print("="*70 + "\n")
    
    # ==========================================
    # LOAD ENVIRONMENT VARIABLES
    # ==========================================
    
    print("📁 Loading environment variables...")
    env_vars = load_env_file()
    
    # Check required variables
    required_vars = ['CREATOR_MNEMONIC', 'ALGOD_TOKEN', 'ALGOD_SERVER']
    missing_vars = [var for var in required_vars if var not in env_vars or not env_vars[var]]
    
    if missing_vars:
        print(f"\n❌ ERROR: Missing required variables in .env:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease update your .env file")
        exit(1)
    
    print("✅ All required variables found\n")
    
    # ==========================================
    # STEP 1: CONNECT TO ALGORAND
    # ==========================================
    
    print("📡 Connecting to Algorand testnet...")
    
    try:
        client = algod.AlgodClient(
            env_vars['ALGOD_TOKEN'],
            env_vars['ALGOD_SERVER']
        )
        
        # Test connection
        status = client.status()
        print(f"✅ Connected!")
        print(f"   Network: Testnet")
        print(f"   Current round: {status['last-round']}\n")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nCheck:")
        print("  - ALGOD_SERVER is correct")
        print("  - Internet connection is working")
        exit(1)
    
    # ==========================================
    # STEP 2: GET CREATOR ACCOUNT
    # ==========================================
    
    print("👤 Loading creator account...")
    
    try:
        creator_mnemonic = env_vars['CREATOR_MNEMONIC']
        
        # Verify mnemonic has 25 words
        word_count = len(creator_mnemonic.split())
        print(f"   Mnemonic word count: {word_count}")
        
        if word_count != 25:
            print(f"❌ ERROR: Mnemonic should have 25 words, found {word_count}")
            print("   Check your CREATOR_MNEMONIC in .env file")
            exit(1)
        
        creator_private_key = mnemonic.to_private_key(creator_mnemonic)
        creator_address = account.address_from_private_key(creator_private_key)
        
        print(f"   Address: {creator_address}")
        
    except Exception as e:
        print(f"❌ Invalid mnemonic: {e}")
        print("   Check CREATOR_MNEMONIC in .env file")
        exit(1)
    
    # Check balance
    try:
        account_info = client.account_information(creator_address)
        balance = account_info['amount'] / 1_000_000
        print(f"   Balance: {balance} ALGO\n")
        
        if balance < 0.5:
            print("❌ ERROR: Insufficient balance!")
            print("   You need at least 0.5 ALGO to deploy")
            print(f"\n   Fund this address: {creator_address}")
            print("   Faucet: https://bank.testnet.algorand.network/")
            exit(1)
            
    except Exception as e:
        print(f"❌ Cannot check balance: {e}")
        exit(1)
    
    # ==========================================
    # STEP 3: READ AND COMPILE CONTRACT
    # ==========================================
    
    print("📄 Reading contract files...")
    
    # Check if TEAL files exist
    contract_dir = Path(__file__).parent
    approval_path = contract_dir / "vault_approval.teal"
    clear_path = contract_dir / "vault_clear.teal"
    
    if not approval_path.exists():
        print(f"❌ ERROR: vault_approval.teal not found!")
        print(f"   Expected at: {approval_path}")
        print("\n   Run this first: python simple_vault.py")
        exit(1)
    
    if not clear_path.exists():
        print(f"❌ ERROR: vault_clear.teal not found!")
        print(f"   Expected at: {clear_path}")
        print("\n   Run this first: python simple_vault.py")
        exit(1)
    
    # Read TEAL files
    with open(approval_path, "r") as f:
        approval_teal = f.read()
        print(f"   ✅ {approval_path.name}")
    
    with open(clear_path, "r") as f:
        clear_teal = f.read()
        print(f"   ✅ {clear_path.name}")
    
    # Compile to bytecode
    print("\n🔨 Compiling to bytecode...")
    
    try:
        approval_result = client.compile(approval_teal)
        approval_program = base64.b64decode(approval_result['result'])
        
        clear_result = client.compile(clear_teal)
        clear_program = base64.b64decode(clear_result['result'])
        
        print("   ✅ Compilation successful\n")
        
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
        exit(1)
    
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
    
    # Find .env path again
    env_path = None
    possible_paths = [
        Path(__file__).parent.parent / '.env',
        Path(__file__).parent / '.env',
        Path.cwd() / '.env',
    ]
    
    for path in possible_paths:
        if path.exists():
            env_path = path
            break
    
    if env_path:
        # Read current .env
        with open(env_path, "r") as f:
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
        with open(env_path, "w") as f:
            f.write(env_content)
        
        print(f"   ✅ Saved to {env_path}\n")
    else:
        print("   ⚠️  Could not save to .env (file not found)")
        print(f"   Manually add this line: VAULT_APP_ID={app_id}\n")
    
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
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user\n")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        print("\nPlease report this error with details")
        import traceback
        traceback.print_exc()