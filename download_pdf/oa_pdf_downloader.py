import pandas as pd
import numpy as np
import requests
import os
import json

def get_pdf_url_and_doi(data_path):
    data = pd.read_csv(data_path)
    return data["pdf_url"], data["dois_id"]

def generate_downloaded_list(txt_downloaded_pdfs ,folder_pdfs):
    downloaded_list = os.listdir(folder_pdfs)
    with open(txt_downloaded_pdfs, 'w') as f:
            f.write('\n'.join(downloaded_list))

def check_downloaded_list(name,file_path):
    if not os.path.exists(file_path):
        return False
    with open(file_path, 'r') as f:
        downloaded_list = f.readlines()
    downloaded_list = [x.strip() for x in downloaded_list]
    if name.strip() in downloaded_list:
        return True
    else:
        return False



#downloads pdf and returns file directory if correctly downloaded
def download_pdf(url,name_of_pdf, output_dir, dir_txt_downloaded_pdfs):

    # replace dois_id / with _
    name = name_of_pdf.replace('http://doi.org/','').replace('https://doi.org/', '').replace('/','_').replace('.','-DOT-') + '.pdf'
    filepath_downloaded = dir_txt_downloaded_pdfs + '/download_trace.txt'
    if check_downloaded_list(name, filepath_downloaded):
        print('already downloaded')
        return None
    try:
        try:
            r = requests.get(url)
             # Save the pdf
            pdf_filepath = output_dir + '/' + name
            # pdf = requests.get(r.content.url)
            # print(r.content)
            idk = str(r.content)
            idk = idk.split('\'')[1]
            json_idk = json.loads(idk)
            pdf = requests.get(json_idk['best_oa_location']['url'])
            with open(pdf_filepath, 'wb') as f: #here download the pdf
                f.write(pdf.content)
            # make a file for downloading trace
            with open(filepath_downloaded, 'a') as f:
                f.write(f'\n{name}')

            return output_dir + '/' + name

        except Exception as e:
            print(str(e))

    except Exception as e:
        # make a file for the error trace
        print(str(e))
        with open('error_trace.txt', 'a') as f:
            f.write(f'\n{url}')
        return 404


#TODO
def download_oa():
    oa_url,doi_id = get_pdf_url_and_doi('dois_not_arxiv_with_pdf_url.csv')
    for url,doi in zip(oa_url,doi_id):
        #check if url is not empty
        if url is not np.nan:
            print('Downloading: ', url)
            download_pdf(url,doi)
            break #remove this line to download all the pdfs

if __name__ == '__main__':
    generate_downloaded_list()
    download_oa()


