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
    cv2.resizeの使い方を勘違いしてハマったことがあったので、二度とハマらないように専用クラスを作った。なくてもいい
    """
    def resize(self, target_mat, after_resized_x, after_resized_y):
        """
        Matオブジェクトを拡縮する
        """
        return cv2.resize(target_mat, (after_resized_x, after_resized_y))
    """
    Matオブジェクトの色を判定する。
    本システムでは現状、白色の画素だけで構成されているかどうかのチェックにのみ使用。
    """
    def is_almost_white(self, target_mat, threshold):
        """
        渡されたMatオブジェクトが、全て白いピクセルだけで出来ていればTrueを返す。
        ただし、thresholdの割合だけは黒いピクセルが含まれていても許容範囲とする。
        """
        height = target_mat.shape[0]
        width = target_mat.shape[1]
        black_pixels = []

        # 白か黒かの判定なので、グレースケール化する。既にグレースケール化されてる場合は再度処理しない（エラーになる）
        is_color = len(target_mat.shape) == 3
        if is_color:
            target_mat = cv2.cvtColor(target_mat, cv2.COLOR_BGR2GRAY)

        # 値がゼロに近いほど、黒っぽい色。0～255。32という数値は適当に決めた
        barely_white_value = 32

        for h_pixel in range(height):
            for w_pixel in range(width):
                if target_mat[h_pixel][w_pixel] < barely_white_value:
                    black_pixels.append(target_mat[h_pixel][w_pixel])
        #画像が全て白になっている場合、その部位であると決定
        return len(black_pixels) / (height * width) < threshold

def test():
    """テストでコケたときにいじくりまわすスペース"""
    pass

if __name__ == '__main__':
    test()
