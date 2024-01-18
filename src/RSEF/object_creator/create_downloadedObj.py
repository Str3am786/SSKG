import logging
import os
import json
from ..download_pdf.download_pipeline import pdf_download_pipeline
from ..download_pdf.downloaded_obj import DownloadedObj
from ..object_creator.create_metadata_obj import metaDict_to_metaObj, doi_to_metadataObj
from ..extraction.pdf_title_extraction import extract_pdf_title
from ..metadata.api.openAlex_api_queries import pdf_title_to_meta
from ..object_creator.create_metadata_obj import extract_arxivID
from ..utils.regex import str_to_doiID


def meta_to_dwnldd(metadata_obj, output_dir):
    """
    :param metadata_obj: metadata object will be used to download the pdf
    :param output_dir: String output directory to where the pdf will be downloaded
    ----
    :returns:
    downloaded Object, which has a filename and filepath
    """
    # takes metadata and downloads the pdf
    if not metadata_obj:
        return None
    try:
        file_path = pdf_download_pipeline(id=metadata_obj.doi, output_directory=output_dir)
        file_name = os.path.basename(file_path)
        return DownloadedObj(title=metadata_obj.title, doi=metadata_obj.doi, arxiv=metadata_obj.arxiv, file_name=file_name, file_path=file_path)
    except Exception as e:
        try:
            meta_doi = str(metadata_obj.doi)
            logging.error("Error while creating the downloaded object with this doi: %s for due to %s", meta_doi, str(e))
        except:
            print("Error with metadataObj")
            logging.error("Error due to metadataObj")
        return None


def downloaded_dictionary(dwnldd_obj):
    """
    :param dwnldd_obj: Downloaded Object
    ----
    :returns:
    Dictionary of Downloaded Dictionary
    K: is the DOI V: Dictionary of downloaded Object
    """
    if not dwnldd_obj:
        return None
    return {dwnldd_obj.doi: dwnldd_obj.to_dict()}


def create_downloaded_json(downloaded_dict, output_folder):
    """
    Creates JSON from a downloaded object or list of downloaded Objects
    :param downloaded_dict: Dictionary representing a Downloaded Object
    :param output_folder: Path to folder where the json will be saved
    ----
    :returns:
    path to created JSON
    """
    output_path = output_folder + "/" + "downloaded_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(downloaded_dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path


def downloadedDic_to_downloadedObj(dwnldd_dict):
    """
    Turns a dictionary into a downloaded object
    :param dwnldd_dict: Dictionary representing a Downloaded Object
    ----
    :returns:
    DownloadedObject
    """
    title = safe_dic(dwnldd_dict, "title")
    doi = safe_dic(dwnldd_dict, "doi")
    arxiv = safe_dic(dwnldd_dict, "arxiv")
    file_name = safe_dic(dwnldd_dict, "file_name")
    file_path = safe_dic(dwnldd_dict, "file_path")
    return DownloadedObj(title=title, doi=doi, arxiv=arxiv, file_name=file_name, file_path=file_path)


def metaDict_to_downloaded(meta_dict, output_dir):
    """
    Metadata dictinary into downloaded Object
    :param meta_dict: metaObj as a dictionary
    :param output_dir: where the pdf will be downloaded
    ----
    :returns:
    downloadedObj
    """
    meta = metaDict_to_metaObj(meta_dict)
    return meta_to_dwnldd(metadata_obj=meta, output_dir=output_dir)


def metaJson_to_downloaded_dic(meta_json, output_dir):
    """
    :param meta_json: takes json of metadata objects,
    :param output_dir: where the pdfs will be downloaded
    -----
    :returns:
    Dictionary of downloaded dictionaries
    """
    result = {}
    try:
        with open(meta_json, 'r') as f:
            metas_dict = json.load(f)
    except Exception as e:
        print(str(e) + "Error while opening metadata json")
    for doi in metas_dict:
        meta_dict = safe_dic(metas_dict,doi)
        dwn_obj = metaDict_to_downloaded(meta_dict=meta_dict, output_dir= output_dir)
        result.update({dwn_obj.doi: dwn_obj.to_dict()})
    return result


def metaJson_to_downloadedJson(meta_json, output_dir):
    """
    :param meta_json: takes json of metadata objects,
    :param output_dir: where the pdfs will be downloaded and the output JSON will be put
    -----
    :returns:
    path to JSON of downloaded dictionaries
    """
    dict = metaJson_to_downloaded_dic(meta_json, output_dir)
    output_path = output_dir + "/" + "downloaded_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path


def doi_to_downloadedObj(doi, output_dir):
    """
    Takes DOI extracts metadata and download pdf, Creating a Downloaded Object
    :param doi: String representing a DOI
    :param output_dir: Path to where the pdf will be downloaded
    :returns:
    downloaded Object
    """
    meta = doi_to_metadataObj(doi)
    if meta:
        return meta_to_dwnldd(meta, output_dir)
    else:
        return _doi_to_downloaded_obj_backup(doi, output_dir)


def _doi_to_downloaded_obj_backup(doi, output_dir):
    """Used if the doi given does not return any metadata from Open Alex
    :returns:
    downloaded Object
    """
    try:
        file_path = pdf_download_pipeline(id=doi, output_directory=output_dir)
        if not file_path:
            return None
        #TODO extract title
        return DownloadedObj(title=extract_pdf_title(pdf_path=file_path), doi=doi, arxiv=None,
                             file_name=os.path.basename(file_path), file_path=file_path)
    except Exception as e:
        logging.error(f"An error occurred in _doi_to_downloaded_obj_backup: {str(e)}")
        return None


def doi_to_downloadedDic(doi, output_dir) -> dict:
    """
    Takes DOI extracts metadata and download pdf, Creating a Downloaded Object
    :param doi: String representing a DOI
    :param output_dir: Path to where the pdf will be downloaded
    :returns:
    downloaded Object as Dictionary
    """
    return downloaded_dictionary(doi_to_downloadedObj(doi, output_dir))


def dois_to_downloadedDics(dois_list, output_dir):
    result = {}
    if not dois_list:
        return
    for doi in dois_list:
        if doi:
            if dwnldd := doi_to_downloadedDic(doi, output_dir):
                result.update(dwnldd)
    return result


def dois_txt_to_downloadedDics(dois_txt, output_dir):
    try:
        with open(dois_txt, 'r') as file:
            dois = file.read().splitlines()
    except:
        print("Error while opening the txt")
    return dois_to_downloadedDics(dois,output_dir)


def doi_to_downloadedJson(doi, output_dir):
    dict = doi_to_downloadedDic(doi, output_dir)
    output_path = output_dir + "/" + "downloaded_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path


def dois_to_downloadedJson(dois, output_dir):
    """
    Takes list of DOIs extracts metadata and download pdf, Creating a Downloaded Object for each and saves it in JSON
    :param doi: String representing a DOI
    :param output_dir: Path to where the pdf will be downloaded
    :returns:
    Path to JSON
    """
    dict = dois_to_downloadedDics(dois, output_dir)
    output_path = output_dir + "/" + "downloaded_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path


def dois_txt_to_downloadedJson(dois_txt, output_dir):
    dic = dois_txt_to_downloadedDics(dois_txt, output_dir)
    output_path = output_dir + "/" + "downloaded_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(dic, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path


def pdf_to_downloaded_obj(pdf, output_dir):
    # TODO
    if not os.path.exists(output_dir):
        raise FileNotFoundError
    if not (title := extract_pdf_title(pdf_path=pdf)):
        return None
    resp_jsn = pdf_title_to_meta(title)
    title = safe_dic(resp_jsn, "title")
    doi = str_to_doiID(safe_dic(resp_jsn, "doi"))
    arxiv = extract_arxivID(resp_jsn)
    return DownloadedObj(title=title,doi=doi,arxiv=arxiv,file_name="",file_path=pdf)


def download_from_doi(doi,output_dir):
    return doi_to_downloadedJson(doi,output_dir)


def download_from_doi_list(dois, output_dir):
    return dois_to_downloadedJson(dois, output_dir)


def download_from_doi_txt(dois_txt, output_dir):
    return dois_to_downloadedJson(dois_txt, output_dir)


def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None
