import json
import requests
import xmltodict

UPM = "openorgs____::cad284878801b9465fa51a95b1d779db"
BASE_URL = "https://api.openaire.eu/search/"
def get_openaire_projects(base_url=BASE_URL,org_id=UPM):
    url = base_url + "projects?openaireParticipantID=" + org_id + "&size=1000"
    response = requests.get(url)
    dict_data = xmltodict.parse(response.content)
    return dict_data

def get_openaire_publications(project_id,base_url=BASE_URL,org_id=UPM):
    url = base_url + "publications?openaireProjectID=" + project_id + "&size=1000"
    response = requests.get(url)
    dict_data = xmltodict.parse(response.content)
    return dict_data

def get_openaire_software(project_id,base_url=BASE_URL,org_id=UPM):
    url = base_url + "software?openaireProjectID=" + project_id + "&size=1000"
    response = requests.get(url)
    dict_data = xmltodict.parse(response.content)
    return dict_data

def save_json_data(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile,indent=4)
    return len(data)

def get_software_data(project_id):
    try:
        software = get_openaire_software(project_id)['response']['results']['result']
    except:
        software = False
    return software

def get_publications_data(project_id):
    try:
        publications = get_openaire_publications(project_id)['response']['results']['result']
    except:
        publications = False
    return publications


def get_openaire_data():
    projects = get_openaire_projects()
    save_json_data(projects, "apis/openaire/projects.json")
    count = 0
    len_publications = 0
    len_software = 0
    project_list = {}
    for project in projects["response"]["results"]["result"]:

        project_id = project['header']['dri:objIdentifier']
        project_list[count] = project_id
        
        publications = get_publications_data(project_id)
        if publications:
            len_publications = save_json_data(publications, "apis/openaire/publications/publications_" + str(count) + ".json")

        software = get_software_data(project_id)
        if software:
            len_software = save_json_data(software, "apis/openaire/software/software_" + str(count) + ".json")

        print(count,project_id, 'n_publications:', len_publications, 'n_software:', len_software)
        count += 1
    
    save_json_data(project_list, "apis/openaire/projects.json")
    
if __name__ == '__main__':
    get_openaire_data()

# result = get_openaire_projects()

# for i in result['response']['results']['result']:
#     project = i['header']['dri:objIdentifier']
#     publications = get_openaire_publications(project)
#     publications_list = publications['response']['results']['result']
#     software = get_openaire_software(project)
#     print(project)
#     print(publications)
#     print(software)
