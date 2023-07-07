import re

#pipeline

DOI_REGEX= r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
ARXIV_REGEX = r'.*(\d{4}\.\d{4,5}).*'

def str_to_doiID(string):
    match = re.search(DOI_REGEX, string)
    if match:
        doi = match.group(1)
        return doi
    return None

def str_to_arxivID(string):
    match = re.search(ARXIV_REGEX, string)
    if match:
        arxiv = match.group(1)
        return arxiv
    return None

def url_to_doiID(doi_url):
    pattern = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
    match = re.search(pattern, doi_url)
    if match:
        doi = match.group(1)
        return doi
    return None

def url_to_arxivID(arxiv_url):
    pattern = r'.*(\d{4}\.\d{4,5}).*'
    match = re.search(pattern, arxiv_url)
    if match:
        arxiv = match.group(1)
        return arxiv
    return None

#somef extraction

def list_dois(value):
    pattern = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
    matches = re.findall(pattern, value)
    return matches
def list_arxivs(value):
    pattern = r'.*(\d{4}\.\d{4,5}).*'
    matches = re.findall(pattern, value)
    return matches

#paperobj

#TODO put this into a regex.py and remove all the instances of this
def arxiv_cleaner(value):
    pattern = r'.*(\d{4}\.\d{4,5}).*'
    matches = re.findall(pattern, value)
    return matches

def doi_cleaner(value):
    pattern = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
    matches = re.findall(pattern, value)
    return matches

#tika

def is_filename_doi(file_name):
    """
    Regex on the file name and return it if it is of DOI ID format.
    Returns
    -------
    List Strings (doi's)
    """
    file_name = file_name.replace('_','/').replace('.pdf','').replace('-DOT-','.')
    pattern = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
    match = re.search(pattern,file_name)
    if match:
        return file_name
    else:
        return False

    matches = re.findall(pattern, file_name)
    return matches