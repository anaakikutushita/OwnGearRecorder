# coding: utf-8
"""このファイルを実行すれば、全ての処理が完結するようにプログラムする"""
import sys
sys.path.append('code/library/importers')
sys.path.append('code/library/analyzers/preprocessing')
sys.path.append('code/library/analyzers/main_process')

from pathlib import Path
import cv2
import import_image as Importer
import resize_image as Resizer
import classify_image as Classifier
import crop_gears as Cropper
import identify_gears_name as Identifier

def main():
    """entry point"""

    #ゲーム画面のスクショが溜まっているフォルダから、全ての画像を取り込む
    _input_folder = 'images/temp/input/'
    orig_mat_list = Importer.ImageImporter(_input_folder).get_mat_list()

    #スクショのキャンバスサイズが揃っていないと処理できないので、統一する
    resized_mat_list = Resizer.ImageResizer().get(orig_mat_list)

    #スクショをアタマ/フク/クツに分類し、対応する部位のフォルダ内に画像ファイルを書き出す
    classifier = Classifier.GearPartClassifier(resized_mat_list)
    # 保存先のフォルダもmain_systemから指定できるようにした方がいいと思う
    classifier.write_image_file_in_each_folder()

    #分類した画像をそれぞれ1個ずつのギアの画像に切り分けて一時保存
    _output_folder = 'images/temp/output/'
    _parts = ['Body', 'Foot', 'Head']
    for part in _parts:
        customize_mats = Importer.ImageImporter(_output_folder + part + '/').get_mat_list()
        for index, img in enumerate(customize_mats):
            cropper = Cropper.GearIconCropper(img)
            cropper.crop(_output_folder + part + '/cutted/', str(index))

    #切り分けた画像から、ギアそのものだけが映っている上半分の画像を抽出する
    for part in _parts:
        only_gear_mats = Importer.ImageImporter(_output_folder + part + '/cutted/').get_mat_list()
        top = 0
        gear_image_bottom = 79
        left = 0
        for index, img in enumerate(only_gear_mats):
            upper_half = img[top:gear_image_bottom, left:img.shape[1]]
            cv2.imwrite(_output_folder + part + '/OnlyGear/' + str(index) + '.jpg', upper_half)

    #標本のヒストグラムを取得
    gear_hist = Identifier.GearHist()
    hists_dic = gear_hist.get_all_dict()

    #抽出した画像と標本を比較して、ギアの名前を特定する


    #切り分けた画像から、ギアパワーの部分の画像を抽出する

    #抽出した画像から、基本ギアパワーと追加ギアパワーを特定する

    #特定に使用した画像・部位・ギア名・基本ギアパワー・追加ギアパワー1,2,3のデータを登録する

    #特定できなかったギアや、誤認識が起こったデータの中身は簡単に修正できるようにしたい

if __name__ == '__main__':
    main()
