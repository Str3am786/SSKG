import json
import os.path
from pathlib import Path
from shutil import rmtree
from unittest import TestCase

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
#-------------------------------------------------Metadata Testing------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from SSKG.metadata.api.openAlex_api_queries import pdf_title_to_meta, convert_to_doi_url, query_openalex_api


class test_open_alex_query(TestCase):
    #!-----------------------------------------------
    #convert_to_doi_url:
    def test_convert_to_doi_url(self):
        test_doi = "10.21428/58320208.e46b7b81"
        expected = "https://doi.org/10.21428/58320208.e46b7b81"
        ans = convert_to_doi_url(test_doi)
        self.assertEquals(ans,expected)

    def test_convert_to_doi_url_already(self):
        test_doi = "https://doi.org/10.21428/58320208.e46b7b81"
        expected = "https://doi.org/10.21428/58320208.e46b7b81"
        ans = convert_to_doi_url(test_doi)
        self.assertEquals(ans,expected)

    def test_convert_to_doi_url_notdoi(self):
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


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-------------------------------------------------Download Testing------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ..download_pdf.arxiv_downloader import download_pdf, convert_to_arxiv_url
from ..download_pdf.unpaywall_pdf_url_extractor import (
    create_unpaywall_url_from_string,
    create_unpaywall_url,
    get_unpaywall_pdf_url
)

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

class test_oa_downloader(TestCase):
    pass

class test_download_pipeline(TestCase):
    pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-------------------------------------------------Extraction Testing----------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ..extraction.somef_extraction.somef_extractor import is_github_repo_url, download_repo_metadata, get_related_paper, \
    description_finder, find_doi_citation, find_arxiv_citation


class test_somef_extraction(TestCase):

    def test_github_url(self):
        test = "https://github.com/SoftwareUnderstanding/SSKG"
        ans = is_github_repo_url(test)
        self.assertTrue(ans)

    def test_not_github_url(self):
        test = "https://github.com/SoftwareUnderstandingSSKG"
        ans = is_github_repo_url(test)
        self.assertFalse(ans)

    def test_None_github_url(self):
        test = None
        ans = is_github_repo_url(test)
        self.assertFalse(ans)
    #!-----------------------------------------------
    #Test download_repo_metadata:
    #

    def test_dwnld_repo_meta(self):
        wipe_directory(PIPELINE_FOLDER)
        real_url = "https://github.com/SoftwareUnderstanding/SSKG"
        ans = download_repo_metadata(url=real_url, output_folder_path=PIPELINE_FOLDER)
        self.assertTrue(os.path.exists(ans))

    def test_already_dwnldd_repo_meta(self):
        real_url = "https://github.com/SoftwareUnderstanding/SSKG"
        output_dir = os.path.join(TEST_DIR,"json")
        expected = os.path.join(output_dir, "JSONs/SoftwareUnderstanding_SSKG.json")
        ans = download_repo_metadata(url=real_url, output_folder_path=output_dir)
        self.assertEquals(ans,str(expected))

    def test_d_r_m_not_url(self):
        fake_url = ""
        ans = download_repo_metadata(url=fake_url, output_folder_path=PIPELINE_FOLDER)
        self.assertIsNone(ans)

    def test_d_r_m_none_url(self):
        none_url = None
        ans = download_repo_metadata(url=none_url, output_folder_path=PIPELINE_FOLDER)
        self.assertIsNone(ans)

    def test_d_r_m_output_nonexistent(self):
        wipe_directory(PIPELINE_FOLDER)
        real_url = "https://github.com/SoftwareUnderstanding/SSKG"
        non_existent_dir = os.path.join(PIPELINE_FOLDER,"non_existent")
        ans = download_repo_metadata(url=real_url, output_folder_path=non_existent_dir)
        self.assertTrue(os.path.exists(ans))
    def test_d_r_m_output_path_none(self):
        real_url = "https://github.com/SoftwareUnderstanding/SSKG"
        ans = download_repo_metadata(url=real_url, output_folder_path=None)
        self.assertIsNone(ans)

    def test_d_r_m_somef_fail(self):
        wipe_directory(PIPELINE_FOLDER)
        real_url = "https://github.com/oeg-upm/web-oeg"
        ans = download_repo_metadata(url=real_url, output_folder_path=PIPELINE_FOLDER)
        self.assertIsNone(ans)

    # !-----------------------------------------------
    # Test related paper extraction:
    #
    def test_related_paper(self):
        false_dict = {"related_papers": [{"result": {"value": ";alskdfja2206.05328"}}]}
        ans = get_related_paper(false_dict)
        expected = "2206.05328"
        self.assertEquals(ans[0],expected)
        pass

    def test_related_none(self):
        ans = get_related_paper(None)
        self.assertIsNone(ans)

    def test_no_related(self):
        false_dic = {}
        ans = get_related_paper(false_dic)
        self.assertIsNone(ans)

    def test_empty_related_paper_1(self):
        false_dict = {"related_papers": [{"result": {"value": ""}}]}
        ans = get_related_paper(false_dict)
        self.assertIsNone(ans)

    def test_empty_related_paper_2(self):
        false_dict = {"related_papers": [{"result": {}}]}
        ans = get_related_paper(false_dict)
        self.assertIsNone(ans)

    def test_empty_related_paper_3(self):
        false_dict = {"related_papers": []}
        ans = get_related_paper(false_dict)
        self.assertIsNone(ans)

    #!-----------------------------------------------
    #Test Description extraction:
    #
    def test_description_arxiv(self):
        false_dict = {"description": [{"result": {"value": ";alskdfja2206.05328"}}]}
        ans = description_finder(false_dict)
        expected = "2206.05328"
        self.assertEquals(ans['arxiv'].pop(),expected)

    def test_description_doi(self):
        false_dict = {"description": [{"result": {"value": ";alskdfja2206.05328https://doi.org/10.5281/zenodo.838601"}}]}
        ans = description_finder(false_dict)
        expected = "10.5281/zenodo.838601"
        self.assertEquals(ans['doi'].pop(),expected)

    def test_description_both(self):
        false_dict = {"description": [{"result": {"value": ";alskdfja2206.05328asfhttps://doi.org/10.5555/KVTD-VPWM"}}]}
        ans = description_finder(false_dict)
        expected_doi = "10.5555/KVTD-VPWM"
        expected_arxiv = "2206.05328"
        self.assertTrue((ans['doi'].pop() == expected_doi) and (ans['arxiv'].pop() == expected_arxiv))

    def test_description_none(self):
        ans = description_finder(None)
        self.assertIsNone(ans)

    def test_no_description(self):
        false_dic = {}
        ans = description_finder(false_dic)
        self.assertTrue(len(ans['doi']) == 0)

    def test_empty_description_1(self):
        false_dict = {"related_papers": [{"result": {"value": ""}}]}
        ans = description_finder(false_dict)
        self.assertTrue(len(ans['doi']) == 0)
    def test_empty_description_2(self):
        false_dict = {"related_papers": [{"result": {}}]}
        ans = description_finder(false_dict)
        self.assertTrue(len(ans['doi']) == 0)
    def test_empty_description_3(self):
        false_dict = {"related_papers": []}
        ans = description_finder(false_dict)
        self.assertTrue(len(ans['doi']) == 0)

    #!-----------------------------------------------
    #Test find_doi_citation:
    #
    def test_find_doi_citation_cff(self):
        false_dict = {"citation": [{"result": {"format": "cff", "value": "https://doi.org/10.5555/KVTD-VPWM"}}]}
        expected = "10.5555/KVTD-VPWM"
        ans = find_doi_citation(false_dict)
        self.assertEquals(ans[0], expected)

    def test_find_doi_citation_none(self):
        ans = find_doi_citation(None)
        self.assertIsNone(ans)

    def test_find_doi_broken_citation_cff(self):
        false_dict = {"citation": [{"result":{"format":"cff", "value": ""}}]}
        ans = find_doi_citation(false_dict)
        self.assertIsNone(ans)

    def test_find_doi_broken_citation_2_cff(self):
        false_dict = {"citation": [{"result":{"format":"cff"}}]}
        ans = find_doi_citation(false_dict)
        self.assertIsNone(ans)

    def test_find_doi_broken_citation_3(self):
        false_dict = {"citation": [{}]}
        ans = find_doi_citation(false_dict)
        self.assertIsNone(ans)
    def test_find_doi_citation_bib(self):
        false_dict = {"citation": [{"result": {"format": "bibtex","value":"https://doi.org/10.5555/KVTD-VPWM"}}]}
        expected = "10.5555/KVTD-VPWM"
        ans = find_doi_citation(false_dict)
        self.assertEquals(ans[0],expected)

    def test_find_doi_broken_citation(self):
        false_dict = {"citation": [{"result": {"format": "RANDOM", "value": ""}}]}
        ans = find_doi_citation(false_dict)
        self.assertIsNone(ans)

    def test_find_doi_text_excerpt(self):
        false_dict = {"citation": [{"result": {"type": "Text_excerpt", "value": "https://doi.org/10.5555/KVTD-VPWM"}}]}
        expected = "10.5555/KVTD-VPWM"
        ans = find_doi_citation(false_dict)
        self.assertEquals(ans[0], expected)

    def test_real_life_example_2_dois(self):
        examp_json = os.path.join(TEST_DIR, "json/somef.json")
        somef_data = load_json(examp_json)
        ans = find_doi_citation(somef_data = somef_data)
        self.assertTrue(len(ans) > 0)

    #!-----------------------------------------------
    #Test find_arxiv_citation:
    #
    def test_find_arxiv_citation_cff(self):
        false_dict = {"citation": [{"result": {"format": "cff", "value": "https://arxiv.org/abs/2206.05328"}}]}
        expected = "2206.05328"
        ans = find_arxiv_citation(false_dict)
        self.assertEquals(ans[0], expected)

    def test_find_arxiv_citation_none(self):
        ans = find_arxiv_citation(None)
        self.assertIsNone(ans)

    def test_find_arxiv_broken_citation_cff(self):
        false_dict = {"citation": [{"result":{"format":"cff", "value": ""}}]}
        ans = find_arxiv_citation(false_dict)
        self.assertIsNone(ans)

    def test_find_arxiv_broken_citation_2_cff(self):
        false_dict = {"citation": [{"result":{"format":"cff"}}]}
        ans = find_arxiv_citation(false_dict)
        self.assertIsNone(ans)

    def test_find_arxiv_broken_citation_3(self):
        false_dict = {"citation": [{}]}
        ans = find_arxiv_citation(false_dict)
        self.assertIsNone(ans)
    def test_find_arxiv_citation_bib(self):
        false_dict = {"citation": [{"result": {"format": "bibtex","value":"ads;fl\n2206.05328"}}]}
        expected = "2206.05328"
        ans = find_arxiv_citation(false_dict)
        self.assertEquals(ans[0],expected)

    def test_find_arxiv_broken_citation(self):
        false_dict = {"citation": [{"result": {"format": "RANDOM", "value": ""}}]}
        ans = find_arxiv_citation(false_dict)
        self.assertIsNone(ans)

    def test_find_arxiv_text_excerpt(self):
        false_dict = {"citation": [{"result": {"type": "Text_excerpt", "value": "a;lskdfj;l2206.05328"}}]}
        expected = "2206.05328"
        ans = find_arxiv_citation(false_dict)
        self.assertEquals(ans[0], expected)

    def test_real_life_example_2_arxivs(self):
        examp_json = os.path.join(TEST_DIR, "json/somef.json")
        somef_data = load_json(examp_json)
        ans = find_arxiv_citation(somef_data = somef_data)
        self.assertTrue(len(ans) > 0)










