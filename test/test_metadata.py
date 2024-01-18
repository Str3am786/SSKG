import json
import os.path
from pathlib import Path
from shutil import rmtree
from unittest import TestCase
from src.RSEF.metadata.api.openAlex_api_queries import pdf_title_to_meta, convert_to_doi_url, query_openalex_api
from src.RSEF.metadata.api.zenodo_api import get_redirect_url, get_record, get_github_from_zenodo

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_FOLDER = os.path.join(TEST_DIR, "pipeline_folder")


def wipe_directory(directory_path):
    for path in Path(directory_path).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-------------------------------------------------Metadata Testing------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class TestOpenAlexQuery(TestCase):

    #!-----------------------------------------------
    #convert_to_doi_url:

    def test_convert_to_doi_url(self):
        test_doi = "10.21428/58320208.e46b7b81"
        expected = "https://doi.org/10.21428/58320208.e46b7b81"
        ans = convert_to_doi_url(test_doi)
        self.assertEquals(ans, expected)

    def test_convert_to_doi_url_already(self):
        test_doi = "https://doi.org/10.21428/58320208.e46b7b81"
        expected = "https://doi.org/10.21428/58320208.e46b7b81"
        ans = convert_to_doi_url(test_doi)
        self.assertEquals(ans, expected)

    def test_convert_to_doi_url_not_doi(self):
        test_doi = "https://doi.org/1021428/58320208.e46b7b81"
        ans = convert_to_doi_url(test_doi)
        self.assertIsNone(ans)

    def test_convert_to_doi_None(self):
        ans = convert_to_doi_url(None)
        self.assertIsNone(ans)
    #!-----------------------------------------------
    #DOI queries:
    #

    def test_oa_doi_query(self):
        doi = "10.1007/978-3-319-68204-4_9"
        expected = "WIDOCO: A Wizard for Documenting Ontologies"
        ans = query_openalex_api(doi)
        title = ans['title']
        self.assertEquals(title,expected)

    def test_oa_doi_query_none(self):
        ans = query_openalex_api(None)
        self.assertIsNone(ans)
        pass

    def test_oa_doi_query_not_doi(self):
        doi = "1231/12039-1"
        ans = query_openalex_api(doi)
        self.assertIsNone(ans)
        pass

    def test_oa_doi_query_4xx(self):
        doi = "10.1007/978-3-319-68204"
        ans = query_openalex_api(doi)
        self.assertIsNone(ans)
    #!-----------------------------------------------
    #PDF name to doi:
    #
    #TODO

    def test_pdf_name_to_doi(self):
        pass

    def test_pdf_name_not_doi(self):
        pass

    def test_pdf_doesnt_exist(self):
        pass

    def test_pdf_name_to_doi_out_fail(self):
        pass
    #!-----------------------------------------------
    #pdf title to metadata:
    #

    def test_title_query(self):
        title = "Widoco"
        resp_json = pdf_title_to_meta(title)
        doi = resp_json["doi"]
        self.assertEquals(doi,"https://doi.org/10.1007/978-3-319-68204-4_9")

    def test_no_title_query(self):
        title = ""
        resp_json = pdf_title_to_meta(title)
        self.assertIsNone(resp_json)

    def test_None_title(self):
        test = pdf_title_to_meta(None)
        self.assertIsNone(test)

    def test_title_with_spaces(self):
        title = "SPARQL2Flink: Evaluation of SPARQL Queries on Apache Flink"
        resp_json = pdf_title_to_meta(title)
        doi = resp_json["doi"]
        self.assertEquals(doi, "https://doi.org/10.3390/app11157033")

    def test_problematic_title(self):
        #TODO fails due to OA
        title = "(In)Stability for the Blockchain: Deleveraging Spirals and Stablecoin Attacks"
        resp_json = resp_json = pdf_title_to_meta(title)
        doi = resp_json["doi"]
        expected = "https://doi.org/10.21428/58320208.e46b7b81"
        self.assertIsNone(doi)


class TestZenodoApi(TestCase):

    def test_get_redirect(self):
        doi_url = 'https://doi.org/10.5281/zenodo.591294'
        expected = "https://zenodo.org/record/591294"
        ans = get_redirect_url(doi_url)
        self.assertEquals(expected, ans)

    def test_get_redirect_invalid_doi(self):
        doi_url = 'https://doi.org/10,5281/made_up.591294'
        with self.assertRaises(ValueError):
            get_redirect_url(doi_url)


    def test_get_redirect_made_up_doi(self):
        doi_url = 'https://doi.org/10.5281/made_up.591294'
        with self.assertRaises(RuntimeError):
            get_redirect_url(doi_url)

    def test_get_redirect_none(self):
        with self.assertRaises(ValueError):
            get_redirect_url(None)


    # ------------------------------------------------
    # Test Zenodo get record:
    #

    def test_get_record_doi(self):
        doi_url = 'https://doi.org/10.5281/zenodo.591294'
        ans = get_record(doi_url)
        self.assertIsNotNone(ans)

    def test_get_record_record_url(self):
        record_url = 'https://zenodo.org/record/591294'
        ans = get_record(record_url)
        self.assertIsNotNone(ans)

    def test_get_record_empty_url(self):
        with self.assertRaises(ValueError):
            get_redirect_url("")

    def test_get_record_None(self):
        with self.assertRaises(ValueError):
            get_redirect_url(None)

    # ------------------------------------------------
    # Test Zenodo get github from zenodo:
    #

    def test_get_github_zenodo(self):
        doi_url = 'https://doi.org/10.5281/zenodo.591294'
        record = get_record(doi_url)
        ans = get_github_from_zenodo(record[0])
        expected = ['https://github.com/dgarijo/Widoco']
        self.assertEquals(ans, expected)

    def test_get_github_zenodo_empty_text(self):
        empty_text = ""
        ans = get_github_from_zenodo(empty_text)
        self.assertEquals(ans, [])

    def test_get_github_zenodo_None(self):
        ans = get_github_from_zenodo(None)
        self.assertEquals(ans, [])

