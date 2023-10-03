from ..download_pdf.download_pipeline import pdf_download_pipeline
from ..download_pdf.downloaded_obj import DownloadedObj
import os
import json
from .doi_to_metadata import metaDict_to_metaObj, doi_to_metadataObj


def meta_to_dwnldd(metadataObj, output_dir):
    """
    @Param metdataObj metadata object will be used to download the pdf
    @Param output_dir output directory to where the pdf will be downloaded
    ----
    :returns
    downloaded Object, which has a filename and filepath
    """
    # takes metadata and downloads the pdf
    if not metadataObj:
        return None
    try:
        file_path = pdf_download_pipeline(doi=metadataObj.doi,output_directory=output_dir)
        file_name = os.path.basename(file_path)
        return DownloadedObj(title=metadataObj.title,doi=metadataObj.doi,arxiv=metadataObj.arxiv,file_name=file_name,file_path=file_path)
    except Exception as e:
        print("Error while creating the downloaded object")
        print(str(e))
        return None


def downloaded_dictionary(dwnldd_obj):
    """
    @Param dwnldd_obj
    ----
    :returns 
    Dictionary of Downloaded Dictionary
    K: is the DOI V: Dictionary of downloaded Object
    """
    return {dwnldd_obj.doi: dwnldd_obj.to_dict()}

def create_downloaded_json(downloaded_dict,output_folder):
    output_path = output_folder + "/" + "downloaded_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(downloaded_dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path

def downloadedDic_to_downloadedObj(dwnldd_dict):
    title = safe_dic(dwnldd_dict, "title")
    doi = safe_dic(dwnldd_dict, "doi")
    arxiv = safe_dic(dwnldd_dict, "arxiv")
    file_name = safe_dic(dwnldd_dict,"file_name")
    file_path = safe_dic(dwnldd_dict,"file_path")
    return DownloadedObj(title=title, doi=doi, arxiv=arxiv, file_name=file_name, file_path=file_path)


def metaDict_to_downloaded(meta_dict, output_dir):
    '''
    @Param meta_dict metaObj as a dictionary
    @Param output_dir where the pdf will be downloaded
    ----
    :return
    downloadedObj
    '''
    meta = metaDict_to_metaObj(meta_dict)
    return meta_to_dwnldd(metadataObj=meta, output_dir=output_dir)


def metaJson_to_downloaded_dic(meta_json, output_dir):
    '''
    @Param meta_json takes json of metadata objects,
    @Param output_dir where the pdfs will be downloaded
    -----
    :returns
    Dictionary of downloaded dictionaries
    '''
    result = {}
    try:
        with open(meta_json, 'r') as f:
            metas_dict = json.load(f)
    except Exception as e:
        print(str(e) + "Error while opening metadata json")
    for doi in metas_dict:
        meta_dict = safe_dic(metas_dict,doi)
        dwnObj = metaDict_to_downloaded(meta_dict=meta_dict, output_dir= output_dir)
        result.update({dwnObj.doi: dwnObj.to_dict()})
    return result

def metaJson_to_downloadedJson(meta_json, output_dir):
    '''
    @Param meta_json takes json of metadata objects,
    @Param output_dir where the pdfs will be downloaded and the output JSON will be put
    -----
    :returns
    path to JSON of downloaded dictionaries
    '''
    dict = metaJson_to_downloaded_dic(meta_json, output_dir)
    output_path = output_dir + "/" + "downloaded_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path

def doi_to_downloadedObj(doi,output_dir):
    meta = doi_to_metadataObj(doi)
    return meta_to_dwnldd(meta,output_dir)

def doi_to_downloadedDic(doi,output_dir):
    return downloaded_dictionary(doi_to_downloadedObj(doi, output_dir))


def dois_to_downloadedDics(dois_list, output_dir):
    result = {}
    for doi in dois_list:
        result.update(doi_to_downloadedDic(doi,output_dir))
    return result
def dois_txt_to_downloadedDics(dois_txt,output_dir):
    try:
        with open(dois_txt, 'r') as file:
            dois = file.read().splitlines()
    except:
        print("Error while opening the txt")
    return dois_to_downloadedDics(dois,output_dir)

def doi_to_downloadedJson(doi,output_dir):
    dict = doi_to_downloadedDic(doi, output_dir)
    output_path = output_dir + "/" + "downloaded_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path
def dois_to_downloadedJson(dois,output_dir):
    dict = dois_to_downloadedDics(dois, output_dir)
    output_path = output_dir + "/" + "downloaded_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path
def dois_txt_to_downloadedJson(dois_txt,output_dir):
    dict = dois_txt_to_downloadedDics(dois_txt, output_dir)
    output_path = output_dir + "/" + "downloaded_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path

def download_from_doi(doi,output_dir):
    return doi_to_downloadedJson(doi,output_dir)
def download_from_doi_list(dois,output_dir):
    return dois_to_downloadedJson(dois,output_dir)
def download_from_doi_txt(dois_txt,output_dir):
    return dois_to_downloadedJson(dois_txt, output_dir)
def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None
