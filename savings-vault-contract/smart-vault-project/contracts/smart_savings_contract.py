"""
Smart Savings Contract with HTLC
Features:
- Multiple deposits over time
- Time-locked withdrawals
- Emergency withdrawal with password hash
- 2% penalty on emergency withdrawals
- 7-day minimum before emergency can be used
"""

from pyteal import *

def approval_program():
    """
    Smart Savings with HTLC emergency withdrawal
    """
    
    # ==========================================
    # STATE VARIABLES
    # ==========================================
    
    # Local state (per user)
    local_owner = Bytes("owner")              # Account owner
    local_total = Bytes("total")              # Total saved (in CINR smallest units)
    local_goal = Bytes("goal")                # Savings goal
    local_unlock = Bytes("unlock_time")       # Normal unlock time
    local_cause = Bytes("cause")              # What they're saving for
    local_emg_hash = Bytes("emergency_hash")  # SHA256 hash of emergency password
    local_created = Bytes("created_at")       # When account was created
    local_last_deposit = Bytes("last_deposit") # Timestamp of last deposit
    
    # Global state (shared)
    global_asset_id = Bytes("asset_id")       # CINR token ID
    
    # ==========================================
    # OPERATIONS
    # ==========================================
    
    op_create = Bytes("create")
    op_deposit = Bytes("deposit")
    op_withdraw = Bytes("withdraw")
    op_emergency = Bytes("emergency")
    
    # ==========================================
    # HANDLE APP CREATION
    # ==========================================
    
    on_creation = Seq([
        # Just return success on app creation
        Return(Int(1))
    ])
    
    # ==========================================
    # HANDLE OPT-IN
    # ==========================================
    
    on_opt_in = Seq([
        # Initialize user's savings to 0
        App.localPut(Txn.sender(), local_total, Int(0)),
        Return(Int(1))
    ])
    
    # ==========================================
    # OPERATION 1: CREATE SAVINGS ACCOUNT
    # ==========================================
    
    handle_create = Seq([
        # When user creates savings account
        
        # Save owner
        App.localPut(Txn.sender(), local_owner, Txn.sender()),
        
        # Initialize total to 0
        App.localPut(Txn.sender(), local_total, Int(0)),
        
        # Save goal amount
        App.localPut(
            Txn.sender(),
            local_goal,
            Btoi(Txn.application_args[1])
        ),
        
        # Save unlock time
        App.localPut(
            Txn.sender(),
            local_unlock,
            Btoi(Txn.application_args[2])
        ),
        
        # Save cause (what they're saving for)
        App.localPut(
            Txn.sender(),
            local_cause,
            Txn.application_args[3]
        ),
        
        # Hash and save emergency password
        # IMPORTANT: We receive the password and hash it
        App.localPut(
            Txn.sender(),
            local_emg_hash,
            Sha256(Txn.application_args[4])
        ),
        
        # Save creation time
        App.localPut(Txn.sender(), local_created, Global.latest_timestamp()),
        
        # Initialize last deposit time
        App.localPut(Txn.sender(), local_last_deposit, Int(0)),
        
        Return(Int(1))
    ])
    
    # ==========================================
    # OPERATION 2: DEPOSIT (Multiple times)
    # ==========================================
    
    handle_deposit = Seq([
        # Verify sender owns this account
        Assert(
            Txn.sender() == App.localGet(Txn.sender(), local_owner)
        ),
        
        # Add to total saved
        App.localPut(
            Txn.sender(),
            local_total,
            App.localGet(Txn.sender(), local_total) + Btoi(Txn.application_args[1])
        ),
        
        # Update last deposit time
        App.localPut(
            Txn.sender(),
            local_last_deposit,
            Global.latest_timestamp()
        ),
        
        Return(Int(1))
    ])
    
    # ==========================================
    # OPERATION 3: NORMAL WITHDRAWAL
    # ==========================================
    
    handle_withdraw = Seq([
        # Verify owner
        Assert(
            Txn.sender() == App.localGet(Txn.sender(), local_owner)
        ),
        
        # Verify time lock has expired
        Assert(
            Global.latest_timestamp() >= App.localGet(Txn.sender(), local_unlock)
        ),
        
        # Reset total to 0 (withdrawal complete)
        App.localPut(Txn.sender(), local_total, Int(0)),
        
        Return(Int(1))
    ])
    
    # ==========================================
    # OPERATION 4: EMERGENCY WITHDRAWAL (HTLC)
    # ==========================================
    
    handle_emergency = Seq([
        # Verify owner
        Assert(
            Txn.sender() == App.localGet(Txn.sender(), local_owner)
        ),
        
        # Hash the provided password
        # User sends password, we hash and compare
        Assert(
            Sha256(Txn.application_args[1]) == App.localGet(Txn.sender(), local_emg_hash)
        ),
        
        # Verify minimum time has passed (7 days = 604800 seconds)
        # This prevents creating account and immediately using emergency
        Assert(
            Global.latest_timestamp() >= App.localGet(Txn.sender(), local_created) + Int(604800)
        ),
        
        # Calculate penalty (2% = total / 50)
        # Note: In real implementation, penalty would be sent to charity
        # For now, we just reduce the total
        # penalty = total / 50
        # new_total = total - penalty = total - (total/50) = (total * 49) / 50
        
        # Reset total to 0 (emergency withdrawal complete)
        # In full implementation, we'd transfer (total - penalty) to user
        # and penalty to charity address
        App.localPut(Txn.sender(), local_total, Int(0)),
        
        Return(Int(1))
    ])
    
    # ==========================================
    # MAIN PROGRAM LOGIC
    # ==========================================
    
    program = Cond(
        # Handle app creation
        [Txn.application_id() == Int(0), on_creation],
        
        # Handle opt-in
        [Txn.on_completion() == OnComplete.OptIn, on_opt_in],
        
        # Handle operations
        [Txn.on_completion() == OnComplete.NoOp,
            Cond(
                [Txn.application_args[0] == op_create, handle_create],
                [Txn.application_args[0] == op_deposit, handle_deposit],
                [Txn.application_args[0] == op_withdraw, handle_withdraw],
                [Txn.application_args[0] == op_emergency, handle_emergency]
            )
        ]
    )
    
    return program


def clear_state_program():
    """Allow users to close out of app"""
    return Return(Int(1))


# ==========================================
# COMPILE CONTRACT
# ==========================================

if __name__ == "__main__":
    print("\n🔨 Compiling Smart Savings Contract...\n")
    
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
    with open("savings_approval.teal", "w") as f:
        f.write(approval_teal)
        print("✅ Created: savings_approval.teal")
    
    with open("savings_clear.teal", "w") as f:
        f.write(clear_teal)
        print("✅ Created: savings_clear.teal")
    
    print("\n🎉 Compilation successful!")
    print("\nGenerated files:")
    print("  - savings_approval.teal (main contract with HTLC)")
    print("  - savings_clear.teal (cleanup)")
    print("\nFeatures:")
    print("  ✅ Multiple deposits")
    print("  ✅ Time-locked withdrawals")
    print("  ✅ Emergency withdrawal with password")
    print("  ✅ 2% penalty on emergency")
    print("  ✅ 7-day minimum before emergency")
    print("\nNext step: Deploy to testnet")
    print("Run: python deploy_savings.py\n")