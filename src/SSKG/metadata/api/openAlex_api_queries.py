import os

import requests
import json
from fuzzywuzzy import fuzz
from urllib.parse import quote

BASE_URL = 'https://api.openalex.org/works'

def query_openalex_api(doi):
    doi_url = convert_to_doi_url(doi)
    url = BASE_URL + "/" + doi_url
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('Error:', response.status_code)
        print(doi)
        return None


def convert_to_doi_url(input_string):
    if input_string.startswith('http://doi.org/') or input_string.startswith('https://doi.org/'):
        return input_string

    doi = input_string.strip()
    doi_url = 'https://doi.org/' + doi
    return doi_url

def pdf_name_to_meta(pdf_folder,path_out):
    list_datas = []
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            doi = file.replace("_","/").replace(".pdf",'')
            data = query_openalex_api(doi)
            list_datas.append(data)
    with open(path_out, 'w') as json_file:
        json.dump(list_datas, json_file, indent=4)

def txt_to_meta(txt,path_out):
    list_datas = []
    with open(txt, 'r') as file:
        dois = file.read().splitlines()

    for doi in dois:
        data = query_openalex_api(doi)
        list_datas.append(data)

    with open(path_out, 'w') as json_file:
        json.dump(list_datas, json_file, indent=4)

#TODO need to create a way to double check the pdf title vs the one extracted
#TODO ensure that the first option in the returned list is the one I want

def _verify_title(response_json, og_title):
    """
    Give the correct result by comparing titles based on a fuzzy matching ratio.

    :param response_json: JSON response from the search.
    :param original_title: PDF title to match against.
    :return: Metadata of result if the titles match.
    """
    fuzzy_threshold = 85
    try:
        results = response_json["results"]
    except KeyError:
        return None
    for result in results:
        try:
            title = result['title']
        except:
            continue
        if (fuzz.partial_ratio(og_title.lower(), title.lower())) > fuzzy_threshold:
            return result
    print("Work not found within OpenAlex")
    return None

def pdf_title_to_meta(title):
    """

    """
    if title == None or title == "":
        return None
    title_url = quote(title)
    url = BASE_URL + "?filter=title.search:" + title_url
    try:
        response = requests.get(url)
        if response.status_code == 200:

            return _verify_title(response_json=response.json(), og_title=title)
        else:
            raise requests.RequestException(f"Error: {response.status_code}")
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {str(e)}")


#input = '../../corpus_papers_w_code/papers_with_code'
#pdf_name_to_meta(input,'./penis.json')

#txt_to_meta('./dois.txt','./pls.json')