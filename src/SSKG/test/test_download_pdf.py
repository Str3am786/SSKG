import json
import os.path
from pathlib import Path
from shutil import rmtree
from unittest import TestCase
from ..download_pdf.download_pipeline import pdf_download_pipeline
from ..download_pdf.arxiv_downloader import download_pdf, convert_to_arxiv_url
from ..download_pdf.unpaywall_pdf_url_extractor import (
    create_unpaywall_url_from_string,
    create_unpaywall_url,
    get_unpaywall_pdf_url
)

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_FOLDER = os.path.join(TEST_DIR, "pipeline_folder")

def wipe_directory(directory_path):
    for path in Path(directory_path).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)

def load_json(path):
    with open(path,'r') as f:
        return json.load(f)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-------------------------------------------------Download Testing------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



class test_arxiv_downloader(TestCase):
    #!-----------------------------------------------
    #Arxiv url test:
    #
    def test_arxiv_url(self):
        arxiv = "2212.13788"
        expected = "https://arxiv.org/pdf/2212.13788.pdf"
        ans = convert_to_arxiv_url(arxiv)
        self.assertEquals(ans, expected)

    def test_not_arxiv_url(self):
        arxiv = ""
        ans = convert_to_arxiv_url(arxiv)
        self.assertIsNone(ans)

    def test_None_arxiv_url(self):
        arxiv = None
        ans = convert_to_arxiv_url(arxiv)
        self.assertIsNone(ans)


    #!-----------------------------------------------
    #Arxiv pdf download test:
    #
    def test_download_arxiv_pdf(self):
        wipe_directory(PIPELINE_FOLDER)
        arxiv = "2212.13788"
        output_file = download_pdf(url=arxiv, output_dir=PIPELINE_FOLDER)
        self.assertTrue(os.path.exists(output_file))

    def test_download_arxiv_pdf_url(self):
        wipe_directory(PIPELINE_FOLDER)
        arxiv = "https://arxiv.org/abs/2212.13788"
        output_file = download_pdf(url=arxiv, output_dir=PIPELINE_FOLDER)
        self.assertTrue(os.path.exists(output_file))

    def test_download_not_arxiv_pdf(self):
        wipe_directory(PIPELINE_FOLDER)
        arxiv = "221213.788"
        output_file = download_pdf(url=arxiv, output_dir=PIPELINE_FOLDER)
        self.assertIsNone(output_file)

    def test_download_none_arxiv_pdf(self):
        wipe_directory(PIPELINE_FOLDER)
        arxiv = "221213.788"
        output_file = download_pdf(url=arxiv, output_dir=PIPELINE_FOLDER)
        self.assertIsNone(output_file)

    def test_download_arxiv_pdf_no_dir(self):
        wipe_directory(PIPELINE_FOLDER)
        arxiv = "2212.13788"
        output_file = download_pdf(url=arxiv, output_dir=None)
        self.assertIsNone(output_file)
class test_open_alex_url_extractor(TestCase):
    pass

from ..download_pdf.unpaywall_pdf_downloader import doi_download_pdf, backup
class test_oa_downloader(TestCase):
    def test_download_html_response(self):
        doi = "10.7554/elife.21634"
        url = create_unpaywall_url_from_string(doi)
        output_dir = PIPELINE_FOLDER
        doi_download_pdf(url,doi,output_dir)
    pass

class test_download_pipeline(TestCase):
    def test_pdf_pipeline_html_response(self):
        doi = "10.7554/elife!21634"
        pdf_download_pipeline(doi)

    pass