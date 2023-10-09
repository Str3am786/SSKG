import logging
import os

from SSKG.download_pdf.oa_pdf_url_extractor import create_unpaywall_url_from_string as paywall_url
#TODO fix naming scheme
from SSKG.download_pdf.arxiv_downloader import download_pdf as download_arxiv_pdf
from SSKG.download_pdf.oa_pdf_downloader import download_pdf



def _is_arxiv(doi):
    '''
    :param doi: doi in string format
    :return:
    a url for the arxiv pdf
    '''
    if doi is None:
        return None
    if 'arxiv' in doi:
        arxiv_ID = doi.split('/arxiv.')[-1]
        arxiv_url = 'https://arxiv.org/pdf/' + arxiv_ID + '.pdf'
        return arxiv_url
    else:
        return False


def pdf_download_pipeline(doi, output_directory):
    """
    Input
    Takes a doi as a string.
    pdf_output_directory: where the pdf will be downloaded. The title being a converted do
    ----
    Verifies if it is a arxiv DOI or other doi
    If arxiv doi
        uses arxiv to download
    else:
        uses unpaywall
    Output
    :return:
    path to downloaded pdf

    """
    try:
        #Creates Directory if it does not exist
        if not os.path.exists(output_directory):
            os.mkdir(output_directory)
        # creates a folder within the wanted output directory
        pdf_output_directory = os.path.join(output_directory,"PDFs")
        if not os.path.exists(pdf_output_directory):
            # Creates Directory if it does not exist
            os.mkdir(pdf_output_directory)
    except Exception as e:
        print("Error while trying to create the directory  Err@ PDF download")
        print(str(e))

    if(arxiv_url:=_is_arxiv(doi)):
        file_path = download_arxiv_pdf(arxiv_url,pdf_output_directory)
    if arxiv_url is None:
        return None
    else:
        url = paywall_url(doi)
        file_path = download_pdf(url, doi, pdf_output_directory)
    if file_path:
        logging.info("Success downloading the pdf file")
        return file_path
    else:
        return None
