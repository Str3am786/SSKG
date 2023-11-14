from SSKG.extraction.somef_extraction.somef_extractor import download_repo_metadata
from SSKG.modelling.bidirectionality import is_doi_bidir, is_arxiv_bidir
from SSKG.modelling.unidirectionality import is_repo_unidir
import logging


def check_bidir(paper,output_dir):
    return check_paper_directionality(paper, True, output_dir)


def check_unidir(paper,output_dir):
    return check_paper_directionality(paper, False, output_dir)


def check_paper_directionality(paper, directionality, output_dir):
    """
     Input
     :param paper: PaperObj type
     :param directionality: Boolean True: to assess bidirectionality False: to assess Unidirectionality
     :param output_dir: Output path to where the jsons will be saved
     -------
     Output
     :returns
     dictionary K: iden, V: List of urls that link back to the paper
     -------
     """
    result = {}
    is_unidir = False
    is_bidir = False

    iden = paper.doi
    if iden is None:
        iden = paper.arxiv

    try:
        # runs through the list of extracted gitHub urls, starting with the most frequently mentioned
        first_time = True
        for pair in paper.urls:
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
                if first_time:
                    result[iden] = []
                    first_time = False
                result[iden].append(url)
                print(result)
    except Exception as e:
        print("error while trying to extract metadata")
        print(str(e))
        logging.error("An error occurred: %s", str(e))
        pass
    if len(result.keys()) > 0:
        return result
    else:
        return None
