
import os
from fpdf import FPDF
from datetime import datetime


FINAL_BOOK_DIR = "../assets/final_book"
TXT_PATH = os.path.join(FINAL_BOOK_DIR, "final_book_latest.txt")

#text exists
if not os.path.exists(TXT_PATH):
    raise FileNotFoundError("-- 'final_book_latest.txt' not found. Run merging step first!")


with open(TXT_PATH, "r", encoding="utf-8") as f:
    book_content = f.read()

#pdf Setup
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Times", size=12)


paragraphs = book_content.split("\n\n")

for para in paragraphs:
    
    if para.strip() == "":
        continue
    pdf.multi_cell(0, 10, para.strip())
    pdf.ln()

#Save pdf
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
pdf_path = os.path.join(FINAL_BOOK_DIR, f"final_book_{timestamp}.pdf")
latest_path = os.path.join(FINAL_BOOK_DIR, "final_book_latest.pdf")

pdf.output(pdf_path)
pdf.output(latest_path)

print("-- PDF generated at:", pdf_path)
print("-- Also saved as latest at:", latest_path)
