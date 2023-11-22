import json
import jaro
import arxiv
import requests
from bs4 import BeautifulSoup
from SSKG.extraction.somef_extraction.somef_extractor import (
    find_doi_citation,
    description_finder,
    find_arxiv_citation,
    get_related_paper
)


def is_it_bidir(paper_obj, repo_json):
    """
    Checks if the paper relationship with the repository is bidirectional.

    :param paper_obj: An instance of the Paper class representing the paper.
    :param repo_json: A string representing the path to the JSON file of the repository.

    :returns:
    ID and its location (Two strings)
    """
    try:
        # Load somef json
        repo_data = load_json(repo_json)
    except Exception as e:
        # TODO update to a logging
        print("Error while trying to open the repository JSON")
        print(str(e))
        return None

    if doi := paper_obj.doi:
        bidir_location = is_doi_bidir(doi, repo_data)
        if bidir_location != "NOT_BIDIR":
            return doi, bidir_location

    if arxiv_id := paper_obj.arxiv:
        bidir_location = is_arxiv_bidir(arxiv_id, repo_data, paper_obj.title)
        if bidir_location != "NOT_BIDIR":
            return arxiv_id, bidir_location
    # TODO add other forms of identification
    else:
        return None

    return None


def is_doi_bidir(doi, repo_data):

    if _doi_is_citation_bidir(doi, repo_data):
        return "CITATION"
    if _doi_is_description_bidir(doi, repo_data):
        return "DESCRIPTION"
    else:
        return "NOT_BIDIR"


def _doi_is_description_bidir(pp_doi, repo_data):
    # run through description, if doi is found, will be within dictionary of lists
    doi_list = safe_dic(description_finder(repo_data), 'doi')
    if doi_list:
        for doi in doi_list:
            if not doi:
                continue
            if doi.lower() == pp_doi.lower():
                return True
    return False


def _doi_is_citation_bidir(pp_doi, repo_data):
    doi_list = find_doi_citation(repo_data)
    if doi_list:
        for doi in doi_list:
            if not doi:
                continue
            if doi.lower() == pp_doi.lower():
                return True
    return False

def is_arxiv_bidir(arxiv_id, repo_data, title):

    if _arxiv_in_citation(arxiv_id, repo_data):
        return "CITATION"

    elif _arxiv_in_description(arxiv_id, repo_data):
        return "DESCRIPTION"
    elif location := _arxiv_in_related(arxiv_id, repo_data, title):
        return location
    else:
        return "NOT_BIDIR"



def _arxiv_in_citation(arxiv_id, repo_data):

    if arxivID_list := find_arxiv_citation(repo_data):
        if arxivID_list is not None:
            if arxiv_id in arxivID_list:
                return "CITATION"
    else:
        return None


def _arxiv_in_description(arxiv_id, repo_data):

    arxiv_list = safe_dic(description_finder(repo_data), 'arxiv')
    if arxiv_list is not None and arxiv_id in arxiv_list:
        return "DESCRIPTION"
    else:
        return None


def _arxiv_in_related(arxiv_id, repo_data, title):

    if arxivID_list := get_related_paper(repo_data):
        if arxivID_list is not None:
            if arxiv_id in arxivID_list:
                return "RELATED_PAPERS"
            ls_papers = get_paper_from_arxiv_id(arxivID_list)
            if title.lower() in get_title_from_arxiv_id(ls_papers):
                return "TITLE ARXIV"
    return None


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
            ls_titles.append(paper.title.lower())
    return ls_titles


def get_paper_from_arxiv_id(arxiv_id_list):
    ls_papers = []
    for id in arxiv_id_list:
        search = arxiv.Search(id_list=[str(id)])
        paper = next(search.results())
        ls_papers.append(paper)
        return ls_papers if len(ls_papers) > 0 else False

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

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