import tkinter as tk
from threading import Thread

from src.database_page import DatabasePage
from src.params_page import ParamsPage
from src.progress_page import ProgressPage
from src.series_page import SeriesPage
from utilities.path_handler import resource_path


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Chitanka Downloader")
        self.iconbitmap(resource_path("img/logo.ico"))
        self.geometry("600x400")
        self.configure(bg='black')
        self.t = Thread()
        self.app_data = {
            "cur": None,
            "filenames": 'кирилица',
            'file_type': '.fb2.zip',
            'output_dir': '../Читанка',
            'update': True,
            'urls': {},
            'user_urls': {},
            'book_series_ids': {},
            'user_series': {},
            'entries_to_process': [],
            'current_progress': 0,
            'db_output_text': tk.StringVar(),
            'download_content': tk.StringVar(),
            'progress_label_text': tk.StringVar(),
            'process_finished_text': tk.StringVar()
        }

        self.container = tk.Frame(self, height=400, width=600)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {
            'DatabasePage': DatabasePage,
            'ParamsPage': ParamsPage,
            'ProgressPage': ProgressPage,
            'SeriesPage': SeriesPage
        }

        self.show_frame('DatabasePage')

    def show_frame(self, frame_name):
        frame = self.frames[frame_name](self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
