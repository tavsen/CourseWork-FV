import sys
from unittest import TestCase
from unittest.mock import MagicMock

from PyQt5 import QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from Facade import Facade
from gui import MainWindow, DialogInput, DialogDelete


class FunctionalTest(TestCase):
    def setUp(self):
        self.qapp = QApplication(sys.argv)
        self.facade = Facade('DB_test.db')
        self.window = MainWindow(self.facade)

    def test_add(self):
        btn_add = self.window.ui.btn_add
        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)     # открываем диалоговое окно, нажав на кнопку
        for window in self.qapp.topLevelWidgets():      # возвращает список ссылок на все открытые окна (главное и диалоговые окна (при чем каждый раз в разном порядке))
            if isinstance(window, DialogInput):     # проверяем принадлежит ли открытое окно классу DialogInput
                dialog = window
                break
        else:
            self.fail()

        self.facade.insert_value(1)    # записываем данные в поля
        QTest.mouseClick(dialog.btn_insert, QtCore.Qt.MouseButton.LeftButton)       # и пытаемся их добавить, нажав на кнопку

        self.facade.insert_value(2)
        QTest.mouseClick(dialog.btn_insert, QtCore.Qt.MouseButton.LeftButton)

        self.window.draw_el = MagicMock()
        self.facade.insert_value(3)
        QTest.mouseClick(dialog.btn_insert, QtCore.Qt.MouseButton.LeftButton)
        self.window.draw_el.assert_called()

        self.facade.insert_value(4)
        self.facade.insert_value = MagicMock()
        QTest.mouseClick(dialog.btn_insert, QtCore.Qt.MouseButton.LeftButton)

    def test_delete(self):
        self.facade.insert_value(123)
        btn_delete = self.window.ui.btn_delete
        QTest.mouseClick(btn_delete, QtCore.Qt.MouseButton.LeftButton)
        for window in self.qapp.topLevelWidgets():
            if isinstance(window, DialogDelete):
                dialog = window
                break
        else:
            self.fail()

        self.facade.delete_value(123)
        self.facade.delete_value = MagicMock()
        QTest.mouseClick(dialog.btn_remove, QtCore.Qt.MouseButton.LeftButton)
        self.facade.delete_value(10)

        self.facade.insert_value(1)
        self.facade.insert_value(2)
        self.facade.insert_value(3)

        QTest.mouseClick(dialog.btn_remove_all, QtCore.Qt.MouseButton.LeftButton)

        message_box = self.qapp.activeModalWidget()
        if message_box is None:
            self.fail()

    def test_save(self):
        btn_save = self.window.ui.btn_save
        self.facade.insert_value(12)

        self.facade.DB.save_all = MagicMock()
        QTest.mouseClick(btn_save, QtCore.Qt.MouseButton.LeftButton)
        self.facade.DB.save_all.assert_called()


    def tearDown(self) -> None:   # закрывает окно после остановки проекта
        self.qapp.deleteLater()


if __name__ == '__main__':
    pass