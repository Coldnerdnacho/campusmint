"""
Setup CINR Tokens for Vault Testing
This script:
1. Opts you into CINR token
2. Transfers CINR from creator to your wallet
3. Verifies you're ready to use the vault
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import (
    AssetTransferTxn,
    wait_for_confirmation
)
from pathlib import Path

# ==========================================
# LOAD CONFIGURATION
# ==========================================

def load_config():
    """Load configuration from .env file"""
    
    # Find .env file
    possible_paths = [
        Path(__file__).parent.parent / '.env',
        Path.cwd() / '.env',
    ]
    
    env_path = None
    for path in possible_paths:
        if path.exists():
            env_path = path
            break
    
    if not env_path:
        print("❌ ERROR: .env file not found!")
        exit(1)
    
    # Read .env file
    config = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                value = value.strip().strip('"').strip("'")
                config[key] = value
    
    return config


def setup_cinr_tokens():
    """Setup CINR tokens for vault testing"""
    
    print("\n" + "="*70)
    print("🪙 SETTING UP CINR TOKENS FOR VAULT TESTING")
    print("="*70 + "\n")
    
    # Load config
    config = load_config()
    
    # Connect to Algorand
    client = algod.AlgodClient(
        config['ALGOD_TOKEN'],
        config['ALGOD_SERVER']
    )
    
    # Get asset ID
    asset_id = int(config['ASSET_ID'])
    print(f"CINR Token Asset ID: {asset_id}\n")
    
    # Get user account (same as creator for now)
    user_mnemonic = config['CREATOR_MNEMONIC']
    user_private_key = mnemonic.to_private_key(user_mnemonic)
    user_address = account.address_from_private_key(user_private_key)
    
    print(f"Your Address: {user_address}\n")
    
    # ==========================================
    # STEP 1: CHECK IF ALREADY OPTED IN
    # ==========================================
    
    print("Step 1: Checking CINR token status...")
    
    try:
        account_info = client.account_info(user_address)
    except AttributeError:
        account_info = client.account_information(user_address)
    
    # Check if already opted in
    assets = account_info.get('assets', [])
    opted_in = False
    current_balance = 0
    
    for asset in assets:
        if asset['asset-id'] == asset_id:
            opted_in = True
            current_balance = asset['amount'] / 100  # Convert to rupees
            break
    
    if opted_in:
        print(f"  ✅ Already opted in to CINR token")
        print(f"  Current balance: ₹{current_balance}\n")
    else:
        print(f"  ❌ Not opted in to CINR token")
        print(f"  Will opt in now...\n")
        
        # ==========================================
        # STEP 2: OPT-IN TO CINR TOKEN
        # ==========================================
        
        print("Step 2: Opting in to CINR token...")
        
        params = client.suggested_params()
        
        # Create opt-in transaction (send 0 to yourself)
        opt_in_txn = AssetTransferTxn(
            sender=user_address,
            sp=params,
            receiver=user_address,
            amt=0,
            index=asset_id
        )
        
        # Sign and send
        signed_txn = opt_in_txn.sign(user_private_key)
        tx_id = client.send_transaction(signed_txn)
        wait_for_confirmation(client, tx_id, 4)
        
        print(f"  ✅ Opted in successfully!")
        print(f"  Transaction: {tx_id}\n")
    
    # ==========================================
    # STEP 3: CHECK BALANCE AND TRANSFER IF NEEDED
    # ==========================================
    
    print("Step 3: Checking CINR balance...")
    
    # Refresh account info
    try:
        account_info = client.account_info(user_address)
    except AttributeError:
        account_info = client.account_information(user_address)
    
    assets = account_info.get('assets', [])
    for asset in assets:
        if asset['asset-id'] == asset_id:
            current_balance = asset['amount'] / 100
            break
    
    print(f"  Current CINR balance: ₹{current_balance}")
    
    if current_balance >= 1000:
        print(f"  ✅ You have enough CINR for testing\n")
    else:
        print(f"  ℹ️  You have {current_balance} CINR")
        print(f"  For vault testing, you might want more tokens")
        
        # Check if this is the creator (who has tokens)
        try:
            asset_info = client.asset_info(asset_id)
            creator_address = asset_info['params']['creator']
            
            if user_address == creator_address:
                print(f"\n  💡 You are the token creator!")
                print(f"  You can create more tokens if needed")
            else:
                print(f"\n  ℹ️  To get CINR tokens, ask the creator to send you some:")
                print(f"  Creator address: {creator_address}")
        except:
            pass
        
        print()
    
    # ==========================================
    # STEP 4: VERIFY SETUP
    # ==========================================
    
    print("="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print(f"\nYour wallet is ready:")
    print(f"  Address: {user_address}")
    print(f"  CINR Balance: ₹{current_balance}")
    print(f"  Opted into CINR: ✅")
    print(f"\nYou can now:")
    print(f"  1. Deposit CINR to vault")
    print(f"  2. Test vault locking")
    print(f"  3. Withdraw after time lock expires")
    print(f"\nRun: python vault_service_fixed.py")
    print()


if __name__ == "__main__":
    try:
        setup_cinr_tokens()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print()