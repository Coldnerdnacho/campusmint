from algosdk.v2client import algod
from algosdk import transaction
from algosdk.transaction import ApplicationCreateTxn, StateSchema, wait_for_confirmation
from pyteal import *
import base64
import time
import json

# Load wallet
with open('python_wallet.json', 'r') as f:
    wallet = json.load(f)

PRIVATE_KEY = wallet['private_key']
student_address = wallet['address']

algod_client = algod.AlgodClient('', 'https://testnet-api.algonode.cloud')

# ALGO-ONLY VAULT CONTRACT
def approval_program():
    return Cond(
        [Txn.application_id() == Int(0), Seq([
            App.globalPut(Bytes('owner'), Txn.sender()),
            App.globalPut(Bytes('unlock_time'), Btoi(Txn.application_args[0])),
            App.globalPut(Bytes('beneficiary'), Txn.application_args[1]),
            App.globalPut(Bytes('amount'), Int(0)),
            Approve()
        ])],
        [Txn.application_args[0] == Bytes('deposit'), Seq([
            Assert(Global.group_size() == Int(2)),
            Assert(Gtxn[1].type_enum() == TxnType.Payment),
            Assert(Gtxn[1].receiver() == Global.current_application_address()),
            App.globalPut(Bytes('amount'), App.globalGet(Bytes('amount')) + Gtxn[1].amount()),
            Approve()
        ])],
        [Txn.application_args[0] == Bytes('withdraw'), Seq([
            Assert(Txn.sender() == App.globalGet(Bytes('beneficiary'))),
            Assert(Global.latest_timestamp() >= App.globalGet(Bytes('unlock_time'))),
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: App.globalGet(Bytes('beneficiary')),
                TxnField.amount: App.globalGet(Bytes('amount')),
            }),
            InnerTxnBuilder.Submit(),
            App.globalPut(Bytes('amount'), Int(0)),
            Approve()
        ])]
    )

def clear_program():
    return Approve()

# Compile
approval = base64.b64decode(algod_client.compile(compileTeal(approval_program(), mode=Mode.Application, version=6))['result'])
clear = base64.b64decode(algod_client.compile(compileTeal(clear_program(), mode=Mode.Application, version=6))['result'])

# Deploy with 1 MINUTE lock
unlock_time = int(time.time()) + 60
beneficiary = student_address

params = algod_client.suggested_params()

# FIXED: Use 0 instead of OnComplete enum
txn = ApplicationCreateTxn(
    sender=student_address,
    sp=params,
    on_complete=0,  # 0 = NoOp
    approval_program=approval,
    clear_program=clear,
    global_schema=StateSchema(2, 2),
    local_schema=StateSchema(0, 0),
    app_args=[unlock_time.to_bytes(8, 'big'), beneficiary],
    note=b''
)

signed = txn.sign(PRIVATE_KEY)
txid = algod_client.send_transaction(signed)
wait_for_confirmation(algod_client, txid, 4)

app_id = algod_client.pending_transaction_info(txid)['application-index']
app_address = transaction.logic.get_application_address(app_id)

print('=' * 50)
print('✅ 1-MINUTE VAULT DEPLOYED!')
print('=' * 50)
print(f'App ID: {app_id}')
print(f'App Address: {app_address}')
print(f'Unlocks at: {time.ctime(unlock_time)}')
print(f'⏰ Time remaining: {unlock_time - int(time.time())} seconds')
print('=' * 50)
print('\n📝 Save these:')
print(f'VAULT_1MIN_ID = {app_id}')
print(f'VAULT_1MIN_ADDRESS = {app_address}')