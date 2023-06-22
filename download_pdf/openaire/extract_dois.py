import os
import json

def extract_paths(folder_path):
    list_files = os.listdir(folder_path)
    return list_files

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    return len(data)

def extract_dois(json_data):
    dois = []
    for item in json_data:
        try:
            for pid in item['metadata']['oaf:entity']['oaf:result']['pid']:
                if pid['@classid'] == 'doi':
                    dois.append('https://doi.org/'+pid['#text'])
        except:
            pass
    return dois



def main():
    folder_path = 'apis/openaire/publications/'
    list_files = extract_paths(folder_path)
    dois_total = []
    for file in list_files:
        file_path = folder_path + file
        json_data = read_json_file(file_path)
        dois = extract_dois(json_data)
        dois_total.extend(dois)
    print('Total DOIs: {}'.format(len(dois_total)))
    save_json_file('apis/openaire/openaire_dois.json', dois_total)


if __name__ == '__main__':
    main()
