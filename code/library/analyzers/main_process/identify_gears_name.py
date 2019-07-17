# coding: utf-8
"""
Analyze the 12 gear images cut out from the customized screen image
and identify the name of each gear.
"""

from pathlib import Path
import cv2
import numpy as np

class GearHist():
    """見本となるギア画像のヒストグラムを取得する"""
    def get_all_dict(self):
        """ギアIDとndarrayの辞書形式で各ギア画像のヒストグラムを取得する"""
        models_path = Path('images/original_model')
        model_files = list(models_path.glob('*.png'))

        vecs_dict = {}
        for model_file in model_files:
            hist_vec = self.get_vec(model_file)
            vecs_dict[model_file.stem] = hist_vec

        return vecs_dict

    def get_vec(self, image_file_path: Path):
        """カラー画像ファイルを示すPathオブジェクトを受け取って、
        三原色それぞれのヒストグラムを計算して合成したベクトルを返す"""
        img = cv2.imread(str(image_file_path))

        # この辺はヒストグラム計算のために必要だから仕方なく書いてるやつ
        mask = None
        all_bins = [256]
        all_ranges = [0, 256]
        hist_bgr = []
        for channel in range(3):
            hist = cv2.calcHist([img], [channel], mask, all_bins, all_ranges)
            hist_bgr.append(hist)

        hist_array = np.array(hist_bgr)
        hist_vec = hist_array.reshape(hist_array.shape[0]*hist_array.shape[1], 1)

        return hist_vec

# def test():
#     """いろいろ試せるスペース"""

#     pass

# if __name__ == '__main__':
#     test()
