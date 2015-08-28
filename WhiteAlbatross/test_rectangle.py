# encoding: utf8
from unittest import TestCase

from PySide.QtCore import QPoint

from WhiteAlbatrossWidget import Rectangle


class TestRectangle(TestCase):
    def test_ctor(self):
        r = Rectangle(10, 20, 30, 40)
        self.assertEqual(r.p1, QPoint(10, 20))
        self.assertEqual(r.p2, QPoint(30, 40))

        r = Rectangle(QPoint(30, 40), QPoint(50, 60))
        self.assertEqual(r.p1, QPoint(30, 40))
        self.assertEqual(r.p2, QPoint(50, 60))

        r = Rectangle(p1=QPoint(60, 70), p2=QPoint(80, 90))
        self.assertEqual(r.p1, QPoint(60, 70))
        self.assertEqual(r.p2, QPoint(80, 90))

        r = Rectangle(x1=110, y1=120, x2=130, y2=140)
        self.assertEqual(r.p1, QPoint(110, 120))
        self.assertEqual(r.p2, QPoint(130, 140))

        r = Rectangle(figure={'x1': 100, 'y1': 110, 'x2': 120, 'y2': 130})
        self.assertEqual(r.p1, QPoint(100, 110))
        self.assertEqual(r.p2, QPoint(120, 130))

    def test_getDict(self):
        r = Rectangle(QPoint(10, 20), QPoint(30, 40))
        self.assertEqual(r.getDict(), {'rect': {'x1': 10, 'y1': 20, 'x2': 30, 'y2': 40}})
