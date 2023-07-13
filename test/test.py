import os
import unittest
from unittest import TestCase, mock
import json
from pathlib import Path
from pathlib import Path
from shutil import rmtree


def wipe_directory(directory_path):
    for path in Path(directory_path).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)

from metadata_extraction import metadata_obj

from pipeline.doi_to_metadata import *
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
