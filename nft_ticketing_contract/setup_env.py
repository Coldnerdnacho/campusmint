# Read wallet info
with open("NEW_WALLET_INFO.txt", "r") as f:
    lines = f.readlines()

# Extract mnemonic
mnemonic = None
for i, line in enumerate(lines):
    if "25-Word Mnemonic:" in line:
        mnemonic = lines[i + 1].strip()
        break

if not mnemonic:
    print("❌ Could not find mnemonic in file")
    exit()

# Create .env file
env_content = f'''CREATOR_MNEMONIC="{mnemonic}"
ALGOD_TOKEN="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ALGOD_SERVER="https://testnet-api.algonode.cloud"
ALGOD_PORT=""
'''

with open(".env", "w") as f:
    f.write(env_content)

print("✅ Created .env file")
print(f"✅ Mnemonic has {len(mnemonic.split())} words")
print("\nVerify with: type .env\n")