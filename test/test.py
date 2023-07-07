import os
import unittest
from unittest import TestCase, mock
import json
from pathlib import Path

from download_pdf.pipeline import pdf_download_pipeline

def wipe_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file: {file_path} - {e}")

from metadata_extraction.paper_obj import PaperObj
class test_paper_obj(TestCase):

    def test_normal_paper(self):
        paper = PaperObj("title","urls","10.1007/978-3-030-16350-1_1","0705.0123","filename","/path/to/file")
        self.assertTrue(paper.doi and paper.arxiv)
    def test_wrong_doi(self):
        #should return none for doi
        paper = PaperObj("title","urls","10.1007_978-3-030-16350-1_1","0705.0123","filename","/path/to/file")
        self.assertIsNone(paper.doi)
    def test_wrong_arxiv(self):
        #should return none for arxiv
        paper = PaperObj("title","urls","10.1007/978-3-030-16350-1_1","0705/0123","filename","/path/to/file")
        self.assertIsNone(paper.arxiv)
class test_download_pdf(TestCase):

    def test_download_oa_pdf(self):
        wipe_directory("./pdfs")
        #DOI should be Association of genomic subtypes of lower-grade gliomas ....
        doi = "10.1016/j.compbiomed.2019.05.002"
        file_path = pdf_download_pipeline(doi, "./pdfs")

        self.assertEquals(file_path, "./pdfs/10-DOT-1016_j-DOT-compbiomed-DOT-2019-DOT-05-DOT-002.pdf")

    def test_already_downloaded_oa_pdf(self):
        wipe_directory("./pdfs")
        doi = "10.1016/j.compbiomed.2019.05.002"
        doi1 = "https://doi.org/10.1016/j.compbiomed.2019.05.002"
        pdf_download_pipeline(doi, "./pdfs")
        filepath2 = pdf_download_pipeline(doi1, "./pdfs")

        self.assertIsNone(filepath2)
    #TODO
    def test_arvix_download(self):
        pass


#Test of bidirectionality


from modelling.bidirectionality import is_arxiv_bidir
from modelling.bidirectionality import is_doi_bidir

class test_bidir(TestCase):

    def test_doi_bib_citation(self):
        title = "Association of genomic subtypes of lower-grade gliomas with shape features ..."
        doi = "https://doi.org/10.1016/j.compbiomed.2019.05.002"
        urls = None
        arxiv = None
        pdfObj = PaperObj(title, urls, doi, arxiv, file_name=None, file_path=None)
        self.assertTrue(is_doi_bidir(pdfObj, "./json/doi_in_citation.json"))

    def test_doi_citation_url(self):
        title = "On Sampling Collaborative Filtering Datasets"
        doi = "https://doi.org/10.1145/3488560.3498439"
        urls = None
        arxiv = None
        pdfObj = PaperObj(title, urls, doi, arxiv, file_name=None, file_path=None)
        self.assertTrue(is_doi_bidir(pdfObj,"./json/doi_in_citation_url.json"))

    def test_doi_description(self):
        title = "On Sampling Collaborative Filtering Datasets"
        doi = "https://doi.org/10.1145/3488560.3498439"
        urls = None
        arxiv = None
        pdfObj = PaperObj(title, urls, doi, arxiv, file_name=None, file_path=None)
        self.assertTrue(is_doi_bidir(pdfObj,"./json/doi_in_description.json"))

    def test_arxiv_url_desc(self):
        #arxiv ID in url
        title = "Identifying and Analyzing Cryptocurrency Manipulations in Social Media"
        doi = "10.31219/osf.io/dqz89"
        urls = None
        arxiv = "1902.03110v2"
        pdfObj = PaperObj(title,urls,doi,arxiv,file_name=None,file_path=None)
        self.assertTrue(is_arxiv_bidir(pdfObj, "./json/url_arxiv_description.json"))

    def test_arxiv_text_citation(self):
        #arxiv ID in url
        title = "Identifying and Analyzing Cryptocurrency Manipulations in Social Media"
        doi = "10.31219/osf.io/dqz89"
        urls = None
        arxiv = "1902.03110v2"
        pdfObj = PaperObj(title,urls,doi,arxiv,file_name=None,file_path=None)
        self.assertTrue(is_arxiv_bidir(pdfObj, "./json/url_arxiv_text_citation.json"))

    def test_arxiv_url_desc(self):
        #arxiv ID in url
        title = "Identifying and Analyzing Cryptocurrency Manipulations in Social Media"
        doi = "10.31219/osf.io/dqz89"
        urls = None
        arxiv = "1902.03110v2"
        pdfObj = PaperObj(title,urls,doi,arxiv,file_name=None,file_path=None)
        self.assertTrue(is_arxiv_bidir(pdfObj, "./json/url_arxiv_description.json"))

    def test_arxiv_desc2(self):
        #TODO test fails due to somef issue
        # Does not extract the citation nor the description on it
        title = ""
        doi = "10.1109/itsc.2019.8917177"
        urls = None
        arxiv = "1907.11111"
        pdfObj = PaperObj(title, urls, doi, arxiv, file_name=None, file_path=None)
        #self.assertTrue(is_arxiv_bidir(pdfObj, "./json/arxiv_desc_2.json"))

from modelling.unidirectionality import is_repo_unidir
class test_unidir(TestCase):
    def test_unidir(self):
        title = "Learning Dynamic Memory Networks for Object Tracking"
        doi = "10.1007/978-3-030-01240-3_10"
        urls = None
        arxiv = None
        pdfObj = PaperObj(title, urls, doi, arxiv, file_name=None, file_path=None)
        self.assertTrue(is_repo_unidir(pdfObj, "./json/unidir.json"))

    def test_unidir_citation(self):
        title = "How Suitable Are Subword Segmentation Strategies for Translating Non-Concatenative Morphology?"
        doi = "10.18653/v1/2021.findings-emnlp.60"
        urls = None
        arxiv = None
        pdfObj = PaperObj(title, urls, doi, arxiv, file_name=None, file_path=None)
        self.assertTrue(is_repo_unidir(pdfObj, "./json/unidir_citation.json"))


#TODO rename
from pipeline import check_paper_directionality, pipeline_to_json, bidir_to_json


class test_pipeline(TestCase):

    def test_doi_pipeline(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1016/j.compbiomed.2019.05.002"
        result = check_paper_directionality(doi,True,'./pipeline_folder')
        expected_result = 'https://github.com/mateuszbuda/brain-segmentation'
        self.assertEquals(result[doi][0], expected_result)

    def test_doi_pipeline1(self):
        wipe_directory("./pipeline_folder")
        doi = "10.18653/v1/2021.findings-emnlp.116"
        result = check_paper_directionality(doi, True,'./pipeline_folder')
        expected_result = 'https://github.com/YunqiuXu/H-KGA'
        self.assertEquals(result[doi][0], expected_result)

    def test_doi_pipeline2(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1051/0004-6361/201935695"
        result = check_paper_directionality(doi,True,'./pipeline_folder')
        expected_result = 'https://github.com/astro-alexis/magnotron-tts'
        self.assertEquals(result[doi][0], expected_result)

    def test_doi_pipeline3(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1109/itsc.2019.8917177"
        result = check_paper_directionality(doi, True, './pipeline_folder')
        expected_result = 'https://github.com/lukasliebel/MultiDepth'
        self.assertEquals(result[doi][0], expected_result)

    def test_doi_pipeline4(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1109/iwis56333.2022.9920762"
        result = check_paper_directionality(doi, True,'./pipeline_folder')
        self.assertIsNone(result)
    def test_doi_pipeline5(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1145/3485447.3511945"
        result = check_paper_directionality(doi, True, './pipeline_folder')
        expected_result = 'https://github.com/THUDM/SelfKG'
        self.assertEquals(result[doi][0], expected_result)

    def test_doi_pipeline5(self):
        #FAILS, SOMEF ISSUE
        wipe_directory("./pipeline_folder")
        doi = "10.1145/3485447.3511945"
        result = check_paper_directionality(doi, True, './pipeline_folder')
        expected_result = 'https://github.com/THUDM/SelfKG'
        #self.assertEquals(result[doi][0], expected_result)
    def test_doi_pipeline6(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1007/978-3-319-26123-2_24"
        result = check_paper_directionality(doi, True, './pipeline_folder')
        expected_result = 'https://github.com/IlyaTrofimov/dlr'
        self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_related(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1109/itsc.2019.8917177"
        result = check_paper_directionality(doi, True, './pipeline_folder')
        expected_result = 'https://github.com/lukasliebel/MultiDepth'
        self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_related2(self):
        '''It is not mentioned within the paper'''
        wipe_directory("./pipeline_folder")
        doi = "10.18653/v1/2021.naacl-main.458"
        result = check_paper_directionality(doi,True, './pipeline_folder')
        expected_result = None
        self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_1(self):
        '''Test to download first OA the best pdf has 403 forbidden'''
        wipe_directory("./pipeline_folder")
        doi = "10.1109/iccv48922.2021.00338"
        result = check_paper_directionality(doi,True, './pipeline_folder')
        expected_result = "https://github.com/uncbiag/ICON"
        self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_2(self):
        '''Test to download first OA the best pdf has 403 forbidden'''
        wipe_directory("./pipeline_folder")
        doi = "10.18653/v1/2020.acl-main.55"
        result = check_paper_directionality(doi,True, './pipeline_folder')
        expected_result = "https://github.com/cl-tohoku/eval-via-selection"
        self.assertEquals(result[doi][0], expected_result)

    def test_arxiv_3(self):
        '''Will fail due to OpenAlex'''
        wipe_directory("./pipeline_folder")
        doi = "10.24963/ijcai.2022/208"
        result = check_paper_directionality(doi,True,'./pipeline_folder')
        expected_result = "https://github.com/Robbie-Xu/CPSD"
        #self.assertEquals(result[doi][0], expected_result)

    def test_arxiv_4(self):
        '''Issue Due to SOMEF'''
        wipe_directory("./pipeline_folder")
        doi = "10.1007/978-3-319-26123-2_24"
        result = check_paper_directionality(doi,True,'./pipeline_folder')
        expected_result = "https://github.com/IlyaTrofimov/dlr"
        #self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_5(self):
        '''Issue Due to SOMEF'''
        wipe_directory("./pipeline_folder")
        doi = "10.1007/978-3-319-26123-2_24"
        result = check_paper_directionality(doi,True,'./pipeline_folder')
        expected_result = "https://github.com/IlyaTrofimov/dlr"
        #self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_6(self):
        ''''''
        wipe_directory("./pipeline_folder")
        doi = "10.2478/pralin-2018-0002"
        result = check_paper_directionality(doi, True, './pipeline_folder')
        expected_result = "https://github.com/tensorflow/tensor2tensor"
        self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_7(self):
        wipe_directory("./pipeline_folder")
        doi = "10.21428/58320208.e46b7b81"
        result = check_paper_directionality(doi, True, './pipeline_folder')
        expected_result = "https://github.com/aklamun/Stablecoin_Deleveraging"
        self.assertTrue(expected_result in result[doi])
    def test_arxiv_8(self):
        wipe_directory("./pipeline_folder")
        doi = "10.18653/v1/2020.emnlp-main.495"
        result = check_paper_directionality(doi, True, './pipeline_folder')
        expected_result = "https://github.com/AI-secure/T3/"
        self.assertTrue(expected_result in result[doi])
    def test_doi_2(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1145/3508352.3549415"
        result = check_paper_directionality(doi, True, './pipeline_folder')
        expected_result = "https://github.com/momalab/e3"
        self.assertTrue(expected_result in result[doi])
    def test_unidir_doi(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1007/978-3-030-01240-3_10"
        result = check_paper_directionality(doi, False, './pipeline_folder')
        expected_result = 'https://github.com/skyoung/MemTrack'
        self.assertEquals(result[doi][0], expected_result)


    def test_unidir_doi2(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1109/iccv48922.2021.00338"
        result = check_paper_directionality(doi, False, './pipeline_folder')
        expected_result = 'https://github.com/ryosuke-akashi/AtomREM'
        self.assertEquals(result[doi][0], expected_result)


    # def test_dois_pipeline(self):
    #     wipe_directory("./pipeline_folder")
    #     dois_txt = "./dois.txt"
    #     print(bidir_to_json(dois_txt,'./pipeline_folder'))



    # def test_dois_pipeline(self):
    #     wipe_directory("./pipeline_folder")
    #     dois_txt = "./dois.txt"
    #     print(pipeline_to_json(dois_txt, False,'./pipeline_folder'))


