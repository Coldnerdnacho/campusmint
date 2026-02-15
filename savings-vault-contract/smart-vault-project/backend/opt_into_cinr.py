"""
Opt-In to Your Own CINR Token
After creating a token, you need to opt-in to receive it
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


def opt_in_to_own_token():
    """Opt-in to your own CINR token"""
    
    print("\n" + "="*70)
    print("📝 OPTING IN TO YOUR CINR TOKEN")
    print("="*70 + "\n")
    
    # Load config
    config = load_config()
    
    # Connect to Algorand
    client = algod.AlgodClient(
        config['ALGOD_TOKEN'],
        config['ALGOD_SERVER']
    )
    
    # Get your account
    your_mnemonic = config['CREATOR_MNEMONIC']
    your_private_key = mnemonic.to_private_key(your_mnemonic)
    your_address = account.address_from_private_key(your_private_key)
    
    # Get asset ID
    asset_id = int(config['ASSET_ID'])
    
    print(f"Your Address: {your_address}")
    print(f"CINR Asset ID: {asset_id}\n")
    
    # ==========================================
    # CHECK IF ALREADY OPTED IN
    # ==========================================
    
    print("Step 1: Checking current status...")
    
    try:
        account_info = client.account_info(your_address)
    except AttributeError:
        account_info = client.account_information(your_address)
    
    assets = account_info.get('assets', [])
    opted_in = False
    current_balance = 0
    
    for asset in assets:
        if asset['asset-id'] == asset_id:
            opted_in = True
            current_balance = asset['amount'] / 100
            break
    
    if opted_in:
        print(f"  ✅ Already opted in!")
        print(f"  CINR Balance: ₹{current_balance:,.0f}\n")
        
        if current_balance > 0:
            print("="*70)
            print("✅ You're all set!")
            print("="*70)
            print(f"\nYou have ₹{current_balance:,.0f} CINR")
            print(f"You can now use the vault!\n")
            return
        else:
            print("  ⚠️  You're opted in but have 0 CINR tokens")
            print("  This shouldn't happen if you created the token...")
            print("  Let me check the token info...\n")
            
            # Check token info
            try:
                asset_info = client.asset_info(asset_id)
                creator = asset_info['params']['creator']
                total = asset_info['params']['total']
                
                print(f"  Token Creator: {creator}")
                print(f"  Total Supply: {total / 100:,.0f} CINR")
                
                if creator == your_address:
                    print(f"\n  ✅ You ARE the creator!")
                    print(f"  The {total / 100:,.0f} CINR should be in your wallet")
                else:
                    print(f"\n  ❌ You are NOT the creator")
                    print(f"  Creator is: {creator}")
                    print(f"  Your address: {your_address}")
            except Exception as e:
                print(f"  Error checking token: {e}")
            
            print()
            return
    
    # ==========================================
    # OPT-IN TO TOKEN
    # ==========================================
    
    print("  ❌ Not opted in yet")
    print("\nStep 2: Opting in to CINR token...\n")
    
    params = client.suggested_params()
    
    # Opt-in transaction (send 0 to yourself)
    opt_in_txn = AssetTransferTxn(
        sender=your_address,
        sp=params,
        receiver=your_address,
        amt=0,
        index=asset_id
    )
    
    # Sign and send
    signed_txn = opt_in_txn.sign(your_private_key)
    tx_id = client.send_transaction(signed_txn)
    
    print(f"  Transaction sent: {tx_id}")
    print(f"  Waiting for confirmation...")
    
    wait_for_confirmation(client, tx_id, 4)
    
    print(f"  ✅ Opted in successfully!\n")
    
    # ==========================================
    # VERIFY BALANCE
    # ==========================================
    
    print("Step 3: Checking your CINR balance...")
    
    try:
        account_info = client.account_info(your_address)
    except AttributeError:
        account_info = client.account_information(your_address)
    
    assets = account_info.get('assets', [])
    final_balance = 0
    
    for asset in assets:
        if asset['asset-id'] == asset_id:
            final_balance = asset['amount'] / 100
            break
    
    print(f"  Your CINR balance: ₹{final_balance:,.0f}\n")
    
    # ==========================================
    # SUCCESS
    # ==========================================
    
    print("="*70)
    print("✅ OPT-IN COMPLETE!")
    print("="*70)
    
    if final_balance > 0:
        print(f"\n🎉 You now have ₹{final_balance:,.0f} CINR tokens!")
        print(f"\nYou can now test the vault:")
        print(f"  Run: python vault_service_fixed.py")
        print(f"  Choose option 2 (Deposit)\n")
    else:
        print(f"\n⚠️  Opted in, but balance is still 0")
        print(f"This means you might not be the token creator.")
        print(f"\nCheck:")
        print(f"  1. Is ASSET_ID correct in .env?")
        print(f"  2. Did you create the token with this wallet?")
        print(f"  3. View token: https://testnet.algoexplorer.io/asset/{asset_id}\n")


if __name__ == "__main__":
    try:
        opt_in_to_own_token()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print()