import pypdf
from pathlib import Path
import sys
import os

if __name__ == "__main__":
	pdf_dir_path = Path(sys.argv[1])
	dir_name = pdf_dir_path.name
	if pdf_dir_path.is_dir() :
		dst = pypdf.PdfWriter()
		for pdf_file in pdf_dir_path.glob("**/*.pdf"):
			reader = pypdf.PdfReader(pdf_file)
			for page in reader.pages:
				dst.add_page(page)
			if len(reader.pages) % 2 == 1:
				dst.add_blank_page()
		dst.write(f"{os.getcwd()}/{dir_name}_merged.pdf")
		dst.close()
	else:
		raise ValueError("The argument must be a directory path.")