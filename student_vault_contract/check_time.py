from algosdk.v2client import algod
import base64
import time

algod_client = algod.AlgodClient('', 'https://testnet-api.algonode.cloud')
app_info = algod_client.application_info(755426130)

for item in app_info['params']['global-state']:
    key = base64.b64decode(item['key']).decode('utf-8')
    if key == 'unlock_time':
        unlock = item['value']['uint']
        now = int(time.time())
        print(f'⏰ Current time: {time.ctime(now)}')
        print(f'🔓 Unlock time: {time.ctime(unlock)}')
        print(f'⏳ Seconds remaining: {unlock - now}')
        print(f'✅ Ready to withdraw? {now >= unlock}')