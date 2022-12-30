import tkinter as tk
from tkinter import ttk

from src.database_page import DatabasePage


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Chitanka Downloader")
        self.geometry("600x400")
        self.configure(bg='black')
        self.app_data = {
            "cur": None,
            "filenames": 'кирилица',
            'file_type': '.fb2.zip',
            'output_dir': '../Читанка',
            'update': True,
            'urls': {},
            'book_series_ids': {},
            'download_progress': 0,
            'db_output_text': tk.StringVar(),
            'download_content': tk.StringVar(),
            'progress_label_text': tk.StringVar()
        }

        self.container = tk.Frame(self, height=400, width=600)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame(DatabasePage)

    def show_frame(self, f):
        frame = f(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
