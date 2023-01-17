import tkinter as tk
from tkinter import ttk

from src.page import Page


class ProgressPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        all_files = len(controller.app_data['entries_to_process'])
        progress_value = tk.StringVar()
        progress_value.set("0")
        s = ttk.Style()
        s.layout("LabeledProgressbar",
                 [('LabeledProgressbar.trough',
                   {'children': [('LabeledProgressbar.pbar',
                                  {'side': 'left', 'sticky': 'ns'}),
                                 ("LabeledProgressbar.label",  # label inside the bar
                                  {"sticky": ""})],
                    'sticky': 'nswe'})])
        s.configure("LabeledProgressbar", text=f"{progress_value.get()} %      ")
        p = ttk.Progressbar(self.upper_frame, orient="horizontal", length=400, mode='determinate',
                            style="LabeledProgressbar", name="progress_bar")
        p.daemon = True
        p.pack(padx=10)

        progress_label = tk.Label(self.upper_frame,
                                  textvariable=controller.app_data['progress_label_text'],
                                  bg="black",
                                  fg="white",
                                  font="none 12 bold",
                                  name="progress_label")
        progress_label.pack(padx=10, pady=10)

        def update_progress_bar():
            if controller.t.is_alive():
                if all_files > 0:
                    progress_value.set(str(round(controller.app_data['current_progress'] / all_files * 100, 2)))
                s.configure("LabeledProgressbar", text=f"{progress_value.get()} %      ")
                p["value"] = progress_value.get()
                p.after(5000, update_progress_bar)
            else:
                s.configure("LabeledProgressbar", text=f"{progress_value.get()} %      ")
                p["value"] = progress_value.get()
                p.destroy()
                progress_label.destroy()
                process_finished = tk.Label(self.upper_frame,
                                            textvariable=controller.app_data['process_finished_text'],
                                            bg="black",
                                            fg="green",
                                            font="none 12 bold",
                                            name="process_finished")
                process_finished.pack(padx=10, pady=10)

                if (controller.app_data['file_type'] == ".fb2.zip" or controller.app_data['file_type'] == ".fb2") \
                        and controller.t.name == "download":
                    controller.show_frame('SeriesPage')

        update_progress_bar()
