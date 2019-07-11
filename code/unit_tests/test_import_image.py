# coding: utf-8
"""unittest of import_image.py"""

from unittest import TestCase
import glob
import cv2
from ..library.importers.import_image import ImageImporter

class TestImageImporter(TestCase):
    """ImageImporterクラス"""
    def test_get_mat_list(self):
        """フォルダから全てのjpg画像ファイルをmatのリストとして取得できるか"""
        path = 'code/unit_tests/assets_for_test/library/importers/'
        importer = ImageImporter(path)

        # ほとんどテストになってないけど、これ以外にやりようがない……
        paths = glob.glob(path + "*.jpg")
        expected_mats = []
        for path in paths:
            expected_mats.append(cv2.imread(path))

        mat_list = importer.get_mat_list()

        # matを一つずつ確認
        results = []
        for index, test_mat in enumerate(mat_list):
            results.append((test_mat == expected_mats[index]).all())

        # import数も確認
        results.append(len(mat_list) == len(expected_mats))

        self.assertTrue(all(results))
