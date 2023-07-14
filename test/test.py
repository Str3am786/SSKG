import os
import unittest
from unittest import TestCase, mock
import json
from pathlib import Path
from pathlib import Path
from shutil import rmtree
from object_creator.doi_to_metadata import *
from object_creator.create_downloadedObj import *
from object_creator.pdf_to_downloaded import *

def wipe_directory(directory_path):
    for path in Path(directory_path).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)


class test_doi_to_Obj(TestCase):
    def test_doi_toPaperObj(self):
        result = doi_to_metadataObj("10.1016/j.compbiomed.2019.05.002")
        expected_result = 'Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm'
        self.assertEquals(result.title, expected_result)
    def test_doi_toPdfJson(self):
        doi = "10.1016/j.compbiomed.2019.05.002"
        result_p = doi_to_metaJson(doi,"./pipeline_folder")
        expected_result = 'Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm'
        with open(result_p, 'r') as f:
            result = json.load(f)
        self.assertEquals(result[doi]['title'], expected_result)

    def test_doi_toPaperDict(self):
        doi = "10.1016/j.compbiomed.2019.05.002"
        result = doi_to_metaDict(doi)
        self.assertTrue(doi in result.keys())

    def test_dois_to_dict(self):
        with open("./dois.txt", 'r') as file:
            dois = file.read().splitlines()
        result = dois_to_metaDicts(dois)
        assert(result)


class test_create_DownloadedObj(TestCase):

    def test_normal_pipeline(self):
        doi = "10.1016/j.compbiomed.2019.05.002"
        meta = doi_to_metadataObj(doi)
        dwn_obj = meta_to_dwnldd(meta, "./pipeline_folder")
        self.assertEquals(dwn_obj.doi, doi)
    def test_problematic_doi(self):
        doi = "10.18653/v1/2020.acl-main.55"
        meta = doi_to_metadataObj(doi)
        dwn_obj = meta_to_dwnldd(meta, "./pipeline_folder")
        self.assertEquals(dwn_obj.doi, doi)
    def test_metaJson_to_downloadedJson(self):
        meta_json = "./json/oa_metadata.json"
        dict_dwn = metaJson_to_downloaded_dic(meta_json,"./pipeline_folder")
        assert(dict_dwn)
        pass

class test_pdf_to_downloaded(TestCase):
    def test_adrian_to_dict(self):
        directory = "./pdfs     "
        result = adrian_pdfs_2dictionary(directory)
        assert(result["10.1109/jstsp.2016.2617302"])
    def test_null_adrian_to_dict(self):
        directory = ""
        result = adrian_pdfs_2dictionary(directory)
        self.assertIsNone(result)

    def test_adrian_pdf_toJson(self):
        directory = "./pdfs"
        output_path = adrian_pdfs_2Json(directory)
        assert(output_path)

from object_creator.paper_to_directionality import check_paper_directionality
from object_creator.pipeline import doi_to_paper, pipeline_multiple_bidir, pipeline_single_bidir


class test_bidir(TestCase):
    def test_doi_pipeline(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1016/j.compbiomed.2019.05.002"
        paper = doi_to_paper(doi,"./pipeline_folder" )
        result = check_paper_directionality(paper,True,'./pipeline_folder')
        expected_result = 'https://github.com/mateuszbuda/brain-segmentation'
        self.assertEquals(result[doi][0], expected_result)

    def test_doi_pipeline1(self):
        wipe_directory("./pipeline_folder")
        doi = "10.18653/v1/2021.findings-emnlp.116"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = 'https://github.com/YunqiuXu/H-KGA'
        self.assertEquals(result[doi][0], expected_result)

    def test_doi_pipeline2(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1051/0004-6361/201935695"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = 'https://github.com/astro-alexis/magnotron-tts'
        self.assertEquals(result[doi][0], expected_result)

    def test_doi_pipeline3(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1109/itsc.2019.8917177"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = 'https://github.com/lukasliebel/MultiDepth'
        self.assertEquals(result[doi][0], expected_result)

    def test_doi_pipeline4(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1109/iwis56333.2022.9920762"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        self.assertIsNone(result)
    def test_doi_pipeline5(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1145/3485447.3511945"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = 'https://github.com/THUDM/SelfKG'
        self.assertEquals(result[doi][0], expected_result)

    def test_doi_pipeline5(self):
        #FAILS, SOMEF ISSUE
        wipe_directory("./pipeline_folder")
        doi = "10.1145/3485447.3511945"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = 'https://github.com/THUDM/SelfKG'
        #self.assertEquals(result[doi][0], expected_result)
    def test_doi_pipeline6(self):
        #TODO
        #fails due to pointing to a new version of arxiv. Has a new ID
        wipe_directory("./pipeline_folder")
        doi = "10.1007/978-3-319-26123-2_24"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = 'https://github.com/IlyaTrofimov/dlr'
        #self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_related(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1109/itsc.2019.8917177"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = 'https://github.com/lukasliebel/MultiDepth'
        self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_related2(self):
        '''It is not mentioned within the paper'''
        wipe_directory("./pipeline_folder")
        doi = "10.18653/v1/2021.naacl-main.458"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = None
        self.assertEquals(result, expected_result)
    def test_arxiv_1(self):
        '''Test to download first OA the best pdf has 403 forbidden'''
        wipe_directory("./pipeline_folder")
        doi = "10.1109/iccv48922.2021.00338"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "https://github.com/uncbiag/ICON"
        self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_2(self):
        '''Test to download first OA the best pdf has 403 forbidden'''
        wipe_directory("./pipeline_folder")
        doi = "10.18653/v1/2020.acl-main.55"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "https://github.com/cl-tohoku/eval-via-selection"
        self.assertEquals(result[doi][0], expected_result)

    def test_arxiv_3(self):
        #TODO add the crossref to fix this openAlex issue
        '''Will fail due to OpenAlex'''
        wipe_directory("./pipeline_folder")
        doi = "10.24963/ijcai.2022/208"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "https://github.com/Robbie-Xu/CPSD"
        #self.assertEquals(result[doi][0], expected_result)

    def test_arxiv_4(self):
        '''Issue Due to SOMEF'''
        wipe_directory("./pipeline_folder")
        doi = "10.1007/978-3-319-26123-2_24"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "https://github.com/IlyaTrofimov/dlr"
        #self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_5(self):
        #TODO
        '''Different Arxiv's'''
        wipe_directory("./pipeline_folder")
        doi = "10.1007/978-3-319-26123-2_24"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "https://github.com/IlyaTrofimov/dlr"
        #self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_6(self):
        ''''''
        wipe_directory("./pipeline_folder")
        doi = "10.2478/pralin-2018-0002"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "https://github.com/tensorflow/tensor2tensor"
        self.assertEquals(result[doi][0], expected_result)
    def test_arxiv_7(self):
        wipe_directory("./pipeline_folder")
        doi = "10.21428/58320208.e46b7b81"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "https://github.com/aklamun/Stablecoin_Deleveraging"
        self.assertTrue(expected_result in result[doi])
    def test_arxiv_8(self):
        '''Test should pass, readme is an absolute mess'''
        wipe_directory("./pipeline_folder")
        doi = "10.1051/0004-6361/202039603"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "http://github.com/mianbreton/RR_code"
        self.assertTrue(expected_result in result[doi])
    def test_arxiv_9(self):
        wipe_directory("./pipeline_folder")
        doi = "10.18653/v1/2020.emnlp-main.495"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "https://github.com/AI-secure/T3/"
        self.assertTrue(expected_result in result[doi])
    def test_doi_2(self):
        wipe_directory("./pipeline_folder")
        doi = "10.1145/3508352.3549415"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "https://github.com/momalab/e3"
        self.assertTrue(expected_result in result[doi])

    def test_doi_3(self):
        #TODO SOMEF ISSUE
        wipe_directory("./pipeline_folder")
        doi = "10.1145/3318170.3318183"
        paper = doi_to_paper(doi, "./pipeline_folder")
        result = check_paper_directionality(paper, True, './pipeline_folder')
        expected_result = "https://github.com/CodeplaySoftware/SYCL-DNN"
        #self.assertTrue(expected_result in result[doi])


    # def test_unidir_doi(self):
    #     wipe_directory("./pipeline_folder")
    #     doi = "10.1007/978-3-030-01240-3_10"
    #     result = check_paper_directionality(doi, False, './pipeline_folder')
    #     expected_result = 'https://github.com/skyoung/MemTrack'
    #     self.assertEquals(result[doi][0], expected_result)
    #
    #
    # def test_unidir_doi2(self):
    #     wipe_directory("./pipeline_folder")
    #     doi = "10.1109/iccv48922.2021.00338"
    #     result = check_paper_directionality(doi, False, './pipeline_folder')
    #     expected_result = 'https://github.com/uncbiag/ICON'
    #     self.assertEquals(result[doi][0], expected_result)
    #
    # def test_unidir_doi3(self):
    #     wipe_directory("./pipeline_folder")
    #     doi = "10.18653/v1/2020.emnlp-main.495"
    #     result = check_paper_directionality(doi, False, './pipeline_folder')
    #     expected_result = 'https://github.com/AI-secure/T3'
    #     self.assertEquals(result[doi][0], expected_result)
class test_pipeline(TestCase):
    def test_one_doi(self):
        wipe_directory("./pipeline_folder")
        doi = '10.1007/978-3-030-16350-1_1'
        output_dir = "./pipeline_folder"
        pipeline_single_bidir(doi, output_dir)
    def test_short_list_doi(self):
        wipe_directory("./pipeline_folder")
        list_dois_txt = "./dois.txt"
        output_dir = "./pipeline_folder"
        with open(list_dois_txt, 'r') as file:
            dois = file.read().splitlines()
        result = pipeline_multiple_bidir(dois, output_dir)
        print(result)