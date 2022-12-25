from src.database_connection import ConnectDatabase
import re


class GetDatabaseData(ConnectDatabase):

    def __init__(self):
        super().__init__()
        self.cur = None

    def get_books(self):
        sql_books = "SELECT \
            book.id AS bid, book.slug as slug, book.title_author AS author, \
            book.title AS btitle, book.subtitle AS bsubtitle, book.title_extra as extra,  \
            (SELECT GROUP_CONCAT \
            (DISTINCT '[' || text.id || ',\"' || COALESCE(series.name, 'NULL') || '\",\"' || person.name || '\"]') \
            as s_n FROM book_text WHERE series.name NOT NULL GROUP BY book_text.text_id \
            ) AS ser_name, \
            GROUP_CONCAT(DISTINCT text.sernr) as ser_num, book_revision.date, book.lang \
            FROM book \
            LEFT JOIN book_text ON book.id = book_text.book_id \
            LEFT JOIN book_revision ON book.id = book_revision.book_id \
            LEFT JOIN text ON text.id = book_text.text_id \
            LEFT JOIN text_revision ON text_revision.text_id = text.id \
            LEFT JOIN series ON series.id = text.series_id \
            LEFT JOIN text_author ON text_author.text_id = text.id \
            LEFT JOIN person ON person.id = text_author.person_id \
            WHERE book.formats LIKE '%\"sfb\"%'\
            GROUP BY bid \
            ORDER BY bid "
        self.cur.execute(sql_books)
        return self.cur.fetchall()

    def get_texts(self):
        sql_text_book = "SELECT \
            text.id AS tid, text.slug as slug, person.name AS author, text.title AS t_title, text.subtitle, \
            series.name as ser_name, text.sernr as ser_num, text_revision.date, text.lang \
            FROM text \
            LEFT JOIN text_revision ON text_revision.text_id = text.id \
            LEFT JOIN series ON series.id = text.series_id \
            LEFT JOIN text_author ON text_author.text_id = text.id \
            LEFT JOIN person ON person.id = text_author.person_id \
            WHERE tid NOT IN (SELECT text_id FROM book_text) \
            GROUP BY tid \
            ORDER BY tid "
        self.cur.execute(sql_text_book)
        return self.cur.fetchall()

    def _get_orig_author_names(self):
        names = {}
        sql_orig_author_names = f"SELECT person.name AS person_name, person.orig_name as orig_name " \
                            f"FROM person " \
                            f"WHERE person.orig_name IS NOT NULL "
        self.cur.execute(sql_orig_author_names)
        orig_author_names = self.cur.fetchall()
        for t in orig_author_names:
            if t and t[1] and re.search(r'([a-zA-Z]+)', t[1]):
                names[t[0]] = t[1]
        return names
