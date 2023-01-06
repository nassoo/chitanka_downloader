import os
import json
import logging
import zipfile
import requests
from requests.exceptions import HTTPError

from utilities.powermanagement import long_running

IP = 'http://127.0.0.1:8000/'


class DownloadFiles:
    def __init__(self, app_data):
        self.app_data = app_data
        self.app_data['current_progress'] = 0
        self.app_data['user_urls'] = json.load(open('user_data/user_files.json', 'r', encoding='utf-8'))
        self.app_data['user_series'] = json.load(open('user_data/user_series.json', 'r', encoding='utf-8'))
        self.get_new_urls()

    @long_running
    def download(self):
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.info('Starting download')
        for key in self.app_data['entries_to_process']:
            try:
                self.app_data['current_progress'] += 1
                short_name, path = self.app_data['urls'][key][1:3]
                url = IP + key + '-' + short_name + self.app_data['file_type']
                dir_name = os.path.join(self.app_data['output_dir'], '/'.join(path.split('/')[:-1]))
                file_name = path.split('/')[-1] + self.app_data['file_type']
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                try:
                    head = requests.head(url).headers['Location']
                    r = requests.get(IP + head)
                    r.raise_for_status()
                except (KeyError, HTTPError) as e:
                    try:
                        ext = '.sfb.zip'
                        head = requests.head(IP + key + '-' + short_name + ext).headers['location']
                        head = head.replace(ext, self.app_data['file_type'])
                        r = requests.get(IP + head)
                        r.raise_for_status()
                        logging.exception(f'{e}\n    {key}: {url} [SUCCESS form localhost with link to .sfb.zip]',
                                          exc_info=False)
                    except (KeyError, HTTPError) as e:
                        url = 'https://chitanka.info/' + key + '-' + short_name + self.app_data['file_type']
                        r = requests.get(url)
                        r.raise_for_status()
                        logging.exception(f'{e}\n    {key}: {url} [SUCCESS form chitanka.info]', exc_info=False)

                with open(os.path.join(dir_name, file_name), 'wb') as f:
                    f.write(r.content)

                # TODO: Move it to get_new_urls(), so it can't delete accidentally duplicated files?
                if self.app_data['update'] and key in self.app_data['user_urls'] \
                        and self.app_data['user_urls'][key][2] != self.app_data['urls'][key][2]:
                    old_file = os.path.join(self.app_data['output_dir'],
                                            self.app_data['user_urls'][key][2] + self.app_data['file_type'])
                    old_dir = os.path.dirname(old_file)
                    if os.path.exists(old_file):
                        os.remove(old_file)
                        self.remove_empty_dirs(old_dir)

                self.app_data['user_urls'][key] = self.app_data['urls'][key]
                self.app_data['user_series'].pop(key, None)

            except Exception as e:
                logging.exception(f'{e} \n    {key} [FAIL]')
                self.app_data['user_urls'].pop(key, None)
                self.app_data['user_series'].pop(key, None)

        # TODO: add an option to save the progress after each iteration
        self.save_urls()
        logging.info('End of download')

    def save_urls(self):
        with open("./user_data/user_files.json", "w", encoding='utf-8') as f:
            json.dump(self.app_data['user_urls'], f, ensure_ascii=False, indent=4)
        with open("./user_data/user_series.json", "w", encoding='utf-8') as f:
            json.dump(self.app_data['user_series'], f, ensure_ascii=False, indent=4)

    def get_new_urls(self):
        if self.app_data['update']:
            self.app_data['entries_to_process'] = [k for k, v in self.app_data['urls'].items()
                                                   if k not in self.app_data['user_urls'].keys()
                                                   or self.app_data['user_urls'][k][3] < v[3]
                                                   or self.app_data['user_urls'][k][2] != v[2]]
            if self.app_data['check_files'] and self.app_data['file_type'] == '.fb2.zip':
                for key, value in self.app_data['user_urls'].items():
                    file_to_check = os.path.join(self.app_data['output_dir'], value[2] + '.fb2.zip')
                    try:
                        with zipfile.ZipFile(file_to_check, 'r') as zf:
                            zip_file = zf.namelist()[0]
                            if not zip_file.endswith('.fb2'):
                                self.app_data['entries_to_process'].append(key)
                                logging.exception(f'File will be replaced: {key}: {file_to_check}', exc_info=False)
                    except Exception as e:
                        self.app_data['entries_to_process'].append(key)
                        logging.exception(f'{e} \n    File will be replaced: {key}: {file_to_check}', exc_info=False)
        else:
            self.app_data['entries_to_process'] = [k for k in self.app_data['urls'].keys()]

    def remove_empty_dirs(self, dir_name):
        if not os.listdir(dir_name):
            os.rmdir(dir_name)
            self.remove_empty_dirs(os.path.dirname(dir_name))
