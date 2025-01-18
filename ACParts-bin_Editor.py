import tkinter as tk
from tkinter import ttk, filedialog
from configparser import ConfigParser
import os

# INIファイルを読み込む関数
def load_ini_file(file_path):
    config = ConfigParser()
    config.read(file_path, encoding='ANSI')  # ANSIエンコーディングで読み込む
    return config

# セクションのラベルを取得する関数
def get_section_label(section, config):
    parts_name = config[section].get('PartsName', '')
    return f"{section}: {parts_name}" if parts_name else section

# ディレクトリ選択時の処理
def on_directory_select():
    dir_path = filedialog.askdirectory()
    if dir_path:
        try:
            global file_paths
            file_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.txt')]
            file_menu['values'] = [os.path.basename(f) for f in file_paths]
            file_var.set('')
            section_menu['values'] = []
            section_var.set('')
            parameter_menu['values'] = []
            parameter_var.set('')
            value_var.set('')
        except Exception as e:
            value_var.set(f"Error: {e}")

# ファイル選択時の処理
def on_file_select(event):
    file_name = file_var.get()
    if file_name:
        file_path = next((f for f in file_paths if os.path.basename(f) == file_name), None)
        if file_path:
            try:
                global config
                config = load_ini_file(file_path)
                section_menu['values'] = [get_section_label(section, config) for section in config.sections()]
                section_var.set('')
                parameter_menu['values'] = []
                parameter_var.set('')
                value_var.set('')
            except Exception as e:
                value_var.set(f"Error: {e}")

# セクション選択時の処理
def on_section_select(event):
    section_label = section_var.get()
    section = section_label.split(':')[0].strip()  # セクション名を抽出
    parameter_menu['values'] = list(config[section].keys())
    parameter_var.set('')
    value_var.set('')

# パラメータ選択時の処理
def on_parameter_select(event):
    section_label = section_var.get()
    section = section_label.split(':')[0].strip()  # セクション名を抽出
    parameter = parameter_var.get()
    value = config[section].get(parameter, '')
    value_var.set(value)

# 値を保存する処理
def save_value():
    section_label = section_var.get()
    section = section_label.split(':')[0].strip()  # セクション名を抽出
    parameter = parameter_var.get()
    new_value = value_var.get()

    if section and parameter and new_value:
        try:
            # 設定を更新
            config[section][parameter] = new_value
            # ファイルに保存
            file_name = file_var.get()
            file_path = next((f for f in file_paths if os.path.basename(f) == file_name), None)
            if file_path:
                with open(file_path, 'w', encoding='shift_jis') as configfile:
                    config.write(configfile)
                value_var.set(f"Value saved: {new_value}")
        except Exception as e:
            value_var.set(f"Error: {e}")
    else:
        value_var.set("Invalid data")

# メインウィンドウの作成
root = tk.Tk()
root.title("ACParts-bin Editor")

# ディレクトリ選択ボタン
dir_button = ttk.Button(root, text="Select Directory", command=on_directory_select)
dir_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

# ファイル選択
file_label = ttk.Label(root, text="File:")
file_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

file_var = tk.StringVar()
file_menu = ttk.Combobox(root, textvariable=file_var, state="readonly")
file_menu.grid(row=1, column=1, padx=5, pady=5)
file_menu.bind("<<ComboboxSelected>>", on_file_select)

# セクション選択
section_label = ttk.Label(root, text="Parts:")
section_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

section_var = tk.StringVar()
section_menu = ttk.Combobox(root, textvariable=section_var, state="readonly")
section_menu.grid(row=2, column=1, padx=5, pady=5)
section_menu.bind("<<ComboboxSelected>>", on_section_select)

# パラメータ選択
parameter_label = ttk.Label(root, text="Param:")
parameter_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

parameter_var = tk.StringVar()
parameter_menu = ttk.Combobox(root, textvariable=parameter_var, state="readonly")
parameter_menu.grid(row=3, column=1, padx=5, pady=5)
parameter_menu.bind("<<ComboboxSelected>>", on_parameter_select)

# 値表示（編集可能）
value_label = ttk.Label(root, text="Value:")
value_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

value_var = tk.StringVar()
value_entry = ttk.Entry(root, textvariable=value_var)
value_entry.grid(row=4, column=1, padx=5, pady=5)

# 保存ボタン
save_button = ttk.Button(root, text="Save", command=save_value)
save_button.grid(row=5, column=0, columnspan=2, pady=5)

# ウィンドウを開始
root.mainloop()
