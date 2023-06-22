import json
import pandas as pd

def load_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def transform_json(data,name):
    data_name = [name]*len(data)
    df = pd.DataFrame([data,data_name]).T
    df.columns = ['doi','name']
    return df

def concat_dfs(dfs):
    df = pd.concat(dfs, axis=0)
    return df

def main():
    paths = [
    './openaire/openaire_dois.json',
    './openalex/openalex_dois.json',
    './zenodo/zenodo_dois.json'      
    ]
    names = ['openaire', 'openalex', 'zenodo']

    dfs = []
    for path, name in zip(paths, names):
        data = load_json(path)
        df = transform_json(data, name)
        dfs.append(df)

    df = concat_dfs(dfs)
    df.drop_duplicates('doi',keep='first',inplace=True)
    df.to_csv('doi_filtered.csv', index=False)

if __name__ == '__main__':
    main()