#!/usr/bin/env python3
import logging
import os
import sys
import subprocess

logger = logging.getLogger(__name__)

def convert_pptx_to_png(input_pptx_file):
    # Convert PPTX to PDF, writes to cur dir
    logger.info('reading pptx %s', input_pptx_file)
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', input_pptx_file])

    out_dir = os.path.splitext(input_pptx_file)[0]
    if not os.path.exists(out_dir):
        logger.info('creating output dir', out_dir)
        os.makedirs(out_dir)

    # Convert PDF to PNG
    base_file = os.path.splitext(os.path.split(input_pptx_file)[1])[0]
    pdf_file = f'{base_file}.pdf'
    logger.info('converting pdf %s to images', pdf_file)
    subprocess.run(['pdftoppm', '-jpeg', pdf_file, os.path.join(out_dir, base_file)])

    # Clean up the intermediate PDF file
    os.remove(pdf_file)

    print("Conversion completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_pptx_to_png.py <input_pptx_file>")
        sys.exit(1)

    input_pptx_file = sys.argv[1]
    convert_pptx_to_png(input_pptx_file)

