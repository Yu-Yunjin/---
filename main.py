import sys
import time

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QLabel, QTableWidgetItem
import log_in  # 导入QtTest文件
import error_one
import administrator
import create_user
import create_shelf
import create_book
import modify_book

import sql_search



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # 窗口初始化设置
        super(MainWindow, self).__init__()
        self.ui = log_in.Ui_MainWindow()
        self.ui.setupUi(self)

        # 声明子窗口
        self.administrator_window = AdministratorWindow()

    def signIn(self):  # 登录槽函数
        print("sign in")
        uid = self.ui.lineEdit.text()
        user_key = self.ui.lineEdit_2.text()
        sql = "select * from users WHERE uid = '" + uid + "'"
        # print(sql)
        data = sql_search.search_sql(sql)
        # print(data)
        if len(data) == 0:
            dialog = ErrorDialogOne()
            dialog.label.setText("请输入正确的用户名")
            dialog.label.setAlignment(QtCore.Qt.AlignCenter)
            dialog.exec_()
        elif data[0][1] == user_key:
            print("success")
            # 登录逻辑
            if data[0][2] == '管理员':
                self.administrator_window.ui.label_2.setText(str(uid))
                self.administrator_window.show()

            # else
        else:
            dialog = ErrorDialogOne()
            dialog.label.setText("用户名或密码错误")
            dialog.label.setAlignment(QtCore.Qt.AlignCenter)
            dialog.exec_()

    def signUp(self):  #注册槽函数
        print("sign up")
        # dialog = errorDialogOne()


class ErrorDialogOne(QtWidgets.QDialog, error_one.Ui_Dialog):
    def __init__(self, parent=None):
        super(ErrorDialogOne, self).__init__(parent)
        self.setupUi(self)

        # # Connect buttons to functions
        # self.pushButton_2.clicked.connect(self.ask_more)


class AdministratorWindow(QtWidgets.QMainWindow, administrator.Ui_MainWindow):
    def __init__(self):
        super(AdministratorWindow, self).__init__()
        self.ui = administrator.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label_5.setText(str(sql_search.getSum("book", "total_num")))
        self.ui.label_7.setText(str(sql_search.getSum("book", "total_num") - sql_search.getSum("book", "now_num")))
        self.ui.label_9.setText(str(sql_search.getCount("borrow_information", "statue", "审核中")))
        self.ui.label_11.setText(str(sql_search.getCount("borrow_information", "statue", "已逾期")))

        # 声明子窗口
        self.user_window = CreateUserWindow()
        self.shelf_window = CreateShelf()
        self.book_window = CreateBook()
        self.book_change_window = ModifyBook()

    # 槽函数
    def choose_page(self, index):
        if index == 0:
            self.ui.label_5.setText(str(sql_search.getSum("book", "total_num")))
            self.ui.label_7.setText(str(sql_search.getSum("book", "total_num") - sql_search.getSum("book", "now_num")))
            self.ui.label_9.setText(str(sql_search.getCount("borrow_information", "statue", "审核中")))
            self.ui.label_11.setText(str(sql_search.getCount("borrow_information", "statue", "已逾期")))
        elif index == 1:
            data = sql_search.search_sql("SELECT * FROM borrow_information WHERE statue = '审核中'")
            if len(data) > 0:
                self.ui.tableWidget.setRowCount(len(data))
                self.ui.tableWidget.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, item in enumerate(row):
                        table_item = QTableWidgetItem(str(item))
                        self.ui.tableWidget.setItem(i, j, table_item)

            # self.setCentralWidget(table_widget)


    def ac_borrow(self):
        selected_items = self.ui.tableWidget.selectedItems()
        items = selected_items[0].text()
        # print(items)
        sql_search.modify('borrow_information', 'tid', items, 'statue', '借阅中')

    def ask_uid(self):
        uid = self.ui.lineEdit.text()
        data = sql_search.search_sql("SELECT * FROM users WHERE uid = '" + uid + "'")
        if len(data) > 0:
            self.ui.tableWidget_2.setRowCount(len(data))
            self.ui.tableWidget_2.setColumnCount(len(data[0]))

            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table_item = QTableWidgetItem(str(item))
                    self.ui.tableWidget_2.setItem(i, j, table_item)

    def new_user(self):
        self.user_window.show()

    def delete_user(self):
        selected_items = self.ui.tableWidget_2.selectedItems()
        items = selected_items[0].text()
        # print(items)
        sql_search.delete_sth('users', 'uid', items)

    def ask_bid(self):
        bid = self.ui.lineEdit_2.text()
        data = sql_search.search_sql("SELECT * FROM book WHERE bid = '" + bid + "'")
        if len(data) > 0:
            self.ui.tableWidget_3.setRowCount(len(data))
            self.ui.tableWidget_3.setColumnCount(len(data[0]))

            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table_item = QTableWidgetItem(str(item))
                    self.ui.tableWidget_3.setItem(i, j, table_item)

    def new_book(self):
        self.book_window.show()

    def book_editor(self):
        bid = self.ui.lineEdit_2.text()
        self.book_change_window.ui.lineEdit_2.setText(bid)
        self.book_change_window.show()

    def ask_sid(self):
        sid = self.ui.lineEdit_3.text()
        data = sql_search.search_sql("SELECT * FROM bookshelf WHERE sid = '" + sid + "'")
        if len(data) > 0:
            self.ui.tableWidget_4.setRowCount(len(data))
            self.ui.tableWidget_4.setColumnCount(len(data[0]))

            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    table_item = QTableWidgetItem(str(item))
                    self.ui.tableWidget_4.setItem(i, j, table_item)

    def new_shelf(self):
        self.shelf_window.show()

    def shelf_editor(self):
        selected_items = self.ui.tableWidget_4.selectedItems()
        items = selected_items[0].text()
        # print(items)
        sql_search.delete_sth('bookshelf', 'sid', items)


class CreateUserWindow(QtWidgets.QMainWindow, create_user.Ui_MainWindow):
    def __init__(self):
        super(CreateUserWindow, self).__init__()
        self.ui = create_user.Ui_MainWindow()
        self.ui.setupUi(self)

    def create(self):
        uid = self.ui.lineEdit.text()
        key = self.ui.lineEdit_2.text()
        current_index1 = self.ui.comboBox.currentIndex()
        types = self.ui.comboBox.itemText(current_index1)
        sql = "INSERT INTO users (uid, user_key, user_type) VALUES('" + uid + "', '" + key + "', '" + str(types) +"')"
        sql_search.insert_sql(sql)


class CreateShelf(QtWidgets.QMainWindow, create_shelf.Ui_MainWindow):
    def __init__(self):
        super(CreateShelf, self).__init__()
        self.ui = create_shelf.Ui_MainWindow()
        self.ui.setupUi(self)

    def create(self):
        sid = self.ui.lineEdit.text()
        sql = "INSERT INTO bookshelf (sid, book_num) VALUES('" + sid + "', 0)"
        sql_search.insert_sql(sql)


class ModifyBook(QtWidgets.QMainWindow, modify_book.Ui_MainWindow):
    def __init__(self):
        super(ModifyBook, self).__init__()
        self.ui = modify_book.Ui_MainWindow()
        self.ui.setupUi(self)

    def change(self):
        bid = self.ui.lineEdit_2.text()
        ch = self.ui.lineEdit.text()
        current_index1 = self.ui.comboBox.currentIndex()
        col = self.ui.comboBox.itemText(current_index1)
        sql_search.modify('book', 'bid', bid, col, ch)


class CreateBook(QtWidgets.QMainWindow, create_book.Ui_MainWindow):
    def __init__(self):
        super(CreateBook, self).__init__()
        self.ui = create_book.Ui_MainWindow()
        self.ui.setupUi(self)

    def create(self):
        bid = self.ui.lineEdit.text()
        book_name = self.ui.lineEdit_2.text()
        author = self.ui.lineEdit_3.text()
        total_num = self.ui.lineEdit_4.text()
        sid = self.ui.lineEdit_5.text()
        book_price = self.ui.lineEdit_6.text()
        publishing = self.ui.lineEdit_7.text()
        sql = "INSERT INTO book (bid, book_name, author, total_num, now_num, sid, book_price, publishing) VALUES('" + bid + "', '" + book_name + "', '" + author + "', '" + total_num + "', '" + total_num + "', '" + sid + "', '" + book_price + "', '" + publishing +"')"
        sql_search.insert_sql(sql)


if __name__ == '__main__':
    # 获取UIC窗口操作权限
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # 显示窗口并释放资源
    window.show()
    sys.exit(app.exec_())
