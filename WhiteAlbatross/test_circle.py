# encoding: utf8
from unittest import TestCase
from PySide.QtCore import QPoint
from WhiteAlbatross import Circle

__author__ = 'pavel'


class TestCircle(TestCase):

    def test_ctor(self):
        c = Circle(10, 20, 30, 40)
        self.assertEqual(c.center, QPoint(10, 20))
        self.assertEqual(c.ctrl, QPoint(30, 40))

        c = Circle(QPoint(50, 60), QPoint(70, 80))
        self.assertEqual(c.center, QPoint(50, 60))
        self.assertEqual(c.ctrl, QPoint(70, 80))

        c = Circle(figure={'center': {'x': 90, 'y': 100}, 'ctrl': {'x': 110, 'y': 120}})
        self.assertEqual(c.center, QPoint(90, 100))
        self.assertEqual(c.ctrl, QPoint(110, 120))

        c = Circle(center=QPoint(10, 20), ctrl=QPoint(30, 40))
        self.assertEqual(c.center, QPoint(10, 20))
        self.assertEqual(c.ctrl, QPoint(30, 40))

    def test_get_dict(self):

        c = Circle(QPoint(10, 10), QPoint(20, 10))

        self.assertEqual(c.getDict(),
                         {
                             'circle':
                                 {
                                     'center':
                                         {
                                             'x': c.center.x(),
                                             'y': c.center.y()
                                         },
                                     'ctrl':
                                         {
                                             'x': c.ctrl.x(),
                                             'y': c.ctrl.y()
                                         }
                                 }
                         })
