from PyQt6 import QtWidgets
import sys
from start_page import StartPage

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open('styles.qss').read())
    start_page = StartPage()
    start_page.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
