class ResolveSeries:

    def __init__(self, authors, s_num, s_info):
        self.authors = authors
        self.series_num = s_num
        self.series = s_info

    def check_series(self):
        if self.authors:
            author_ser = [x for x in self.series if x[2] in self.authors]
        else:
            author_ser = self.series

        series_name = ''
        for i, el in enumerate(author_ser):
            series_name = el[1]
            if i > 0 and not author_ser[i - 1][1] == series_name:
                return [None, None]
            if series_name == 'NULL':
                return [None, None]

        return [series_name, self.series_num]
