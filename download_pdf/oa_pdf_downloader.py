import pandas as pd
import numpy as np
import requests
import os
import json
import logging
def get_pdf_url_and_doi(data_path):
    data = pd.read_csv(data_path)
    return data["pdf_url"], data["dois_id"]

def backup(jayson):
    '''Used if the best_oa fails will attempt to get the first OA'''
    try:
        for location in jayson['oa_locations']:
            pdf = requests.get(location['url'])
            if pdf.status_code != 200:
                continue
            else:
                return pdf
    except Exception as e:
        print(str(e))
        return None
#downloads pdf and returns file directory if correctly downloaded
def download_pdf(url,name_of_pdf, output_dir):

    # replace dois_id / with _
    name = name_of_pdf.replace('http://doi.org/','').replace('https://doi.org/', '').replace('/','_').replace('.','-DOT-') + '.pdf'
    try:
        try:
            r = requests.get(url)
            logging.debug(r)
             # Save the pdf
            pdf_filepath = output_dir + '/' + name
            idk = str(r.content)
            idk = idk.split('\'')[1]
            json_idk = json.loads(idk)
            pdf = requests.get(json_idk['best_oa_location']['url'])
            if pdf.status_code != 200:
                print("Request Rejected with code" + str(pdf.status_code))
                pdf = backup(json_idk)
            with open(pdf_filepath, 'wb') as f: #here download the pdf
                f.write(pdf.content)
                logging.info('written pdf successfully')
            return output_dir + '/' + name

        except Exception as e:
            print(str(e))

    except Exception as e:
        # make a file for the error trace
        print(str(e))
        with open('error_trace.txt', 'a') as f:
            f.write(f'\n{url}')
        return None



