import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import os


class XLSXViewerApp:
    def __init__(self, root):
        self.root = root
        self.WIDTH = 800
        self.HEIGHT = 600
        self.root.title("Excel Viewer")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)
        
        # Переменные
        self.current_file = None
        self.df = None
        
        # Создание интерфейса
        self.create_widgets()
    
    def create_widgets(self):
        # Фрейм для кнопок
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # Кнопка выбора файла
        self.select_button = tk.Button(
            button_frame, 
            text="Выбрать файл", 
            command=self.open_file
        )
        self.select_button.pack(side=tk.LEFT, padx=5)
        
        # Метка с именем выбранного файла
        self.file_label = tk.Label(button_frame, text="Файл не выбран")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        # Фрейм для Treeview и Scrollbar
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview для отображения данных
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Статус бар
        self.status_bar = tk.Label(
            self.root, 
            text="Готово", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл XLSX",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        
        if not file_path:
            return
        
        try:
            # Загрузка данных из файла
            self.df = pd.read_excel(file_path)
            self.current_file = file_path
            
            # Обновление интерфейса
            self.update_file_label()
            self.display_data()
            
            self.status_bar.config(text=f"Успешно загружен файл: {os.path.basename(file_path)}")
        except Exception as e:
            self.status_bar.config(text=f"Ошибка: {str(e)}")
    
    def update_file_label(self):
        if self.current_file:
            self.file_label.config(text=os.path.basename(self.current_file))
        else:
            self.file_label.config(text="Файл не выбран")
    
    def display_data(self):
        # Очистка предыдущих данных
        self.tree.delete(*self.tree.get_children())
        
        if self.df is None:
            return
        
        # Установка колонок
        self.tree["columns"] = list(self.df.columns)
        num_columns = len(self.df.columns)
        avg_col_width = sum(len(col) for col in self.df.columns) // num_columns
        
        # Форматирование заголовков
        for col in self.df.columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=(self.WIDTH // num_columns) * min(6, avg_col_width), anchor=tk.W)
        
        # Добавление данных
        for i, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=list(row))


if __name__ == "__main__":
    root = tk.Tk()
    app = XLSXViewerApp(root)
    root.mainloop()