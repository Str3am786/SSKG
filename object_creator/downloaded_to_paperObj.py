from metadata_extraction.github_extractor_tika import ranked_git_url, read_pdf
from metadata_extraction.paper_obj import PaperObj
from object_creator.create_downloadedObj import downloadedDic_to_downloadedObj
import json


def downloaded_to_paperObj(downloadedObj):
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

def dwnlddJson_to_paper_dic(meta_json, output_dir):
    result = {}
    try:
        with open(meta_json, 'r') as f:
            metas_dict = json.load(f)
    except Exception as e:
        print(str(e) + "Error while opening metadata json")
    count = 0
    for doi in metas_dict:
        dwnldd_dict = safe_dic(metas_dict,doi)
        dwnObj = downloadedDic_to_downloadedObj(dwnldd_dict=dwnldd_dict)
        paper = downloaded_to_paperObj(dwnObj)
        result.update({paper.doi: paper.to_dict()})
        print(doi)
        count += 1
        print("Processed %s, \n Total Processed: %s Papers" %(doi,count))
    return result

def dwnlddJson_to_paperJson(dwnldd_json, output_dir):
    dict = dwnlddJson_to_paper_dic(dwnldd_json, output_dir)
    output_path = output_dir + "/" + "paper_metadata.json"
    with open(output_path, 'w+') as out_file:
        json.dump(dict, out_file, sort_keys=True, indent=4,
                  ensure_ascii=False)
    return output_path

def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None

