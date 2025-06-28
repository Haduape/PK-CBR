from pdfminer.high_level import extract_text
import os

# Folder containing PDFs
pdf_folder = "CBR\Case"  
output_folder = "extracted_texts"  

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through each PDF in the folder
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        
        # Extract text
        text = extract_text(pdf_path)
        
        # Save to a .txt file with the same name as the PDF
        output_path = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"Extracted: {pdf_file}")

print("Done! All PDFs processed.")