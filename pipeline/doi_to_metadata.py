from metadata_extraction.api.openAlex_api_queries import query_openalex_api
from metadata_extraction.metadata_obj import MetadataObj
from utils.regex import (
    str_to_arxivID,
    str_to_doiID
)
import json
def extract_arxivID (openAlexJson):
    location = safe_dic(openAlexJson, "locations")
    for locat in location:
        if safe_dic(locat, "is_oa") == True:
            if safe_dic(locat, "pdf_url") and "arxiv" in safe_dic(locat, "pdf_url"):
                return str_to_arxivID(safe_dic(locat,"pdf_url"))

def doi_to_metadataObj(doi):
    '''
    Input doi
    ------
    output
    :returns
    metadata Object
    '''
    try:
        try:
            oa_meta = query_openalex_api(doi)
        except Exception as e:
            print(str(e))
        if oa_meta is None:
            print("No meta")
        titL = safe_dic(oa_meta, "title")
        doi = str_to_doiID(safe_dic(oa_meta, "doi"))
        arxiv = extract_arxivID(oa_meta)
        metadata = MetadataObj(title=titL, doi=doi, arxiv=arxiv)
        return metadata
    except Exception as e:
        print(str(e))
def doi_to_metaDict(doi):
    mt_dict = doi_to_metadataObj(doi).to_dict()
    result = {mt_dict["doi"]: mt_dict}
    return result

def dois_to_metaDicts(list_of_dois):
    result = {}
    for doi in list_of_dois:
        result.update(doi_to_metaDict(doi))
    return result

def doi_to_metaJson(doi,output_folder):
    meta_dict = doi_to_metaDict(doi)
    output_path = output_folder + "/" +  "metadata.json"
    return create_meta_json(meta_dict,output_folder)

def dois_to_metaJson(doi,output_folder):
    meta_dict = dois_to_metaDicts(doi)
    return create_meta_json(meta_dict,output_folder)

def create_meta_json(meta_dict,output_folder):
    output_path = output_folder + "/" + "metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(meta_dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path
def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None