from pikepdf import Pdf
from pathlib import WindowsPath
from types import GenericAlias
from tqdm import tqdm
import random
import sys
import os
import keyboard

def order_select_screen_list(input_path: list[str], cursor: int, order: list[int], cursor_display=True):
	# 画面をクリアして再描画
	os.system('cls')
	for i, path in enumerate(input_path):
		# カーソル位置と選択された順番を表示
		if cursor == i and cursor_display:
			print('> ', end='')
		elif order[i] != -1:
			print(f'{order[i]+1} ', end='')
		else:
			print('  ', end='')
		print(path)

def order_select_screen_select(input_path: list[str], cursor: int, order: list[int]):
	order_select_screen_list(input_path, cursor, order)
	# 操作説明を表示
	print('-'*10)
	print('上下キーでカーソル移動 Enterで選択 escで終了')
	print('順番を決めなかったpdfファイルはランダムで順番が決まります')

def is_num(s):
    # 文字列が数値かどうかをチェック
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

def order_select_screen_input(input_path: list[str], cursor: int, order: list[int]) -> int:
	while True:
		# カーソル位置を非表示にして再描画
		order_select_screen_list(input_path, cursor, order, cursor_display=False)
		print('-'*10)
		order_num = input(f"何番目にしますか？[1~{len(input_path)}] :")
		if is_num(order_num):
			order_num = int(order_num)
			# 入力された順番を設定
			if 1 <= order_num <= len(input_path):
				if order_num-1 in order:
					order[order.index(order_num-1)] = -1
				order[cursor] = order_num-1
				return order

def order_select(input_path: list[str]) -> list[int]:
	cursor = 0
	order = [-1 for _ in range(len(input_path))]
	while True:
		order_select_screen_select(input_path, cursor, order)
		get_key = keyboard.read_event()
		# カーソルを上に移動
		if get_key.event_type == keyboard.KEY_UP and get_key.name == 'up':
			if cursor-1 >= 0:
				cursor = cursor - 1
		# カーソルを下に移動
		elif get_key.event_type == keyboard.KEY_UP and get_key.name == 'down':
			if cursor+1 < len(input_path):
				cursor = cursor + 1
		# Enterキーで順番を入力
		elif get_key.event_type == keyboard.KEY_DOWN and get_key.name == 'enter':
			order = order_select_screen_input(input_path, cursor, order)
		# Escキーで終了し、ランダム順に設定
		elif get_key.event_type == keyboard.KEY_DOWN and get_key.name == 'esc':
			order_set = set(order)
			order_set.remove(-1)
			not_select_num = set(range(len(input_path))) - order_set
			not_select_num = list(not_select_num)
			random.shuffle(not_select_num)
			for i, v in enumerate(order):
				if v == -1:
					order[i] = not_select_num.pop()
			os.system('cls')
			return order

def merge(order: dict[int, str], output_path: WindowsPath):
	dst = Pdf.new() # 空のpdfを作成

	for i in tqdm(range(len(order))):
		pdf_file = order[i]
		try:
			with Pdf.open(pdf_file) as reader:
				# ページを追加
				dst.pages.extend(reader.pages)
				# 奇数ページの場合、白紙ページを追加
				if len(reader.pages) % 2 == 1:
					dst.add_blank_page()
		except AttributeError as e:
			print("pdfの作成に失敗しました")
			print(e)
			print(f"{pdf_file}のpdf処理で失敗")
	dst.save(output_path) # 保存
	print(f"Done! {output_path}")

if __name__ == "__main__":
	os.system('cls')
	try:
		# 入力ディレクトリを取得
		pdf_dir_path = sys.argv[1]
	except IndexError:
		while True:
			pdf_dir_path = input("入力のディレクトリのpathを入力してください: ")
			pdf_dir_path = WindowsPath(pdf_dir_path)
			if pdf_dir_path.is_dir():
				break
	# 指定ディレクトリからpdfファイルを取得
	pdf_file_paths = list(pdf_dir_path.glob("**/*.pdf"))
	if pdf_file_paths is None:
		print("pdfが見つかりませんでした...")

	try:
		# 出力ディレクトリを取得
		output_dir_path = sys.argv[2]
	except IndexError:
		while True:
			output_dir_path = input("出力のディレクトリのpathを入力してください(空白でカレントディレクトリ): ")
			output_dir_path = WindowsPath(output_dir_path)
			if output_dir_path == None:
				output_dir_path = WindowsPath.cwd()
			if output_dir_path.is_dir():
				break

	# 出力ファイルパスを設定
	dir_name = pdf_dir_path.name
	output_dir_path = WindowsPath(output_dir_path) / WindowsPath(f"{dir_name}_merged.pdf")

	order = []
	while True:
		# 順番設定をユーザーに確認
		select_flag = input("pdfの順番を設定しますか？[y/n]")
		if select_flag == 'y':
			order = order_select(pdf_file_paths)
			break
		elif select_flag == 'n':
			order = list(range(len(pdf_file_paths)))
			random.shuffle(order)
			break
	# 順番とパスを辞書にまとめる
	order_dict = {ord: path for path, ord in zip(pdf_file_paths, order)}

	# マージ処理を実行
	merge(order_dict, output_dir_path)
