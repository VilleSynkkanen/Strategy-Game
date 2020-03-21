import sys
from PyQt5.QtWidgets import QApplication
from pelinohjain import Pelinohjain

def main():

    global app
    app = QApplication(sys.argv)
    pelinojain = Pelinohjain()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()