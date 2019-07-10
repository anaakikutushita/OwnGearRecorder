# coding: utf-8
"""unittest of classify_image.py"""

from unittest import TestCase
from pathlib import Path
import cv2
from ..library.analyzers.preprocessing.classify_image import _Cv2ImageLoader
from ..library.analyzers.preprocessing.classify_image import _MatColorDeterminer

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
        source_path = str(Path(ASSET_FOLDER + 'Cv2ImageLoader/a.jpg'))
        mat = cv2.imread(source_path)
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
        result = _Cv2ImageLoader().load_gray(source_path)
        self.assertTrue((result == mat).all())

class TestMatColorDeterminer(TestCase):
    """MatColorDeterminerクラス"""
    def test_is_almost_white(self):
        """白い画像を渡す"""
        path = str(Path(ASSET_FOLDER + 'MatColorDeterminer/white.jpg'))
        mat = cv2.imread(path)
        thresh = 0.01
        is_white = _MatColorDeterminer().is_almost_white(mat, thresh)
        self.assertTrue(is_white)

    def test_is_not_almost_white(self):
        """白くはない画像を渡す"""
        path = str(Path(ASSET_FOLDER + 'MatColorDeterminer/black.jpg'))
        mat = cv2.imread(path)
        thresh = 0.01
        is_white = _MatColorDeterminer().is_almost_white(mat, thresh)
        self.assertFalse(is_white)
