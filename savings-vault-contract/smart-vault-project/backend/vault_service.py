"""
Smart Vault Backend Service
FIXED VERSION - loads .env correctly
"""

from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from algosdk.transaction import (
    ApplicationOptInTxn,
    ApplicationNoOpTxn,
    AssetTransferTxn,
    assign_group_id,
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
        Path(__file__).parent.parent / '.env',  # Parent of backend/
        Path.cwd() / '.env',
    ]
    
    env_path = None
    for path in possible_paths:
        if path.exists():
            env_path = path
            break
    
    if not env_path:
        print("❌ ERROR: .env file not found!")
        print("\nSearched in:")
        for p in possible_paths:
            print(f"  - {p}")
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


class VaultService:
    """Service for interacting with Smart Vault"""
    
    def __init__(self):
        # Load config
        config = load_config()
        
        # Connect to Algorand
        self.client = algod.AlgodClient(
            config['ALGOD_TOKEN'],
            config['ALGOD_SERVER']
        )
        
        # Get IDs
        self.asset_id = int(config['ASSET_ID'])
        
        # Check if vault is deployed
        if not config.get('VAULT_APP_ID'):
            print("❌ ERROR: VAULT_APP_ID not set in .env!")
            print("   Deploy the vault first: python deploy_vault_final.py")
            exit(1)
        
        self.app_id = int(config['VAULT_APP_ID'])
        
        # Store mnemonic for easy access
        self.creator_mnemonic = config['CREATOR_MNEMONIC']
        
        print(f"✅ Vault Service Initialized")
        print(f"   Asset ID (CINR): {self.asset_id}")
        print(f"   Vault App ID: {self.app_id}\n")
    
    
    # ================================================
    # STEP 1: OPT-IN TO VAULT
    # ================================================
    
    def opt_in(self, user_private_key):
        """
        User must opt-in to vault app before using it
        (One-time operation)
        """
        print("📝 Opting in to Smart Vault...")
        
        user_address = account.address_from_private_key(user_private_key)
        params = self.client.suggested_params()
        
        # Create opt-in transaction
        txn = ApplicationOptInTxn(
            sender=user_address,
            sp=params,
            index=self.app_id
        )
        
        # Sign and send
        signed_txn = txn.sign(user_private_key)
        tx_id = self.client.send_transaction(signed_txn)
        wait_for_confirmation(self.client, tx_id, 4)
        
        print(f"✅ Opted in! TX: {tx_id}\n")
        
        return {"success": True, "tx_id": tx_id}
    
    
    # ================================================
    # STEP 2: DEPOSIT TO VAULT
    # ================================================
    
    def deposit(
        self,
        user_private_key,
        amount_inr,        # Amount in rupees (e.g., 5000 for ₹5000)
        unlock_timestamp   # Unix timestamp when unlocks
    ):
        """
        Deposit CINR tokens to vault
        
        Example:
        vault.deposit(
            user_key="...",
            amount_inr=5000,  # ₹5,000
            unlock_timestamp=1719792000  # July 1, 2025
        )
        """
        print(f"\n💰 Depositing ₹{amount_inr} to vault...")
        print(f"   Unlock time: {unlock_timestamp}")
        
        user_address = account.address_from_private_key(user_private_key)
        params = self.client.suggested_params()
        
        # Convert rupees to smallest unit (2 decimals)
        amount_units = int(amount_inr * 100)
        
        # Get vault app address
        app_address = logic.get_application_address(self.app_id)
        print(f"   Vault address: {app_address[:8]}...")
        
        # Transaction 1: Application call
        app_args = [
            b"deposit",
            amount_units.to_bytes(8, 'big'),
            unlock_timestamp.to_bytes(8, 'big')
        ]
        
        app_txn = ApplicationNoOpTxn(
            sender=user_address,
            sp=params,
            index=self.app_id,
            app_args=app_args,
            foreign_assets=[self.asset_id]
        )
        
        # Transaction 2: Asset transfer to vault
        asset_txn = AssetTransferTxn(
            sender=user_address,
            sp=params,
            receiver=app_address,
            amt=amount_units,
            index=self.asset_id
        )
        
        # Group transactions (atomic - both succeed or both fail)
        txns = [app_txn, asset_txn]
        assign_group_id(txns)
        
        # Sign both
        signed_txns = [
            txns[0].sign(user_private_key),
            txns[1].sign(user_private_key)
        ]
        
        # Send
        tx_id = self.client.send_transactions(signed_txns)
        wait_for_confirmation(self.client, tx_id, 4)
        
        print(f"✅ Deposited ₹{amount_inr}!")
        print(f"   TX: {tx_id}\n")
        
        return {
            "success": True,
            "tx_id": tx_id,
            "amount": amount_inr,
            "unlock_time": unlock_timestamp
        }
    
    
    # ================================================
    # STEP 3: WITHDRAW FROM VAULT
    # ================================================
    
    def withdraw(self, user_private_key):
        """
        Withdraw from vault (only after unlock time)
        """
        print("\n💸 Withdrawing from vault...")
        
        user_address = account.address_from_private_key(user_private_key)
        params = self.client.suggested_params()
        
        # Application call
        app_args = [b"withdraw"]
        
        txn = ApplicationNoOpTxn(
            sender=user_address,
            sp=params,
            index=self.app_id,
            app_args=app_args,
            foreign_assets=[self.asset_id]
        )
        
        # Sign and send
        signed_txn = txn.sign(user_private_key)
        tx_id = self.client.send_transaction(signed_txn)
        
        try:
            wait_for_confirmation(self.client, tx_id, 4)
            print(f"✅ Withdrawal successful!")
            print(f"   TX: {tx_id}\n")
            
            return {"success": True, "tx_id": tx_id}
        
        except Exception as e:
            print(f"❌ Withdrawal failed: {e}")
            print("   Check:")
            print("   - Has unlock time passed?")
            print("   - Do you have a deposit in the vault?\n")
            
            return {"success": False, "error": str(e)}
    
    
    # ================================================
    # STEP 4: CHECK VAULT STATUS
    # ================================================
    
    def get_status(self, user_address):
        """Get vault status for a user"""
        print(f"\n📊 Checking vault status for {user_address[:8]}...")
        
        try:
            # Get application local state
            try:
                app_info = self.client.account_application_info(
                    user_address,
                    self.app_id
                )
            except AttributeError:
                # Try older SDK method
                account_info = self.client.account_info(user_address)
                apps = account_info.get('apps-local-state', [])
                app_info = None
                for app in apps:
                    if app['id'] == self.app_id:
                        app_info = {'app-local-state': app}
                        break
                
                if not app_info:
                    raise Exception("Not opted in")
            
            if 'app-local-state' not in app_info:
                print("   ❌ No vault found for this address")
                return {"success": False, "error": "Not opted in"}
            
            # Parse local state
            import base64
            local_state = app_info['app-local-state'].get('key-value', [])
            
            vault_data = {}
            for item in local_state:
                key = base64.b64decode(item['key']).decode()
                
                if item['value']['type'] == 2:  # uint
                    value = item['value']['uint']
                else:  # bytes
                    value = base64.b64decode(item['value']['bytes'])
                
                vault_data[key] = value
            
            # Convert to readable format
            amount_inr = vault_data.get('amount', 0) / 100
            unlock_time = vault_data.get('unlock', 0)
            
            import time
            current_time = int(time.time())
            can_withdraw = current_time >= unlock_time if unlock_time > 0 else False
            
            if amount_inr > 0:
                print(f"   Amount locked: ₹{amount_inr}")
                print(f"   Unlock time: {unlock_time}")
                print(f"   Can withdraw: {can_withdraw}\n")
            else:
                print(f"   No active vault deposit\n")
            
            return {
                "success": True,
                "amount": amount_inr,
                "unlock_time": unlock_time,
                "can_withdraw": can_withdraw
            }
        
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            return {"success": False, "error": str(e)}


# ================================================
# TESTING
# ================================================

if __name__ == "__main__":
    import time
    
    print("\n" + "="*70)
    print("🧪 TESTING VAULT SERVICE")
    print("="*70 + "\n")
    
    # Initialize
    vault = VaultService()
    
    # Get test account from config
    config = load_config()
    test_key = mnemonic.to_private_key(config['CREATOR_MNEMONIC'])
    test_address = account.address_from_private_key(test_key)
    
    print(f"Test Account: {test_address}\n")
    
    # Menu
    print("What would you like to test?")
    print("  1. Opt-in to vault")
    print("  2. Deposit to vault")
    print("  3. Check vault status")
    print("  4. Withdraw from vault")
    
    choice = input("\nEnter choice (1-4): ")
    
    if choice == "1":
        print("\n--- Opting in to vault ---")
        vault.opt_in(test_key)
    
    elif choice == "2":
        print("\n--- Depositing to vault ---")
        amount = float(input("Amount (in rupees): "))
        days = int(input("Lock for how many days: "))
        unlock_time = int(time.time()) + (days * 24 * 60 * 60)
        
        print(f"\nYou're depositing ₹{amount} locked for {days} days")
        confirm = input("Confirm? (y/n): ")
        
        if confirm.lower() == 'y':
            vault.deposit(test_key, amount, unlock_time)
    
    elif choice == "3":
        print("\n--- Checking vault status ---")
        vault.get_status(test_address)
    
    elif choice == "4":
        print("\n--- Withdrawing from vault ---")
        print("⚠️  This will only work if unlock time has passed")
        confirm = input("Confirm? (y/n): ")
        
        if confirm.lower() == 'y':
            vault.withdraw(test_key)
    
    else:
        print("\n❌ Invalid choice")
    
    print("\n" + "="*70)
    print("✅ Test complete!")
    print("="*70 + "\n")