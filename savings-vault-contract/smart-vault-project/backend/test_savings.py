"""
Smart Savings Testing Interface - Clean Version
"""

from smart_savings_service import SmartSavingsService, load_config
from algosdk import account, mnemonic
import time

def main():
    """Main testing interface"""
    
    print("\n" + "="*70)
    print("💰 SMART SAVINGS - GOAL-BASED SAVINGS WITH EMERGENCY WITHDRAWAL")
    print("="*70 + "\n")
    
    savings = SmartSavingsService()
    
    config = load_config()
    user_key = mnemonic.to_private_key(config['CREATOR_MNEMONIC'])
    user_address = account.address_from_private_key(user_key)
    
    print(f"Your Wallet: {user_address}\n")
    
    while True:
        print("╔══════════════════════════════════════════════════════════╗")
        print("║              SMART SAVINGS OPERATIONS                    ║")
        print("╠══════════════════════════════════════════════════════════╣")
        print("║  1. Opt-in to Smart Savings                             ║")
        print("║  2. Create new savings account                          ║")
        print("║  3. Add money to savings                                ║")
        print("║  4. Check savings status                                ║")
        print("║  5. Normal withdrawal (after goal date)                 ║")
        print("║  6. Emergency withdrawal (2% penalty)                   ║")
        print("║  0. Exit                                                ║")
        print("╚══════════════════════════════════════════════════════════╝")
        
        choice = input("\nEnter choice (0-6): ")
        
        if choice == "0":
            print("\n👋 Goodbye!\n")
            break
        
        elif choice == "1":
            print()
            savings.opt_in(user_key)
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            print("\n" + "="*60)
            print("CREATE NEW SAVINGS ACCOUNT")
            print("="*60 + "\n")
            
            goal = float(input("Goal amount (₹): "))
            days = int(input("Goal period (days): "))
            cause = input("What are you saving for: ")
            
            print("\n⚠️  Set emergency password (for 2% penalty withdrawal)")
            pwd = input("Emergency password: ")
            confirm = input("Confirm password: ")
            
            if pwd != confirm:
                print("\n❌ Passwords don't match!\n")
                input("Press Enter to continue...")
                continue
            
            print(f"\nCreating savings: ₹{goal:,.2f} in {days} days")
            confirm_create = input("Confirm? (y/n): ")
            
            if confirm_create.lower() == 'y':
                savings.create_savings(user_key, goal, days, cause, pwd)
            
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            print()
            amount = float(input("Amount to deposit (₹): "))
            
            confirm_dep = input(f"Deposit ₹{amount:,.2f}? (y/n): ")
            if confirm_dep.lower() == 'y':
                savings.deposit(user_key, amount)
            
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            print()
            savings.get_status(user_address)
            input("Press Enter to continue...")
        
        elif choice == "5":
            print()
            confirm_w = input("Withdraw (100%, no penalty)? (y/n): ")
            if confirm_w.lower() == 'y':
                savings.withdraw(user_key)
            
            input("\nPress Enter to continue...")
        
        elif choice == "6":
            print("\n⚠️  EMERGENCY WITHDRAWAL WARNING")
            print("  - 2% penalty applies")
            print("  - Requires password")
            print("  - Must be 7+ days old\n")
            
            confirm_e = input("Continue? (y/n): ")
            if confirm_e.lower() != 'y':
                continue
            
            pwd = input("\nEmergency password: ")
            
            final = input("Type 'EMERGENCY' to confirm: ")
            if final == "EMERGENCY":
                savings.emergency_withdraw(user_key, pwd)
            
            input("\nPress Enter to continue...")
        
        else:
            print("\n❌ Invalid choice\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")