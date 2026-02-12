from algosdk.v2client import algod
from algosdk import transaction
from algosdk.transaction import ApplicationDeleteTxn, wait_for_confirmation
import json

# Load wallet
with open('python_wallet.json', 'r') as f:
    wallet = json.load(f)

PRIVATE_KEY = wallet['private_key']
student_address = wallet['address']

algod_client = algod.AlgodClient('', 'https://testnet-api.algonode.cloud')

# List of old broken vaults to delete
old_apps = [755414328, 755414724, 755414948, 755423706, 755425047, 755426130]

print("🧹 Cleaning up old apps...")
print("=" * 50)

for app_id in old_apps:
    try:
        params = algod_client.suggested_params()
        txn = ApplicationDeleteTxn(
            sender=student_address,
            sp=params,
            index=app_id
        )
        signed = txn.sign(PRIVATE_KEY)
        txid = algod_client.send_transaction(signed)
        wait_for_confirmation(algod_client, txid, 4)
        print(f"✅ Deleted app: {app_id}")
    except Exception as e:
        print(f"❌ Could not delete {app_id}: {e}")

print("=" * 50)
print("✅ Cleanup complete!")