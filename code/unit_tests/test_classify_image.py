# coding: utf-8
"""unittest of classify_image.py"""

from unittest import TestCase
from pathlib import Path
import cv2
from ..library.analyzers.preprocessing.classify_image import GearPartClassifier
from ..library.analyzers.preprocessing.classify_image import _GearPartDetecter
from ..library.analyzers.preprocessing.classify_image import _Cv2ImageLoader
from ..library.analyzers.preprocessing.classify_image import _MatColorDeterminer

ASSET_FOLDER = 'code/unit_tests/assets_for_test/library/analyzers/preprocessing/classify_image/'

class TestGearClassifier(TestCase):
    """GearClassifierクラス"""
    def test_write_file(self):
        """複数のカスタマイズ画面のスクショをそれぞれの部位のフォルダに振り分けることができるか"""
        test_times_by_parts = 2
        # アタマ・フク・クツの画像を2枚ずつ取得する
        source_path = Path(ASSET_FOLDER + 'GearClassifier/')
        mats = []
        for img_file in list(source_path.glob('*.jpg')):
            mats.append(cv2.imread(str(img_file)))

        # 取得したmatを放り込む
        classifier = GearPartClassifier(mats)
        classifier.write_image_file_in_each_folder()

        # それぞれのフォルダに2枚ずつ入っていることを確認する
        no_bugs = True
        result_folder = Path('images/temp/result')
        for part_folder in result_folder.iterdir():
            if not part_folder.is_dir():
                continue
            files = list(part_folder.glob('*.jpg'))
            no_bugs = len(files) == test_times_by_parts
            # 2枚入ってないフォルダが見つかった場合、その時点でテスト失敗とする。
            if not no_bugs:
                break

        self.assertTrue(no_bugs)

        # それぞれのフォルダから放り込んだ画像を削除する
        for result_files in list(result_folder.glob('**/*.jpg')):
            result_files.unlink()

class TestGearPartDetecter(TestCase):
    """GearPartDetecterクラス"""
    def test_detect_head(self):
        """カスタマイズ画面のスクショがアタマギア一覧を表示していると特定する"""
        source_path = str(Path(ASSET_FOLDER + 'GearPartDetecter/head.jpg'))
        mat = cv2.imread(source_path)
        result = _GearPartDetecter(mat).detect()
        self.assertEqual(result, 'Head')

    def test_detect_body(self):
        """カスタマイズ画面のスクショがフクギア一覧を表示していると特定する"""
        source_path = str(Path(ASSET_FOLDER + 'GearPartDetecter/body.jpg'))
        mat = cv2.imread(source_path)
        result = _GearPartDetecter(mat).detect()
        self.assertEqual(result, 'Body')

    def test_detect_foot(self):
        """カスタマイズ画面のスクショがクツギア一覧を表示していると特定する"""
        source_path = str(Path(ASSET_FOLDER + 'GearPartDetecter/foot.jpg'))
        mat = cv2.imread(source_path)
        result = _GearPartDetecter(mat).detect()
        self.assertEqual(result, 'Foot')

    def test_detect_unknown(self):
        """解像度だけ一致している黒色画像を入力する"""
        source_path = str(Path(ASSET_FOLDER + 'GearPartDetecter/Unknown.jpg'))
        mat = cv2.imread(source_path)
        result = _GearPartDetecter(mat).detect()
        self.assertEqual(result, 'Unknown')

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

    def test_gray(self):
        """既にグレースケール化が済んでいる、白い画像を渡す"""
        path = str(Path(ASSET_FOLDER + 'MatColorDeterminer/white.jpg'))
        mat = cv2.imread(path)
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
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
