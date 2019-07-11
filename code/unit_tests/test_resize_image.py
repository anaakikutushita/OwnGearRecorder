# coding: utf-8
"""unittest of resize_image.py"""

from unittest import TestCase
from pathlib import Path
import cv2
from ..library.analyzers.preprocessing.resize_image import ImageResizer
from ..library.analyzers.preprocessing.resize_image import _MatResizer

ASSET_FOLDER = 'code/unit_tests/assets_for_test/library/analyzers/preprocessing/resize_image/'

class TestImageResizer(TestCase):
    """ImageResizerクラス"""
    def test_get(self):
        """複数の解像度を持つ複数の画像を、全て同じシステム解像度に拡縮して返せるか"""
        source_path = Path(ASSET_FOLDER + 'ImageResizer/')
        mat_list = []
        for img_file in list(source_path.glob('*.jpg')):
            mat_list.append(cv2.imread(str(img_file)))

        resized_list = ImageResizer().get(mat_list)

        results = []
        system_height = 720
        system_width = 1280
        for resized in resized_list:
            results.append((resized.shape[0] == system_height)
                           and (resized.shape[1] == system_width))

        self.assertTrue(all(results))

class TestMatResizer(TestCase):
    """_MatResizerクラス"""
    def test_resize(self):
        """ライブラリの機能を使っているだけなので、本当はテストしなくてもいいと思う"""
        source_path = Path(ASSET_FOLDER + 'MatResizer/a.jpg')
        mat = cv2.imread(str(source_path))
        width = 1280
        hight = 720
        resized = cv2.resize(mat, (width, hight))

        result = _MatResizer().resize(mat, width, hight)
        self.assertTrue((result == resized).all())
