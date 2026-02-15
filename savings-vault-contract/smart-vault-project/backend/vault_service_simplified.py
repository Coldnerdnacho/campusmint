"""
Smart Vault Service - Days-Based Locking
Simplified: Only asks for number of days to lock funds
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import (
    ApplicationOptInTxn,
    ApplicationNoOpTxn,
    wait_for_confirmation
)
from pathlib import Path
from datetime import datetime, timedelta

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


def timestamp_to_readable(timestamp):
    """Convert Unix timestamp to readable date"""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%B %d, %Y at %I:%M %p")  # e.g., "February 15, 2026 at 11:30 PM"


def get_time_remaining(unlock_timestamp):
    """Get human-readable time remaining"""
    import time
    current = int(time.time())
    
    if current >= unlock_timestamp:
        return "UNLOCKED! ✅"
    
    remaining = unlock_timestamp - current
    
    days = remaining // (24 * 60 * 60)
    hours = (remaining % (24 * 60 * 60)) // (60 * 60)
    minutes = (remaining % (60 * 60)) // 60
    
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    
    if not parts:
        return "less than 1 minute"
    
    return ", ".join(parts)


class VaultService:
    """Smart Vault with time-locked savings"""
    
    def __init__(self):
        config = load_config()
        
        self.client = algod.AlgodClient(
            config['ALGOD_TOKEN'],
            config['ALGOD_SERVER']
        )
        
        self.asset_id = int(config['ASSET_ID'])
        self.app_id = int(config['VAULT_APP_ID'])
        self.creator_mnemonic = config['CREATOR_MNEMONIC']
        
        print(f"✅ Smart Vault Service Initialized")
        print(f"   Asset ID (CINR): {self.asset_id}")
        print(f"   Vault App ID: {self.app_id}\n")
    
    
    def opt_in(self, user_private_key):
        """Opt-in to vault app"""
        print("📝 Opting in to Smart Vault...")
        
        user_address = account.address_from_private_key(user_private_key)
        params = self.client.suggested_params()
        
        txn = ApplicationOptInTxn(
            sender=user_address,
            sp=params,
            index=self.app_id
        )
        
        signed_txn = txn.sign(user_private_key)
        tx_id = self.client.send_transaction(signed_txn)
        wait_for_confirmation(self.client, tx_id, 4)
        
        print(f"✅ Opted in! TX: {tx_id}\n")
        return {"success": True, "tx_id": tx_id}
    
    
    def deposit(self, user_private_key, amount_inr, unlock_timestamp):
        """Deposit with readable dates"""
        
        unlock_date = timestamp_to_readable(unlock_timestamp)
        
        print(f"\n💰 Creating Time-Locked Vault")
        print(f"=" * 60)
        print(f"Amount:       ₹{amount_inr:,.2f}")
        print(f"Unlock Date:  {unlock_date}")
        print(f"=" * 60 + "\n")
        
        user_address = account.address_from_private_key(user_private_key)
        params = self.client.suggested_params()
        
        amount_units = int(amount_inr * 100)
        
        app_args = [
            b"deposit",
            amount_units.to_bytes(8, 'big'),
            unlock_timestamp.to_bytes(8, 'big')
        ]
        
        txn = ApplicationNoOpTxn(
            sender=user_address,
            sp=params,
            index=self.app_id,
            app_args=app_args
        )
        
        signed_txn = txn.sign(user_private_key)
        tx_id = self.client.send_transaction(signed_txn)
        wait_for_confirmation(self.client, tx_id, 4)
        
        print(f"✅ Vault Created Successfully!")
        print(f"   Transaction: {tx_id}")
        print(f"   Status: Locked until {unlock_date}\n")
        
        return {
            "success": True,
            "tx_id": tx_id,
            "amount": amount_inr,
            "unlock_time": unlock_timestamp,
            "unlock_date": unlock_date
        }
    
    
    def withdraw(self, user_private_key):
        """Withdraw after unlock time"""
        print("\n💸 Attempting Withdrawal...")
        
        user_address = account.address_from_private_key(user_private_key)
        params = self.client.suggested_params()
        
        app_args = [b"withdraw"]
        
        txn = ApplicationNoOpTxn(
            sender=user_address,
            sp=params,
            index=self.app_id,
            app_args=app_args
        )
        
        signed_txn = txn.sign(user_private_key)
        tx_id = self.client.send_transaction(signed_txn)
        
        try:
            wait_for_confirmation(self.client, tx_id, 4)
            print(f"✅ Withdrawal Successful!")
            print(f"   Funds Released!")
            print(f"   TX: {tx_id}\n")
            
            return {"success": True, "tx_id": tx_id}
        
        except Exception as e:
            error_msg = str(e)
            
            if "assert" in error_msg.lower():
                print(f"❌ Withdrawal Denied: Time lock still active")
            else:
                print(f"❌ Withdrawal failed: {e}")
            
            print("   Check vault status for unlock time\n")
            return {"success": False, "error": str(e)}
    
    
    def get_status(self, user_address):
        """Get vault status with readable dates"""
        
        try:
            try:
                app_info = self.client.account_application_info(user_address, self.app_id)
            except AttributeError:
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
                print("\n❌ No vault found for this address\n")
                return {"success": False, "error": "Not opted in"}
            
            # Parse state
            import base64
            local_state = app_info['app-local-state'].get('key-value', [])
            
            vault_data = {}
            for item in local_state:
                key = base64.b64decode(item['key']).decode()
                
                if item['value']['type'] == 2:
                    value = item['value']['uint']
                else:
                    value = base64.b64decode(item['value']['bytes'])
                
                vault_data[key] = value
            
            amount_inr = vault_data.get('amount', 0) / 100
            unlock_time = vault_data.get('unlock', 0)
            
            if amount_inr <= 0:
                print("\n📊 Vault Status: Empty")
                print("   No active deposits\n")
                return {"success": True, "amount": 0}
            
            import time
            current_time = int(time.time())
            can_withdraw = current_time >= unlock_time
            
            unlock_date = timestamp_to_readable(unlock_time)
            time_remaining = get_time_remaining(unlock_time)
            
            # Display vault status
            print("\n" + "="*60)
            print("📊 VAULT STATUS")
            print("="*60)
            print(f"Amount Locked:    ₹{amount_inr:,.2f}")
            print(f"Unlock Date:      {unlock_date}")
            print(f"Time Remaining:   {time_remaining}")
            print(f"Status:           {'🔓 UNLOCKED' if can_withdraw else '🔒 LOCKED'}")
            print("="*60 + "\n")
            
            if can_withdraw:
                print("✅ You can withdraw now!\n")
            else:
                print(f"⏳ Please wait {time_remaining}\n")
            
            return {
                "success": True,
                "amount": amount_inr,
                "unlock_time": unlock_time,
                "unlock_date": unlock_date,
                "can_withdraw": can_withdraw,
                "time_remaining": time_remaining
            }
        
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            return {"success": False, "error": str(e)}


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":
    import time
    
    print("\n" + "="*70)
    print("🏦 SMART VAULT - TIME-LOCKED SAVINGS")
    print("="*70 + "\n")
    
    vault = VaultService()
    
    config = load_config()
    test_key = mnemonic.to_private_key(config['CREATOR_MNEMONIC'])
    test_address = account.address_from_private_key(test_key)
    
    print(f"Your Wallet: {test_address}\n")
    
    print("╔══════════════════════════════════════════╗")
    print("║         VAULT OPERATIONS MENU            ║")
    print("╠══════════════════════════════════════════╣")
    print("║  1. Opt-in to vault (one-time setup)    ║")
    print("║  2. Create time-locked deposit           ║")
    print("║  3. Check vault status                   ║")
    print("║  4. Withdraw (if unlocked)               ║")
    print("╚══════════════════════════════════════════╝")
    
    choice = input("\nEnter choice (1-4): ")
    
    if choice == "1":
        print()
        vault.opt_in(test_key)
    
    elif choice == "2":
        print()
        amount = float(input("Amount to lock (₹): "))
        days = int(input("Lock for how many days: "))
        
        # Calculate unlock time
        unlock_time = int(time.time()) + (days * 24 * 60 * 60)
        unlock_date = timestamp_to_readable(unlock_time)
        
        print(f"\n" + "="*60)
        print("CONFIRMATION")
        print("="*60)
        print(f"Amount:      ₹{amount:,.2f}")
        print(f"Lock Period: {days} day{'s' if days != 1 else ''}")
        print(f"Unlock Date: {unlock_date}")
        print("="*60)
        
        confirm = input("\nConfirm deposit? (y/n): ")
        
        if confirm.lower() == 'y':
            vault.deposit(test_key, amount, unlock_time)
        else:
            print("\n❌ Deposit cancelled\n")
    
    elif choice == "3":
        print()
        vault.get_status(test_address)
    
    elif choice == "4":
        print()
        vault.withdraw(test_key)
    
    else:
        print("\n❌ Invalid choice")
    
    print("="*70)
    print("✅ Session complete!")
    print("="*70 + "\n")