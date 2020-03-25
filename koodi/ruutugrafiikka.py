from PyQt5 import QtGui, QtWidgets, QtCore, Qt

from kayttoliittyma import Kayttoliittyma

class Ruutugrafiikka(QtWidgets.QGraphicsRectItem):

    def __init__(self, koordinaatit, koko, kayttoliittyma, vari, ruutu):
        super(Ruutugrafiikka, self).__init__()
        self.__kayttoliittyma = kayttoliittyma
        self.__ruutu = ruutu

        # määritellään, onko kartan x- vai y-koko suurempi ja tallennetaan suurempi pituus

        pidempi_sivu = 0
        if self.__kayttoliittyma.pelinohjain.koko[0] > self.__kayttoliittyma.pelinohjain.koko[1]:
            pidempi_sivu = self.__kayttoliittyma.pelinohjain.koko[0]
        else:
            pidempi_sivu = self.__kayttoliittyma.pelinohjain.koko[1]

        self.__koko = self.__kayttoliittyma.scene_size / pidempi_sivu
        self.__koordinaatit = koordinaatit
        self.__vari = vari    # self.vari = alkuperäinen väri

        # teksti
        self.__teksti = QtWidgets.QGraphicsTextItem("", self)
        self.__teksti.setPos(self.__koordinaatit.x * self.__koko, self.__koordinaatit.y * self.__koko)
        self.__teksti.setFont(QtGui.QFont("Times", 12))

        self.__piirra_ruutu()
        self.paivita_tooltip()

        # värien määrittely
        self.__voi_liikkua_vari = QtGui.QColor(0.3 * self.__vari[0], 0.3 * self.__vari[1], 0.3 * self.__vari[2])
        self.__kantaman_sisalla_vari = QtGui.QColor(0.8 * self.__vari[0], 0.8 * self.__vari[1], 0.8 * self.__vari[2])
        self.__valittu_kohteeksi_vari = QtGui.QColor(0.5 * self.__vari[0], 0.5 * self.__vari[1], 0.5 * self.__vari[2])

    @property
    def teksti(self):
        return self.__teksti

    @property
    def vari(self):
        return self.__vari

    @property
    def voi_liikkua_vari(self):
        return self.__voi_liikkua_vari

    @property
    def kantaman_sisalla_vari(self):
        return self.__kantaman_sisalla_vari

    @property
    def valittu_kohteeksi_vari(self):
        return self.__valittu_kohteeksi_vari

    def __piirra_ruutu(self):
        brush = QtGui.QBrush(QtGui.QColor(self.__vari[0], self.__vari[1], self.__vari[2]))
        self.setRect(self.__koordinaatit.x * self.__koko, self.__koordinaatit.y * self.__koko,
                     self.__koko, self.__koko)
        self.setBrush(brush)
        self.setZValue(-2)
        self.__kayttoliittyma.scene.addItem(self)

    def mousePressEvent(self, *args, **kwargs):
        if self.__kayttoliittyma.valittu_yksikko is not None:
            if self.__kayttoliittyma.valittu_yksikko.kyky1_valitsee_kohteita:
                self.__kayttoliittyma.valittu_yksikko.kyky1_lisaa_kohde(self.__ruutu)
            elif self.__kayttoliittyma.valittu_yksikko.kyky2_valitsee_kohteita:
                pass
            elif self.__ruutu in self.__kayttoliittyma.valittu_yksikko.mahdolliset_ruudut and \
                    self.__kayttoliittyma.valitsee_hyokkayksen_kohdetta is False:
                self.__kayttoliittyma.valittu_yksikko.liiku_ruutuun(self.__ruutu)

    # muuta siten, että parametrina annetaan QColor
    def muuta_vari(self, vari):
        brush = QtGui.QBrush(vari)
        self.setBrush(brush)

    def palauta_vari(self):
        brush = QtGui.QBrush(QtGui.QColor(self.__vari[0], self.__vari[1], self.__vari[2]))
        self.setBrush(brush)

    def __aseta_tooltip(self, teksti):
        QtWidgets.QToolTip.setFont(Qt.QFont('SansSerif', 10))
        self.setToolTip(teksti)

    def paivita_tooltip(self):
        maasto = self.__ruutu.maasto
        # määrittelee läpinäkyvyyden ja liikkumisen
        liikkuminen = "kyllä"
        lapinakyvyys = "kyllä"
        if maasto.liikkuminen is False:
            liikkuminen = "ei"
        if maasto.lapinakyvyys is False:
            lapinakyvyys = "ei"

        self.__aseta_tooltip(self.__ruutu.maasto.__str__())

    def voi_liikkua(self):
        brush = QtGui.QBrush(self.__voi_liikkua_vari)
        self.setBrush(brush)
