from PyQt5 import QtGui, QtWidgets, QtCore

from kayttoliittyma import Kayttoliittyma

class Ruutugrafiikka(QtWidgets.QGraphicsRectItem):

    def __init__(self, koordinaatit, koko, kayttoliittyma, vari, ruutu):
        super(Ruutugrafiikka, self).__init__()
        self.kayttoliittyma = kayttoliittyma
        self.ruutu = ruutu

        # määritellään, onko kartan x- vai y-koko suurempi ja tallennetaan suurempi pituus

        pidempi_sivu = 0
        if self.kayttoliittyma.pelinohjain.koko[0] > self.kayttoliittyma.pelinohjain.koko[1]:
            pidempi_sivu = self.kayttoliittyma.pelinohjain.koko[0]
        else:
            pidempi_sivu = self.kayttoliittyma.pelinohjain.koko[1]

        self.koko = self.kayttoliittyma.scene_size / pidempi_sivu
        self.koordinaatit = koordinaatit
        self.vari = vari    # self.vari = alkuperäinen väri

        # teksti
        self.teksti = QtWidgets.QGraphicsTextItem("", self)
        self.teksti.setPos(self.koordinaatit.x * self.koko, self.koordinaatit.y * self.koko)
        self.teksti.setFont(QtGui.QFont("Times", 12))

        self.piirra_ruutu()

        # värien määrittely
        self.voi_liikkua_vari = QtGui.QColor(0.5 * self.vari[0], 0.5 * self.vari[1], 0.5 * self.vari[2])

    def piirra_ruutu(self):
        brush = QtGui.QBrush(QtGui.QColor(self.vari[0], self.vari[1], self.vari[2]))
        self.setRect(self.koordinaatit.x * self.koko, self.koordinaatit.y * self.koko,
                                            self.koko, self.koko)
        self.setBrush(brush)
        self.kayttoliittyma.scene.addItem(self)

    def paivita_grafiikka(self):
        pass

    def mousePressEvent(self, *args, **kwargs):
        if self.kayttoliittyma.valittu_yksikko is not None and self.ruutu in \
                self.kayttoliittyma.valittu_yksikko.mahdolliset_ruudut and \
                self.kayttoliittyma.valitsee_hyokkayksen_kohdetta is False:
            self.kayttoliittyma.valittu_yksikko.liiku_ruutuun(self.ruutu)

    def maarita_teksti(self, teksti):
        self.teksti.setPlainText(str(teksti))           # polunhaun testausta varten

    # muuta siten, että parametrina annetaan QColor
    def muuta_vari(self, vari):
        brush = QtGui.QBrush(QtGui.QColor(vari[0], vari[1], vari[2]))
        self.setBrush(brush)

    def palauta_vari(self):
        brush = QtGui.QBrush(QtGui.QColor(self.vari[0], self.vari[1], self.vari[2]))
        self.setBrush(brush)

    def voi_liikkua(self):
        brush = QtGui.QBrush(self.voi_liikkua_vari)
        self.setBrush(brush)
