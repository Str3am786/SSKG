import os

import requests
import json
import xmltodict


BASE_URL = 'https://api.openalex.org/works/'

def query_openalex_api(doi):
    doi_url = convert_to_doi_url(doi)
    url = BASE_URL + doi_url
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


#input = '../../corpus_papers_w_code/papers_with_code'
#pdf_name_to_meta(input,'./penis.json')

#txt_to_meta('./dois.txt','./pls.json')