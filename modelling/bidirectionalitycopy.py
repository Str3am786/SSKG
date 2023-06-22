import os
import json
import arxiv
from metadata_extraction.somef_extraction.somef_extractor import find_doi
from metadata_extraction.somef_extraction.somef_extractor import description_finder
from metadata_extraction.somef_extraction.somef_extractor import find_arxiv
import requests
import jaro
from bs4 import BeautifulSoup
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def is_doi_bidirectional(repo_file, pdf_file_name):
    try:
        repo_data = load_json(repo_file)
    except:
        print("Error while opening the repository file")
        return False
    doi = find_doi(repo_data)
    if doi:
        doi_pdf = pdf_file_name.replace('.pdf','').replace('_','/')
        return doi == doi_pdf
    else:
        print("No doi found within the citation")
        return False

def is_citation_bidirectional(pdfObj,repo_json):
    is_bidir = False
    try:
        repo_data = load_json(repo_json)
    except:
        print ("Error while opening the repository file")
        return False
    doi = find_doi(repo_data)
    doi_pdf = pdfObj.doi
    if doi:
            is_bidir = (doi == doi_pdf)
    if ((arxivID:= find_arxiv(repo_data)) and not is_bidir):
        try:
            if arxivID is not None and arxivID == pdfObj.arxiv:
                return True
            paper_list = get_paper_from_arxiv_id(arxivID)
            if len(ls_doi := get_doi_from_arxiv_id(paper_list)) > 0:
                for doi in ls_doi:
                    if doi == doi_pdf:
                        return True
            if len(ls_titles := get_title_from_arxiv_id(paper_list)) > 0:
                if pdfObj.title in ls_titles:
                    return True

        except:
            print("Error while trying to request for arxiv")
            return False
    return is_bidir
def is_desc_bidirectional(paper, repo_file):
    pdf_doi = ""
    try:
        repo_data = load_json(repo_file)
    except:
        print("Error while opening the repo file")
        return False

    description = description_finder(repo_data)
    if len(description['doi'])>0:
        return pdf_doi in description['doi']
    elif len(description['arxiv'])>0:
        if paper.arxiv in description['arxiv']:
            return True
        paper_list = get_paper_from_arxiv_id(description['arxiv'])
        ls_repo_doi = get_doi_from_arxiv_id(paper_list)
        return pdf_doi in ls_repo_doi

def get_paper_from_arxiv_id(arxiv_id_list):
    ls_papers = []
    for id in arxiv_id_list:
        search = arxiv.Search(id_list=[str(id)])
        paper = next(search.results())
        ls_papers.append(paper)
        return ls_papers if len(ls_papers) > 0 else False
def get_doi_from_arxiv_id(arxiv_paperList):
    ls_dois = []
    for paper in arxiv_paperList:
        if paper.doi:
            ls_dois.append(paper.doi)
    return ls_dois
def get_title_from_arxiv_id(arxiv_paperList):
    ls_titles = []
    for paper in arxiv_paperList:
        if paper.title:
            ls_titles.append(paper.title)
    return ls_titles
#TODO
def title_compare(found_title, pdf_title):
    jaro_score = jaro.jaro_winkler_metric(found_title, pdf_title)
    return True if jaro_score > 0.85 else False

def get_doi_from_arxiv(arxiv_id):
    # Step 1: Query arXiv API to retrieve metadata
    url = f"https://arxiv.org/abs/{arxiv_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        doi_link = soup.find('a', href=lambda href: href and 'doi.org' in href)
        if doi_link:
            return doi_link.contents
        return None
        print("DOI not found for the given arXiv ID.")
    else:
        print("Error occurred while querying the arXiv API.")
    return None


def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None

def safe_list(list, i):
    try:
        return list[i]
    except:
        return None