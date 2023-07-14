from .doi_to_metadata import doi_to_metadataObj
from .create_downloadedObj import meta_to_dwnldd
from .downloaded_to_paperObj import downloaded_to_paperObj
from .paper_to_directionality import check_bidir


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
            paper = doi_to_paper(doi)
            result.update(check_bidir(paper,output_dir))
        return result
    except Exception as e:
        print(str(e))
        return None