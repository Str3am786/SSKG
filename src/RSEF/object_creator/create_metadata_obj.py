import json
from ..metadata.api.openAlex_api_queries import query_openalex_api
from ..metadata.metadata_obj import MetadataObj
from RSEF.metadata.api.openAlex_api_queries import pdf_title_to_meta
from ..utils.regex import (
    str_to_arxivID,
    str_to_doiID
)


def extract_arxivID (openAlexJson):
    if openAlexJson is None:
        return None
    location = safe_dic(openAlexJson, "locations")
    for locat in location:
        if safe_dic(locat, "is_oa"):
            if safe_dic(locat, "pdf_url") and "arxiv" in safe_dic(locat, "pdf_url"):
                return str_to_arxivID(safe_dic(locat,"pdf_url"))


def doi_to_metadataObj(doi):
    """
    :param doi: String, DOI ID
    ------
    output
    :returns:
    metadata Object
    """
    if not (doi := str_to_doiID(doi)):
        print("Not a doi")
        return None
    try:
        try:
            oa_meta = query_openalex_api(doi)
        except Exception as e:
            print(str(e))
            return None
        if oa_meta is None:
            print("No meta")
        title = safe_dic(oa_meta, "title")
        doi = str_to_doiID(safe_dic(oa_meta, "doi"))
        arxiv = extract_arxivID(oa_meta)
        metadata = MetadataObj(title=title, doi=doi, arxiv=arxiv)
        return metadata
    except Exception as e:
        print(str(e))

# def title_to_meta_obj(title):
#     oa_meta = pdf_title_to_meta(title)
#     titL = safe_dic(oa_meta, "title")
#     doi = str_to_doiID(safe_dic(oa_meta, "doi"))
#     arxiv = extract_arxivID(oa_meta)
#     metadata = MetadataObj(title=titL, doi=doi, arxiv=arxiv)
#     return metadata


def doi_to_metaDict(doi):
    """
    :param doi: String, DOI ID
    ------
    output
    :returns:
    Dictionary:
        K: doi
        V: metadataObj.to_dict
    """
    if not (doi := str_to_doiID(doi)):
        print("Not a doi")
        return None
    mt_dict = doi_to_metadataObj(doi).to_dict()
    result = {mt_dict["doi"]: mt_dict}
    return result


def dois_to_metaDicts(list_of_dois):
    """
    :param list_of_dois: List of strings DOI
    ------
    output
    :returns:
    Dictionary:
        K: doi
        V: metadataObj.to_dict
    """
    result = {}
    for doi in list_of_dois:
        result.update(doi_to_metaDict(doi))
    return result


def doi_to_metaJson(doi, output_folder):
    """
    Input
    single doi
    ------
    output
    :returns
    path to JSON
    """
    meta_dict = doi_to_metaDict(doi)
    return create_meta_json(meta_dict, output_folder)


def dois_to_metaJson(doi, output_folder):
    """
    Input
    multiple dois
    ------
    output
    :returns
    path to JSON
    """
    meta_dict = dois_to_metaDicts(doi)
    return create_meta_json(meta_dict, output_folder)


def create_meta_json(meta_dict,output_folder):
    output_path = output_folder + "/" + "oa_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(meta_dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path


def metadataObj_to_metadataDict(metaObj):
    return {metaObj.doi: metaObj.to_dict()}


def metaDict_to_metaObj(meta_dict):
    if not meta_dict:
        return None
    title = safe_dic(meta_dict, "title")
    doi = safe_dic(meta_dict, "doi")
    arxiv = safe_dic(meta_dict, "arxiv")
    return MetadataObj(title=title, doi=doi, arxiv=arxiv)


def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None
