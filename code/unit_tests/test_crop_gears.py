# coding: utf-8
"""unittest of crop_gears.py"""

from unittest import TestCase
from pathlib import Path
import cv2
from ..library.analyzers.preprocessing.crop_gears import GearIconCropper
from ..library.analyzers.preprocessing.crop_gears import _ExistsDetecter

ASSET_FOLDER = 'code/unit_tests/assets_for_test/library/analyzers/preprocessing/crop_gears/'

class TestGearIconCropper(TestCase):
    """GearIconCropperクラス"""
    def test_full_crop(self):
        """ギアが12個あるカスタマイズ画面のスクショから切り分けてそれぞれ保存できるか"""
        source_path = Path(ASSET_FOLDER + 'GearIconCropper/crop/full.jpg')
        mat = cv2.imread(str(source_path))
        cropper = GearIconCropper(mat)

        dest_path = Path(ASSET_FOLDER + 'GearIconCropper/crop/result/')
        cropper.crop(str(dest_path), source_path.stem)

        # cropの後に12枚の画像が保存されていれば成功
        files = list(dest_path.glob('*.jpg'))
        expected_num = 12
        self.assertEqual(len(files), expected_num)

        # 終わったら、生成した画像を削除する
        for del_file in files:
            del_file.unlink()

    def test_few_crop(self):
        """ギアが12個未満のカスタマイズ画面のスクショから切り分けて保存できるか"""
        source_path = Path(ASSET_FOLDER + 'GearIconCropper/crop/few_7.jpg')
        mat = cv2.imread(str(source_path))
        cropper = GearIconCropper(mat)

        dest_path = Path(ASSET_FOLDER + 'GearIconCropper/crop/result/')
        cropper.crop(str(dest_path), source_path.stem)

        # cropの後に7枚の画像が保存されていれば成功
        files = list(dest_path.glob('*.jpg'))
        expected_num = 7
        self.assertEqual(len(files), expected_num)

        # 終わったら、生成した画像を削除する
        for del_file in files:
            del_file.unlink()

    def test_cut(self):
        """カスタマイズ画面のスクショからギアを1着ずつ切り出せるか"""
        tops = [101, 232, 364]
        bottoms = [218, 349, 481]
        lefts = [136, 259, 377, 491]
        rights = [249, 372, 490, 604]
        source_path = Path(ASSET_FOLDER + 'GearIconCropper/cut/a.jpg')
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

class TestExistsDetecter(TestCase):
    """_ExistsDetecterクラス"""
    def test_find_gear(self):
        """切り出した画像にギアが含まれる場合にTrue"""
        source_path = Path(ASSET_FOLDER + 'ExistsDetecter/a.jpg')
        cropper = GearIconCropper(cv2.imread(str(source_path)))
        cutted = cropper._get_cutted_image(0, 0)

        self.assertTrue(_ExistsDetecter().include_gear_image(cutted))

    def test_miss_gear(self):
        """切り出した画像にギアが存在しない場合にFalse"""
        source_path = Path(ASSET_FOLDER + 'ExistsDetecter/a.jpg')
        cropper = GearIconCropper(cv2.imread(str(source_path)))
        cutted = cropper._get_cutted_image(0, 1)

        self.assertFalse(_ExistsDetecter().include_gear_image(cutted))
