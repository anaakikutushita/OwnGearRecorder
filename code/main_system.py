# coding: utf-8
"""このファイルを実行すれば、全ての処理が完結するようにプログラムする"""

import cv2
import library.importers.import_image as Importer
import library.analyzers.preprocessing.resize_image as Resizer
import library.analyzers.preprocessing.classify_image as Classifier
import library.analyzers.preprocessing.crop_gears as Cropper

def main():
    """entry point"""

    #ゲーム画面のスクショが溜まっているフォルダから、全ての画像を取り込む
    _source_folder = '../temp_images/source/'
    orig_mat_list = Importer.ImageImporter(_source_folder).get_mat_list()

    #スクショのキャンバスサイズが揃っていないと処理できないので、統一する
    resized_mat_list = Resizer.ImageResizer().get(orig_mat_list)

    #スクショをアタマ/フク/クツに分類し、対応する部位のフォルダ内に画像ファイルを書き出す
    classifier = Classifier.GearPartClassifier(resized_mat_list)
    classifier.write_image_file_in_each_folder()

    #分類した画像をそれぞれ1個ずつのギアの画像に切り分けて一時保存
    _result_folder = '../images/temp/result/'
    _parts = ['body', 'foot', 'head']
    for part in _parts:
        customize_mats = Importer.ImageImporter(_result_folder + part + '/').get_mat_list()
        for index, img in enumerate(customize_mats):
            cropper = Cropper.GearIconCropper(img)
            cropper.crop(_result_folder + part + '/cutted/', str(index))

    #切り分けた画像から、ギアそのものだけが映っている上半分の画像を抽出する
    for part in _parts:
        only_gear_mats = Importer.ImageImporter(_result_folder + part + '/cutted/').get_mat_list()
        top = 0
        gear_image_bottom = 79
        left = 0
        for index, img in enumerate(only_gear_mats):
            upper_half = img[top:gear_image_bottom, left:img.shape[1]]
            cv2.imwrite(_result_folder + part + '/OnlyGear/' + str(index) + '.jpg', upper_half)

    #標本画像を用意する

    #抽出した画像と標本画像を比較して、ギアの名前を特定する

    #切り分けた画像から、ギアパワーの部分の画像を抽出する

    #抽出した画像から、基本ギアパワーと追加ギアパワーを特定する

    #特定に使用した画像・部位・ギア名・基本ギアパワー・追加ギアパワー1,2,3のデータを登録する

    #特定できなかったギアや、誤認識が起こったデータの中身は簡単に修正できるようにしたい

if __name__ == '__main__':
    main()
