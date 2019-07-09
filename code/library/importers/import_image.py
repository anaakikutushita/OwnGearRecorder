# coding: utf-8
"""import image by using OpenCV"""

import glob
import cv2

class ImageImporter():
    """
    解析対象の画像を読み込む
    """
    def __init__(self, image_folder_path):
        #あとで、フォルダの区切り文字とか末尾の文字を揃える処理が必要になるはず
        #今のところは「スラッシュ1文字区切り」「フォルダパスの最後にスラッシュが入っている」条件で決め打ちする
        self._image_folder_path = image_folder_path

    def get_mat_list(self):
        """
        sourceフォルダに入っている全ての画像をMat型オブジェクトのリストとして返す。
        Switchのスクリーンショットの拡張子はjpg（デフォルト）の場合のみを考慮する。
        """
        image_file_path_list = glob.glob(self._image_folder_path + "*.jpg")

        img_list = []
        for image_file_path in image_file_path_list:
            orig_img = cv2.imread(image_file_path)
            img_list.append(orig_img)

        return img_list
