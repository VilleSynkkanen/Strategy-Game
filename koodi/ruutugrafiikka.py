from PyQt5 import QtGui, QtWidgets

from kayttoliittyma import Kayttoliittyma

class Ruutugrafiikka:

    def __init__(self, koordinaatit, koko, kayttoliittyma):
        self.kayttoliittyma = kayttoliittyma

        # määritellään, onko  kartan x- vai y-koko suurempi ja tallennetaan suurempi pituus
        pidempi_sivu = 0
        if self.kayttoliittyma.pelinohjain.koko[0] > self.kayttoliittyma.pelinohjain.koko[1]:
            pidempi_sivu = self.kayttoliittyma.pelinohjain.koko[0]
        else:
            pidempi_sivu = self.kayttoliittyma.pelinohjain.koko[1]

        self.koko = self.kayttoliittyma.scene_size / pidempi_sivu
        self.koordinaatit = koordinaatit
        self.väri = None        #implement
        self.piirra_ruutu()

    def piirra_ruutu(self):
        brush = QtGui.QBrush(QtGui.QColor(10, 10, 10))
        ruutu = QtWidgets.QGraphicsRectItem(self.koordinaatit.x * self.koko, self.koordinaatit.y * self.koko,
                                            self.koko, self.koko)
        self.kayttoliittyma.scene.addItem(ruutu)

    def paivita_grafiikka(self):
        pass