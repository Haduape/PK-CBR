import re
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('indonesian'))

def bersihkan_teks(teks):
    teks = re.sub(r'\n+', ' ', teks)  # hilangkan baris kosong
    teks = re.sub(r'[^\w\s]', '', teks)  # hilangkan tanda baca
    teks = teks.lower()  # huruf kecil semua
    tokens = nltk.word_tokenize(teks)
    tokens = [t for t in tokens if t not in stop_words]
    return ' '.join(tokens)
