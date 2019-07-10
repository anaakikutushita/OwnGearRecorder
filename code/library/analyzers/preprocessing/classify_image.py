# coding: utf-8
"""Classify the customize scene image into one of three types: Body, Foot, Head."""

import cv2

class GearPartClassifier():
    """
    カスタマイズ画面のスクショをアタマ・フク・クツのいずれかに分類する
    """
    def __init__(self, mat_list):
        self._mat_list = mat_list

    def write_image_file_in_each_folder(self):
        """
        カスタマイズ画面の画像がアタマ・フク・クツのいずれかであると特定したあと、
        対応するフォルダに画像ファイルとして書き出す
        """
        for index, mat in enumerate(self._mat_list):
            detecter = _GearPartDetecter(mat)
            part = detecter.detect()
            cv2.imwrite("../ResultImage/" + part + "/" + str(index) + ".jpg", mat)

class _GearPartDetecter():
    """
    カスタマイズ画面の画像には「アタマ」「フク」「クツ」の文字を含む領域が存在する。
    画像からその領域だけを切り出して、あらかじめ用意した「アタマ」「フク」「クツ」の文字の画像と一致するかどうかという観点でギアの部位を特定する。
    """
    def __init__(self, customize_scene_mat):
        self._mat = customize_scene_mat
        self._detect_region_left = 399
        self._detect_region_right = 813
        self._detect_region_top = 526
        self._detect_region_bottom = 582
        self._thresh_value = 240
        self._max_value = 255

        self._permit_black_ratio = 0.01

        self._mask_image_body_path = "../../../images/mask_model/body.jpg"
        self._mask_image_foot_path = "../../../images/mask_model/foot.jpg"
        self._mask_image_head_path = "../../../images/mask_model/head.jpg"

        self._part_of_body = ["Body", "Foot", "Head", "Unknown"]

    def detect(self):
        """
        画像の部位を示す文字列を返す
        """
        #決定に必要な部分の画像を切り出す
        detect_sample = self._mat[self._detect_region_top:self._detect_region_bottom,
                                  self._detect_region_left:self._detect_region_right]

        #グレースケール化→スレッショルドフィルタをかけて白黒2値の画像を取得
        gray = cv2.cvtColor(detect_sample, cv2.COLOR_BGR2GRAY)
        #thresholdだけが欲しいんだけど、それだけを取得する方法を知らないので、使わないretも取得してしまっている
        ret, threshold = cv2.threshold(gray, self._thresh_value, self._max_value, cv2.THRESH_BINARY)

        #マスク画像を加算する
        loader = _Cv2ImageLoader()
        mask_body = loader.load_gray(self._mask_image_body_path)
        mask_foot = loader.load_gray(self._mask_image_foot_path)
        mask_head = loader.load_gray(self._mask_image_head_path)
        # 切り出した画像がアタマだった場合、予め用意した「アタマ」画像を加算すれば、加算後は全てのピクセルが白いピクセルになるはず。
        # 逆にアタマではなかった場合、どこかのピクセルが黒いまま残る。
        masked_body = cv2.add(threshold, mask_body)
        masked_foot = cv2.add(threshold, mask_foot)
        masked_head = cv2.add(threshold, mask_head)
        masked_group = [masked_body, masked_foot, masked_head]

        # masked_***の3つのmatのうち、どれが全て白ピクセルだったかを判定。
        # 例えばmasked_headが全て白ピクセルだった場合は、切り出す前のカスタマイズ画面のスクショはアタマギアのものということになる。
        determiner = _MatColorDeterminer()
        for index, masked_image in enumerate(masked_group):
            if determiner.is_almost_white(masked_image, self._permit_black_ratio):
                return self._part_of_body[index]

        #どの部位でもなかった場合の処理を一応書いておく
        return self._part_of_body[3]

class _Cv2ImageLoader():
    """
    何かひと手間加えてcv2.readしたいときのクラス
    """
    def load_gray(self, image_path):
        """
        パスからグレースケール化したmatを返す
        """
        return cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)

class _MatColorDeterminer():
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

        for h_pixels in range(height):
            for w_pixels in range(width):
                if target_mat[h_pixels][w_pixels] < 32:
                    black_pixels.append(target_mat[h_pixels][w_pixels])
        #画像が全て白になっている場合、その部位であると決定
        return len(black_pixels) / (height * width) < threshold
