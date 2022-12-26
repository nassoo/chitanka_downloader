import os
import requests
import json
import logging

from helpers.path_handler import resoure_path
from helpers.powermanagement import long_running
from src.get_urls import GetContent

IP = 'http://127.0.0.1:8000/'


class DownloadFiles(GetContent):
    def __init__(self):
        super().__init__()
        self.urls_to_download = {}
        self.user_urls = json.load(open('user_data/user_files.json', 'r', encoding='utf-8'))
        self.output_dir = "../Читанка" if self.filenames == 'кирилица' else 'Chitanka'  # self.get_directory()
        self.file_type = '.fb2.zip'
        self.download_progress = 0
        self.update = True

    @long_running
    def download(self):
        headers = {'User-Agent': 'PostmanRuntime/7.29.0'}
        try:
            for key in self.urls_to_download.keys():
                self.download_progress += 1
                short_name, path = self.urls_to_download[key][1:3]
                url = IP + key + '-' + short_name + self.file_type
                dir_name = os.path.join(self.output_dir, '/'.join(path.split('/')[:-1]))
                file_name = path.split('/')[-1] + self.file_type
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                try:
                    head = requests.head(url).headers['Location']
                    r = requests.get(IP + head)
                except requests.exceptions.MissingSchema:
                    r = requests.get(url, headers=headers, stream=True)
                    url_fixed = r.url.replace('book/%5C', '').replace('text/%5C', '')
                    r = requests.get(url_fixed)

                with open(os.path.join(dir_name, file_name), 'wb') as f:
                    f.write(r.content)

                if self.update and self.urls_to_download[key][2] != self.urls[key][2]:
                    os.remove(os.path.join(self.output_dir, self.urls[key][2] + self.file_type))

                self.user_urls[key] = self.urls_to_download[key]
        except Exception as e:
            logging.exception(e)
        self.save_urls()

    def save_urls(self):
        with open("./user_data/user_files.json", "w", encoding='utf-8') as f:
            json.dump(self.user_urls, f, ensure_ascii=False, indent=4)

    def get_new_urls(self):
        if self.update:
            self.urls_to_download = {k: v for k, v in self.urls.items()
                                     if k not in self.user_urls.keys() or self.user_urls[k][3] < v[3]}
        else:
            self.urls_to_download = self.urls
