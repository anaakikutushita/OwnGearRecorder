# coding: utf-8
"""align to the same resolution before analyzing the image"""

from pathlib import Path
import cv2

class ImageResizer():
    """決まった解像度に画像を拡縮する"""
    def __init__(self):
        self.sys_resolution_x = 1280
        self.sys_resolution_y = 720

    def get(self, mat_list):
        """
        Matオブジェクトのリストを受け取り、それら全てをシステム用の決め打ち解像度に拡縮して、リストとして返す
        """
        resized_mat_list = []

        resizer = _MatResizer()
        for image in mat_list:
            #720pに拡縮する
            resized_image = resizer.resize(image, self.sys_resolution_x, self.sys_resolution_y)
            resized_mat_list.append(resized_image)

        return resized_mat_list

class _MatResizer():
    """
    Matオブジェクトを拡縮する
    """
    def resize(self, target_mat, after_resized_x, after_resized_y):
        """
        cv2.resizeの使い方を勘違いしてハマったことがあったので、二度とハマらないように専用クラスを作った。なくてもいい
        """
        return cv2.resize(target_mat, (after_resized_x, after_resized_y))

# def test():
#     """テストでコケたときにいじくりまわすスペース"""
    
#     pass

# if __name__ == '__main__':
#     test()
