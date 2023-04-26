import pypdf
from pathlib import Path
import sys

if __name__ == "__main__":
	pdf_dir_path = Path(sys.argv[1])
	dir_name = pdf_dir_path.name
	if pdf_dir_path.is_dir() :
		merger = pypdf.PdfMerger()
		for pdf_file in pdf_dir_path.glob("**/*.pdf"):
			merger.append(pdf_file)
		merger.write(f"./{dir_name}_merged.pdf")
		merger.close()
	else:
		raise ValueError("The argument must be a directory path.")