import lxml.etree as et
import os
import zipfile
import copy
import ntpath

from helpers.powermanagement import long_running
from src.download_from_server import DownloadFiles


class SetSeries(DownloadFiles):
    def __init__(self):
        super().__init__()
        self.download_progress = 0

    ns_map = {"n": 'http://www.gribuser.ru/xml/fictionbook/2.0'}

    @long_running
    def set_series(self):
        for book_id in self.book_series_ids.keys():
            if book_id in self.urls_to_download.keys():
                self.download_progress += 1
                input_file = os.path.join(self.output_dir, self.urls_to_download[book_id][2] + '.fb2.zip')
                output_file = os.path.join(self.output_dir, self.urls_to_download[book_id][2] + '.xml')
                print(input_file)
                with zipfile.ZipFile(input_file, 'r') as zf:
                    zip_file = zf.namelist()[0]
                    with open(output_file, "wb") as f:
                        f.write(zf.read(zip_file))
                os.remove(input_file)
                doc = et.parse(output_file)
                root = doc.getroot()
                new_tree = self.transform(root)
                new_tree.write(output_file, xml_declaration=True, encoding="utf-8")
                filename = ntpath.basename(output_file)
                print(filename)
                with zipfile.ZipFile(input_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.write(output_file, filename)
                os.remove(output_file)

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
                                         number=self.book_series_ids[book_id][1]))
        return new_root_tree
