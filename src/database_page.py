import tkinter as tk
import webbrowser
from functools import partial

from src.database_connection import ConnectDatabase
from src.params_page import ParamsPage
from utilities.tkHyperlinkManager import HyperlinkManager

from src.page import Page


class DatabasePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        intro_text = tk.Text(self.main_frame, bg="black", fg="white", height=5, border=0, font=12, wrap=tk.WORD)
        intro_text.tag_configure("center", justify='center')
        intro_text.insert(tk.END, "Преди да започне обработката, е необходимо да сте изтеглили и стартирали ")
        hyperlink = HyperlinkManager(intro_text)
        intro_text.insert(tk.END,
                          "преносимата версия на Моята библиотека",
                          hyperlink.add(partial(webbrowser.open,
                                                "https://forum.chitanka.info/chitanka-standalone-edition-t6309.html")))
        intro_text.insert(tk.END, '. След това натиснете бутона "База данни" и изберете основната директория на '
                                  'преносимата версия на Моята библиотека '
                                  '(в която се намира изпълнимият файл chitanka), за да се зареди базата данни.')
        intro_text.tag_add("center", "1.0", "end")
        intro_text.pack(padx=10, pady=10)

        db_btn = tk.Button(self.main_frame, text="База данни", width=14, command=self.connect_database)
        db_btn.pack(padx=10, pady=10)

        db_output = tk.Label(self.main_frame,
                             textvariable=self.controller.app_data['db_output_text'],
                             bg="black",
                             fg="red",
                             font="none 12 bold")
        db_output.pack(padx=10, pady=10)

    def connect_database(self):
        db = ConnectDatabase()
        cur, database_message = db.connect_db()
        if cur is not None:
            self.controller.app_data['cur'] = cur
            self.controller.show_frame(ParamsPage)
        else:
            self.controller.app_data['db_output_text'].set(database_message)
