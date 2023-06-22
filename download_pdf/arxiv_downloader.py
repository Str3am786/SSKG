import pandas as pd
import requests

def filter_arxiv(file_path):
    # Read the csv file
    df = pd.read_csv(file_path)
    # Filter the dataframe
    df_arxiv = df[df['doi'].str.contains('arxiv')==True]
    df_not_arxiv = df[df['doi'].str.contains('arxiv')==False]
    # Save the filtered dataframe
    df_not_arxiv.to_csv('dois_not_arxiv.csv', index=False)
    df_arxiv = df_arxiv.drop(['name'], axis=1)
    # Create new column with the arxiv id
    df_arxiv['arxiv_id'] = df_arxiv['doi']\
        .str.split('/arxiv.').str[-1]
    # lets create new urls for the arxiv, in the form of https://arxiv.org/pdf/{arxiv_id}.pdf
    df_arxiv['arxiv_url'] = 'https://arxiv.org/pdf/' + df_arxiv['arxiv_id'] + '.pdf'

    return df_arxiv['arxiv_url']

def download_pdf(url, output_dir):
    try:
        r = requests.get(url)
        with open(output_dir + url.split('/')[-1], 'wb') as f:
            f.write(r.content)
        return output_dir + url.split('/')[-1]
    except Exception as e:
        print(str(e))

def main():
    arxiv_url = filter_arxiv('doi_filtered.csv')
    for url in arxiv_url:
        print('Downloading: ', url)
        download_pdf(url, '../pdf_info_extractor/data_pdf/')
        break #remove this line to download all the pdfs

if __name__ == '__main__':
    main()
    
