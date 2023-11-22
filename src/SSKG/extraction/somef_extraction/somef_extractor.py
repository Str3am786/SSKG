import json
import logging
import os
import re
import subprocess

from ...utils.regex import str_to_doi_list, str_to_arxiv_list, str_to_arxivID


# DOWNLOAD
def is_github_repo_url(url):
    '''
    :param url: String, possible github url
    :returns:
    if the url is a github Repository
        True
    Else
        False
    '''
    if not url:
        return False
    pattern = r'^http(s)?://github\.com/[\w-]+/[\w-]+/?$'
    match = re.match(pattern, url)
    return match is not None


def download_repo_metadata(url, output_folder_path):
    '''
    :param url: String with github url
    :param output_folder_path: Path to the desired output folder

    :returns:
    path to the somef json file for the given url
    or
    None if failure/invalid input
    '''
    if not is_github_repo_url(url):
        logging.error("download_repo_metadata: URL given is not a valid github url")
        return None
    if not output_folder_path:
        logging.error("download_repo_metadata: No output path")
        return None
    pattern = r'(?:http|https)://(?:gitlab\.com|github\.com)/'
    replacement = ''
    file = re.sub(pattern, replacement, url)
    file = file.replace('/', '_') + '.json'
    # Creates Directory if it does not exist
    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)
    output_folder_path = os.path.join(output_folder_path,"JSONs")
    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)

    output_file_path = os.path.join(output_folder_path, file)
    if os.path.exists(output_file_path):
        print('Already created a file: ' + output_file_path)
        return output_file_path
    else:
        try:
            command = f"somef describe -r {url} -o {output_file_path} -t 0.8"
            # Timeout set to 5 minutes, somef should not take longer than a couple of minutes, should cover most cases.
            completed_process = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
            if completed_process.returncode != 0:
                raise Exception(
                    f"SOMEF Command failed with return code {completed_process.returncode}: {completed_process.stderr}")
        except subprocess.TimeoutExpired:
            logging.error(f"ERROR: {url} SOMEF command timed out after 5 minutes")
            return None
        except Exception as e:
            logging.error(f"ERROR:{url} SOMEF failed due to: {str(e)}")
            return None
    return output_file_path

# ----------------
# EXTRACTION


def get_related_paper(somef_data: dict):
    """
    Extracts a list of related paper IDs from a repository based on somef output.

    :param somef_data: A dictionary containing the output from somef, representing repository metadata.

    :returns:
        list: A list of all related paper arxivs found within the repository.
        None: Returns None if no paper IDs are found.
    """
    list_ids = []
    related_papers = safe_dic(somef_data, 'related_papers')
    if not related_papers:
        return None
    for paper in related_papers:
        url = safe_dic(safe_dic(paper,"result"),"value")
        if url:
            arxivID = str_to_arxivID(url)
            list_ids.append(arxivID)
    return list_ids if len(list_ids) > 0 else None


def description_finder(somef_data: dict):
    """
    :param somef_data: A dictionary containing the output from somef, representing repository metadata.

    :returns:
        Dictionary: {doi: "", arxiv: ""} of all the related papers IDs within the repo's description
    """
    description = safe_dic(somef_data, 'description')
    desc = {'doi': set(), 'arxiv': set()}
    if description is None:
        return desc
    for result in description:
        value = safe_dic(safe_dic(result, 'result'), 'value')
        if value is None:
            continue
        if (doi := str_to_doi_list(value)):
            desc['doi'].update(doi)
        if (arxiv := str_to_arxiv_list(value)):
            desc['arxiv'].update(arxiv)
    return desc


# TODO might need to return to parsing the bibtex to avoid non-pickup due to noise
def find_doi_citation(somef_data: dict):
    """
    Extracts DOI citations from a given repository metadata.

    :param somef_data: A dictionary containing repository metadata extracted using somef.

    :returns:
        list: A list of DOIs if available in the metadata.
        None: Returns None if no DOIs are found.
    """
    #See if there is citations within the repository
    if not (citations := safe_dic(somef_data, 'citation')):
        return None
    doi_list = []
    for cite in citations:
        result = safe_dic(cite, 'result')
        if (format:=(safe_dic(result,'format'))):
            if format == "cff":
                doi = str_to_doi_list(safe_dic(result,"value"))
                if doi:
                    doi_list.extend(doi)
            elif format == "bibtex":
                doi = str_to_doi_list(safe_dic(result, "value"))
                if doi:
                    doi_list.extend(doi)
            else:
                print("Unexpected, maybe a somef update?")
        else:
            if safe_dic(result,"type") == 'Text_excerpt':
                doi = str_to_doi_list(safe_dic(result,'value'))
                if doi:
                    doi_list.extend(doi)
    return doi_list if len(doi_list) > 0 else None


# TODO might need to return to parsing the bibtex to avoid non-pickup due to noise
def find_arxiv_citation(somef_data: dict):
    """
    Extracts DOI citations from a given repository metadata.

    :param somef_data: A dictionary containing repository metadata extracted using somef.

    :returns:
        list: A list of arxiv ID's if available in the metadata.
        None: Returns None if no DOIs are found.
    """
    # See if there is citations within the repository
    if not (citations := safe_dic(somef_data, 'citation')):
        return None
    arxiv_list = []
    for cite in citations:
        result = safe_dic(cite, 'result')
        if (format:=(safe_dic(result,'format'))):
            if format == "cff":
                arxiv = str_to_arxiv_list(safe_dic(result,"value"))
                if arxiv:
                    arxiv_list.extend(arxiv)
            elif format == "bibtex":
                arxiv = str_to_arxiv_list(safe_dic(result, "value"))
                if arxiv:
                    arxiv_list.extend(arxiv)
            else:
                print("Unexpected, maybe a somef update?")
        else:
            if safe_dic(result, "type") == 'Text_excerpt':
                arxiv = str_to_arxiv_list(safe_dic(result,'value'))
                if arxiv:
                    arxiv_list.extend(arxiv)
    return arxiv_list if len(arxiv_list) > 0 else None


# PARSERS
def bibtex_parser(cite_text: str):
    if not isinstance(cite_text, str):
        return None
    break_up_keys = _break_up_bibtex_text(bibtx_str=cite_text)
    return _parse_bib_item_list(break_up_keys)


def _parse_bib_item_list(cite_list: list):
    """
    Parse the citation list of a bibtex ref given by somef
    """
    # parse first element
    cite_list[0] = cite_list[0].replace('{','=')
    # remove @ and {}
    cite_list = [element.replace('@', '').replace('{', '').replace('}', '') for element in cite_list]
    # remove empty elements
    cite_list = [element for element in cite_list if element != '']
    # strip elements
    cite_list = [element.strip() for element in cite_list]
    # remove final comma
    cite_list = [element[:-1] if element[-1] == ',' else element for element in cite_list]
    parsed_dict = {}
    for element in cite_list:
        if element.count('=') > 1:
            key = element.split('=')[0].strip()
            key = key.lower()
            value = '='.join(element.split('=')[1:])
            parsed_dict[key] = value
        else:
            try:
                key, value = element.split('=')
                key = key.strip()
                key = key.lower()
                value = value.strip()
            except ValueError:
                key = element.split('=')[0].strip()
                value = ''
            parsed_dict[key] = value
    return parsed_dict


def _break_up_bibtex_text(bibtx_str):
    broken_up_into_list = []
    elemnt = ""
    for char in bibtx_str:
        if char == "\n":
            broken_up_into_list.append(elemnt)
            elemnt = ""
        else:
            elemnt = elemnt + char

    return broken_up_into_list


def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None