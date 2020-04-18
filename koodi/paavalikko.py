from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from kenttaeditori import Kenttaeditori
from pelinohjain import Pelinohjain
from maaston_lukija import Maaston_lukija
from yksikoiden_lukija import Yksikoiden_lukija
from kartan_lukija import Kartan_lukija
from kayttoliittyman_lukija import Kayttoliittyman_lukija
from pelaa_valikko import Pelaa_valikko
import sys


class Paavalikko(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Paavalikko, self).__init__()
        self.__kayttoliittyman_lukija = Kayttoliittyman_lukija()
        if self.__kayttoliittyman_lukija.koko != 0:
            self.__scene_size = self.__kayttoliittyman_lukija.koko
        else:
            self.__scene_size = 880
        self.setCentralWidget(QtWidgets.QWidget())  # QMainWindown must have a centralWidget to be able to add layouts
        self.__paa_layout = QtWidgets.QVBoxLayout()  # Vertical main layout
        self.centralWidget().setLayout(self.__paa_layout)

        self.setGeometry(0, 0, self.__scene_size + 360, self.__scene_size + 20)
        self.setWindowTitle('Strategiapeli')
        self.show()

        self.__virheteksti = QtWidgets.QLabel("")
        self.__pelaa_nappi = QtWidgets.QPushButton("PELAA")
        self.__pelaa_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__kenttaeditori_nappi = QtWidgets.QPushButton("KENTTÄEDITORI")
        self.__kenttaeditori_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__poistu_nappi = QtWidgets.QPushButton("POISTU")
        self.__poistu_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.__virheteksti.setStyleSheet("font: 20pt Arial")
        self.__pelaa_nappi.setStyleSheet("font: 10pt Arial")
        self.__kenttaeditori_nappi.setStyleSheet("font: 10pt Arial")
        self.__poistu_nappi.setStyleSheet("font: 10pt Arial")

        # nappien yhdistäminen
        self.__pelaa_nappi.clicked.connect(self.__pelaa)
        self.__kenttaeditori_nappi.clicked.connect(self.__kenttaeditori)
        self.__poistu_nappi.clicked.connect(self.__poistu)

        # nappi widgetit
        self.__paa_layout.addWidget(self.__virheteksti, 1)
        self.__paa_layout.addWidget(self.__pelaa_nappi, 2)
        self.__paa_layout.addWidget(self.__kenttaeditori_nappi, 2)
        self.__paa_layout.addWidget(self.__poistu_nappi, 2)

        # kenttäeditori
        self.kenttaeditori = None
        self.__pelaa_valikko = None

        # tiedostojen lukijat
        self.__maastojen_lukija = Maaston_lukija()
        self.__yksikoiden_lukija = Yksikoiden_lukija()
        self.__kartan_lukija = Kartan_lukija()

        # virheet
        if not self.__kayttoliittyman_lukija.lukeminen_onnistui:
            self.__virhe_lukemisessa("kayttoliittyma")

        # keskelle liikuttaminen
        if self.kayttoliittyman_lukija.x != 0 and self.kayttoliittyman_lukija.y != 0:
            res_x = self.kayttoliittyman_lukija.x
            res_y = self.kayttoliittyman_lukija.y
        else:
            res_x = 1920
            res_y = 1080
        self.move(int(res_x / 2) - int(self.frameSize().width() / 2),
                  int(res_y / 2) - int(self.frameSize().height() / 2))

    @property
    def maastojen_lukija(self):
        return self.__maastojen_lukija

    @property
    def yksikoiden_lukija(self):
        return self.__yksikoiden_lukija

    @property
    def kartan_lukija(self):
        return self.__kartan_lukija

    @property
    def kayttoliittyman_lukija(self):
        return self.__kayttoliittyman_lukija

    @property
    def scene_size(self):
        return self.__scene_size

    @property
    def pelaa_valikko(self):
        return self.__pelaa_valikko

    def __virhe_lukemisessa(self, tyyppi):
        if tyyppi == "kayttoliittyma":
            self.__virheteksti.setText("Käyttöliittymän lukemisessa tapahtui virhe.\n"
                                       "Korjaa tiedosto ja avaa ohjelma uudestaan")


    def __pelaa(self):
        if self.__pelaa_valikko is None:
            self.__pelaa_valikko = Pelaa_valikko(self)
        self.__pelaa_valikko.show()
        self.hide()

    def __kenttaeditori(self):
        if self.kenttaeditori is None:
            self.kenttaeditori = Kenttaeditori(self)
        self.kenttaeditori.show()
        self.hide()

    def __poistu(self):
        sys.exit()
