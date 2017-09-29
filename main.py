import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MyMainWindow


def main():
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()