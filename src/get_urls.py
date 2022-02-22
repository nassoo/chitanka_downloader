from src.get_sql_data import GetDatabaseData
from src.series_resolve import ResolveSeries
from src.resolve_authors import ResolveAuthors


class GetBooks(GetDatabaseData):

    def __init__(self):
        super().__init__()
        self.urls = []
        self.books = self.get_books()
        self.texts = self.get_texts()
        self.chars_to_replace = {'&': 'и', '%': '_', ':': '_', '>': '_', '!': '_', '?': '_', '\\n': ' ', '//': 'II'}
        self.book_series_ids = {}

    def urls_list(self):

        for book in self.books:
            s_info = None
            series = None
            series_num = None
            book_id, slug, book_authors, book_title, \
                book_subtitle, book_title_extra, ser_info, ser_num, date, lang = book
            if ser_info:
                s_info = [x for x in eval(ser_info)]
                if not type(s_info[0]) == list:
                    s_info = [s_info]
                series, series_num = ResolveSeries(book_authors, ser_num, s_info).check_series()
            authors, book_authors = ResolveAuthors(book_authors).clear_authors()
            curr_book_path = '/'
            if lang == 'bg':
                curr_book_path += 'Български/'
            elif lang == 'en':
                curr_book_path += 'Английски/'
            else:
                curr_book_path += 'Други/'
            curr_book_path += authors[0] + '/'
            if not authors == '_':
                curr_book_path += authors + '/'
            if series:
                curr_book_path += series + '/'
                book_key = 'book/' + str(book_id)
                self.book_series_ids[book_key] = [series, series_num]
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
            for key, value in self.chars_to_replace.items():
                curr_book_path = curr_book_path.replace(key, value)
            date = int(date.replace(' ', '').replace(':', '').replace('-', ''))
            self.urls.append(['book/' + str(book_id), lang, slug, curr_book_path, date])

        for text in self.texts:
            text_id, slug, text_authors, text_title, text_subtitle, ser_name, ser_num, date, lang = text
            curr_text_path = '/'
            if lang == 'bg':
                curr_text_path += 'Български/'
            elif lang == 'en':
                curr_text_path += 'Английски/'
            else:
                curr_text_path += 'Други/'
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
            for key, value in self.chars_to_replace.items():
                curr_text_path = curr_text_path.replace(key, value)
            date = date.replace(' ', '').replace(':', '').replace('-', '')
            self.urls.append(['text', str(text_id), lang, slug, curr_text_path, date])

        with open("./output/test_texts-output.txt", "w", encoding='UTF8') as output:
            for row in self.urls:
                output.write(str(row) + '\n')
