import os
from pdf2image import convert_from_path


folder_path = './data/'
pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]


for pdf_file in pdf_files:
    
    pdf_path = os.path.join(folder_path, pdf_file)
    images = convert_from_path(pdf_path,poppler_path='C:/poppler-24.08.0/Library/bin',dpi=300)
    for i, image in enumerate(images):
        output_file = os.path.join('./png/', f"{os.path.splitext(pdf_file)[0]}_page_{i + 1}.png")
        image.save(output_file, 'PNG')
        print(f"Saved {output_file}")
