asset_id = 755378709

# Save without emojis (Windows-friendly)
with open("ASSET_ID.txt", "w", encoding='utf-8') as f:
    f.write(f"Campus INR Token - CampusMint Hackathon\n")
    f.write(f"="*50 + "\n\n")
    f.write(f"Asset ID: {asset_id}\n\n")
    f.write(f"AlgoExplorer Link:\n")
    f.write(f"https://testnet.algoexplorer.io/asset/{asset_id}\n\n")
    f.write(f"Token Details:\n")
    f.write(f"- Name: Campus INR\n")
    f.write(f"- Unit: CINR\n")
    f.write(f"- Supply: 1,000,000 CINR\n")
    f.write(f"- Decimals: 2\n\n")
    f.write(f"="*50 + "\n")
    f.write(f"SHARE THIS ASSET ID WITH YOUR ENTIRE TEAM!\n")

# Add to .env
with open(".env", "a", encoding='utf-8') as f:
    f.write(f"\nASSET_ID={asset_id}\n")

print("Asset ID saved to ASSET_ID.txt and .env")