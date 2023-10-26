import json
import logging
import pandas as pd
import requests
import os

from bs4 import BeautifulSoup


def get_pdf_url_and_doi(data_path):
    data = pd.read_csv(data_path)
    return data["pdf_url"], data["dois_id"]

def _doi_to_pdf_name(doi):
    '''
    @Param doi: string of doi ID
    ----------
    :returns:
    String that works within UNIX/MacOS filesystems. Windows(NTFS) not tested

    Takes a doi and returns a file_name
    replaces / with %
        and  . with !
    '''
    if not doi:
        return None
    else:
    # characters within doi that is allowed -._;()/
    # replace dois_id / with _
        name = doi.replace('http://doi.org/', '').replace('https://doi.org/', '')\
                   .replace('/', '%').replace('.', '!') + '.pdf'
    return name
def detect_content_type(response):
    try:
        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type:
            return "HTML"
        elif "application/pdf" in content_type:
            return "PDF"
        else:
            return "Unknown"

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "Error"

def find_pdf_download_link(html):
    try:
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(html.content, 'html.parser')

        # Find all anchor (<a>) elements in the HTML
        for link in soup.find_all('a'):
            # Check if the link contains '.pdf' in the href attribute
            if link.get('href') and '.pdf' in link.get('href'):
                pdf_link = link.get('href')
                # Make sure the link is an absolute URL
                if not pdf_link.startswith('http'):
                    pdf_link = "http://" + pdf_link
                return pdf_link

        # If no PDF link is found, return None
        return None

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None

def download_pdf_from_html(response):
    if not response:
        return None
    url = find_pdf_download_link(html=response)
    if not url:
        return None
    try:
        pdf  = requests.get(url)
        return pdf
    except:
        return None


def backup(jayson):
    '''Used if the best_oa fails will attempt to get the first OA
    @Param Jayson: unpaywall response json
    '''
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

def doi_download_pdf(url,doi, output_dir):
    if not (name := _doi_to_pdf_name(doi)):
        return None
    try:
        try:
            r = requests.get(url)
            pdf_filepath = os.path.join(output_dir, name)
            idk = str(r.content)
            idk = idk.split('\'')[1]
            json_idk = json.loads(idk)
            try:
                pdf = requests.get(json_idk['best_oa_location']['url'])
            except:
                print("Error while trying to get the best_oa_location")
                pdf = backup(json_idk)

            if pdf.status_code != 200:
                logging.warning("Request Rejected with code " + str(pdf.status_code) + "\n" + \
                                "Running backup")
                pdf = backup(json_idk)
            if not pdf:
                logging.error(f"Failed to download the pdf for {str(doi)} with {str(url)}")
                print("-------------------------------")
                return None

            if (detect_content_type(response=pdf) == "HTML"):
                pdf = download_pdf_from_html(pdf)
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



