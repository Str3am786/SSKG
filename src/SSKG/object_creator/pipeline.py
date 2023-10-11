from SSKG.object_creator.doi_to_metadata import doi_to_metadataObj
from SSKG.object_creator.create_downloadedObj import meta_to_dwnldd
from SSKG.object_creator.downloaded_to_paperObj import downloaded_to_paperObj
from SSKG.object_creator.paper_to_directionality import check_bidir, check_unidir
from SSKG.object_creator.paper_obj_utils import paperDict_to_paperObj
import json
import os

def doi_to_paper(doi,output_dir):
    '''
    @Param doi: doi
    @Param output_dir: where the pdf will be downloaded to
    :returns
    paperObj
    '''
    meta = doi_to_metadataObj(doi)
    downldd = meta_to_dwnldd(meta, output_dir)
    paper = downloaded_to_paperObj(downldd)
    return paper

def pipeline_single_bidir(doi,output_dir):
    '''
    @Param doi: doi
    @Param output_dir: where the pdf will be downloaded to
    :returns
    dictionary with doi and the urls found that are bidirectional for that doi
    '''
    paper = doi_to_paper(doi,output_dir)
    result = check_bidir(paper,output_dir)
    return result
def pipeline_single_unidir(doi,output_dir):
    '''
    @Param doi: doi
    @Param output_dir: where the pdf will be downloaded to
    :returns
    dictionary with doi and the urls found that are unidirectional for that doi
    '''
    paper = doi_to_paper(doi,output_dir)
    if not paper:
        print("Error while creating paperObj")
        return None
    result = check_unidir(paper,output_dir)
    return result

def pipeline_multiple_bidir(list_dois, output_dir):
    '''
    @Param list_dois: list of dois
    @Param output_dir: where the pdf will be downloaded to
    :returns
    dictionary with dois and the urls found that are bidirectional for that doi
    '''
    result = {}
    try:
        for doi in list_dois:
            paper = doi_to_paper(doi,output_dir)
            if not paper:
                continue
            if (bidir:=(check_bidir(paper,output_dir))):
                result.update(bidir)
        return result
    except Exception as e:
        print(str(e))
        return None
def pipeline_multiple_unidir(list_dois, output_dir):
    '''
    @Param list_dois: list of dois
    @Param output_dir: where the pdf will be downloaded to
    :returns
    dictionary with dois and the urls found that are unidirectional for that doi
    '''
    result = {}
    try:
        for doi in list_dois:
            paper = doi_to_paper(doi,output_dir)
            if not paper:
                continue
            if (unidir:=(check_unidir(paper,output_dir))):
                result.update(unidir)
        return result
    except Exception as e:
        print(str(e))
        return None

def pipeline_txt_dois_bidir(dois_txt, output_dir):
    '''
    @Param dois_txt: dois seperated by \n within a txt
    @Param output_dir: where the pdf will be downloaded to
    :returns
    dictionary with dois and the urls found that are bidirectional for that doi
    '''
    try:
        with open(dois_txt, 'r') as file:
            dois = file.read().splitlines()
    except:
        print("Error while opening the txt")
    return pipeline_multiple_bidir(dois,output_dir)

def pipeline_txt_dois_unidir(dois_txt, output_dir):
    '''
    @Param dois_txt: dois seperated by \n within a txt
    @Param output_dir: where the pdf will be downloaded to
    :returns
    dictionary with dois and the urls found that are bidirectional for that doi
    '''
    try:
        with open(dois_txt, 'r') as file:
            dois = file.read().splitlines()
    except:
        print("Error while opening the txt")
    return pipeline_multiple_unidir(dois,output_dir)

def from_papers_json_to_bidir(papers_json, output_dir):
    '''
    @Param papers_json: json of papers, Key: DOI, V: paperObj (as a dictionary)
    @Param output_dir: where the json will be saved to
    :returns
    path to output JSON
    '''
    result = {}
    try:
        paper_dicts = load_json(papers_json)
    except Exception as e:
        print("Error while trying to load the Papers JSON")
        print(str(e))
    for doi in paper_dicts:
        paperDict = safe_dic(paper_dicts, doi)
        paper = paperDict_to_paperObj(paperDict)
        bidir = check_bidir(paper,output_dir)
        if bidir:
            result.update(bidir)
    return dict_to_json(result,output_path=os.path.join(output_dir,"bidir.json"))

def dict_to_json(dictionary, output_path):
    '''
    @Param dictionary: dictionary to be turned to a json
    :returns
    path to output JSON
    '''
    try:
        with open(output_path, 'w+') as out_file:
            json.dump(dictionary, out_file, sort_keys=True, indent=4,
                    ensure_ascii=False)
        return output_path
    except Exception as e:
        print(str(e))
        return None

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def dois_txt_to_bidir_json(dois_txt, output_dir):
    '''
    @Param dois_txt: dois seperated by \n within a txt
    @Param output_dir: where the pdf will be downloaded to
    :returns
    path to output JSON
    '''
    output_path = os.path.join(output_dir,"bidir.json")
    return dict_to_json(pipeline_txt_dois_bidir(dois_txt,output_dir),output_path)
def dois_txt_to_unidir_json(dois_txt, output_dir):
    '''
    @Param dois_txt: dois seperated by \n within a txt
    @Param output_dir: where the pdf will be downloaded to
    :returns
    path to output JSON
    '''
    output_path = os.path.join(output_dir,"unidir.json")
    return dict_to_json(pipeline_txt_dois_unidir(dois_txt,output_dir),output_path)


def from_papers_json_to_unidir(papers_json, output_dir):
    '''
    @Param papers_json: Json of papers K:doi V: paperObj
    @Param output_dir: where the pdf will be downloaded to
    :returns
    dictionary with dois and the urls found that are unidirectional for that doi
    '''
    result = {}
    try:
        paper_dicts = load_json(papers_json)
    except Exception as e:
        print("Error while trying to load the Papers JSON")
        print(str(e))
    for doi in paper_dicts:
        paperDict = safe_dic(paper_dicts, doi)
        paper = paperDict_to_paperObj(paperDict)
        unidir = check_unidir(paper, output_dir)
        if unidir:
            result.update(unidir)
    return dict_to_json(result,output_path=os.path.join(output_dir,"unidir.json"))



def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None
