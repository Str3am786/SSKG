#from metadata_extraction.pdf_extraction.github_extractor_tika import pdf_to_git_url
from metadata_extraction.somef_extraction.somef_extractor import download_repo_metadata
from modelling.bidirectionality import is_doi_bidirectional, is_doi_bidir, is_arxiv_bidir
from modelling.unidirectionality import is_repo_unidir
from metadata_extraction.pdf_extraction.github_extractor_tika import make_Pdf_Obj, is_filename_doi, read_pdf, \
    ranked_git_url
from download_pdf.openalex.api_queries import query_openalex_api
from metadata_extraction.paper_obj import PaperObj
from download_pdf.pipeline import pdf_download_pipeline
import json
import os
import re

#AUX====================
#TODO cleanup
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
def extract_arxivID (openAlexJson):
    location = safe_dic(openAlexJson, "locations")
    for locat in location:
        if safe_dic(locat, "is_oa") == True:
            if safe_dic(locat, "pdf_url") and "arxiv" in safe_dic(locat, "pdf_url"):
                return url_to_arxivID(safe_dic(locat,"pdf_url"))


def get_directory_and_filename(file_path):
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    return directory, filename

def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)
#===========================
#TODO
def _iter_urls():
    return


def check_paper_bidir(doi, output_folder):
    """
    Takes doi and output folder to download the somef JSON
    :returns
    dictionary K: doi, V: List of urls that link back to the paper
    -------
    """
    result = {}
    try:
        #gather metadata from DOI (openAlex)
        try:
            pdf_meta = query_openalex_api(doi)
        except Exception as e:
            print(str(e))
        #TODO
        if pdf_meta is None:
            print("No meta")
        firstTime = True
        titL = safe_dic(pdf_meta,"title")
        doi = url_to_doiID(safe_dic(pdf_meta, "doi"))
        arxiv = extract_arxivID(pdf_meta)

        #Download the pdf
        pdf_path = pdf_download_pipeline(doi, output_folder)
        #Open it with Tika
        pdf_data = read_pdf(pdf_path)
        github_urls = ranked_git_url(pdf_data)
        if github_urls is None or len(github_urls) == 0:
            return None
        directory, filename = get_directory_and_filename(pdf_path)
        paper = PaperObj(titL, github_urls,doi,arxiv,filename,pdf_path)
        #runs through the list of extracted github urls, starting with the most frequently mentioned
        for pair in github_urls:
            url = pair[0]
            #Download repository from SOMEF
            repo_file = download_repo_metadata(url, output_folder)
            #assessment of bidirectionality
            is_bidir = (is_doi_bidir(paper, repo_file) or is_arxiv_bidir(paper, repo_file))
            if is_bidir:
                if firstTime:
                    result[doi] = []
                    firstTime = False
                result[doi].append(url)
                #TODO create pair or dict value of doi + list_url
                #TODO if exists, append/extend list
    except Exception as e:
        print("error while trying to extract metadata")
        print(str(e))
        pass

    if len(result.keys()) > 0:
        return result
    else:
        None




def pipeline_bidir(list_dois_txt, output_folder):
    """
    Takes list of dois, as a TXT and output folder to download the somef JSON
    :returns
    list of dictionaries
    dictionary K: doi, V: List of urls that link back to the paper
    -------
    """
    result = {}
    try:
        with open(list_dois_txt, 'r') as file:
            dois = file.read().splitlines()
    except:
        print("Error while opening the txt")

    for doi in dois:
        data = check_paper_bidir(doi,output_folder)
        if data:
            result.update(data)

    return result

def pipeline_unidir(list_dois_txt, output_folder):
    """
    Takes list of dois, as a TXT and output folder to download the somef JSON
    :returns
    list of dictionaries
    dictionary K: doi, V: List of urls that link back to the paper
    -------
    """
    result = {}
    try:
        with open(list_dois_txt, 'r') as file:
            dois = file.read().splitlines()
    except:
        print("Error while opening the txt")

    for doi in dois:
        data = check_paper_unidir(doi,output_folder)
        if data:
            result.update(data)

    return result

def check_paper_unidir(doi, output_folder):
    """
    Takes doi and output folder to download the somef JSON
    :returns
    dictionary K: doi, V: List of repo urls that mention paper
    -------
    """
    result = {}
    try:
        #gather metadata from DOI (openAlex)
        try:
            pdf_meta = query_openalex_api(doi)
        except Exception as e:
            print(str(e))
        #TODO
        if pdf_meta is None:
            print("No meta")
        firstTime = True
        titL = safe_dic(pdf_meta,"title")
        doi = url_to_doiID(safe_dic(pdf_meta, "doi"))
        arxiv = extract_arxivID(pdf_meta)

        #Download the pdf
        pdf_path = pdf_download_pipeline(doi, output_folder)
        #Open it with Tika
        pdf_data = read_pdf(pdf_path)
        github_urls = ranked_git_url(pdf_data)
        if github_urls is None or len(github_urls) == 0:
            return None
        directory, filename = get_directory_and_filename(pdf_path)
        paper = PaperObj(titL, github_urls,doi,arxiv,filename,pdf_path)
        #runs through the list of extracted github urls, starting with the most frequently mentioned
        for pair in github_urls:
            url = pair[0]
            #Download repository from SOMEF
            repo_file = download_repo_metadata(url, output_folder)
            #assessment of bidirectionality
            is_unidir = is_repo_unidir(paper, repo_file)
            if is_unidir:
                if firstTime:
                    result[doi] = []
                    firstTime = False
                result[doi].append(url)
    except Exception as e:
        print("error while trying to extract metadata")
        print(str(e))
        pass

    if len(result.keys()) > 0:
        return result
    else:
        None
def unidir_to_json(list_dois_txt, output_folder):
    dict = pipeline_unidir(list_dois_txt,output_folder)

    with open(output_folder + "/" + "unidir.json", 'w+') as out_file:
        json.dump(dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
def bidir_to_json(list_dois_txt, output_folder):
    dict = pipeline_bidir(list_dois_txt,output_folder)

    with open(output_folder + "/" + "bidir.json", 'w+') as out_file:
        json.dump(dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)



