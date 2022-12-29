import lxml.etree as et
import os
import zipfile
import copy
import ntpath
import json
import logging
import urllib.parse

from utilities.powermanagement import long_running
from src.download_from_server import DownloadFiles


class SetSeries:
    def __init__(self, output_dir, update=True, urls=None, user_series=None, book_series_ids=None):
        self.output_dir = output_dir
        self.update = update
        self.urls = urls
        self.user_series = user_series
        self.book_series_ids = book_series_ids
        self.entries_to_process = {}
        self.download_progress = 0

    ns_map = {"n": 'http://www.gribuser.ru/xml/fictionbook/2.0'}

    @long_running
    def set_series(self):
        logging.info("Setting series")
        for book_id in self.entries_to_process.keys():
            self.download_progress += 1
            input_file = os.path.join(self.output_dir, self.urls[book_id][2] + '.fb2.zip')
            output_file = os.path.join(self.output_dir, self.urls[book_id][2] + '.xml')
            # print(input_file)
            try:
                with zipfile.ZipFile(input_file, 'r') as zf:
                    zip_file = zf.namelist()[0]
                    with open(output_file, "wb") as f:
                        f.write(zf.read(zip_file))
            except Exception as e:
                logging.exception(f'{urllib.parse.unquote(str(e))}\n    {book_id}: {input_file}', exc_info=False)
                continue
            try:
                doc = et.parse(output_file)
                root = doc.getroot()
                new_tree = self.transform(root)
                new_tree.write(output_file, xml_declaration=True, encoding="utf-8")
                os.remove(input_file)
            except Exception as e:
                logging.exception(f'{urllib.parse.unquote(str(e))}\n    {book_id}: {input_file}', exc_info=False)
                os.remove(output_file)
                continue
            filename = ntpath.basename(output_file)  # That way it is platform independent
            print(f'{book_id}: {filename}')
            with zipfile.ZipFile(input_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.write(output_file, filename)
            os.remove(output_file)

            self.user_series[book_id] = self.entries_to_process[book_id]

        self.save_series()
        logging.info("Series set")

    def transform(self, root_org):
        root_tree_org = root_org.getroottree()  # Get whole tree
        new_root_tree = copy.deepcopy(root_tree_org)  # Deep copy whole tree INCLUDING doctype
        new_root = new_root_tree.getroot()  # Now work on the root element
        book_id_list = new_root.find('n:description[1]/n:document-info[1]/n:id[1]',
                                     namespaces=SetSeries.ns_map).text.split('/')
        book_id = book_id_list[-2] + '/' + book_id_list[-1]
        title_info = new_root.find("n:description[1]/n:title-info[1]", namespaces=SetSeries.ns_map)
        sequence = title_info.find("n:sequence", namespaces=SetSeries.ns_map)
        if sequence is None:
            title_info.append(et.Element("sequence",
                                         name=self.book_series_ids[book_id][0],
                                         number=self.book_series_ids[book_id][1]
                                         if self.book_series_ids[book_id][1] else ''))
        return new_root_tree

    def save_series(self):
        with open("./user_data/user_series.json", "w", encoding='utf-8') as f:
            json.dump(self.user_series, f, ensure_ascii=False, indent=4)

    def get_new_series(self):
        if self.update:
            self.user_series = json.load(open('user_data/user_series.json', 'r', encoding='utf-8'))
            self.entries_to_process = {k: v for k, v in self.book_series_ids.items()
                                       if k not in self.user_series.keys()}
        else:
            self.entries_to_process = self.book_series_ids
