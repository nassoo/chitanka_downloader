import os
import requests

from src.get_urls import GetContent

IP = 'http://127.0.0.1:8000/'


class DownloadFiles(GetContent):
    def __init__(self):
        super().__init__()
        self.output_dir = "d:\Читанка"  # self.get_directory()
        self.file_type = '.fb2.zip'
        self.filenames = 'кирилица'
        self.download_progress = 0

    def download(self):
        for key in list(self.urls.keys())[:10]:
            self.download_progress += 1
            short_name, path = self.urls[key][1:3]
            url = IP + key + '-' + short_name + self.file_type
            dir_name = self.output_dir + '/'.join(path.split('/')[:-1])
            file_name = path.split('/')[-1] + self.file_type
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            r = requests.get(url)
            url_fixed = r.url.replace('book/%5C', '')
            r_fixed = requests.get(url_fixed)

            with open(os.path.join(dir_name, file_name), 'wb') as f:
                f.write(r_fixed.content)
