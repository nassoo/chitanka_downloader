import lxml.etree as et
import os
import zipfile
import copy
import ntpath
import json
import logging
import urllib.parse

from utilities.powermanagement import long_running


class SetSeries:
    def __init__(self, controller):
        self.controller = controller
        self.controller.app_data['current_progress'] = 0
        self.get_new_series()

    ns_map = {"n": 'http://www.gribuser.ru/xml/fictionbook/2.0'}

    @long_running
    def set_series(self):
        logging.info("Setting series")
        for book_id in self.controller.app_data['entries_to_process']:
            self.controller.app_data['current_progress'] += 1
            input_file = os.path.join(self.controller.app_data['output_dir'],
                                      self.controller.app_data['urls'][book_id][2] + '.fb2.zip')
            dir_path = ntpath.dirname(ntpath.abspath(input_file))  # That way it is platform independent
            output_file = ''
            zip_file = ''
            try:
                with zipfile.ZipFile(input_file, 'r') as zf:
                    zip_file += zf.namelist()[0]
                    output_file += os.path.join(dir_path, zip_file)
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
            print(f'{book_id}: {input_file}')
            with zipfile.ZipFile(input_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.write(output_file, zip_file)
            os.remove(output_file)

            self.controller.app_data['user_series'][book_id] = self.controller.app_data['book_series_ids'][book_id]

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
                                         name=self.controller.app_data['book_series_ids'][book_id][0],
                                         number=self.controller.app_data['book_series_ids'][book_id][1]
                                         if self.controller.app_data['book_series_ids'][book_id][1] else ''))
        return new_root_tree

    def save_series(self):
        with open("./user_data/user_series.json", "w", encoding='utf-8') as f:
            json.dump(self.controller.app_data['user_series'], f, ensure_ascii=False, indent=4)

    def get_new_series(self):
        if self.controller.app_data['update']:
            self.controller.app_data['user_series'] = json.load(
                open('user_data/user_series.json', 'r', encoding='utf-8'))
            self.controller.app_data['entries_to_process'] = [k for k, v
                                                              in self.controller.app_data['book_series_ids'].items()
                                                              if
                                                              k not in self.controller.app_data['user_series'].keys()]
        else:
            self.controller.app_data['entries_to_process'] = [k for k
                                                              in self.controller.app_data['book_series_ids'].keys()]
