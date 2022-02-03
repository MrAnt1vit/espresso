import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class AddChange(QWidget):
    def __init__(self, main, title):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI(main, title)

    def initUI(self, main, title):
        self.setWindowTitle(title)
        self.fl = False
        self.saveBtn.clicked.connect(self.save)
        self.main = main
        if title == 'Изменить элемент':
            self.set_text()
            self.fl = True

    def set_text(self):
        self.name.setText(self.main.out[0])
        self.degree.setText(self.main.out[1])
        if self.main.out[2] == 'False':
            self.truefalse.setCurrentIndex(1)
        self.taste.setText(str(self.main.out[3]))
        self.price.setText(str(self.main.out[4]))
        self.sz.setText(str(self.main.out[5]))

    def save(self):
        if self.name.text() == '' or self.degree.text() == '' or self.taste.text() == '' \
                or self.price.text() == '' or self.sz.text() == '' or not self.price.text().isdigit() \
                or not self.sz.text().isdigit():
            return
        self.main.out[0] = self.name.text()
        self.main.out[1] = self.degree.text()
        self.main.out[2] = \
            self.main.cur.execute("""select Type from ground_or_grains where Gg = ?""",
                                  (self.truefalse.currentText(),)).fetchone()[0]
        self.main.out[3] = self.taste.text()
        self.main.out[4] = int(self.price.text())
        self.main.out[5] = int(self.sz.text())
        if not self.fl:
            self.main.add()
        else:
            self.main.change()
        self.close()


class Main(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('table.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Coffee')
        self.setFixedSize(self.size())
        self.changeBtn.clicked.connect(self.change_window)
        self.addBtn.clicked.connect(self.add_window)
        self.table.cellClicked.connect(self.set_id)
        self.out = ['', '', 0, '', '', '']
        self.id = -1
        self.db = sqlite3.connect('cofee.sqlite')
        self.cur = self.db.cursor()
        self.a = self.cur.execute("""select * from info""").fetchall()
        for i in range(len(self.a)):
            self.a[i] = list(self.a[i])
            self.a[i][3] = self.cur.execute("""select Gg from ground_or_grains where Type = (?)""",
                                            (self.a[i][3],)).fetchone()[0]
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Степень обжарки', 'Молотый / В зернах', 'Вкус', 'Цена', 'Объем'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.resizeColumnsToContents()
        self.view_table()

    def set_id(self, x, y):
        self.output.setText("")
        self.id = int(self.table.item(x, 0).text())

    def add_window(self):
        self.wind = AddChange(self, "Добавить элемент")
        self.wind.show()

    def add(self):
        self.id = list(self.cur.execute("""SELECT id FROM info order by id""").fetchall())[-1][
                      0] + 1
        self.cur.execute(
            """insert into info (ID, Name, Degree_of_roast, Gg, Description, Price, Size)
            values (?, ?, ?, ?, ?, ?, ?)""",
            (self.id, *self.out))
        self.a = list(self.cur.execute("""SELECT * FROM info""").fetchall())
        for i in range(len(self.a)):
            self.a[i] = list(self.a[i])
            self.a[i][3] = self.cur.execute("""select Gg from ground_or_grains where Type = (?)""",
                                            (self.a[i][3],)).fetchone()[0]
        self.db.commit()
        self.view_table()
        self.id = -1

    def change_window(self):
        if self.id == -1:
            self.output.setText("Выберите ячейку")
            return
        self.out = list(self.cur.execute("""SELECT Name, Degree_of_roast, Gg, Description, Price, Size FROM info where ID = ?""", (self.id, )).fetchone())
        self.wind = AddChange(self, 'Изменить элемент')
        self.wind.show()

    def change(self):
        self.cur.execute(
            """update info set Name = ?, Degree_of_roast = ?, Gg = ?, Description = ?, Price = ?, Size = ? where id = ?""", (*self.out, self.id))
        self.a = list(self.cur.execute("""SELECT * FROM info""").fetchall())
        self.db.commit()
        self.view_table()
        self.id = -1

    def view_table(self):
        self.table.setRowCount(0)
        for i in range(len(self.a)):
            self.table.setRowCount(self.table.rowCount() + 1)
            self.a[i] = list(self.a[i])
            for j in range(len(self.a[i])):
                self.a[i][j] = str(self.a[i][j])
                self.table.setItem(i, j, QTableWidgetItem(str(self.a[i][j])))
                self.table.item(i, j).setFlags(Qt.ItemIsEnabled)
        self.table.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
