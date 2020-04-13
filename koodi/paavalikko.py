from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from kenttaeditori import Kenttaeditori
from pelinohjain import Pelinohjain


class Paavalikko(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Paavalikko, self).__init__()

        self.setCentralWidget(QtWidgets.QWidget())  # QMainWindown must have a centralWidget to be able to add layouts
        self.__paa_layout = QtWidgets.QVBoxLayout()  # Vertical main layout
        self.centralWidget().setLayout(self.__paa_layout)

        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle('Strategiapeli')
        self.show()

        self.__pelaa_nappi = QtWidgets.QPushButton("PELAA")
        self.__pelaa_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__kenttaeditori_nappi = QtWidgets.QPushButton("KENTTÄEDITORI")
        self.__kenttaeditori_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__poistu_nappi = QtWidgets.QPushButton("POISTU")
        self.__poistu_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.__pelaa_nappi.setStyleSheet("font: 10pt Arial")
        self.__kenttaeditori_nappi.setStyleSheet("font: 10pt Arial")
        self.__poistu_nappi.setStyleSheet("font: 10pt Arial")

        # nappien yhdistäminen
        self.__pelaa_nappi.clicked.connect(self.__pelaa)
        self.__kenttaeditori_nappi.clicked.connect(self.__kenttaeditori)
        self.__poistu_nappi.clicked.connect(self.__poistu)

        # nappi widgetit
        self.__paa_layout.addWidget(self.__pelaa_nappi, 1)

        self.__paa_layout.addWidget(self.__kenttaeditori_nappi, 1)
        self.__paa_layout.addWidget(self.__poistu_nappi, 1)


    def __pelaa(self):
        self.pelinohjain = Pelinohjain()
        self.hide()

    def __kenttaeditori(self):
        self.kenttaeditori = Kenttaeditori()
        self.kenttaeditori.show()
        self.hide()

    def __poistu(self):
        pass
