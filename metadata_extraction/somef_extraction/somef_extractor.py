import os
import re
import json
import bibtexparser

#downloads repo metadata creating a json as the github project name.json

def is_github_url(url):
    pattern = r'^https://github\.com/[\w-]+/[\w-]+$'
    match = re.match(pattern, url)
    return match is not None
def download_repo_metadata(url, output_folder_path):
    if not is_github_url(url):
        return False
    pattern = r'(?:http|https)://(?:gitlab\.com|github\.com)/'
    replacement = ''
    file = re.sub(pattern, replacement, url)
    file = file.replace('/', '_') + '.json'

    output_file_path = os.path.join(output_folder_path, file)

    if os.path.exists(output_file_path):
        print('Already created a file: ' + output_file_path)
        return output_file_path
    else:
        command = f"somef describe -r {url} -o {output_file_path} -t 0.8"
        print(command)
        os.system((command))
    return output_file_path

#extraction of metadata

def load_json(path):
    with open(path,'r') as f:
        return json.load(f)

def cff_parser(cite_list: list):
    '''
    Parse the citation list of a cff file given by somef
    '''
    # remove empty elements
    cite_list = [element for element in cite_list if element != '']
    # replace " by ''
    cite_list = [element.replace('"', '') for element in cite_list]
    parsed_dict = {}
    for element in cite_list:
        if element.count(':') > 1:
            key = element.split(':')[0].strip()
            value = ':'.join(element.split(':')[1:]).strip()
            parsed_dict[key] = value
        else:
            try:
                key, value = element.split(':')
                key = key.strip()
                value = value.strip()
            except ValueError:
                key = element.split(':')[0].strip()
                value = ''
            parsed_dict[key] = value
    return parsed_dict

def bibtex_parser(cite_list: list):
    '''
    Parse the citation list of a bibtex ref given by somef
    '''
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
            value = '='.join(element.split('=')[1:])
            parsed_dict[key] = value
        else:
            try:
                key, value = element.split('=')
                key = key.strip()
                value = value.strip()
            except ValueError:
                key = element.split('=')[0].strip()
                value = ''
            parsed_dict[key] = value
    return parsed_dict


def text_excerpt_parser(cite_list: list):
    # remove @ and {}
    cite_list = [element.replace('@', '').replace('{', '').replace('}', '') for element in cite_list]
    # strip elements
    cite_list = [element.strip() for element in cite_list]
    # remove empty elements
    cite_list = [element for element in cite_list if element != '']
    # remove final comma
    cite_list = [element[:-1] if element[-1] == ',' else element for element in cite_list]

    parsed_dict = {}
    for element in cite_list:
        if element.count('=') == 1:
            try:
                key, value = element.split('=')
                key = key.strip()
                value = value.strip()
            except ValueError:
                key = element.split('=')[0].strip()
                value = ''
            parsed_dict[key] = value

    return parsed_dict

#WARNING returns the doi's with the / replaced by the "_"
def find_doi_citation(somef_data: dict):
    '''
    Find the doi in somef data
    '''
    try:
        data = somef_data['citation']
    except KeyError:
        return False

    for cite in data:
        try:
            if cite['result']['format'] == 'cff':
                cff = cff_parser(cite['result']['value'].split('\n'))
                doi_find = description_doi_finder(cff['doi'])
                return doi_find

            elif cite['result']['format'] == 'bibtex':
                try:
                    bibtex = bibtexparser.loads(cite["result"]["value"]).entries[0]
                except:
                    print('Error parsing bibtex')
                    bibtex = bibtex_parser(cite['result']['value'].split('\n'))
                try:
                    doi_find = description_doi_finder(bibtex['doi'])
                except:
                    doi_find = description_doi_finder(bibtex['url'])

                return doi_find
        except:
            try:
                if cite['result']['type'] == 'Text_excerpt':
                    doi_find = description_doi_finder((cite['result']['value']))
                    return doi_find
            except:
                return False
    return False

def find_arxiv_citation(somef_data: dict):
    '''
    Find the arxiv in somef data citation
    '''
    try:
        data = somef_data['citation']
    except KeyError:
        return False

    for cite in data:
        try:
            if cite['result']['format'] == 'cff':
                cff = cff_parser(cite['result']['value'].split('\n'))
                arxiv_find = description_arxiv_finder(cff['arxiv'])
                return arxiv_find

            elif cite['result']['format'] == 'bibtex':
                try:
                    bibtex = bibtexparser.loads(cite["result"]["value"]).entries[0]
                except:
                    print('Error parsing bibtex')
                    bibtex = bibtex_parser(cite['result']['value'].split('\n'))
                try:
                    arxiv_find = description_arxiv_finder(bibtex['arxiv'])
                except:
                    arxiv_find = description_arxiv_finder(bibtex['url'])

                return arxiv_find
        except:
            try:
                if cite['result']['type'] == 'Text_excerpt':
                    arxiv_find = description_arxiv_finder((cite['result']['value']))
                    return arxiv_find
            except:
                return False
    return False

def description_finder(somef_data: dict):
    description = safe_dic(somef_data, 'description')
    desc = {'doi': set(), 'arxiv': set()}
    if description is None:
        return desc
    for result in description:
        value = safe_dic(safe_dic(result, 'result'), 'value')
        if value is None:
            continue
        if len(doi := description_doi_finder(value)) > 0:
            desc['doi'].update(doi)
        elif len(arxiv := description_arxiv_finder(value)) > 0:
            desc['arxiv'].update(arxiv)
        else:
            description_Name_finder(value)
    return desc

def description_doi_finder(value):
    pattern = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
    matches = re.findall(pattern, value)
    return matches


def description_arxiv_finder(value):
    pattern = r'.*(\d{4}\.\d{4,5}).*'
    matches = re.findall(pattern, value)
    return matches


def description_Name_finder(value):
    return

def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None