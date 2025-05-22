import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import os

from .csvplot.plot3d import plot3d
from .csvplot.plot2d import plot2d
from .styles import init_styles
from .locales import locales
from .locales.utils import get_locale


class ExcelViewerApp:
    def __init__(self, root):
        self.root = root
        self.WIDTH = 800
        self.HEIGHT = 600
        self.root.title("Excel Viewer")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        # self.root.resizable(False, False)

        try:
            self.root.iconbitmap(r"app/public/icon.ico")
        except Exception:
            pass

        init_styles(self.root)
        locale = get_locale()
        if locale.startswith("en_"): 
            locale = "en_US"
        self.locale = locales[locale]
        
        self.current_file = None
        self.df = None
        self.selected_columns = []
        
        self.create_widgets()
    
    def create_widgets(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.select_button = ttk.Button(
            button_frame, 
            width=20,
            text=self.locale["button"]["fileselect"], 
            style="hightlight.TButton",
            command=self.open_file
        )
        self.select_button.pack(side=tk.TOP, pady=15)
        
        self.file_label = ttk.Label(button_frame, text=self.locale["label"]["filenotselected"], style="primary.TLabel")
        self.file_label.pack(side=tk.BOTTOM)
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.plot_bar = tk.Frame(self.root)
        self.plot_bar.pack(fill=tk.X, pady=5, padx=5)
        
        self.clear_selected_columns_button = ttk.Button(
            self.plot_bar, 
            text=self.locale["button"]["clear"], 
            command=self.clear_selected_columns
        )
        self.clear_selected_columns_button.configure(style="clear.TButton")
        self.clear_selected_columns_button.pack(side=tk.LEFT, padx=10)

        self.selected_columns_label = ttk.Label(self.plot_bar, text=self.locale["label"]["columnsnotselected"], style="primary.TLabel")
        self.selected_columns_label.configure(style="primary.TLabel")
        self.selected_columns_label.pack(side=tk.LEFT)

        self.plot2d_button = ttk.Button(
            self.plot_bar, 
            text=self.locale["button"]["plot2d"], 
            command=self.plot_data_2d
        )
        self.plot2d_button.configure(style="primary.TButton")
        self.plot2d_button.pack(side=tk.RIGHT, pady=5)

        self.plot3d_button = ttk.Button(
            self.plot_bar, 
            text=self.locale["button"]["plot3d"], 
            command=self.plot_data_3d
        )
        self.plot3d_button.configure(style="primary.TButton")
        self.plot3d_button.pack(side=tk.RIGHT, pady=5)
        
        self.status_bar = ttk.Label(
            self.root, 
            text=self.locale["status"]["fileselect"],  
            anchor=tk.W,
            style="status.TLabel"
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=10)
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title=f"{self.locale['button']['fileselect']} XLSX",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        
        if not file_path:
            return
        
        self.clear_selected_columns()
        
        try:
            self.df = pd.read_excel(file_path)
            self.current_file = file_path
            
            self.update_file_label()
            self.display_data()
            
            self.status_bar.config(text=f"{self.locale['status']['loaded']}: {os.path.basename(file_path)}")
        except Exception as e:
            self.status_bar.config(text=f"{self.locale['status']['error']}: {str(e)}")
    
    def update_file_label(self):
        if self.current_file:
            self.file_label.config(text=os.path.basename(self.current_file))
            self.file_label.configure(style="success.TLabel")
        else:
            self.file_label.config(text=self.locale["label"]["filenotselected"])
    
    def display_data(self):
        self.tree.delete(*self.tree.get_children())
        
        if self.df is None:
            return
        
        self.tree["columns"] = list(self.df.columns)
        num_columns = len(self.df.columns)
        min_w = (self.WIDTH) // (num_columns + 1)

        for col in self.df.columns:
            self.tree.heading(col, text=col, anchor=tk.W, command=lambda c=col: self.toggle_select_column(c))
            self.tree.column(col, minwidth=min_w, stretch=True)
        
        for i, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    
    def update_selected_cols_label(self):
        if not self.selected_columns:
            self.selected_columns_label.config(text=self.locale["label"]["columnsnotselected"])
            return
        if len(self.selected_columns) == 1:
            self.selected_columns_label.config(
                text=f"{self.locale['label']['plot']['plot']} {self.selected_columns[0]} {self.locale['label']['plot']['rest']}"
            )
            return
            
        selected_cols_text = ', '.join(self.selected_columns[1::])
        screen_width = self.root.winfo_width()
        if screen_width // len(selected_cols_text) < 16:
            selected_cols_text = selected_cols_text[:screen_width // 16] + '...'
        self.selected_columns_label.config(
            text=f"{self.locale['label']['plot']['plot']} {self.selected_columns[0]} {self.locale['label']['plot']['of']} {selected_cols_text}"
        )
            
    
    def toggle_select_column(self, col):
        if col in self.selected_columns:
            self.selected_columns.remove(col)
        else:
            self.selected_columns.append(col)
        
        self.update_selected_cols_label()
            
            
    def clear_selected_columns(self):
        self.selected_columns = []
        self.selected_columns_label.config(text=self.locale["label"]["columnsnotselected"])
        
    
    def plot_data_3d(self):
        if self.df is None:
            self.status_bar.config(text=self.locale["status"]["fileselect"])
            return      
        if len(self.selected_columns) != 3:
            self.status_bar.config(text=self.locale["status"]["3derror"])
            return
        
        screen_size = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        plot3d(self.df[self.selected_columns], screen_size=screen_size)
        

    def plot_data_2d(self):
        if self.df is None:
            self.status_bar.config(text=self.locale["status"]["fileselect"])
            return
        if len(self.selected_columns) == 1:
            cols = [self.selected_columns[0]] + [col for col in self.df.columns if col != self.selected_columns[0]]
            plot2d(self.df[cols])
            return

        plot2d(self.df[self.selected_columns])
