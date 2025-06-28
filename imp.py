import os
import re
from tqdm import tqdm
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# ===== 1. FIRST-TIME SETUP =====
# Run this block ONCE to download all required NLTK data
print("Downloading NLTK resources...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)  # The missing resource
print("Download complete!")

# ===== 2. TEXT CLEANING FUNCTION =====
def bersihkan_teks(teks):
    """Clean Indonesian text with robust error handling"""
    try:
        # 1. Remove special chars/numbers (keep Indonesian letters)
        teks = re.sub(r'[^a-zA-Z\sÀ-ÿ]', '', teks)
        
        # 2. Convert to lowercase
        teks = teks.lower()
        
        # 3. Tokenize with fallback if punkt fails
        try:
            tokens = word_tokenize(teks)
        except:
            tokens = teks.split()  # Simple space-based fallback
            
        # 4. Load Indonesian stopwords
        stopwords_id = set(stopwords.words('indonesian'))
        
        # 5. Filter tokens
        clean_tokens = [t for t in tokens if t not in stopwords_id and len(t) > 2]
        
        return ' '.join(clean_tokens)
    
    except Exception as e:
        print(f"Error cleaning text: {str(e)}")
        return teks  # Return original text if cleaning fails

# ===== 3. PROCESS FILES =====
folder_txt = "CBR/data/extracted_texts/"
folder_cleaned = "CBR/data/cleaned/"
os.makedirs(folder_cleaned, exist_ok=True)

for nama_file in tqdm(os.listdir(folder_txt)):
    if nama_file.endswith(".txt"):
        try:
            with open(os.path.join(folder_txt, nama_file), "r", encoding="utf-8") as f:
                teks_mentah = f.read()
            
            teks_bersih = bersihkan_teks(teks_mentah)
            
            with open(os.path.join(folder_cleaned, nama_file), "w", encoding="utf-8") as f:
                f.write(teks_bersih)
                
        except Exception as e:
            print(f"Error processing {nama_file}: {str(e)}")
            continue