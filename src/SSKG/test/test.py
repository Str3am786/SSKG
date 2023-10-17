from pathlib import Path
from shutil import rmtree
from unittest import TestCase

from SSKG.metadata.api.openAlex_api_queries import pdf_title_to_meta
from SSKG.extraction.paper_obj import PaperObj
from SSKG.modelling.unidirectionality import *
from SSKG.object_creator.create_downloadedObj import *
from SSKG.object_creator.doi_to_metadata import *
from SSKG.object_creator.downloaded_to_paperObj import dwnlddJson_to_paperJson
from SSKG.object_creator.pdf_to_downloaded import *
from SSKG.object_creator.pipeline import *


def wipe_directory(directory_path):
    for path in Path(directory_path).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)

class test_open_alex_query(TestCase):
    def test_title_query(self):
        title = "Widoco"
        resp_json = pdf_title_to_meta(title)
        doi = resp_json["results"][0]["doi"]
        self.assertEquals(doi,"https://doi.org/10.1007/978-3-319-68204-4_9")

    def test_no_title_query(self):
        title = ""
        resp_json = pdf_title_to_meta(title)
        assert(resp_json)

    def test_title_with_spaces(self):
        title = "SPARQL2Flink: Evaluation of SPARQL Queries on Apache Flink"
        resp_json = pdf_title_to_meta(title)
        doi = resp_json["results"][0]["doi"]
        self.assertEquals(doi, "https://doi.org/10.3390/app11157033")

    def test_None_title(self):
        test = pdf_title_to_meta(None)
        self.assertIsNone(test)
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

class test_download_pdf_pipeline(TestCase):

    def test_normal_download(self):
        assert(True)
    def test_download_directory_doesnt_exist_prior(TestCase):
        non_existent = "./not_exist"
        doi = "10.3233/sw-223135"
        result = pdf_download_pipeline(doi,non_existent)
        wipe_directory("./not_exist")
        os.rmdir("./not_exist")
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
    #TODO create work around redirect
    # def test_problematic_doi2(self):
    #     doi = "10.1016/j.engappai.2022.104755"
    #     meta = doi_to_metadataObj(doi)
    #     dwn_obj = meta_to_dwnldd(meta, "./pipeline_folder")
    #     self.assertEquals(dwn_obj.doi, doi)
    def test_dois_txt_to_json(self):
        wipe_directory("./pipeline_folder")
        doi_txt = "./testOEG.txt"
        output_dir = "./pipeline_folder"
        result = dois_txt_to_downloadedJson(dois_txt=doi_txt,output_dir=output_dir)
        assert(result)
    def test_metaJson_to_downloadedJson(self):
        meta_json = "./json/oa_metadata.json"
        dict_dwn = metaJson_to_downloaded_dic(meta_json,"./pipeline_folder")
        assert(dict_dwn)
        pass

class test_pdf_to_downloaded(TestCase):
    def test_adrian_to_dict(self):
        directory = "./pdfs"
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

from SSKG.object_creator.paper_to_directionality import check_paper_directionality
from SSKG.object_creator.pipeline import doi_to_paper, pipeline_multiple_bidir, pipeline_single_bidir, \
    pipeline_txt_dois_bidir


class test_downloaded_to_paper_obj(TestCase):

    def test_downloadedJson_to_pp_Json(self):
        dwn_json = "./pdfs/pdf_metadata.json"
        output_path = "./pdfs/"
        dwnlddJson_to_paperJson(dwn_json,output_path)


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
        expected_result = "https://github.com/AI-secure/T3"
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
class test_downloaded_to_paperObj(TestCase):
    def test_dwnldd_2_paper_json(self):
        assert(dwnlddJson_to_paperJson("../test/pdfs/pdf_metadata.json", "../test/pdfs"))
class test_pipeline(TestCase):
    def test_one_doi(self):
        wipe_directory("./pipeline_folder")
        doi = '10.1016/j.compbiomed.2019.05.002'
        output_dir = "./pipeline_folder"
        result = pipeline_single_bidir(doi, output_dir)
        assert(result)
    def test_one_doi2(self):
        wipe_directory("./pipeline_folder")
        doi = '10.3233/SW-223135'
        output_dir = "./pipeline_folder"
        result = pipeline_single_bidir(doi, output_dir)
        assert(result)

    def test_short_list_doi(self):
        wipe_directory("./pipeline_folder")
        list_dois_txt = "./short.txt"
        output_dir = "./pipeline_folder"
        with open(list_dois_txt, 'r') as file:
            dois = file.read().splitlines()
        result = pipeline_multiple_bidir(dois, output_dir)
        assert(result)
    def test_txts_bidir(self):
        wipe_directory("./pipeline_folder")
        list_dois_txt = "./short.txt"
        output_dir = "./pipeline_folder"
        result = pipeline_txt_dois_bidir(list_dois_txt,output_dir)
        assert(result)
    # def test_txts_to_bidir(self):
    #     wipe_directory("./pipeline_folder")
    #     list_dois_txt = "./dois.txt"
    #     output_dir = "./pipeline_folder"
    #     result = dois_txt_to_bidir_json(list_dois_txt,output_dir)
    #     assert(result)

class test_paperJson_to_bidir(TestCase):

    def test_ppJson_to_bidir(self):
        wipe_directory("./pipeline_folder")
        from_papers_json_to_bidir("./json/paperTest.json","./pipeline_folder")


class test_unidir(TestCase):

    #SubString finder set to 85
    def test_substring_1(self):
        to_find = ["vish_editor", "ViSH_Editor", "vish editor", "vishEdit", "vishEditor", "ViSh_EdItOR"]
        testJson = "./json/string_finder_tests.json"
        with open(testJson, 'r') as f:
            jayson = json.load(f)
        vish_test = jayson["vish"]
        for subString in to_find:
            for test in vish_test:
                text = vish_test[test]
                if not is_substring_found(subString, text):
                    self.assertTrue(False)
    def test_substring_2(self):
        to_find = "vishesh_editor" #average score of 73 (71,71,77)
        testJson = "./json/string_finder_tests.json"
        with open(testJson, 'r') as f:
            jayson = json.load(f)
        vish_test = jayson["vish"]
        for test in vish_test:
            text = vish_test[test]
            if not is_substring_found(to_find, text):
                self.assertTrue(True)
    def test_substring_3(self):
        to_find = "HippoUnit_demo" #Score of 64 Will not find the String
        text = "HippoUnit: A software tool for the automated testing and systematic comparison of detailed models of hippocampal neurons based on electrophysiological data"
        result = is_substring_found(to_find, text)

    def test_substring_4(self):
        to_find = "Perturbation_in_dynamical_models" #Score of 88
        text = "Perturbations in dynamical models of whole-brain activity dissociate between the level and stability of consciousness"
        self.assertTrue(is_substring_found(to_find, text))

    def test_substring_5(self):
        to_find = "CovidH_TNG" #Score of 67
        text = "Integrating psychosocial variables and societal diversity in epidemic models for predicting COVID-19 transmission dynamics"
        self.assertFalse(is_substring_found(to_find, text))

    def test_substring_6(self):
        to_find = "DISORDER" #https://github.com/mriphysics/DISORDER 10.1101/2020.09.09.20190777
        text = "Evaluation of DISORDER: retrospective image motion correction for volumetric brain MRI in a pediatric setting"
        self.assertTrue(is_substring_found(to_find, text))

    def test_substring_7(self):
        to_find = "AtomREM" #Found directly
        text = "AtomREM: Non-empirical seeker of the minimum energy escape paths on many-dimensional potential landscapes without coarse graining"
        self.assertTrue(is_substring_found(to_find, text))

    def test_substring_8(self):
        to_find = "AtomREM - Atomistic Rare Event Manager" #Score 53
        text = "AtomREM: Non-empirical seeker of the minimum energy escape paths on many-dimensional potential landscapes without coarse graining"
        self.assertFalse(is_substring_found(to_find, text))

    def test_unidir_1(self):
        #Should return that it is Unidir
        title = "AtomREM: Non-empirical seeker of the minimum energy escape paths on many-dimensional potential landscapes without coarse graining"
        paper = PaperObj(title,urls=None,doi=None,arxiv=None,file_name=None,file_path=None,abstract=None)
        repo_dir = "./json/atomrem.json"
        self.assertTrue(is_repo_unidir(paperObj=paper, repo_json=repo_dir))

    def test_unidir_2(self):
        #Should return that it is Unidir (full title within the description
        title = "Algorithms to compute the Burrows-Wheeler Similarity Distribution"
        paper = PaperObj(title,urls=None,doi=None,arxiv=None,file_name=None,file_path=None,abstract=None)
        repo_dir = "./json/bwsd.json"
        self.assertTrue(is_repo_unidir(paperObj=paper, repo_json=repo_dir))
