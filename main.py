import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget, QLineEdit, QComboBox, \
    QDoubleSpinBox, QDialog, QMessageBox
from PyQt5 import uic
import authorization
import currency_converter
import setuptools


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('main.ui', self)
        self.show()

        # login page
        self.login_page = self.findChild(QWidget, 'login_widget')
        self.main_content = self.findChild(QWidget, 'currency_converter_widget')

        self.login_button = self.findChild(QPushButton, 'login_button')
        self.login_button.clicked.connect(self.login)

        self.username_input = self.findChild(QLineEdit, 'username_input')
        self.password_input = self.findChild(QLineEdit, 'password_input')

        # main page
        self.from_combo = self.findChild(QComboBox, 'from_combo')
        self.to_combo = self.findChild(QComboBox, 'to_combo')
        self.from_amount = self.findChild(QDoubleSpinBox, 'from_amount')
        self.to_amount = self.findChild(QLineEdit, 'to_amount')

        self.convert_button = self.findChild(QPushButton, 'convert_button')
        self.convert_button.clicked.connect(self.convert)

        self.swap_button = self.findChild(QPushButton, 'swap_button')
        self.swap_button.clicked.connect(self.swap)
        self.logout_button = self.findChild(QPushButton, 'logout_button')
        self.logout_button.clicked.connect(self.logout)

        self.stackedWidget.setCurrentWidget(self.login_page)

    def init_main(self):
        self.from_combo.setCurrentIndex(self.from_combo.findText('USD'))
        self.to_combo.setCurrentIndex(self.to_combo.findText('GEL'))
        self.from_amount.setValue(1)
        self.to_amount.setText(str(currency_converter.convert(
            self.from_combo.currentText(),
            self.to_combo.currentText(),
            float(self.from_amount.text().replace(',', '.')))).replace('.', ',')
                               )

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if authorization.authorize(username, password):
            self.stackedWidget.setCurrentWidget(self.main_content)
            self.init_main()
        else:
            self.password_input.clear()
            dialog = QMessageBox(self)
            dialog.setText('incorrect username or password')

            dialog.exec_()

    def convert(self):
        amount = float(self.from_amount.text().replace(',', '.'))
        from_currency = self.from_combo.currentText()
        to_currency = self.to_combo.currentText()
        result = currency_converter.convert(from_currency, to_currency, amount)

        if result == -1:
            dialog = QMessageBox(self)
            dialog.setText('error in network')
            dialog.exec_()
        else:
            self.to_amount.setText(str(result).replace('.', ','))

    def swap(self):
        current_from_currency = self.from_combo.currentText()
        current_to_currency = self.to_combo.currentText()

        current_from_amount = self.from_amount.text()
        current_to_amount = self.to_amount.text()

        self.from_combo.setCurrentIndex(self.from_combo.findText(current_to_currency))
        self.to_combo.setCurrentIndex(self.to_combo.findText(current_from_currency))

        self.from_amount.setValue(float(current_to_amount.replace(',', '.')))
        self.to_amount.setText(str(current_from_amount))

    def logout(self):
        self.stackedWidget.setCurrentWidget(self.login_page)
        self.username_input.clear()
        self.password_input.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec_())
