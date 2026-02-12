from algosdk.v2client import algod
from algosdk import transaction
from algosdk.transaction import ApplicationCallTxn, PaymentTxn, wait_for_confirmation
import json

with open('python_wallet.json', 'r') as f:
    wallet = json.load(f)

PRIVATE_KEY = wallet['private_key']
student_address = wallet['address']

APP_ID = 755426130
APP_ADDRESS = 'CSSSMSWECYVRGKGFU2OP6RUQOCR3EFOVNFDNNUVHD6D3L3ZTWEAQLLOH6Q'

algod_client = algod.AlgodClient('', 'https://testnet-api.algonode.cloud')
params = algod_client.suggested_params()

# Withdraw call
app_call = ApplicationCallTxn(
    sender=student_address,
    sp=params,
    index=APP_ID,
    on_complete=0,
    app_args=['withdraw']
)

# Send 0 ALGO to self to meet group requirement
payment = PaymentTxn(
    sender=student_address,
    sp=params,
    receiver=student_address,
    amt=0
)

# Group them
gid = transaction.calculate_group_id([app_call, payment])
app_call.group = gid
payment.group = gid

# Sign and send
signed_app_call = app_call.sign(PRIVATE_KEY)
signed_payment = payment.sign(PRIVATE_KEY)

txid = algod_client.send_transactions([signed_app_call, signed_payment])
wait_for_confirmation(algod_client, txid, 4)

print('✅ WITHDRAWAL SUCCESSFUL! 1 ALGO returned!')
print(f'Transaction: https://testnet.algoexplorer.io/tx/{txid}')