"""
Deploy Smart Savings Contract to Algorand Testnet
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
from pathlib import Path

# ==========================================
# LOAD CONFIGURATION
# ==========================================

def load_config():
    """Load configuration from .env file"""
    
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        env_path = Path.cwd() / '.env'
    
    config = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                value = value.strip().strip('"').strip("'")
                config[key] = value
    
    return config


def deploy_savings():
    """Deploy Smart Savings contract to testnet"""
    
    print("\n" + "="*70)
    print("🚀 DEPLOYING SMART SAVINGS CONTRACT (WITH HTLC)")
    print("="*70 + "\n")
    
    # Load config
    config = load_config()
    
    # Connect to Algorand
    print("📡 Connecting to Algorand testnet...")
    
    client = algod.AlgodClient(
        config['ALGOD_TOKEN'],
        config['ALGOD_SERVER']
    )
    
    status = client.status()
    print(f"✅ Connected!")
    print(f"   Network: Testnet")
    print(f"   Current round: {status['last-round']}\n")
    
    # Get creator account
    print("👤 Loading creator account...")
    
    creator_mnemonic = config['CREATOR_MNEMONIC']
    creator_private_key = mnemonic.to_private_key(creator_mnemonic)
    creator_address = account.address_from_private_key(creator_private_key)
    
    print(f"   Address: {creator_address}")
    
    # Check balance
    try:
        account_info = client.account_info(creator_address)
    except AttributeError:
        account_info = client.account_information(creator_address)
    
    balance = account_info['amount'] / 1_000_000
    print(f"   Balance: {balance} ALGO\n")
    
    if balance < 0.5:
        print("❌ ERROR: Insufficient balance!")
        print("   You need at least 0.5 ALGO to deploy")
        return
    
    # Read contract files
    print("📄 Reading contract files...")
    
    try:
        with open("savings_approval.teal", "r") as f:
            approval_teal = f.read()
            print("   ✅ savings_approval.teal")
        
        with open("savings_clear.teal", "r") as f:
            clear_teal = f.read()
            print("   ✅ savings_clear.teal")
    
    except FileNotFoundError:
        print("   ❌ Contract files not found!")
        print("\n   Run this first: python smart_savings_contract.py")
        return
    
    # Compile to bytecode
    print("\n🔨 Compiling to bytecode...")
    
    approval_result = client.compile(approval_teal)
    approval_program = base64.b64decode(approval_result['result'])
    
    clear_result = client.compile(clear_teal)
    clear_program = base64.b64decode(clear_result['result'])
    
    print("   ✅ Compilation successful\n")
    
    # Define state schema
    print("📊 Defining state schema...")
    
    # Local schema: variables stored per user
    local_schema = StateSchema(
        num_uints=5,      # total, goal, unlock_time, created_at, last_deposit
        num_byte_slices=3 # owner, cause, emergency_hash
    )
    
    # Global schema
    global_schema = StateSchema(
        num_uints=1,      # asset_id
        num_byte_slices=0
    )
    
    print(f"   Local: {local_schema.num_uints} integers, {local_schema.num_byte_slices} strings")
    print(f"   Global: {global_schema.num_uints} integers, {global_schema.num_byte_slices} strings\n")
    
    # Create deployment transaction
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
    
    # Sign transaction
    print("✍️  Signing transaction...")
    
    signed_txn = txn.sign(creator_private_key)
    
    print("   ✅ Signed\n")
    
    # Send to blockchain
    print("📤 Sending to blockchain...")
    
    tx_id = client.send_transaction(signed_txn)
    print(f"   Transaction ID: {tx_id}")
    
    # Wait for confirmation
    print("\n⏳ Waiting for confirmation (4 seconds)...")
    
    confirmed_txn = wait_for_confirmation(client, tx_id, 4)
    
    # Get application ID
    app_id = confirmed_txn['application-index']
    
    print("\n" + "="*70)
    print("🎉 SUCCESS! SMART SAVINGS DEPLOYED!")
    print("="*70)
    print(f"\n📍 Application ID: {app_id}")
    print(f"\n🔗 View on AlgoExplorer:")
    print(f"   https://testnet.algoexplorer.io/application/{app_id}")
    print("\n" + "="*70)
    
    # Update .env file
    print("\n💾 Updating .env file...")
    
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        env_path = Path.cwd() / '.env'
    
    # Read current .env
    with open(env_path, "r") as f:
        env_content = f.read()
    
    # Update or add SAVINGS_APP_ID
    if "SAVINGS_APP_ID=" in env_content:
        lines = env_content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("SAVINGS_APP_ID="):
                lines[i] = f"SAVINGS_APP_ID={app_id}"
        env_content = '\n'.join(lines)
    else:
        env_content += f"\nSAVINGS_APP_ID={app_id}\n"
    
    # Save
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print(f"   ✅ Added SAVINGS_APP_ID={app_id} to .env\n")
    
    print("="*70)
    print("✨ DEPLOYMENT COMPLETE!")
    print("="*70)
    print("\nFeatures enabled:")
    print("  ✅ Multiple deposits over time")
    print("  ✅ Goal-based savings tracking")
    print("  ✅ Time-locked withdrawals")
    print("  ✅ Emergency withdrawal with password (HTLC)")
    print("  ✅ 2% penalty on emergency withdrawals")
    print("  ✅ 7-day minimum before emergency access")
    print("\nNext steps:")
    print("  1. Test the savings account")
    print("  2. Create savings goals")
    print("  3. Make multiple deposits")
    print("  4. Test emergency withdrawal")
    print("\n")
    
    return app_id


if __name__ == "__main__":
    try:
        deploy_savings()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print()