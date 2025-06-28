# CBR


# 🧠 Sistem Case-Based Reasoning untuk Putusan Pidana Perpajakan

Sistem ini membangun mesin pencarian kasus hukum serupa berbasis dokumen putusan pengadilan. Sistem menggunakan pendekatan **CBR (Case-Based Reasoning)** dan menyediakan dua metode retrieval:
- 🔹 TF-IDF
- 🔸 IndoBERT (Embedding)

---

## 📦 Struktur Proyek

```
project/
├── data/
│   ├── cleaned_txt/       # hasil preprocessing .txt dari file PDF
│   ├── processed/         # hasil ekstraksi metadata & vektor
│   └── eval/
│       └── queries.json   # query evaluasi + ground truth
├── sample.ipynb           # notebook utama (TF-IDF & BERT)
└── README.md
```

---

## 🛠️ 1. Instalasi Awal

Install Python packages:

```bash
pip install transformers torch scikit-learn pandas numpy matplotlib tqdm
```

Jika ingin ekstraksi dari PDF:

```bash
pip install pdfplumber
```

---

## 🧹 2. Preprocessing Teks

Jika kamu mulai dari PDF:
- Convert file ke `.txt`
- Lalu bersihkan dari header/footer

```python
import os

folder_pdf = "data/pdf/"
folder_txt = "data/cleaned_txt/"

os.makedirs(folder_txt, exist_ok=True)

for file in os.listdir(folder_pdf):
    if file.endswith(".pdf"):
        teks = pdf_ke_teks(os.path.join(folder_pdf, file))
        teks_bersih = bersihkan_teks(teks)
        with open(os.path.join(folder_txt, file.replace(".pdf", ".txt")), "w", encoding="utf-8") as f:
            f.write(teks_bersih)
```

Jika kamu sudah punya `cleaned_txt/`, lanjut ke vektorisasi.

---

## 📐 3. Vektorisasi Dokumen

### 🔹 A. TF-IDF

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=1000, stop_words='indonesian')
X_tfidf = vectorizer.fit_transform(docs)
```

Buat fungsi retrieval:

```python
def retrieve_tfidf(query, k=5):
    query_vec = vectorizer.transform([query])
    sims = cosine_similarity(query_vec, X_tfidf).flatten()
    top_k = sims.argsort()[-k:][::-1]
    return [(filenames[i], sims[i]) for i in top_k]
```

### 🔸 B. IndoBERT Embedding

```python
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p1")
model = AutoModel.from_pretrained("indobenchmark/indobert-base-p1")

def bert_embed(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
```

Lalu buat fungsi:

```python
def retrieve_bert(query, k=5):
    q_vec = bert_embed(query)
    sims = cosine_similarity([q_vec], vectors).flatten()
    top_k = sims.argsort()[-k:][::-1]
    return [filenames[i] for i in top_k]
```

---

## 🔍 4. Evaluasi Query

### 🔖 queries.json format:

```json
[
  {
    "query": "Terdakwa tidak menyampaikan SPT Tahunan...",
    "ground_truth": ["putusan_01.txt"]
  }
]
```

Letakkan di: `data/eval/queries.json`

### 🔬 Evaluasi Fungsi:

```python
def evaluate_retrieval(method_name, retrieve_fn, queries, k=5):
    total, match = len(queries), 0
    for q in queries:
        pred = retrieve_fn(q["query"], k)
        pred_files = [p[0] if isinstance(p, tuple) else p for p in pred]
        if any(gt in pred_files for gt in q["ground_truth"]):
            match += 1
    print(f"🔍 {method_name} Accuracy@{k}: {match}/{total} = {match/total:.2%}")
```

Contoh pemanggilan:

```python
evaluate_retrieval("TF-IDF", retrieve_tfidf, queries, k=5)
evaluate_retrieval("BERT", retrieve_bert, queries, k=5)
```

---

## 📊 5. Visualisasi Perbandingan (Opsional)

```python
import matplotlib.pyplot as plt

methods = ['TF-IDF', 'BERT']
scores = [acc_tfidf, acc_bert]

plt.bar(methods, scores, color=['skyblue', 'orange'])
plt.ylabel("Accuracy@5")
plt.title("Perbandingan TF-IDF vs IndoBERT")
plt.show()
```

---

## ✅ Output Final yang Harus Kamu Punya

| File/Folder                         | Keterangan                                   |
|------------------------------------|----------------------------------------------|
| `data/cleaned_txt/`                | Teks putusan bersih                          |
| `data/processed/cases.csv`         | Metadata terstruktur                         |
| `data/eval/queries.json`           | Query evaluasi + ground truth                |
| `retrieve_tfidf()` / `retrieve_bert()` | Fungsi retrieval kasus                      |
| `evaluate_retrieval()`             | Fungsi evaluasi Accuracy@k                   |
