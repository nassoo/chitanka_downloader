class ResolveAuthors:

    def __init__(self, auth):
        self.auth = auth

    def clear_authors(self):
        if self.auth == '' or not self.auth:
            return '_', '_'
        curr_authors = self.auth.split(', ')
        converted_authors = []
        for i, a in enumerate(curr_authors):
            if i > 2:
                break
            a_names = a.split()
            a_str = a_names[-1]
            if len(a_names) > 1:
                a_str += ', '
            a_str += ' '.join(a_names[:-1])
            converted_authors.append(a_str)
        curr_authors_str = ' _ '.join(curr_authors[:3])
        converted_authors_str = ' _ '.join(converted_authors)
        if len(curr_authors) > 3:
            curr_authors_str += '…'
            converted_authors_str += '…'

        return [converted_authors_str, curr_authors_str]
