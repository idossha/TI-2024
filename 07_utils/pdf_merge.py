#!/usr/bin/env python3
import PyPDF2
import argparse

def merge_pdfs(pdf1, pdf2, output_path):
    pdf_merger = PyPDF2.PdfMerger()

    pdf_merger.append(pdf1)
    pdf_merger.append(pdf2)

    with open(output_path, 'wb') as output_pdf:
        pdf_merger.write(output_pdf)

def main():
    parser = argparse.ArgumentParser(description="Merge two PDF files into one.")
    parser.add_argument('pdf1', type=str, help='First PDF file to merge')
    parser.add_argument('pdf2', type=str, help='Second PDF file to merge')
    parser.add_argument('output', type=str, help='Output path for the merged PDF')

    args = parser.parse_args()

    merge_pdfs(args.pdf1, args.pdf2, args.output)

if __name__ == "__main__":
    main()
