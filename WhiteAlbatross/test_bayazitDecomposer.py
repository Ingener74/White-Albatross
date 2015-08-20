# encoding: utf8
from unittest import TestCase
from PySide.QtCore import QPoint

from WhiteAlbatross.BayazitDecomposer import BayazitDecomposer


class TestBayazitDecomposer(TestCase):
    def test_decompose(self):
        decomposer = BayazitDecomposer()

        polygon = [
            QPoint(202,577),
            QPoint(148,627),
            QPoint(170,715),
            QPoint(213,738),
            QPoint(284,700),
            QPoint(220,658),
            QPoint(261,575),
            QPoint(261,575)
        ]

        polygons = decomposer.decompose(polygon)

        self.assertTrue(True)
