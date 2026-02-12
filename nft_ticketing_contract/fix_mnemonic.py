from algosdk import mnemonic, wordlist

# Paste your 24 words here
my_24_words = "settle essay render hen town filter awesome vague decrease blind craft when lizard deal betray struggle source gun absent capable ranch grab rocket detect"

# Split into list
words = my_24_words.split()

print(f"You provided: {len(words)} words")

if len(words) != 24:
    print(f"❌ ERROR: You need exactly 24 words. You have {len(words)}")
    exit()

print("\n🔍 Finding the 25th word (checksum)...\n")

# Try all possible 25th words (there are 2048 words in the wordlist)
found = False
word_list = wordlist.word_list_raw().split("\n")

for possible_word in word_list:
    test_mnemonic = my_24_words + " " + possible_word
    try:
        # Try to convert to private key
        private_key = mnemonic.to_private_key(test_mnemonic)
        address = mnemonic.to_public_key(test_mnemonic)
        
        print("✅ FOUND IT!")
        print("="*70)
        print(f"\nYour COMPLETE 25-word mnemonic is:")
        print(f"\n{test_mnemonic}\n")
        print("="*70)
        print(f"\nThe 25th word is: {possible_word}")
        print("="*70)
        print(f"\nYour Address: {address}")
        print(f"\nYour Private Key: {private_key}")
        print("="*70)
        
        found = True
        break
    except:
        continue

if not found:
    print("❌ Could not find valid 25th word. Please check your 24 words are correct.")