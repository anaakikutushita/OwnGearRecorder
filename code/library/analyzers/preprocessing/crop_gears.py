# coding: utf-8
"""load image and split by gear icons."""

from enum import Enum
import cv2

class CustomizeScene(Enum):
    """
    カスタマイズ画面のスクショに含まれるギアの行と列を定義
    """
    rows = [0, 1, 2]
    columns = [0, 1, 2, 3]

class CutPositions(Enum):
    """
    12個のギア画像に切り分けるときの位置を定義。
    例えば2行・3列目のギア画像を切り分けるときは、
    tops[1], bottoms[1], lefts[2], rights[2]
    の領域で画像を切り分ける。
    """
    tops = [101, 232, 364]
    bottoms = [218, 349, 481]
    lefts = [136, 259, 377, 491]
    rights = [249, 372, 490, 604]

class GearIconCropper():
    """
    1枚のカスタマイズ画面のスクショから、12枚のギア画像を切り出す
    """
    def __init__(self, mat):
        self._mat = mat

    def crop(self, save_folder_path, orig_file_name):
        """
        一つ一つギアの画像を切り分けた後、指定したフォルダに画像ファイルとして書き出す
        """
        detecter = ExistsDetecter()
        for row in CustomizeScene.rows:
            for column in CustomizeScene.columns:
                cutted_image = self._get_cutted_image(row, column)
                if detecter.include_gear_image(cutted_image):
                    file_name = orig_file_name + "-cutted-" + row + column
                    cv2.imwrite(save_folder_path + file_name + ".jpg", cutted_image)

    def _get_cutted_image(self, row, column):
        """
        カスタマイズ画面のスクショから、指定した行と列の位置にある画像を切り出して返す
        """
        top = int(CutPositions.tops[row])
        bottom = int(CutPositions.bottoms[row])
        left = int(CutPositions.lefts[column])
        right = int(CutPositions.rights[column])

        gear_mat = self._mat[top:bottom, left:right]
        return gear_mat

class ExistsDetecter():
    """
    カスタマイズ画面の最後のページは、並んでいるギアが12個未満の場合がある。
    そのときに、12個に切り出した画像の中にギアが映っていないものを見分けるクラス。
    """
    def __init__(self):
        self._white_pixel_must_included_ratio = 0.05
        self._white_threshold_on_gear_image = 230

    def include_gear_image(self, target_cutted_image):
        """
        切り分けた画像の中にギアが含まれていればTrue
        """
        height = target_cutted_image.shape[0]
        width = target_cutted_image.shape[1]

        #ギアの有無を判別するロジックはどうやっていたのか中身の意味がわからなくなっちゃった
        gray = cv2.cvtColor(target_cutted_image, cv2.COLOR_BGR2GRAY)
        white_pixels = []
        for h_pixel in range(height):
            for w_pixel in range(width):
                if gray[h_pixel][w_pixel] > self._white_threshold_on_gear_image:
                    white_pixels.append(gray[h_pixel][w_pixel])

        ratio = len(white_pixels) / (height * width)
        return ratio > self._white_pixel_must_included_ratio
