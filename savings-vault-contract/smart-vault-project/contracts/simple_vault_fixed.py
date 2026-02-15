"""
Simple Smart Vault Contract - FIXED VERSION
Purpose: Lock CINR tokens until a specific date
Now handles deployment correctly
"""

from pyteal import *

def approval_program():
    """
    Main contract logic
    Fixed to handle app creation, opt-in, and operations
    """
    
    # ==========================================
    # STEP 1: DEFINE STATE VARIABLES
    # ==========================================
    
    # Local state (each user has their own)
    local_owner = Bytes("owner")          # Who owns this vault
    local_amount = Bytes("amount")        # How much CINR deposited
    local_unlock_time = Bytes("unlock")   # When it unlocks (Unix timestamp)
    
    # Global state (shared)
    global_asset_id = Bytes("asset_id")   # CINR token ID
    
    # ==========================================
    # STEP 2: DEFINE OPERATIONS
    # ==========================================
    
    op_deposit = Bytes("deposit")
    op_withdraw = Bytes("withdraw")
    
    # ==========================================
    # HANDLE APP CREATION
    # ==========================================
    
    on_creation = Seq([
        # When app is created, just return success
        # No initialization needed
        Return(Int(1))
    ])
    
    # ==========================================
    # HANDLE OPT-IN
    # ==========================================
    
    on_opt_in = Seq([
        # When user opts in, initialize their vault to 0
        App.localPut(Txn.sender(), local_amount, Int(0)),
        Return(Int(1))
    ])
    
    # ==========================================
    # STEP 3: DEPOSIT OPERATION
    # ==========================================
    
    handle_deposit = Seq([
        # When user deposits, do these things in order:
        
        # 1. Save who owns this vault
        App.localPut(Txn.sender(), local_owner, Txn.sender()),
        
        # 2. Save how much they deposited
        # Txn.application_args[1] = amount from user
        # Btoi = convert Bytes to Integer
        App.localPut(
            Txn.sender(),
            local_amount,
            Btoi(Txn.application_args[1])
        ),
        
        # 3. Save unlock time
        # Txn.application_args[2] = unlock timestamp
        App.localPut(
            Txn.sender(),
            local_unlock_time,
            Btoi(Txn.application_args[2])
        ),
        
        # 4. Return success (1 = success, 0 = fail)
        Return(Int(1))
    ])
    
    # ==========================================
    # STEP 4: WITHDRAW OPERATION
    # ==========================================
    
    handle_withdraw = Seq([
        # When user withdraws, check conditions:
        
        # 1. Verify sender owns this vault
        Assert(
            Txn.sender() == App.localGet(Txn.sender(), local_owner)
        ),
        
        # 2. Verify time lock has expired
        # Global.latest_timestamp() = current time
        # Must be >= unlock_time
        Assert(
            Global.latest_timestamp() >= App.localGet(Txn.sender(), local_unlock_time)
        ),
        
        # 3. If both checks pass, allow withdrawal
        # (Actual token transfer happens in backend)
        
        # 4. Reset amount to 0
        App.localPut(Txn.sender(), local_amount, Int(0)),
        
        # 5. Return success
        Return(Int(1))
    ])
    
    # ==========================================
    # STEP 5: MAIN PROGRAM LOGIC
    # ==========================================
    
    program = Cond(
        # Handle app creation
        [Txn.application_id() == Int(0), on_creation],
        
        # Handle opt-in
        [Txn.on_completion() == OnComplete.OptIn, on_opt_in],
        
        # Handle normal operations (deposit/withdraw)
        # Only check application_args if it's a NoOp call
        [Txn.on_completion() == OnComplete.NoOp,
            Cond(
                [Txn.application_args[0] == op_deposit, handle_deposit],
                [Txn.application_args[0] == op_withdraw, handle_withdraw]
            )
        ]
    )
    
    return program


def clear_state_program():
    """
    Runs when user closes out of app
    We allow it (user can always leave)
    """
    return Return(Int(1))


# ==========================================
# COMPILE THE CONTRACT
# ==========================================

if __name__ == "__main__":
    print("\n🔨 Compiling Smart Vault Contract...\n")
    
    # Compile approval program
    approval_teal = compileTeal(
        approval_program(), 
        mode=Mode.Application,
        version=8
    )
    
    # Compile clear state program
    clear_teal = compileTeal(
        clear_state_program(),
        mode=Mode.Application,
        version=8
    )
    
    # Save to files
    with open("vault_approval.teal", "w") as f:
        f.write(approval_teal)
        print("✅ Created: vault_approval.teal")
    
    with open("vault_clear.teal", "w") as f:
        f.write(clear_teal)
        print("✅ Created: vault_clear.teal")
    
    print("\n🎉 Compilation successful!")
    print("Generated files:")
    print("  - vault_approval.teal (main contract)")
    print("  - vault_clear.teal (cleanup)")
    print("\nNext step: Deploy to testnet")
    print("Run: python deploy_vault_final.py\n")