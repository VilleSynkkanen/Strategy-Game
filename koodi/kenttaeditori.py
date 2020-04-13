from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import sys


class Kenttaeditori(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.__scene_size = 880       # kentän koko pikseleinä

        self.setCentralWidget(QtWidgets.QWidget())  # QMainWindown must have a centralWidget to be able to add layouts
        self.__paa_layout = QtWidgets.QHBoxLayout()  # Horizontal main layout
        self.centralWidget().setLayout(self.__paa_layout)

        # set window
        self.setGeometry(0, 0, self.__scene_size + 420, self.__scene_size)
        self.setWindowTitle('Kenttäeditori')
        self.show()

        # Add a scene for drawing 2d objects
        self.__scene = QtWidgets.QGraphicsScene()

        # Add a view for showing the scene
        self.__nakyma = QtWidgets.QGraphicsView(self.__scene, self)
        self.__nakyma.adjustSize()
        self.__nakyma.show()
        self.__paa_layout.addWidget(self.__nakyma)
        # main_layout.addStretch()

        self.__nappi_layout = QtWidgets.QGridLayout()
        self.__paa_layout.addLayout(self.__nappi_layout)

        # napit
        self.__hyokkaa_nappi = QtWidgets.QPushButton("HYÖKKÄÄ")
        self.__hyokkaa_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__kyky1_nappi = QtWidgets.QPushButton("KYKY 1")
        self.__kyky1_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__kyky2_nappi = QtWidgets.QPushButton("KYKY 2")
        self.__kyky2_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__peru_valinta_nappi = QtWidgets.QPushButton("PERU VALINTA")
        self.__peru_valinta_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__yksikon_tiedot_nappi = QtWidgets.QPushButton("YKSIKÖN TIEDOT")
        self.__yksikon_tiedot_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__edellinen_yksikko_nappi = QtWidgets.QPushButton("EDELLINEN YKSIKKÖ")
        self.__edellinen_yksikko_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__seuraava_yksikko_nappi = QtWidgets.QPushButton("SEURAAVA YKSIKKÖ")
        self.__seuraava_yksikko_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__paata_vuoro_nappi = QtWidgets.QPushButton("PÄÄTÄ VUORO")
        self.__paata_vuoro_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__tallenna_peli_napi = QtWidgets.QPushButton("TALLENNA PELI")
        self.__tallenna_peli_napi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.__napit = []
        self.__napit.append(self.__hyokkaa_nappi)
        self.__napit.append(self.__kyky1_nappi)
        self.__napit.append(self.__kyky2_nappi)
        self.__napit.append(self.__peru_valinta_nappi)
        self.__napit.append(self.__yksikon_tiedot_nappi)
        self.__napit.append(self.__edellinen_yksikko_nappi)
        self.__napit.append(self.__seuraava_yksikko_nappi)
        self.__napit.append(self.__paata_vuoro_nappi)
        self.__napit.append(self.__tallenna_peli_napi)

        self.__hyokkaa_nappi.setStyleSheet("font: 10pt Arial")
        self.__kyky1_nappi.setStyleSheet("font: 10pt Arial")
        self.__kyky2_nappi.setStyleSheet("font: 10pt Arial")
        self.__peru_valinta_nappi.setStyleSheet("font: 10pt Arial")
        self.__yksikon_tiedot_nappi.setStyleSheet("font: 10pt Arial")
        self.__edellinen_yksikko_nappi.setStyleSheet("font: 10pt Arial")
        self.__seuraava_yksikko_nappi.setStyleSheet("font: 10pt Arial")
        self.__paata_vuoro_nappi.setStyleSheet("font: 10pt Arial")
        self.__tallenna_peli_napi.setStyleSheet("font: 10pt Arial")

        # nappi widgetit
        self.__nappi_layout.addWidget(self.__hyokkaa_nappi, 0, 0, 1, 2)
        self.__nappi_layout.addWidget(self.__kyky1_nappi, 1, 0)
        self.__nappi_layout.addWidget(self.__kyky2_nappi, 1, 1)
        self.__nappi_layout.addWidget(self.__peru_valinta_nappi, 2, 0)
        self.__nappi_layout.addWidget(self.__yksikon_tiedot_nappi, 2, 1)
        self.__nappi_layout.addWidget(self.__edellinen_yksikko_nappi, 3, 0)
        self.__nappi_layout.addWidget(self.__seuraava_yksikko_nappi, 3, 1)
        self.__nappi_layout.addWidget(self.__paata_vuoro_nappi, 4, 0)
        self.__nappi_layout.addWidget(self.__tallenna_peli_napi, 4, 1)