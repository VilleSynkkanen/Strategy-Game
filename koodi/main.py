import sys
from PyQt5.QtWidgets import QApplication
from paavalikko import Paavalikko


def main():

    global app
    app = QApplication(sys.argv)
    paavalikko = Paavalikko()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
