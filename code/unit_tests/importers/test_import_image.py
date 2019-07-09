# coding: utf-8
"""unittest of import_image.py"""

import unittest
import glob
import cv2
from ...library.importers.import_image import ImageImporter

class TestImageImporter(unittest.TestCase):
    """ImageImporterクラス"""
    def test_get_mat_list(self):
        """フォルダから全てのjpg画像ファイルをmatのリストとして取得できるか"""
        path = 'test_images/'
        importer = ImageImporter(path)

        # ほとんどテストになってないけど、これ以外にやりようがない……
        paths = glob.glob(path + "*.jpg")
        mats = []
        for path in paths:
            mats.append(cv2.imread(path))

        self.assertEqual(importer.get_mat_list(), mats)
