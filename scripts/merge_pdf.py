from pikepdf import Pdf
from pathlib import Path
from types import GenericAlias
import random
import sys
import os

def merge(input_path:list[str],output_path:Path, order:list[int]):
	dst = Pdf.new() # 空のpdf

	for i in order:
		pdf_file = pdf_file_paths[i]
		try:
			with Pdf.open(pdf_file) as reader:
				dst.pages.extend(reader.pages)
				if len(reader.pages) % 2 == 1:
					dst.add_blank_page()
		except AttributeError as e:
			print("pdfの作成に失敗しました")
			print(e)
			print(f"{pdf_file}のpdf処理で失敗")
	dst.save(output_path)
	print(f"Done! {output_path}")

if __name__ == "__main__":
	try:
		pdf_dir_path = sys.argv[1]
	except IndexError:
		while True:
			pdf_dir_path = input("入力のディレクトリのpathを入力してください: ")
			pdf_dir_path = Path(pdf_dir_path)
			if pdf_dir_path.is_dir():
				break
	pdf_file_paths = list(pdf_dir_path.glob("**/*.pdf")) # input_pathからpdfファイルを探す

	try:
		output_dir_path = sys.argv[2]
	except IndexError:
		while True:
			output_dir_path = input("出力のディレクトリのpathを入力してください(空白でカレントディレクトリ): ")
			if output_dir_path == None:
				output_dir_path = Path.cwd()
			if output_dir_path.is_dir():
				break

	dir_name = pdf_dir_path.name
	output_dir_path = Path(output_dir_path) / Path(f"{dir_name}_merged.pdf")

	merge(pdf_file_paths, output_dir_path, random.shuffle(list(range(len(pdf_file_paths)))))
