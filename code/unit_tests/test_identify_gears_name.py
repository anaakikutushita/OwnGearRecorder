# coding: utf-8
"""unittest of identify_gears_name.py"""

from unittest import TestCase
from pathlib import Path
from ..library.analyzers.main_process.identify_gears_name import GearHist

class TestGearHist(TestCase):
    """GearHist"""
    def test_get(self):
        """ギアの見本画像からヒストグラムを計算して取得できるか。
        ヒストグラムそのものの検証はできないので、個数を確認する"""
        models_path = Path('images/original_model')
        models_num = len(list(models_path.glob('*.png')))

        num = len(GearHist().get())
        self.assertEqual(num, models_num)
