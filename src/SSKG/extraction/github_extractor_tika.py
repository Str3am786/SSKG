import collections
import os
import re
from tika import parser
from SSKG.metadata_extraction.paper_obj import PaperObj

def read_pdf(pdf_path):
    try:
        raw = parser.from_file(pdf_path)
        list_pdf_data = raw['content'].split('\n')
        # delete empty lines
        list_pdf_data = [x for x in list_pdf_data if x != '']

        return list_pdf_data
    except Exception as e:
        return []

def find_abstract_index(pdf_data):
    index = 0
    for line in pdf_data:
        if "abstract" in line.lower():
            if index < len(pdf_data):
                return index
        index +=1
def get_possible_abstract(pdf_data):
    try:
        index = find_abstract_index(pdf_data)
        if index:
            return ''.join(pdf_data[index:index+50])
    except Exception as e:
        print(e)

def find_github_in_abstract(pdf_data):
    abstract = get_possible_abstract(pdf_data)
    if abstract:
        return look_for_github_urls(abstract)

#regular expression to get all the urls, returned as a list
def get_git_urls(text):
    """
    Returns
    -------
    List Strings (urls)

    """
    urls_github = re.findall(r'(https?://github.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)', text)
    urls_gitlab = re.findall(r'(https?://gitlab.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)', text)
    # urls_zenodo = re.findall(r'(https?://zenodo.org/\S+)', text)
    # urls_bitbucket = re.findall(r'(https?://bitbucket.org/\S+)', text)
    # urls_sourceforge = re.findall(r'(https?://sourceforge.net/\S+)', text)
    # create a list with all the urls found
    urls = urls_github + urls_gitlab
    return urls

def look_for_github_urls(list_pdf_data):
    github_urls = []
    for value in list_pdf_data:
        results = get_git_urls(value)
        if results:
            github_urls.extend(results)
    github_urls = [url[:-1] if url[-1] == '.' else url for url in github_urls]
    return github_urls

def save_github_urls(github_urls, output_path):
    with open(output_path, 'w') as f:
        f.write('\n'.join(github_urls))
    return 200

def rank_elements(url_list):
    """
    Takes a list of strings

    Returns
    --------
    List of dictionary pairs. Key being the url (String) and the value the number of appearances
    Ordered, High to Low, Number of appearances
    """
    counts = collections.defaultdict(int)
    for url in url_list:
        counts[url] += 1
    return sorted(counts.items(),
                 key=lambda k_v: (k_v[1], k_v[0]),
                 reverse=True)


def ranked_git_url(pdf_data):
    """
    Creates  ranked list of github urls and count pairs or false if none are available
    Returns
    -------
    List Strings (urls)
    --
    Else (none are found)
        False
    """
    try:
        github_urls = look_for_github_urls(pdf_data)
        if github_urls:
            return rank_elements(github_urls)
        else:
            return None
    except Exception as e:
        print(str(e))
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

def get_file_name(file_path):
    file_name = os.path.basename(file_path)
    return file_name



def make_Pdf_Obj(pdf_path):
    """
    DEPRECATED
    Takes pdf path, opens pdf, and
    Creates a paper_obj:
        Title: First extracted line (has fail rate)
        github_urls = extracted and ranked github urls from pdf as list
        doi = filename converted to doi formated, it is checked before if it is correct
    Returns
    -------
    paper obj
    """
    try:
        pdf_data = read_pdf(pdf_path)
        pdf_title =  pdf_data[0]
        github_urls = ranked_git_url(pdf_data)
        pdf_file_name = get_file_name(pdf_path)
        doi = is_filename_doi(pdf_file_name)
        arxiv = None
        pdf = PaperObj(pdf_title, github_urls, doi, arxiv, pdf_file_name, pdf_path)
        return pdf
    except Exception as e:
        print(str(e))