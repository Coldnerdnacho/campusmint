"""
Smart Savings Service
Backend for interacting with Smart Savings contract
Features: Multiple deposits, goal tracking, emergency withdrawal
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import (
    ApplicationOptInTxn,
    ApplicationNoOpTxn,
    wait_for_confirmation
)
from pathlib import Path
from datetime import datetime
import hashlib
import time

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
    return dt.strftime("%B %d, %Y at %I:%M %p")


def get_time_remaining(unlock_timestamp):
    """Get human-readable time remaining"""
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


class SmartSavingsService:
    """Service for Smart Savings with HTLC emergency withdrawals"""
    
    def __init__(self):
        config = load_config()
        
        self.client = algod.AlgodClient(
            config['ALGOD_TOKEN'],
            config['ALGOD_SERVER']
        )
        
        self.asset_id = int(config['ASSET_ID'])
        
        if not config.get('SAVINGS_APP_ID'):
            print("❌ ERROR: SAVINGS_APP_ID not set in .env!")
            print("   Deploy savings contract first: python deploy_savings.py")
            exit(1)
        
        self.app_id = int(config['SAVINGS_APP_ID'])
        self.creator_mnemonic = config['CREATOR_MNEMONIC']
        
        print(f"✅ Smart Savings Service Initialized")
        print(f"   CINR Asset ID: {self.asset_id}")
        print(f"   Savings App ID: {self.app_id}\n")
    
    
    def opt_in(self, user_private_key):
        """Opt-in to savings app"""
        print("📝 Opting in to Smart Savings...")
        
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
    
    
    def create_savings(
        self,
        user_private_key,
        goal_amount,          # Total goal in rupees
        goal_days,            # Days until goal
        cause,                # What they're saving for
        emergency_password    # Secret password for emergencies
    ):
        """Create a new savings account with emergency password"""
        
        unlock_timestamp = int(time.time()) + (goal_days * 24 * 60 * 60)
        unlock_date = timestamp_to_readable(unlock_timestamp)
        
        print(f"\n💰 Creating Smart Savings Account")
        print(f"=" * 60)
        print(f"Goal Amount:       ₹{goal_amount:,.2f}")
        print(f"Goal Period:       {goal_days} days")
        print(f"Unlock Date:       {unlock_date}")
        print(f"Saving For:        {cause}")
        print(f"Emergency Setup:   Password protected (HTLC)")
        print(f"=" * 60 + "\n")
        
        user_address = account.address_from_private_key(user_private_key)
        params = self.client.suggested_params()
        
        # Convert amounts
        goal_units = int(goal_amount * 100)
        
        # Prepare app args
        app_args = [
            b"create",
            goal_units.to_bytes(8, 'big'),
            unlock_timestamp.to_bytes(8, 'big'),
            cause.encode(),
            emergency_password.encode()  # Contract will hash this
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
        
        print(f"✅ Savings Account Created!")
        print(f"   Transaction: {tx_id}")
        print(f"   Goal: ₹{goal_amount:,.2f} by {unlock_date}")
        print(f"   Emergency withdrawal: Available after 7 days\n")
        
        print(f"⚠️  IMPORTANT: Remember your emergency password!")
        print(f"   You'll need it for emergency withdrawals\n")
        
        return {
            "success": True,
            "tx_id": tx_id,
            "goal_amount": goal_amount,
            "unlock_time": unlock_timestamp
        }
    
    
    def deposit(self, user_private_key, amount):
        """Make a deposit to savings account"""
        
        print(f"\n💵 Adding ₹{amount:,.2f} to savings...")
        
        user_address = account.address_from_private_key(user_private_key)
        params = self.client.suggested_params()
        
        amount_units = int(amount * 100)
        
        app_args = [
            b"deposit",
            amount_units.to_bytes(8, 'big')
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
        
        print(f"✅ Deposit successful!")
        print(f"   Added: ₹{amount:,.2f}")
        print(f"   TX: {tx_id}\n")
        
        return {"success": True, "tx_id": tx_id, "amount": amount}
    
    
    def withdraw(self, user_private_key):
        """Normal withdrawal (after goal date)"""
        
        print("\n💸 Attempting Normal Withdrawal...")
        print("   (Full amount, no penalty)\n")
        
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
            print(f"   Full amount released (no penalty)")
            print(f"   TX: {tx_id}\n")
            
            return {"success": True, "tx_id": tx_id, "penalty": 0}
        
        except Exception as e:
            error_msg = str(e)
            
            if "assert" in error_msg.lower():
                print(f"❌ Withdrawal Denied: Goal date not reached yet")
                print(f"   Use emergency withdrawal if urgent\n")
            else:
                print(f"❌ Withdrawal failed: {e}\n")
            
            return {"success": False, "error": str(e)}
    
    
    def emergency_withdraw(self, user_private_key, emergency_password):
        """Emergency withdrawal with password (2% penalty)"""
        
        print("\n🚨 EMERGENCY WITHDRAWAL")
        print("=" * 60)
        print("⚠️  This will charge a 2% penalty")
        print("⚠️  You get 98% of your savings")
        print("⚠️  Must be at least 7 days since account creation")
        print("=" * 60 + "\n")
        
        user_address = account.address_from_private_key(user_private_key)
        params = self.client.suggested_params()
        
        app_args = [
            b"emergency",
            emergency_password.encode()
        ]
        
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
            print(f"✅ Emergency Withdrawal Approved!")
            print(f"   Password verified ✓")
            print(f"   Penalty: 2%")
            print(f"   TX: {tx_id}\n")
            
            return {"success": True, "tx_id": tx_id, "penalty": 2}
        
        except Exception as e:
            error_msg = str(e).lower()
            
            if "assert" in error_msg or "logic eval error" in error_msg:
                print(f"❌ Emergency Withdrawal Denied!")
                
                if "7 days" in error_msg or "604800" in error_msg:
                    print(f"   Reason: Must wait 7 days since account creation")
                else:
                    print(f"   Reason: Incorrect password or conditions not met")
                
                print(f"\n   Troubleshooting:")
                print(f"   - Check if password is correct")
                print(f"   - Account must be at least 7 days old")
                print(f"   - Must have savings to withdraw\n")
            else:
                print(f"❌ Emergency withdrawal failed: {e}\n")
            
            return {"success": False, "error": str(e)}
    
    
    def get_status(self, user_address):
        """Get savings account status"""
        
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
                print("\n❌ No savings account found\n")
                return {"success": False, "error": "Not opted in"}
            
            # Parse state
            import base64
            local_state = app_info['app-local-state'].get('key-value', [])
            
            savings_data = {}
            for item in local_state:
                key = base64.b64decode(item['key']).decode()
                
                if item['value']['type'] == 2:
                    value = item['value']['uint']
                else:
                    value = base64.b64decode(item['value']['bytes'])
                
                savings_data[key] = value
            
            # Extract data
            total_saved = savings_data.get('total', 0) / 100
            goal_amount = savings_data.get('goal', 0) / 100
            unlock_time = savings_data.get('unlock_time', 0)
            cause = savings_data.get('cause', b'').decode() if 'cause' in savings_data else "Unknown"
            created_at = savings_data.get('created_at', 0)
            
            if total_saved <= 0 and goal_amount <= 0:
                print("\n📊 Savings Status: Not initialized")
                print("   Create a savings account first\n")
                return {"success": True, "initialized": False}
            
            # Calculate progress
            progress = (total_saved / goal_amount * 100) if goal_amount > 0 else 0
            
            current_time = int(time.time())
            can_withdraw = current_time >= unlock_time
            days_since_creation = (current_time - created_at) // (24 * 60 * 60) if created_at > 0 else 0
            emergency_available = days_since_creation >= 7
            
            unlock_date = timestamp_to_readable(unlock_time)
            time_remaining = get_time_remaining(unlock_time)
            
            # Display status
            print("\n" + "="*60)
            print("💰 SMART SAVINGS STATUS")
            print("="*60)
            print(f"Saving For:        {cause}")
            print(f"Goal Amount:       ₹{goal_amount:,.2f}")
            print(f"Saved So Far:      ₹{total_saved:,.2f}")
            print(f"Progress:          {progress:.1f}%")
            print(f"")
            print(f"Unlock Date:       {unlock_date}")
            print(f"Time Remaining:    {time_remaining}")
            print(f"Status:            {'🔓 UNLOCKED' if can_withdraw else '🔒 LOCKED'}")
            print(f"")
            print(f"Account Age:       {days_since_creation} days")
            print(f"Emergency Option:  {'✅ Available (2% penalty)' if emergency_available else '❌ Wait ' + str(7 - days_since_creation) + ' more days'}")
            print("="*60 + "\n")
            
            if can_withdraw:
                print("✅ You can withdraw your full savings now!\n")
            elif emergency_available:
                print(f"⏳ Goal not reached, but emergency withdrawal available")
                print(f"   (2% penalty applies)\n")
            else:
                print(f"⏳ Keep saving! {time_remaining} until goal\n")
            
            return {
                "success": True,
                "initialized": True,
                "total_saved": total_saved,
                "goal_amount": goal_amount,
                "progress": progress,
                "unlock_time": unlock_time,
                "can_withdraw": can_withdraw,
                "emergency_available": emergency_available,
                "days_since_creation": days_since_creation
            }
        
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    print("\n⚠️  This is the Smart Savings Service module")
    print("Run 'python test_savings.py' to test it\n")