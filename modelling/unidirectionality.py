import os
import json
import jaro
import arxiv
import requests
from bs4 import BeautifulSoup
from metadata_extraction.somef_extraction.somef_extractor import (
    find_doi_citation,
    description_finder
)

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def _iterate_results(results, string_2_find):
    if not results:
        return False
    for result in results:
        value = safe_dic(safe_dic(result,"result"),'value')
        if value:
            score = jaro.jaro_winkler_metric(value,string_2_find)
            if score > 0.8 or string_2_find in value:
                return True
    return False
def is_repo_unidir(pdfObj, repo_json):
    try:
        repo_data = load_json(repo_json)
    except:
        print("Error while opening the repository file")
        return False
    #Test if the titles match.
    results = safe_dic(repo_data,'full_title')
    unidir = _iterate_results(results,pdfObj.title)
    # test if within the description
    if not unidir:
        results = safe_dic(repo_data,'description')
        unidir = _iterate_results(results,pdfObj.title)
    if not unidir:
        results = safe_dic(repo_data,'citation')
        unidir = _iterate_results(results, pdfObj.title)
    return unidir

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