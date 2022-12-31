import tkinter as tk
from threading import Thread

from src.page import Page
from src.set_series import SetSeries


class SeriesPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        # TODO: run the process without downloading the files again
        process_finished = tk.Label(self.main_frame,
                                    textvariable=controller.app_data['process_finished_text'],
                                    bg="black",
                                    fg="green",
                                    font="none 12 bold",
                                    name="process_finished")
        process_finished.pack(padx=10, pady=10)

        series_label = tk.Label(self.main_frame,
                                text="Желаете ли да бъдат импортирани номерата на поредиците в книгите?\n"
                                     "Процесът може да отнеме няколко минути.",
                                bg="black",
                                fg="white",
                                font="none 12 bold",
                                wraplength=self.controller.winfo_width() - 20)
        series_label.pack(pady=10)

        series_button = tk.Button(self.main_frame, text="Импортирай", width=14, command=self.insert_series,
                                  name="series_button")
        series_button.pack(padx=10, pady=10)

    def insert_series(self):
        ss = SetSeries(self.controller)

        # TODO: add an option insert all series or update only the missing ones
        self.controller.t = Thread(target=ss.set_series, name='set_series')
        self.controller.t.daemon = True
        self.controller.t.start()

        self.controller.app_data['progress_label_text'].set("Поредиците се вмъкват във файловете, в които е необходимо."
                                                            "\nПроцесът е бавен - моля, изчакайте!")
        self.controller.app_data['process_finished_text'].set(f"Процесът приключи! Можете да затворите програмата.")
        self.controller.show_frame('ProgressPage')
