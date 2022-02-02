import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class AddChange(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI(args)

    def initUI(self, args):
        print(args)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('table.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Coffee')
        self.setFixedSize(self.size())
        self.changeBtn.clicked.connect(self.change)
        self.addBtn.clicked.connect(self.add)
        self.db = sqlite3.connect('cofee.sqlite')
        self.cur = self.db.cursor()
        self.a = self.cur.execute("""select * from info""").fetchall()
        for i in range(len(self.a)):
            self.a[i] = list(self.a[i])
            self.a[i][3] = self.cur.execute("""select Gg from ground_or_grains where Type = (?)""",
                                            (self.a[i][3],)).fetchone()[0]
        self.table.setColumnCount(7)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Степень обжарки', 'Молотый / В зернах', 'Вкус', 'Цена', 'Объем'])
        self.table.resizeColumnsToContents()
        self.view_table()

    def change(self):
        print('c')

    def add(self):
        print('a')

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
