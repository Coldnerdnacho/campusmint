from algosdk.v2client import algod
from algosdk import transaction
from algosdk.transaction import ApplicationCallTxn, PaymentTxn, wait_for_confirmation
import base64
import json
import time

# Testnet connection
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

# Load wallet
with open("python_wallet.json", "r") as f:
    wallet = json.load(f)

PRIVATE_KEY = wallet["private_key"]
student_address = wallet["address"]

# New pure ALGO vault
APP_ID = 755423706
APP_ADDRESS = "UB6IASA7HXWI5WHMF5YHEICY26JWG2YXYOVFLCGTOCQUNOPBLGG73JMJ4Y"

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

print("=" * 50)
print("💰 TESTING PURE ALGO VAULT")
print("=" * 50)

# Check initial state
app_info = algod_client.application_info(APP_ID)
for item in app_info['params']['global-state']:
    key = base64.b64decode(item['key']).decode('utf-8')
    value = item['value']
    if key == 'amount':
        print(f"Initial balance: {value['uint'] / 1_000_000} ALGO")
    elif key == 'unlock_time':
        unlock = value['uint']
        now = int(time.time())
        if now < unlock:
            print(f"🔒 Locked - unlocks in {unlock - now} seconds")

# Deposit 2 ALGO
print("\n📤 Depositing 2 ALGO...")
params = algod_client.suggested_params()

app_call = ApplicationCallTxn(
    sender=student_address,
    sp=params,
    index=APP_ID,
    on_complete=transaction.OnComplete.NoOpOC,
    app_args=["deposit"]
)

payment = PaymentTxn(
    sender=student_address,
    sp=params,
    receiver=APP_ADDRESS,
    amt=2_000_000  # 2 ALGO
)

gid = transaction.calculate_group_id([app_call, payment])
app_call.group = gid
payment.group = gid

signed_app_call = app_call.sign(PRIVATE_KEY)
signed_payment = payment.sign(PRIVATE_KEY)

txid = algod_client.send_transactions([signed_app_call, signed_payment])
wait_for_confirmation(algod_client, txid, 4)
print(f"✅ Deposited! Tx: https://testnet.algoexplorer.io/tx/{txid}")

# Check balance after deposit
time.sleep(2)
app_info = algod_client.application_info(APP_ID)
for item in app_info['params']['global-state']:
    key = base64.b64decode(item['key']).decode('utf-8')
    if key == 'amount':
        print(f"\n💰 New vault balance: {item['value']['uint'] / 1_000_000} ALGO")
    elif key == 'unlock_time':
        unlock = item['value']['uint']
        now = int(time.time())
        if now < unlock:
            print(f"⏰ Time remaining: {unlock - now} seconds")

print("\n✅ Test complete - vault is working!")
print("⏳ Wait 60 seconds, then run withdraw command")