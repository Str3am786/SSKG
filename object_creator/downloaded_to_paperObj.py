from metadata_extraction.github_extractor_tika import ranked_git_url, read_pdf
from metadata_extraction.paper_obj import PaperObj
from object_creator.create_downloadedObj import downloadedDic_to_downloadedObj
import json
import os


def downloaded_to_paperObj(downloadedObj):
    """
    @Param downloadedObj
    ---
    :returns 
    Paper Obj (will have processed the paper within the downloaded Obj to look for github urls)
    """
    if not downloadedObj:
        return None
    try:
        pdf_data = read_pdf(downloadedObj.file_path)
        urls = ranked_git_url(pdf_data)
        title = downloadedObj.title
        doi = downloadedObj.doi
        arxiv = downloadedObj.arxiv
        file_name = downloadedObj.file_name
        file_path = downloadedObj.file_path
        return PaperObj(title, urls, doi, arxiv, file_name, file_path)
    except Exception as e:
        print(str(e))
        print("Error while trying to read from the pdf")

def dwnlddDic_to_paper_dic(downloadeds_dic):
    result = {}
    count = 0
    for doi in downloadeds_dic:
        dwnldd_dict = safe_dic(downloadeds_dic, doi)
        dwnObj = downloadedDic_to_downloadedObj(dwnldd_dict=dwnldd_dict)
        paper = downloaded_to_paperObj(dwnObj)
        result.update({doi: paper.to_dict()})
        print(doi)
        count += 1
        print("Processed %s, \n Total Processed: %s Papers" %(doi,count))
    return result

def dwnlddDic_to_paperJson(downloadeds_dic,output_dir):
    pp_dic = dwnlddDic_to_paper_dic(downloadeds_dic)
    return pp_dic_to_json(pp_dic,output_dir)

def dwnlddJson_to_paper_dic(dwnldd_json):
    """
    @Param dwnldd_json Json of the downloaded Objects
    ----
    :returns
    dictionary of paper dictionaries
    """
    result = {}
    try:
        with open(dwnldd_json, 'r') as f:
            dwnldd_json = json.load(f)
    except Exception as e:
        print(str(e) + "Error while opening metadata json")
    return dwnlddDic_to_paper_dic(downloadeds_dic=dwnldd_json)

def dwnlddJson_to_paperJson(dwnldd_json, output_dir):
    """
    @Param dwnldd_json: Json of Downloaded Dictionaries
    @Param output_dir: Directory to put the output JSON
    :return
    Path to the paper JSON
    """
    pp_dic = dwnlddJson_to_paper_dic(dwnldd_json)
    return pp_dic_to_json(pp_dic,output_dir)

def pp_dic_to_json(pp_dic, output_dir):
    """
    @Param pp_dic: is a paper dictionary
    @Param output_dir where the JSON will be saved
    --
    :return
    Path to the json
    """
    output_path = os.path.join(output_dir,"processed_metadata.json")
    with open(output_path, 'w+') as out_file:
        json.dump(pp_dic, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path

def paperObj_ppDict(paper):
    return {paper.doi: paper.to_dict()}

def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None

