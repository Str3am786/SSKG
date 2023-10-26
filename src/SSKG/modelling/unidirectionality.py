import json
from fuzzywuzzy import fuzz

FUZZY_THRESHOLD = 85
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)
def is_substring_found(substring, larger_string):
    """
    @Param substring: The string you want to find
    @Param larger_string: The string where you will look for the substring
    :returns
    True or False depending if its been found or not
    """
    index = larger_string.lower().find(substring.lower())
    if index != -1:
        return True
    # If the exact substring is not found, try fuzzy matching
    max_ratio = 0
    for i in range(len(larger_string) - len(substring) + 1):
        ratio = fuzz.partial_ratio(substring.lower(), larger_string[i:i+len(substring)].lower())
        if ratio > max_ratio:
            max_ratio = ratio
    #This is to print the highest scoring fuzzy string comp print(max_ratio)
    if max_ratio > FUZZY_THRESHOLD:
        return True
    else:
        return False

def find_substring(substring, larger_string):
    return

def _iterate_results(results, string_2_find):
    if (not results) or (not string_2_find):
        return False
    for result in results:
        value = safe_dic(safe_dic(result,"result"),'value')
        if value:
            return is_substring_found(string_2_find,value) or is_substring_found(value,string_2_find)
    return False
def is_repo_unidir(paperObj, repo_json):
    try:
        repo_data = load_json(repo_json)
    except:
        print("Error while opening the repository file")
        return False
    #Is short title in paperTitle?
    results = safe_dic(repo_data,'name')
    unidir = _iterate_results(results, paperObj.title)
    if not unidir:
        #Repo title is close to the repo full title
        results = safe_dic(repo_data,'full_title')
        unidir = _iterate_results(results, paperObj.title)
    if not unidir:
        #Repo title is close to the repo full title
        results = safe_dic(repo_data,'name')
        unidir = _iterate_results(results, paperObj.abstract)
    if not unidir:
        #Repo title is close to the repo full title
        results = safe_dic(repo_data,'full_title')
        unidir = _iterate_results(results, paperObj.abstract)
    # See if paper title is within the description
    if not unidir:
        results = safe_dic(repo_data,'description')
        unidir = _iterate_results(results, paperObj.title)
    if not unidir:
        results = safe_dic(repo_data,'citation')
        unidir = _iterate_results(results, paperObj.title)
    return unidir

def safe_dic(dic, key):
    try:
        return dic[key]
    except:
        return None

def safe_list(list, i):
    try:
        return list[i]
    except:
        return None