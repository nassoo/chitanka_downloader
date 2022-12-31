import tkinter as tk
import json

from utilities.path_handler import resource_path


class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')
        self.logo = tk.PhotoImage(file=resource_path("img/logo.png"))

        label_logo = tk.Label(self, image=self.logo, bg='black')
        label_logo.pack(padx=10, pady=5)

        self.upper_frame = tk.Frame(self, bg='black')
        self.upper_frame.pack(padx=10)

        self.main_frame = tk.Frame(self, bg='black')
        self.main_frame.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        exit_btn = tk.Button(self.main_frame, text="Изход", width=14, command=self.end_program, name="exit_btn")
        exit_btn.grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)
        exit_btn.place(anchor=tk.CENTER, relx=0.5, rely=0.95)

    def end_program(self):
        if self.controller.t.is_alive():
            with open("./user_data/user_files.json", "w", encoding='utf-8') as f:
                json.dump(self.controller.app_data['user_urls'], f, ensure_ascii=False, indent=4)
            with open("./user_data/user_series.json", "w", encoding='utf-8') as f:
                json.dump(self.controller.app_data['user_series'], f, ensure_ascii=False, indent=4)
        self.controller.destroy()
        exit()
