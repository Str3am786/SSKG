from metadata_extraction.somef_extraction.somef_extractor import download_repo_metadata
from modelling.bidirectionality import is_doi_bidir, is_arxiv_bidir
from modelling.unidirectionality import is_repo_unidir


def check_bidir(paper,output_dir):
    return check_paper_directionality(paper,True,output_dir)

def check_unidir(paper,output_dir):
    return check_paper_directionality(paper,False,output_dir)

def check_paper_directionality(paper,directionality, output_dir):
    """
     Input
     @param directionality True: to assess bidirectionality False: to assess Unidirectionality
     Takes doi
     Takes output folder to download the somef JSON and pdf
     -------
     Output
     :returns
     dictionary K: doi, V: List of code_urls that link back to the paper
     -------
     """
    result = {}
    is_unidir = False
    is_bidir = False
    doi = paper.doi
    try:
        # runs through the list of extracted github code_urls, starting with the most frequently mentioned
        firstTime = True
        for pair in paper.code_urls:
            url = pair[0]
            # Download repository from SOMEF
            repo_file = download_repo_metadata(url, output_dir)
            if not repo_file:
                continue
            # assessment of bidirectionality
            if directionality:
                is_bidir = (is_doi_bidir(paper, repo_file) or is_arxiv_bidir(paper, repo_file))
            if not directionality:
                is_unidir = is_repo_unidir(paper, repo_file)
            if is_bidir or is_unidir:
                if firstTime:
                    result[doi] = []
                    firstTime = False
                result[doi].append(url)
                print(result)
    except Exception as e:
        print("error while trying to extract metadata")
        print(str(e))
        pass
    if len(result.keys()) > 0:
        return result
    else:
        return None