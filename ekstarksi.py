import os
import re
import pandas as pd

folder_txt = "data/cleaned_txt"
files = sorted([f for f in os.listdir(folder_txt) if f.endswith(".txt")])

def ekstrak_metadata(teks):
    # Nomor perkara
    no_perkara = re.search(r"(nomor|no\.)\s*perkara[:\s]*([A-Za-z0-9\/\.\-]+)", teks, re.IGNORECASE)
    
    # Tanggal
    tanggal = re.search(r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{4})\b", teks)
    
    # Pasal
    pasal = re.findall(r"pasal\s+\d+[A-Za-z]*\s*(?:ayat\s*\([^)]+\))?", teks, re.IGNORECASE)
    
    # Nama pihak (penggugat/tergugat/terdakwa)
    pihak = re.findall(r"(terdakwa|penggugat|tergugat)[:\-–]?\s*([A-Z][^\n\r]+)", teks, re.IGNORECASE)
    
    return {
        "no_perkara": no_perkara.group(2) if no_perkara else "",
        "tanggal": tanggal.group(1) if tanggal else "",
        "pasal": "; ".join(set(pasal)),
        "pihak": "; ".join([f"{p[0].capitalize()}: {p[1].strip()}" for p in pihak])
    }

def ekstrak_ringkasan_fakta(teks):
    match = re.search(r"(menimbang\s+bahwa.*?)(menimbang|mengingat|amar)", teks, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else teks[:700]

# Gabungkan semuanya
case_data = []

for idx, file in enumerate(files):
    with open(os.path.join(folder_txt, file), "r", encoding="utf-8") as f:
        teks = f.read()
    
    metadata = ekstrak_metadata(teks)
    ringkasan = ekstrak_ringkasan_fakta(teks)
    
    case_data.append({
        "case_id": idx + 1,
        "no_perkara": metadata["no_perkara"],
        "tanggal": metadata["tanggal"],
        "ringkasan_fakta": ringkasan,
        "pasal": metadata["pasal"],
        "pihak": metadata["pihak"],
        "text_full": teks[:3000]  # atau simpan seluruh teks
    })

# Simpan ke CSV
os.makedirs("data/processed", exist_ok=True)
df = pd.DataFrame(case_data)
df.to_csv("data/processed/cases.csv", index=False, encoding="utf-8-sig")
