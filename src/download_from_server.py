import os

import requests
import json
import logging

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
                except KeyError as e:
                    try:
                        ext = '.sfb.zip'
                        head = requests.head(IP + key + '-' + short_name + ext).headers['location']
                        head = head.replace(ext, self.app_data['file_type'])
                        r = requests.get(IP + head)
                        logging.exception(f'{e}\n    {key}: {url} [SUCCESS form localhost with link to .sfb.zip]',
                                          exc_info=False)
                    except KeyError as e:
                        url = 'https://chitanka.info/' + key + '-' + short_name + self.app_data['file_type']
                        r = requests.get(url)
                        logging.exception(f'{e}\n    {key}: {url} [SUCCESS form chitanka.info]', exc_info=False)

                with open(os.path.join(dir_name, file_name), 'wb') as f:
                    f.write(r.content)

                # TODO: Move it to get_new_urls(), so it can't delete accidentally duplicated files?
                if self.app_data['update'] and key in self.app_data['user_urls'] \
                        and self.app_data['user_urls'][key][2] != self.app_data['urls'][key][2]:
                    old_file = os.path.join(self.app_data['output_dir'],
                                            self.app_data['user_urls'][key][2] + self.app_data['file_type'])
                    old_dir = os.path.dirname(old_file)
                    os.remove(old_file)
                    self.remove_empty_dirs(old_dir)

                self.app_data['user_urls'][key] = self.app_data['urls'][key]
                self.app_data['user_series'].pop(key, None)

            except Exception as e:
                logging.exception(f'{e} \n    {key} [FAIL]')

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
        else:
            self.app_data['entries_to_process'] = [k for k in self.app_data['urls'].keys()]

    def remove_empty_dirs(self, dir_name):
        if not os.listdir(dir_name):
            os.rmdir(dir_name)
            self.remove_empty_dirs(os.path.dirname(dir_name))
