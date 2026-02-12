from pyteal import *
from algosdk.v2client import algod
from algosdk import account, transaction
from algosdk.transaction import ApplicationCreateTxn, StateSchema, OnComplete, wait_for_confirmation
import base64
import time
import json

# Testnet connection
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

# ===== LOAD PYTHON WALLET =====
with open("python_wallet.json", "r") as f:
    wallet = json.load(f)

PRIVATE_KEY = wallet["private_key"]
student_address = wallet["address"]

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

# ===== PURE ALGO VAULT - NO ASSETS =====
def vault_approval_program():
    owner_key = Bytes("owner")
    unlock_time_key = Bytes("unlock_time")
    amount_key = Bytes("amount")
    beneficiary_key = Bytes("beneficiary")
    
    on_creation = Seq([
        App.globalPut(owner_key, Txn.sender()),
        App.globalPut(unlock_time_key, Btoi(Txn.application_args[0])),
        App.globalPut(beneficiary_key, Txn.application_args[1]),
        App.globalPut(amount_key, Int(0)),
        Approve()
    ])
    
    on_deposit = Seq([
        Assert(Global.group_size() == Int(2)),
        Assert(Gtxn[1].type_enum() == TxnType.Payment),
        Assert(Gtxn[1].receiver() == Global.current_application_address()),
        App.globalPut(amount_key, App.globalGet(amount_key) + Gtxn[1].amount()),
        Approve()
    ])
    
    on_withdraw = Seq([
        Assert(Txn.sender() == App.globalGet(beneficiary_key)),
        Assert(Global.latest_timestamp() >= App.globalGet(unlock_time_key)),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: App.globalGet(beneficiary_key),
            TxnField.amount: App.globalGet(amount_key),
        }),
        InnerTxnBuilder.Submit(),
        App.globalPut(amount_key, Int(0)),
        Approve()
    ])
    
    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.application_args[0] == Bytes("deposit"), on_deposit],
        [Txn.application_args[0] == Bytes("withdraw"), on_withdraw]
    )
    
    return program

def vault_clear_program():
    return Approve()

# Compile
approval_program_compiled = compileTeal(vault_approval_program(), mode=Mode.Application, version=6)
clear_program_compiled = compileTeal(vault_clear_program(), mode=Mode.Application, version=6)

# Compile using algod
approval_result = algod_client.compile(approval_program_compiled)
clear_result = algod_client.compile(clear_program_compiled)

approval_program = base64.b64decode(approval_result['result'])
clear_program = base64.b64decode(clear_result['result'])

# State schema - 2 uints (amount, unlock_time), 2 byte slices (owner, beneficiary)
global_schema = StateSchema(num_uints=2, num_byte_slices=2)
local_schema = StateSchema(num_uints=0, num_byte_slices=0)

# Deploy with 1 minute lock
unlock_time = int(time.time()) + 60
beneficiary = student_address

params = algod_client.suggested_params()

txn = ApplicationCreateTxn(
    sender=student_address,
    sp=params,
    on_complete=OnComplete.NoOpOC,
    approval_program=approval_program,
    clear_program=clear_program,
    global_schema=global_schema,
    local_schema=local_schema,
    app_args=[
        unlock_time.to_bytes(8, 'big'),
        beneficiary
    ]
)

signed_txn = txn.sign(PRIVATE_KEY)
txid = algod_client.send_transaction(signed_txn)
wait_for_confirmation(algod_client, txid, 4)

txn_info = algod_client.pending_transaction_info(txid)
app_id = txn_info['application-index']
app_address = transaction.logic.get_application_address(app_id)

print("=" * 50)
print("✅ PURE ALGO VAULT DEPLOYED!")
print("=" * 50)
print(f"App ID: {app_id}")
print(f"App Address: {app_address}")
print(f"Unlock time: {time.ctime(unlock_time)}")
print("=" * 50)
print("\n📝 Save these in accounts.txt:")
print(f"PURE_ALGO_VAULT_ID = {app_id}")
print(f"PURE_ALGO_VAULT_ADDRESS = {app_address}")