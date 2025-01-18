import tkinter as tk
from tkinter import ttk, filedialog
from configparser import ConfigParser
import os

# 設定ファイルのパス
SETTINGS_FILE = "setting.ini"

# INIファイルを読み込む関数
def load_ini_file(file_path):
    config = ConfigParser()
    config.read(file_path, encoding='ANSI')  # ANSIエンコーディングで読み込む
    return config

# 設定を保存する関数
def save_settings():
    settings = ConfigParser()
    settings['LAST_USED'] = {
        'directory': dir_var.get()
    }
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        settings.write(f)

# 設定を読み込む関数
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        settings = ConfigParser()
        settings.read(SETTINGS_FILE, encoding='utf-8')
        if 'LAST_USED' in settings:
            return settings['LAST_USED']
    return {}

# ディレクトリ選択時の処理
def on_directory_select():
    dir_path = filedialog.askdirectory()
    if dir_path:
        dir_var.set(dir_path)
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
            message_var.set('')
            save_settings()
        except Exception as e:
            message_var.set(f"Error: {e}")

# ファイル選択時の処理
def on_file_select(event):
    file_name = file_var.get()
    if file_name:
        file_path = next((f for f in file_paths if os.path.basename(f) == file_name), None)
        if file_path:
            try:
                global config
                config = load_ini_file(file_path)
                section_menu['values'] = [section for section in config.sections()]
                section_var.set('')
                parameter_menu['values'] = []
                parameter_var.set('')
                value_var.set('')
                message_var.set('')
            except Exception as e:
                message_var.set(f"Error: {e}")

# セクション選択時の処理
def on_section_select(event):
    section = section_var.get()
    parameter_menu['values'] = list(config[section].keys())
    parameter_var.set('')
    value_var.set('')

# パラメータ選択時の処理
def on_parameter_select(event):
    section = section_var.get()
    parameter = parameter_var.get()
    value = config[section].get(parameter, '')
    value_var.set(value)

# 値を保存する処理
def save_value():
    section = section_var.get()
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
                with open(file_path, 'w', encoding='ANSI') as configfile:
                    config.write(configfile)
                message_var.set(f"Value saved: {new_value}")
        except Exception as e:
            message_var.set(f"Error: {e}")
    else:
        message_var.set("Invalid data")

# メインウィンドウの作成
root = tk.Tk()
root.title("ACParts-bin Editor")

# 保存された設定をロード
settings = load_settings()

# ディレクトリ表示ラベル
dir_label = ttk.Label(root, text="Directory:")
dir_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

dir_var = tk.StringVar(value=settings.get('directory', ''))
dir_display = ttk.Entry(root, textvariable=dir_var, state="readonly", width=50)
dir_display.grid(row=0, column=1, padx=5, pady=5)

# ディレクトリ選択ボタン
dir_button = ttk.Button(root, text="Select Directory", command=on_directory_select)
dir_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

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
save_button.grid(row=5, column=0, columnspan=3, pady=5)

# メッセージ表示ラベル
message_var = tk.StringVar()
message_label = ttk.Label(root, textvariable=message_var, foreground="blue")
message_label.grid(row=6, column=0, columnspan=3, pady=5)

# 初期化処理（ディレクトリが設定されている場合）
if dir_var.get():
    try:
        file_paths = [os.path.join(dir_var.get(), f) for f in os.listdir(dir_var.get()) if f.endswith('.txt')]
        file_menu['values'] = [os.path.basename(f) for f in file_paths]
    except Exception as e:
        message_var.set(f"Error: {e}")

# ウィンドウを開始
root.mainloop()