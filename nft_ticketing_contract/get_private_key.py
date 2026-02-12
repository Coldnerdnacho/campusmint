from algosdk import mnemonic

# Paste your 25 words here (keep the quotes)
my_mnemonic = "settle essay render hen town filter awesome vague decrease blind craft when lizard deal betray struggle source gun absent capable ranch grab rocket detect"

# Convert to private key
private_key = mnemonic.to_private_key(my_mnemonic)
print("Your private key:", private_key)