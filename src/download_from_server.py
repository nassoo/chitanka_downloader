import os
import requests
import json

from helpers.path_handler import resoure_path
from helpers.powermanagement import long_running
from src.get_urls import GetContent

IP = 'http://127.0.0.1:8000/'


class DownloadFiles(GetContent):
    def __init__(self):
        super().__init__()
        self.new_urls = {}
        self.output_dir = "d:/Читанка"  # self.get_directory()
        self.file_type = '.fb2.zip'
        self.download_progress = 0
        self.update = True

    @long_running
    def download(self):
        # TODO: add update option vs. download all
        with open("./user_data/user_files.json", "w", encoding='utf-8') as f:
            json.dump(self.urls, f, ensure_ascii=False, indent=4)
        for key in self.new_urls.keys():
            self.download_progress += 1
            short_name, path = self.new_urls[key][1:3]
            url = IP + key + '-' + short_name + self.file_type
            dir_name = os.path.join(self.output_dir, '/'.join(path.split('/')[:-1]))
            file_name = path.split('/')[-1] + self.file_type
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            r = requests.get(url)
            url_fixed = r.url.replace('book/%5C', '')
            r_fixed = requests.get(url_fixed)

            with open(os.path.join(dir_name, file_name), 'wb') as f:
                f.write(r_fixed.content)

            if self.update and self.new_urls[key][2] != self.urls[key][2]:
                os.remove(os.path.join(self.output_dir, self.urls[key][2] + self.file_type))

        with open("./user_data/user_files.json", "w", encoding='utf-8') as f:
            json.dump(self.urls, f, ensure_ascii=False, indent=4)

    def get_new_urls(self):
        old_urls = json.load(open(resoure_path('user_data/user_files.json'), 'r', encoding='utf-8'))
        if self.update:
            self.new_urls = {k: v for k, v in self.urls.items() if k not in old_urls.keys() or old_urls[k][3] < v[3]}
        else:
            self.new_urls = self.urls
