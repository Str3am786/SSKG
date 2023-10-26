import json
import logging
import pandas as pd
import requests
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
        return None
    except Exception as e:
        print(str(e))
        return None
#downloads pdf and returns file directory if correctly downloaded
#TODO change the "/" to "!" instead of _ to avoid doi conversion confusion
def doi_download_pdf(url,doi, output_dir):
    #characters within doi that is allowed -._;()/
    # replace dois_id / with _
    name = doi.replace('http://doi.org/','').replace('https://doi.org/', '').replace('/','%').replace('.','!') + '.pdf'
    try:
        try:
            r = requests.get(url)
             # Save the pdf
            pdf_filepath = output_dir + '/' + name
            idk = str(r.content)
            idk = idk.split('\'')[1]
            json_idk = json.loads(idk)
            try:
                pdf = requests.get(json_idk['best_oa_location']['url'])
                if pdf.status_code != 200:
                    logging.warning("Request Rejected with code " + str(pdf.status_code) + "\n" + \
                                    "Running backup")
                    pdf = backup(json_idk)
            except:
                print("Error while trying to get the best_oa_location")
                pdf = backup(json_idk)
            if not pdf:
                logging.error(f"Failed to download the pdf for {str(doi)} with {str(url)}")
                print("-------------------------------")
                return None
            with open(pdf_filepath, 'wb') as f: #here download the pdf
                f.write(pdf.content)
                print("PDF was downloaded successfully")
                print("-------------------------------")
                logging.info('written pdf successfully')
            return output_dir + '/' + name

        except Exception as e:
            print(str(e))
            print("-------------------------------")

    except Exception as e:
        # make a file for the error trace
        print(str(e))
        with open('error_trace.txt', 'a') as f:
            f.write(f'\n{url}')
        return None



