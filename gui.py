from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QGraphicsScene, QMessageBox
from PyQt5 import uic
from Facade import Facade
import sys
import logging

logging.basicConfig(level=logging.INFO)
# logging.disable(logging.INFO)

#главное окно формы
class MainWindow(QMainWindow):
    """
    Данный класс создает главное окно
    """
    def __init__(self, facade):
        """
        Здесь загружается основное окно, прикрепляются действия к кнопкам (вызов функций) и отрисовывается дерево
        :param facade: ссылка на фасад
        """
        self.facade = facade
        super().__init__()
        self.ui = uic.loadUi("forms/main_menu.ui", self)
        self.window().setWindowTitle(
            "Реализация структуры данных - дерево Арне Андерсона.")
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.ui.canvas.setScene(self.scene)
        self.ui.btn_add.clicked.connect(self.open_dialog_input)
        self.ui.btn_delete.clicked.connect(self.open_dialog_delete)
        self.ui.btn_save.clicked.connect(lambda: self.facade.save_data())
        self.ui.btn_load.clicked.connect(lambda: self.facade.load_data(self))
        self.facade.update_datas.connect(self.update)
        self.draw_tree()

    def update(self) -> None:
        logging.log(logging.INFO, "update gui")
        self.draw_tree()

    def closeEvent(self, event):
        """
        Действия при закрытии основного окна (нажатие на крестик).
        Если есть несохраненные данные, то появится окно с вопросом о сохранении данных ("Хотите их сохранить?")
        :param event: ососбое действие
        :return: None
        """
        if self.facade.data_wait_for_save:
            logging.log(logging.INFO, ' есть несохраненные данные')
            if (QMessageBox.Yes == QMessageBox(QMessageBox.Information, "Есть несохраненные данные...",\
                                               "Сохранить исходные данные в базу данных?", \
                                               QMessageBox.Yes|QMessageBox.No).exec()):
                logging.log(logging.INFO, " данные сохранены")
                self.facade.save_data()
            else:
                logging.log(logging.INFO, " данные не сохранены")
        else:
            logging.log(logging.INFO, ' несохраненных данных нет')
        logging.log(logging.INFO, ' окно закрыто')

    #диалог на вставку элемента
    def open_dialog_input(self):
        """
        Данная функция для открытия диалогового окна ввода данных и установки заголовка окна
        :return: NONE
        """
        dialog = DialogInput(self.facade, self)
        dialog.setWindowTitle("Добавление данных")
        dialog.show()

    #на удаление
    def open_dialog_delete(self):
        """
        Данная функция для открытия диалогового окна удаления данных и установки заголовка окна
        :return: NONE
        """
        dialog = DialogDelete(self.facade, self)  # тут self. нужен для теста (чтобы можно было обратиться к dialog)
        dialog.setWindowTitle("Удаление данных")
        dialog.show()

    #отрисовка элемента дерева
    def draw_el(self, x, y, key, left=None, height=0):
        """
         отрисовка круга, текса (key, data) и линии (ветки)
         :param x: координата отрисовки элементов
         :param y: координата отрисовки элементов
         :param key: данные, которые нужно вывести
         :param left: левый это или правый элемнта в дереве (для отрисовки линии - ветки)
         :param height: высота ветки (если бы это был прямой треугольник)
         :return: None
                 """
        self.scene.addEllipse(x, y, 40, 40)

        long = len(str(key))
        text = self.scene.addText(f"{key}")
        text.moveBy(x + 17 - long * 3, y + 10)

        if left == 1:
            self.scene.addLine(x + 30, y - 5, x + self.branch_len + 15, y - height + 45)
        if left == 0:
            self.scene.addLine(x + 10, y - 5, x - self.branch_len + 25, y - height + 45)

    #отрисовка дерева
    def draw_tree(self):
        """
          Расчет координат элементов и передача их в draw_el
          :return: None
          """
        self.scene.clear()
        path = self.facade.get_tree()
        if path:
            x = 50 * (2 ** path[0]) + 50
            y = 150
            h = 50
            height = h * path[0] + h  # высота ветки (если бы это был прямой треугольник)
            self.branch_len = (x - 50) // 2  # ширина ветки (если бы это был прямой треугольник)
            layer = 0  # слой дерева
            frame_x = 0
            for val in range(1, path[0] + 2):
                frame_x += h * val
            self.scene = QGraphicsScene(0, 0, x * 2 + 100, frame_x + 300)
            logging.log(logging.INFO, f' размер холста - {x * 2 + 100}, {y * path[0] + 100}')
            self.ui.canvas.setScene(self.scene)
            if len(path) != 1:
                self.draw_el(x, y, path[1][0])
            for n in range(2, len(path)):
                if path[n][1] is not None:
                    y += height
                    layer += 1
                    if path[n - 1][0] > path[n][0]:  # значит этот элемент левее --> вычитаем
                        x -= self.branch_len
                        self.draw_el(x, y, path[n][0], 1, height)
                    else:  # значит этот элемент правее --> прибавляем
                        x += self.branch_len
                        self.draw_el(x, y, path[n][0], 0, height)
                    self.branch_len //= 2
                    height -= h
                else:  # возвращаемся назад
                    height += h
                    layer -= 1
                    y -= height
                    self.branch_len *= 2
                    if path[n - 1][0] < path[n][0]:
                        x += self.branch_len
                    else:
                        x -= self.branch_len



#диалог удаления
class DialogDelete(QDialog):
    """
    Класс для инициализации диалогового окна удаления данных
    """
    def __init__(self, facade, parent=None):
        """
        Здесь загружается диалоговое окно удаления данных и прописываются действия при нажатии на кнопки (вызов функций)
        :param facade: ссылка на объект класса Facade
        :param parent: ссылка на родительское окно
        """
        super(DialogDelete, self).__init__(parent)
        self.facade = facade
        self.ui = uic.loadUi("forms/delete.ui", self)
        self.ui.btn_remove.clicked.connect(self.delete)
        self.ui.btn_remove_all.clicked.connect(lambda: self.del_all())

    #удаление всего дерева
    def del_all(self):
        """
        Создание messagebox при нажатии кнопки "удалить все"
        :return: None
        """
        if self.facade.dictionary.root is not None:  # если есть данные для удаления
            self.messagebox_del_all = QMessageBox(self)
            self.messagebox_del_all.setWindowTitle("Удаление данных")
            self.messagebox_del_all.setText("Вы уверены, что хотите удалить все данные?")
            self.messagebox_del_all.setInformativeText("После сохранения данные будут утеряны!")
            self.messagebox_del_all.setIcon(QMessageBox.Question)
            self.messagebox_del_all.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            self.messagebox_del_all.buttonClicked.connect(self.action)
            self.messagebox_del_all.show()
        else:
            QMessageBox.warning(self, 'Удаление данных', "Данных для удаления нет", QMessageBox.Ok)

    #реакция на нажатие кнопки в форме
    def action(self, button):
        """
        При нажатии Ok в messagebox_del_all.
        Удаление данных из структуры данных.
        :param button: нажатая кнопка в messagebox_del_all
        :return: None
                """
        if button.text() == "OK":
            self.facade.del_all_from_tree()
            self.parent().draw_tree()
            logging.log(logging.INFO, 'данные удалены')
        else:
            logging.log(logging.INFO, 'данные не удалены')

    #удаление элемента из дерева
    def delete(self):
        """
    Действия при нажатии кнопки "Удалить".
    Удаляет элемент из структуры данных, если он существует
    :return: None
                """
        link = self.facade.delete_value(self.ui.data_input.text())  # ссылка на элемент, который удаляем
        if link is not None:
            try:
                self.ui.label_info.setText(f"Вы удалили: {self.ui.data_input.text()}")
                self.facade.delete_value(self.ui.data_input.text())
                self.parent().draw_tree()
            except RecursionError:
                self.ui.label_info.setText(f"Дерево слишком высокое!\nПопробуйте ввести элемент для другого поддерева.")

#диалог добавления
class DialogInput(QDialog):
    """
    Класс для инициализации диалогового окна ввода данных
    """
    def __init__(self, facade, parent=None):
        """
        Здесь загружается основное окно и прописываются действия при нажатии на кнопку (вызов функций)
        :param facade: ссылка на объект класса Facade
        :param parent: ссылка на родительское окно
        """
        self.facade = facade
        super(DialogInput, self).__init__(parent)
        self.ui = uic.loadUi("forms/input.ui", self)
        self.ui.btn_insert.clicked.connect(self.add)

    #вставка элемента в дерево
    def add(self):
        """
        действия при нажатии кнопки "Сохранить".
        Добавляет элемент в структуру данных, если он не существует
        :return: None
        """
        if self.ui.data_input.text() != '':
            try:
                self.facade.insert_value(self.ui.data_input.text())
                self.ui.label_info.setText(f"Вы ввели: {self.ui.data_input.text()}")
                self.parent().draw_tree()
            except RecursionError:
                self.ui.label_info.setText(f"Дерево слишком высокое!\nПопробуйте ввести элемент для другого поддерева.")
        elif self.ui.data_input.text() == '':
            self.ui.label_info.setText(f"Заполните поле!")
        else:
            self.ui.label_info.setText(f"Данный элемент уже существует!")
            self.parent().draw_tree() #поскольку делали поиск

#паттерн строитель
class Builder:
    """
    Это порождающий паттерн проектирования, который позволяет создавать сложные объекты пошагово.
    """
    def __init__(self):
        """
        Объявление переменных facade и gui
        """
        self.facade = None
        self.gui = None

    def create_facade(self):
        """
        Создание ссылки на объект фасада (Facade)
        :return: None
        """
        self.facade = Facade()

    def create_gui(self):
        """
        Создание ссылки на объект графики (MainWindow), если создана ссылка на фасад
        :return: None
        """
        if self.facade is not None:
            self.gui = MainWindow(self.facade)

    def get_result(self):
        """
        Получение ссылки на объект графики (MainWindow)
        :return: gui - ссылка на объект графики
        """
        if self.facade is not None and self.gui is not None:
            return self.gui

#вызов всех классов
if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    builder = Builder()
    builder.create_facade()
    builder.create_gui()
    window = builder.get_result()
    window.show()
    qapp.exec()
    qapp.exec()