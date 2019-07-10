# coding: utf-8
"""unittest of classify_image.py"""

from unittest import TestCase
from pathlib import Path
import cv2
from ..library.analyzers.preprocessing.classify_image import _Cv2ImageLoader

ASSET_FOLDER = 'code/unit_tests/assets_for_test/library/analyzers/preprocessing/classify_image/'

class TestGearClassifier(TestCase):
    """GearClassifierクラス"""
    def test_write_image_file_in_each_folder(self):
        pass

class TestGearPartDetecter(TestCase):
    """GearPartDetecterクラス"""
    def test_detect(self):
        pass

class TestCv2ImageLoader(TestCase):
    """Cv2ImageLoaderクラス"""
    def test_load_gray(self):
        """ライブラリの機能をそのまま使ってるだけなので本当はテストしなくても良いと思う"""
        source_path = Path(ASSET_FOLDER + 'Cv2ImageLoader/a.jpg')
        source_path = str(source_path)
        mat = cv2.imread(source_path)
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
        print(mat)
        result = _Cv2ImageLoader().load_gray(source_path)
        print(result)
        self.assertTrue((result == mat).all())

class TestMatColorDeterminer(TestCase):
    """MatColorDeterminerクラス"""
    def test_is_almost_white(self):
        """白い画像を渡して、白い画像だとちゃんと判定できるか"""
        pass
