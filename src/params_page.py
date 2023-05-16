import os
import tkinter as tk
from tkinter import ttk
from threading import Thread
from idlelib.tooltip import Hovertip

from src.download_from_server import DownloadFiles
from src.get_urls import GetContent
from src.page import Page
from src.select_dir_location import GetDirectory


class ParamsPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.ft_warning = None
        self.ft_warning_btn = None
        self.files_dir_output_text = tk.StringVar()
        self.file_types_option_var = tk.StringVar()
        self.filenames_option_var = tk.StringVar()
        self.file_type_output_text = tk.StringVar(
            value=f"Избраният файлов формат е {self.controller.app_data['file_type']}.")
        self.filenames_output_text = tk.StringVar(
            value=f"Имената на файловете ще са на {self.controller.app_data['filenames']}.")
        self.check_files_var = tk.BooleanVar()

        db_txt = tk.Label(self.upper_frame, text="Базата данни е заредена успешно!",
                          bg="black", fg="green", font="none 12 bold")
        db_txt.pack(padx=10)

        params_txt = tk.Label(self.upper_frame, text="Въведете желаните параметри за изтеглянето на книгите.",
                              bg="black", fg="white", font="none 12")
        params_txt.pack(padx=10)

        frame_params = tk.Frame(self.main_frame, height=70, bg="black", name="frame_params")
        frame_params.grid(row=3, column=0, columnspan=4, sticky='nsew')

        files_dir_btn = tk.Button(frame_params, text="Директория", width=14, command=self.select_files_dir)
        files_dir_btn.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=(10, 0))
        self.files_dir_output_text = tk.StringVar()
        self.files_dir_output_text.set("Файловете ще се изтеглят в " + os.path.abspath(
            self.controller.app_data['output_dir']))
        files_dir_output = tk.Label(frame_params, textvariable=self.files_dir_output_text, bg="black", fg="white",
                                    font="none 12")
        files_dir_output.grid(row=0, column=2, sticky=tk.W)
        frame_params.bind('<Configure>', lambda e: files_dir_output.config(
            wraplength=self.controller.winfo_width() - 150))

        file_types = [".fb2.zip", ".fb2", ".epub"]
        ft = ttk.OptionMenu(frame_params, self.file_types_option_var, file_types[0], *file_types,
                            command=self.set_file_type)
        ft.config(width=12)
        ft.grid(row=1, column=0, sticky=tk.NW, padx=10, pady=(10, 0))
        ft_output = tk.Label(frame_params, textvariable=self.file_type_output_text, bg="black", fg="white",
                             font="none 12")
        ft_output.grid(row=1, column=2, sticky=tk.W)
        ft_output.bind('<Configure>', lambda e: ft_output.config(wraplength=self.controller.winfo_width() - 150))

        filenames = ["кирилица", "латиница"]
        fn = ttk.OptionMenu(frame_params, self.filenames_option_var, filenames[0], *filenames,
                            command=self.set_filenames)
        fn.config(width=12)
        fn.grid(row=3, column=0, sticky=tk.NW, padx=10, pady=(10, 0))
        fn_output = tk.Label(frame_params, textvariable=self.filenames_output_text, bg="black", fg="white",
                             font="none 12")
        fn_output.grid(row=3, column=2, sticky=tk.W)
        fn_output.bind('<Configure>', lambda e: fn_output.config(wraplength=self.controller.winfo_width() - 150))

        check_btn = tk.Checkbutton(frame_params,
                                   text="Проверка за грешки във вече изтеглените файлове",
                                   variable=self.check_files_var,
                                   onvalue=True,
                                   offvalue=False,
                                   bg="black",
                                   fg="orange",
                                   command=self.check_files)
        check_btn.grid(row=4, column=1, columnspan=3, sticky=tk.NW, padx=(0, 10), pady=(10, 0))
        check_btn.bind('<Configure>', lambda e: fn_output.config(wraplength=self.controller.winfo_width() - 150))
        check_btn_info = tk.Label(frame_params, text="?")
        check_btn_info.grid(row=4, column=0, sticky=tk.E, padx=10, pady=(10, 0))
        Hovertip(check_btn_info, "Ако сте изтеглили съдържанието на библиотеката с версия 1.0.0 или по-ниска, в някои\n"
                                 "от zip файловете може да има грешки. При включването на тази опиция програмата ще  \n"
                                 "провери за грешки във вече изтеглените файлове, ще ги изтрие и ще опита да ги \n"
                                 "изтегли отново. Проверката ще се извъши само ако изебете обновяване на архива и \n"
                                 "само ако сте избрали формат .fb2.zip.\n"
                                 "Процесът ще забави началото на обновяването с няколко секунди \n"
                                 "(в зависимост от бързината на Вашия твърд диск).", 0)

        download_btn = tk.Button(self.main_frame, text="Изтегли всичко", width=14,
                                 command=lambda: self.download_content(False))
        download_btn.grid(row=4, column=0, columnspan=4, sticky=tk.W, padx=10, pady=(10, 0))
        download_btn.place(anchor=tk.CENTER, relx=0.4, rely=0.82)

        update_btn = tk.Button(self.main_frame, text="Само обнови", width=14,
                               command=lambda: self.download_content(True))
        update_btn.grid(row=4, column=0, columnspan=4, sticky=tk.W, padx=10, pady=(10, 0))
        update_btn.place(anchor=tk.CENTER, relx=0.6, rely=0.82)

    def select_files_dir(self):
        gd = GetDirectory()
        self.controller.app_data['output_dir'] = gd.get_directory()
        self.main_frame.update_idletasks()
        self.files_dir_output_text.set(self.controller.app_data['output_dir'])

    def set_file_type(self, value):
        self.controller.app_data['file_type'] = value
        self.file_type_output_text.set(f"Избраният файлов формат е {value}.")
        frame_params = self.main_frame.nametowidget('frame_params')
        if value == ".fb2.zip" or value == ".fb2":
            #  TODO check if exists
            self.ft_warning.destroy()
            self.ft_warning_btn.destroy()
        elif self.ft_warning not in frame_params.winfo_children():
            self.ft_warning = tk.Label(frame_params,
                                       text="Внимание! Поредиците ще могат да бъдат импортирани в книгите "
                                            "единствено ако форматът е .fb2.zip.",
                                       bg="black", fg="red",
                                       font="none 10")
            self.ft_warning.grid(row=2, column=2, sticky=tk.W)
            self.ft_warning.bind('<Configure>',
                                 lambda e: self.ft_warning.config(wraplength=self.controller.winfo_width() - 150))
            self.ft_warning_btn = tk.Label(frame_params, text="?")
            self.ft_warning_btn.grid(row=2, column=0, sticky=tk.E, padx=10, pady=(10, 0))
            Hovertip(self.ft_warning_btn,
                     "В базата данни на chitanka.info информацията за поредиците \n"
                     "е налична само за произведенията, но не и за книгите. \n"
                     "Ако желаете да импортирате поредиците и номерата им в книгите, \n"
                     "трябва да изберете формат .fb2.zip. \n"
                     "Това не засяга имената на файловете, \n"
                     "а единствено метаданните вътре във файловете, \n"
                     "за да могат програмите за четене на книги да ги разпознават. \n"
                     "Поредиците и номерата им ще бъдат отразени в имената на файловете, \n"
                     "независимо от файловия формат.", 0)

    def set_filenames(self, value):
        self.controller.app_data['filenames'] = value
        self.filenames_output_text.set(f"Имената на файловете ще са на {value}.")

    def check_files(self):
        self.controller.app_data['check_files'] = self.check_files_var.get()

    def download_content(self, update):
        self.controller.app_data['update'] = update

        if self.controller.app_data['output_dir'] is None:
            error_message = tk.Label(self.main_frame,
                                     text="Не сте избрали папка за изтегляне!",
                                     bg="black",
                                     fg="red",
                                     font="none 12 bold",
                                     name="error_message")
            error_message.grid(row=5, column=0, columnspan=4, sticky=tk.W, padx=10, pady=(10, 0))
            error_message.place(anchor=tk.CENTER, relx=0.5, rely=0.7)
        else:
            # TODO: check if error_message exists and destroy it
            gc = GetContent(self.controller.app_data)
            gc.get_content()
            df = DownloadFiles(self.controller.app_data)

            self.controller.t = Thread(target=df.download, name='download')
            self.controller.t.daemon = True
            self.controller.t.start()

            self.controller.app_data['progress_label_text'].set(
                "Файловете се изтеглят. Процесът е бавен - моля, изчакайте!"
                if not self.controller.app_data['update']
                else "Файловете се обновяват. Процесът е бавен - моля, изчакайте!"
                if len(self.controller.app_data['entries_to_process']) > 1000
                else "Файловете се обновяват. Моля, изчакайте!")
            # TODO: add description of the process
            # self.controller.app_data[f'process_finished_text'].set(
            #     f"Изтеглянето приключи за {timedelta(seconds=t_elapsed)}!")
            self.controller.show_frame('ProgressPage')
