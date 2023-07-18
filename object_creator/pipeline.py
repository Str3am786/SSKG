from object_creator.doi_to_metadata import doi_to_metadataObj
from object_creator.create_downloadedObj import meta_to_dwnldd
from object_creator.downloaded_to_paperObj import downloaded_to_paperObj
from object_creator.paper_to_directionality import check_bidir
from object_creator.paper_obj_utils import paperDict_to_paperObj
import json
import os

def doi_to_paper(doi,output_dir):
    meta = doi_to_metadataObj(doi)
    downldd = meta_to_dwnldd(meta, output_dir)
    paper = downloaded_to_paperObj(downldd)
    return paper

def pipeline_single_bidir(doi,output_dir):
    paper = doi_to_paper(doi,output_dir)
    result = check_bidir(paper,output_dir)
    return result

def pipeline_multiple_bidir(list_dois, output_dir):
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

def pipeline_txt_dois_bidir(dois_txt, output_dir):
    try:
        with open(dois_txt, 'r') as file:
            dois = file.read().splitlines()
    except:
        print("Error while opening the txt")
    return pipeline_multiple_bidir(dois,output_dir)

def from_papers_json_to_bidir(papers_json, output_dir):
    result = {}
    try:
        paper_dicts = load_json(papers_json)
    except Exception as e:
        print("Error while trying to load the Papers JSON")
        print(str(e))
    for paperDict in paper_dicts:
        paper = paperDict_to_paperObj(paperDict)
        bidir = pipeline_single_bidir(paper,output_dir)
        if bidir:
            result.extend(bidir)
    return dict_to_json(dict,output_path=os.path.join(output_dir,"bidir.json"))

def dict_to_json(dict, output_path):
    try:
        with open(output_path, 'w+') as out_file:
            json.dump(dict, out_file, sort_keys=True, indent=4,
                    ensure_ascii=False)
        return output_path
    except Exception as e:
        print(str(e))
        return None

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def dois_txt_to_bidir_json(dois_txt, output_dir):
    output_path = os.path.join(output_dir,"bidir.json")
    return dict_to_json(pipeline_txt_dois_bidir(dois_txt,output_dir),output_path)

