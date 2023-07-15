import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from collections import OrderedDict
from tkinterdnd2 import DND_FILES, TkinterDnD

def remove_duplicates():
    file_path = file_path_var.get()
    if file_path == "":
        messagebox.showwarning("Предупреждение", "Выберите файл")
        return

    with open(file_path, 'r') as file:
        trackers = file.readlines()

    unique_trackers = list(OrderedDict.fromkeys(trackers))
    num_duplicates = len(trackers) - len(unique_trackers)

    with open(file_path, 'w') as file:
        file.writelines(unique_trackers)

    messagebox.showinfo("Готово", f"Удалено: {num_duplicates} дубликатов")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    file_path_var.set(file_path)

def on_drop(event):
    file_path = event.data
    file_path_var.set(file_path)

# Создание главного окна с поддержкой перетаскивания файлов
root = TkinterDnD.Tk()
root.title("Удаление дубликатов трекеров")

# Установка стилей для элементов
style = ttk.Style()
style.configure("TButton",
                font=("Arial", 12),
                foreground="black",  # Черный цвет текста
                background="#4CAF50",
                padding=10)
style.configure("TLabel",
                font=("Arial", 14),
                foreground="black",
                background="#F0F0F0")
style.configure("TEntry",
                font=("Arial", 12),
                foreground="black",
                background="white",
                padding=5)

# Переменная для хранения пути к файлу
file_path_var = tk.StringVar()

# Создание метки и поле для отображения пути к файлу
file_label = ttk.Label(root, text="Выберите файл:")
file_label.pack(pady=10)

file_entry = ttk.Entry(root, textvariable=file_path_var, width=50)
file_entry.pack(pady=5)

# Привязка события перетаскивания к полю ввода
file_entry.drop_target_register(DND_FILES)
file_entry.dnd_bind('<<Drop>>', on_drop)

# Создание кнопки для выбора файла
browse_button = ttk.Button(root, text="Обзор", command=browse_file, style="TButton")
browse_button.pack(pady=5)

# Создание кнопки "Удалить дубликаты"
remove_duplicates_button = ttk.Button(root, text="Удалить дубликаты", command=remove_duplicates, style="TButton")
remove_duplicates_button.pack(pady=10)

# Запуск главного цикла
root.mainloop()
