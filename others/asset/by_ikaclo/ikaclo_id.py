# -*- coding: utf-8 -*-
"""イカクロが独自に定義するギアIDやギアパワーIDを利用できるようにする"""

import csv

# These two files are specified to be ignored by git.
GEAR_CSV_FILE = 'm_gears.csv'
GEAR_POWER_CSV_FILE = 'm_gear_powers.csv'

# 本プログラムで取り扱うスプラトゥーンシリーズ
TARGET_SPLATOON_VERSION = '2'

class DicGenerator(object):
    """ID辞書の親クラス"""
    def __init__(self, file_name):
        self._file_name = file_name

        # ikacloのid表CSVファイルにおいて、スプラトゥーンの対象バージョンが記載されている列番号
        self._version_column = 2

    def get(self):
        """CSVの1列目をキーに、2列目を値にした辞書オブジェクトを返す"""
        dic = {}
        with open(self._file_name, newline='', encoding='utf-8-sig') as csvfile:
            rows = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in rows:
                if row[self._version_column] == TARGET_SPLATOON_VERSION:
                    dic[row[0]] = row[1]
        return dic

class GearDic(DicGenerator):
    """イカクロで定義しているギアのIDと名前の辞書クラス"""
    def __init__(self):
        super().__init__(GEAR_CSV_FILE)

class GearPowerDic(DicGenerator):
    """イカクロで定義しているギアパワーのIDと名前の辞書クラス"""
    def __init__(self):
        super().__init__(GEAR_POWER_CSV_FILE)
