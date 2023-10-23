import re

#object_creator

DOI_REGEX= r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
ARXIV_REGEX = r'.*(\d{4}\.\d{4,5}).*'

def str_to_doiID(string):
    try:
        match = re.search(DOI_REGEX, string)
        if match:
            doi = match.group(1)
            return doi
        return None
    except:
        None

def str_to_arxivID(string):
    try:
        match = re.search(ARXIV_REGEX, string)
        if match:
            arxiv = match.group(1)
            return arxiv
        return None
    except:
        return None
#TODO change the _ for ! in the filename doi. Alsolook at oa_pdf_downloader
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

def filename_to_doi_convert(file_name):
    possDOI = file_name.replace('_', '/').replace('.pdf', '').replace('-DOT-', '.')
    pattern = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
    match = re.search(pattern,possDOI)
    if match:
        return match.group(1)
    return None