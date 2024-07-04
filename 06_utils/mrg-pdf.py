import PyPDF2

def merge_pdfs(pdf_list, output_path):
    pdf_merger = PyPDF2.PdfMerger()

    for pdf in pdf_list:
        pdf_merger.append(pdf)

    with open(output_path, 'wb') as output_pdf:
        pdf_merger.write(output_pdf)

# List of PDF files to merge
pdfs_to_merge = ['primary.pdf', 'additional.pdf']

# Output path for the merged PDF
output_file = 'merged.pdf'

# Merge the PDFs
merge_pdfs(pdfs_to_merge, output_file)
