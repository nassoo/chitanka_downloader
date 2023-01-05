from utilities.convert_filenames import convert_cyr_to_lat
from src.get_sql_data import GetDatabaseData
from src.resolve_authors import ResolveAuthors
from src.resolve_series import ResolveSeries


class GetContent:

    def __init__(self, app_data):
        self.app_data = app_data
        self.__chars_to_replace = {'&': 'и', '%': '_', ':': '_', '>': '_', '!': '_', '?': '_', '\\n': ' ', '//': 'II'}
        self.orig_author_names = {}

    def get_content(self):
        db = GetDatabaseData(self.app_data['cur'])
        self.orig_author_names = db.get_orig_author_names()

        for book in db.get_books():
            series = None
            series_num = None
            book_id, slug, book_authors, book_title, \
                book_subtitle, book_title_extra, ser_info, ser_num, date, lang = book
            if ser_info:
                s_info = [x for x in eval(ser_info)]
                if not type(s_info[0]) == list:
                    s_info = [s_info]
                series, series_num = ResolveSeries(book_authors, ser_num, s_info).check_series()
            curr_book_path = self.curr_path(lang)
            if self.app_data['filenames'] == 'латиница' and book_authors and book_authors != '':
                book_authors = self.get_orig_author(book_authors)
            authors, book_authors = ResolveAuthors(book_authors).clear_authors()
            curr_book_path += authors[0] + '/'
            if not authors == '_':
                curr_book_path += authors + '/'
            if series:
                curr_book_path += series[:-3] + '/' if series.endswith('...') else series + '/'
                book_key = 'book/' + str(book_id)
                self.app_data['book_series_ids'][book_key] = [series, series_num]
            if not authors == '_':
                curr_book_path += book_authors + ' - '
            if series:
                series_short_name = [x[0] for x in series.split() if x[0].isalpha()]
                curr_book_path += ''.join(series_short_name) + ' - '
                if series_num:
                    curr_book_path += series_num + ') '
            full_title = book_title
            if book_subtitle:
                full_title += ' [' + book_subtitle + ']'
            if book_title_extra:
                full_title += ' [' + book_title_extra + ']'
            if len(full_title) > 97:
                curr_book_path += full_title[:97]
            else:
                curr_book_path += full_title
            for key, value in self.__chars_to_replace.items():
                curr_book_path = curr_book_path.replace(key, value)
            date = int(date.replace(' ', '').replace(':', '').replace('-', ''))
            if self.app_data['filenames'] == 'латиница':
                curr_book_path = convert_cyr_to_lat(curr_book_path)
            if len(curr_book_path) > 200:
                curr_book_path = curr_book_path[:200].strip() + '…'
            self.app_data['urls']['book/' + str(book_id)] = [lang, slug, curr_book_path, date]

        for text in db.get_texts():
            text_id, slug, text_authors, text_title, text_subtitle, ser_name, ser_num, date, lang = text
            curr_text_path = self.curr_path(lang)
            if self.app_data['filenames'] == 'латиница' and text_authors and text_authors != '':
                text_authors = self.get_orig_author(text_authors)
            authors, text_authors = ResolveAuthors(text_authors).clear_authors()
            curr_text_path += authors[0] + '/'
            if not authors == '_':
                curr_text_path += authors + '/'
            if ser_name:
                curr_text_path += ser_name + '/'
            if not authors == '_':
                curr_text_path += text_authors + ' - '
            if ser_name:
                series_short_name = [x[0] for x in ser_name.split() if x[0].isalpha()]
                curr_text_path += ''.join(series_short_name) + ' - '
                if ser_num:
                    curr_text_path += str(ser_num) + ') '
            full_title = text_title
            if text_subtitle:
                full_title += ' [' + text_subtitle + ']'
            if len(full_title) > 97:
                curr_text_path += full_title[:97] + '…'
            else:
                curr_text_path += full_title
            for key, value in self.__chars_to_replace.items():
                curr_text_path = curr_text_path.replace(key, value)
            date = date.replace(' ', '').replace(':', '').replace('-', '')
            if self.app_data['filenames'] == 'латиница':
                curr_text_path = convert_cyr_to_lat(curr_text_path)
            if len(curr_text_path) > 200:
                curr_text_path = curr_text_path[:200].strip() + '…'
            self.app_data['urls']['text/' + str(text_id)] = [lang, slug, curr_text_path, date]

    def curr_path(self, lang):
        curr_path = ''
        if lang == 'bg':
            curr_path += 'Български/' if self.app_data['filenames'] == 'кирилица' else 'Bulgarian/'
        elif lang == 'en':
            curr_path += 'Английски/' if self.app_data['filenames'] == 'кирилица' else 'English/'
        else:
            curr_path += 'Други/' if self.app_data['filenames'] == 'кирилица' else 'Other/'
        return curr_path

    def get_orig_author(self, authors):
        authors_temp_list = []
        for author in authors.split(', '):
            author = author.strip()
            author_orig = self.orig_author_names[author] if author in self.orig_author_names else author
            authors_temp_list.append(author_orig)
        return ', '.join(authors_temp_list)
