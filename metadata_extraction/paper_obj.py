
import re


#TODO put this into a regex.py and remove all the instances of this
def arxiv_cleaner(value):
    pattern = r'.*(\d{4}\.\d{4,5}).*'
    matches = re.findall(pattern, value)
    return matches

def doi_cleaner(value):
    pattern = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
    matches = re.findall(pattern, value)
    return matches
class PaperObj:
    def __init__(self, title, urls, doi, arxiv, file_name, file_path):
        self._title = title
        self._urls = urls
        try:
            self._doi = doi_cleaner(doi)[0]
        except:
            self._doi = None
        try:
            self._arxiv = arxiv_cleaner(arxiv)[0]
        except:
            self._arxiv = None
        self._file_name = file_name
        self._file_path = file_path


    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def urls(self):
        return self._urls

    @urls.setter
    def urls(self, value):
        self._urls = value

    @property
    def doi(self):
        return self._doi

    @doi.setter
    def doi(self, value):
        self._doi = value

    @property
    def arxiv(self):
        return self._arxiv

    @arxiv.setter
    def arxiv(self, value):
        self._arxiv = value

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value



    def to_dict(self):
        return {
            'title': self._title,
            'urls': self._urls,
            'doi': self._doi,
            'arxiv': self.arxivID,
            'file_name': self._file_name,
            'file_path': self._file_path
        }