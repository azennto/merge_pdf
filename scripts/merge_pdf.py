from pikepdf import Pdf
from pathlib import Path
from types import GenericAlias
import random
import sys
import os
import keyboard

def order_select_screen_list(input_path:list[str], cursor:int, order:list[int], cursor_display=True):
	os.system('cls')
	for i, path in enumerate(input_path):
		if cursor == i and cursor_display:
			print('> ', end='')
		elif order[i] != -1:
			print(f'{order[i]+1} ', end='')
		else:
			print('  ', end='')
		print(path)

def order_select_screen_select(input_path:list[str], cursor:int, order:list[int]):
	order_select_screen_list(input_path, cursor, order)
	print('-'*10)
	print('上下キーでカーソル移動 Enterで選択 escで終了')
	print('順番を決めなかったpdfファイルはランダムで順番が決まります')

def is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

def order_select_screen_input(input_path:list[str], cursor:int, order:list[int]) -> int:
	while True:
		order_select_screen_list(input_path, cursor, order, cursor_display=False)
		print('-'*10)
		print(order)
		order_num = input(f"何番目にしますか？[1~{len(input_path)}] :")
		if is_num(order_num):
			order_num = int(order_num)
			if 1 <= order_num <= len(input_path):
				if order_num-1 in order:
					order[order.index(order_num-1)] = -1
				order[cursor] = order_num-1
				return order

def order_select(input_path:list[str]) -> list[int]:
	cursor = 0
	order = [-1 for _ in range(len(input_path))]
	while True:
		order_select_screen_select(input_path, cursor, order)
		get_key = keyboard.read_event()
		if get_key.event_type == keyboard.KEY_UP and get_key.name == 'up':
			if cursor-1 >= 0:
				cursor = cursor - 1
		elif get_key.event_type == keyboard.KEY_UP and get_key.name == 'down':
			if cursor+1 < len(input_path):
				cursor = cursor + 1
		elif get_key.event_type == keyboard.KEY_DOWN and get_key.name == 'enter':
			order = order_select_screen_input(input_path, cursor, order)
		elif get_key.event_type == keyboard.KEY_DOWN and get_key.name == 'esc':
			order_set = set(order)
			order_set.remove(-1)
			not_select_num = set(range(len(input_path))) - order_set
			not_select_num = list(not_select_num)
			print(not_select_num)
			random.shuffle(not_select_num)
			for i, v in enumerate(order):
				if v == -1:
					order[i] = not_select_num.pop()

			print(order)
			return order

def merge(order:dict[int, str], output_path:Path):
	dst = Pdf.new() # 空のpdf

	for i in range(len(order)):
		pdf_file = order[i]
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
	os.system('cls')
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
			output_dir_path = Path(output_dir_path)
			if output_dir_path == None:
				output_dir_path = Path.cwd()
			if output_dir_path.is_dir():
				break

	dir_name = pdf_dir_path.name
	output_dir_path = Path(output_dir_path) / Path(f"{dir_name}_merged.pdf")

	order = []
	while True:
		select_flag = input("pdfの順番を設定しますか？[y/n]")
		if select_flag == 'y':
			order = order_select(pdf_file_paths)
			break
		elif select_flag == 'n':
			order = random.shuffle(list(range(len(pdf_file_paths))))
			break
	order_dict = {ord:path for path, ord in zip(pdf_file_paths, order)}
	print(order_dict)

	merge(order_dict, output_dir_path)
