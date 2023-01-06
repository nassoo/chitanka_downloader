import tkinter as tk
import webbrowser
import requests
from functools import partial

from src.database_connection import ConnectDatabase
from utilities.tkHyperlinkManager import HyperlinkManager

from src.page import Page


class DatabasePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        self.new_version = None
        self.new_version_text = tk.StringVar(value='')
        self.new_version_description_text = tk.StringVar(value='')
        self.after(1000, self.check_for_new_version)

        new_version_label = tk.Label(self.main_frame,
                                     textvariable=self.new_version_text,
                                     cursor="hand2",
                                     fg="orange",
                                     bg='black',
                                     font=('', 12))
        new_version_label.pack(padx=10)
        new_version_label.bind('<Button-1>', lambda e: webbrowser.open_new(self.new_version))
        new_version_description = tk.Label(self.main_frame,
                                           textvariable=self.new_version_description_text,
                                           fg="orange",
                                           bg='black',
                                           font=('', 10))
        new_version_description.pack(padx=10)

        # TODO: fix height of the frame for linux (it's too small - remove it?)
        intro_text = tk.Text(self.main_frame, bg="black", fg="white", height=6, border=0, font=12, wrap=tk.WORD)
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
        intro_text.pack(padx=10, pady=(10, 0))

        db_btn = tk.Button(self.main_frame, text="База данни", width=14, command=self.connect_database)
        db_btn.pack()

        db_output = tk.Label(self.main_frame,
                             textvariable=self.controller.app_data['db_output_text'],
                             bg="black",
                             fg="red",
                             font="none 12 bold")
        db_output.pack(padx=10, pady=(10, 0))

    def connect_database(self):
        db = ConnectDatabase()
        cur, database_message = db.connect_db()
        if cur is not None:
            self.controller.app_data['cur'] = cur
            try:
                requests.head('http://127.0.0.1:8000/')
                self.controller.show_frame('ParamsPage')
            except Exception:
                self.controller.app_data['db_output_text'].set('Няма връзка с преносимата версия на "Моята библиотека".'
                                                               '\nСтартирайте я и опитайте отново.')
        else:
            self.controller.app_data['db_output_text'].set(database_message)

    def check_for_new_version(self):
        try:
            r = requests.get('https://api.github.com/repos/Nassoo/chitanka_downloader/releases/latest')
            self.new_version = r.json()['html_url']
            latest_version = self.new_version.split('/')[-1][1:]
            if latest_version != self.controller.app_data['version']:
                self.new_version_text.set(f'Налична е нова версия на програмата. Натиснете тук за да я изтеглите.')
                self.new_version_description_text.set('Заместете само изпълнимия файл. '
                                                      'Не презаписвайте папката user_data!')
        except Exception:
            pass
