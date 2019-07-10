# coding: utf-8
"""unittest of resize_image.py"""

from unittest import TestCase
from pathlib import Path
import cv2
from ..library.analyzers.preprocessing.resize_image import _MatResizer

ASSET_FOLDER = 'code/unit_tests/assets_for_test/library/analyzers/preprocessing/resize_image/'

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
