import logging

from .oa_pdf_url_extractor import create_unpaywall_url_from_string as paywall_url
from .arxiv_downloader import download_pdf as download_arxiv_pdf
from .oa_pdf_downloader import download_pdf



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

def pdf_download_pipeline(doi, pdf_output_directory):
    """
    To be used when running Bidirectional pipeline when the pdf's are not downloaded and you want to download them one by one
    of the pdfs (pdfs not downloaded yet)
    Takes a doi as a string.
    pdf_output_directory: Directory where the doi
    Verifies if it is a arxiv DOI or other doi
    If arxiv doi
        uses arxiv to download
    else:
        uses unpaywall
    :return:
    path to downloaded pdf

    """
    if(arxiv_url:=_is_arxiv(doi)):
        file_path = download_arxiv_pdf(arxiv_url,pdf_output_directory)
    if arxiv_url is None:
        return None
    else:
        url = paywall_url(doi)
        file_path = download_pdf(url,doi,pdf_output_directory,pdf_output_directory)
    if file_path:
        logging.info("Success downloading the pdf file")
        return file_path
    else:
        return None
