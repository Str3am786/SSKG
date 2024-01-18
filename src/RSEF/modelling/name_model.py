
import os
import arxiv
import requests
import jaro
import json
from fuzzywuzzy import fuzz


def load_json(path):
    with open(path,'r') as f:
        return json.load(f)


def get_title_somef(path):
    # get description and full title
    data = load_json(path)
    try:
        return data['description']+data['full_title']
    except:
        return []


def get_title(doi):
    try:
        search = arxiv.Search(id_list=[doi])
        paper = next(search.results())
        return paper.title
    except:
        try:
            url_base = "https://api.crossref.org/works/"
            # if doi has more than 1 _ replace first _ with /
            doi = doi.replace('_', '/', 1)
            response = requests.get(url_base + doi)
            reponse_json = response.json()
            return reponse_json['message']['title'][0]
        except:
            return None


def get_best_jaro(title1, list_strings):
    best_jaro = 0
    solution = None
    for strng in list_strings:
        if title1 != None and strng != None:
            metric_jaro = jaro.jaro_winkler_metric(title1, strng)
            if metric_jaro > best_jaro:
                best_jaro = metric_jaro
                solution = strng
    return solution, best_jaro


def get_best_jaro(path):
    #get description path list
    file_path = [os.path.join(path,i) for i in os.listdir(path)]
    #get description
    description = [get_title_somef(i) for i in file_path]
    #get title
    title = get_title(path.split('\\')[-1])
    #get jaro for each description
    best_jaro = 0
    solucion = None
    for index,value in enumerate(description):
        for j in value:
            title_assert = j['result']['value']
            if title_assert != None and title != None:
                metric_jaro = jaro.jaro_winkler_metric(title_assert, title)
                if metric_jaro > best_jaro:
                    best_jaro = metric_jaro
                    solucion = file_path [index]
    return solucion, best_jaro


def calculate_similarity_score(str1, str2):
    # Calculate different similarity scores
    ratio_score = fuzz.ratio(str1, str2)
    partial_ratio_score = fuzz.partial_ratio(str1, str2)
    token_sort_ratio_score = fuzz.token_sort_ratio(str1, str2)
    token_set_ratio_score = fuzz.token_set_ratio(str1, str2)

    # Return a dictionary of scores
    scores = {
        "Ratio": ratio_score,
        "Partial Ratio": partial_ratio_score,
        "Token Sort Ratio": token_sort_ratio_score,
        "Token Set Ratio": token_set_ratio_score
    }

    return scores


# Example usage
string1 = "Hello"
string2 = "Halo"
scores = calculate_similarity_score(string1, string2)

# Print the scores
for score_type, score in scores.items():
    print(score_type + ":", score)
print("jaro:" + str(jaro.jaro_winkler_metric("Halo", "Hello")))