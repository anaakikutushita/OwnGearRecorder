# coding: utf-8
"""unittest of crop_gears.py"""

from unittest import TestCase
from pathlib import Path
import cv2
from ..library.analyzers.preprocessing.crop_gears import GearIconCropper

ASSET_FOLDER = 'code/unit_tests/assets_for_test/library/analyzers/preprocessing/crop_gears/'

class TestGearIconCropper(TestCase):
    """GearIconCropperクラス"""
    def test_cut(self):
        """カスタマイズ画面のスクショからギアを1着ずつ切り出せるか"""
        tops = [101, 232, 364]
        bottoms = [218, 349, 481]
        lefts = [136, 259, 377, 491]
        rights = [249, 372, 490, 604]
        source_path = Path(ASSET_FOLDER + 'GearIconCropper/a.jpg')
        target_mat = cv2.imread(str(source_path))

        results = []
        rows = len(tops)
        cols = len(lefts)
        for row in range(rows):
            for col in range(cols):
                mat = target_mat[tops[row]:bottoms[row], lefts[col]:rights[col]]
                cropper = GearIconCropper(target_mat)
                result = cropper._get_cutted_image(row, col)
                results.append((result == mat).all())

        # 切り出した枚数が12枚であることも確認する
        results.append(len(results) == len(tops) * len(lefts))

        self.assertTrue(all(results))
