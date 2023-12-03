from SSKG.extraction.somef_extraction.somef_extractor import download_repo_metadata
from SSKG.modelling.git_bidirectionality import is_it_bidir as git_is_it_bidir
from SSKG.modelling.unidirectionality import is_repo_unidir
import logging


def check_bidir(paper,output_dir):
    return check_paper_directionality(paper, True, output_dir)


def check_unidir(paper,output_dir):
    return check_paper_directionality(paper, False, output_dir)

def _get_identifier(paper):
    """
    Input
    :param paper: PaperObj, will be used to get the identifier
    ----
    Output
    :returns:
    identifier
    """
    if not paper:
        logging.error("Paper Object is None")
        return None
    # if iden := paper.doi:
    #     return iden
    elif iden := paper.arxiv:
        return iden
    else:
        logging.error("Paper Object Has no identifier to use")
        return None


def check_paper_directionality(paper, directionality, output_dir):
    """
     Input
     :param paper: PaperObj type
     :param directionality: Boolean True -> to assess bidirectionality False-> to assess Unidirectionality
     :param output_dir: Output path to where the jsons will be saved
     -------
     Output
     :returns:
     dictionary K: identifier, V: List of urls that link back to the paper
     -------
     """
    result = {}
    is_unidir = None
    is_bidir = None

    if not (iden := _get_identifier(paper)):
        logging.error("check_paper_directionality: No identifier found for this paper")
        return None

    try:
        # runs through the list of extracted gitHub urls, starting with the most frequently mentioned
        first_time = True
        if not(pp_urls := paper.urls):
            logging.info(f"This paper {iden}, it does not have any urls")
            return None
        git_urls = pp_urls.get("git", [])

        for entry in git_urls:
            url = safe_dic(entry, "url")
            if not url:
                continue
            # Download repository from SOMEF
            repo_file = download_repo_metadata(url, output_dir)
            if not repo_file:
                logging.error(f"Issue while downloading the repository for {iden}")
                continue
            # assessment of bidirectionality
            if directionality:
                is_bidir = git_is_it_bidir(paper, repo_file)
            if not directionality:
                is_unidir = is_repo_unidir(paper, repo_file)
            if is_bidir:
                if first_time:
                    result[iden] = []
                    first_time = False
                entry = {
                    "url": url,
                    "bidirectional": is_bidir
                }
                result[iden].append(entry)
                print(entry)
            if is_unidir:
                if first_time:
                    result[iden] = []
                    first_time = False
                result[iden].append(url)
    except Exception as e:
        print("error while trying to extract metadata")
        print(str(e))
        logging.error("check_paper_directionality: An error occurred: %s", str(e))
        pass
    if len(result.keys()) > 0:
        return result
    else:
        return None


def safe_dic(dict, key):
    try:
        return dict[key]
    except:
        return None
