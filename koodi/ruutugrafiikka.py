from PyQt5 import QtGui, QtWidgets, QtCore, Qt

from kayttoliittyma import Kayttoliittyma

class Ruutugrafiikka(QtWidgets.QGraphicsRectItem):

    def __init__(self, koordinaatit, koko, kayttoliittyma, vari, ruutu):
        super(Ruutugrafiikka, self).__init__()
        self._kayttoliittyma = kayttoliittyma
        self._ruutu = ruutu

        # määritellään, onko kartan x- vai y-koko suurempi ja tallennetaan suurempi pituus

        pidempi_sivu = 0
        if self._kayttoliittyma.pelinohjain.koko[0] > self._kayttoliittyma.pelinohjain.koko[1]:
            pidempi_sivu = self._kayttoliittyma.pelinohjain.koko[0]
        else:
            pidempi_sivu = self._kayttoliittyma.pelinohjain.koko[1]

        self._koko = self._kayttoliittyma.scene_size / pidempi_sivu
        self._koordinaatit = koordinaatit
        self._vari = vari    # self.vari = alkuperäinen väri

        # teksti
        self._teksti = QtWidgets.QGraphicsTextItem("", self)
        self._teksti.setPos(self._koordinaatit.x * self._koko, self._koordinaatit.y * self._koko)
        self._teksti.setFont(QtGui.QFont("Times", 12))

        self.piirra_ruutu()
        self.paivita_tooltip()

        # värien määrittely
        self._voi_liikkua_vari = QtGui.QColor(0.3 * self._vari[0], 0.3 * self._vari[1], 0.3 * self._vari[2])
        self._kantaman_sisalla_vari = QtGui.QColor(0.8 * self._vari[0], 0.8 * self._vari[1], 0.8 * self._vari[2])
        self._valittu_kohteeksi_vari = QtGui.QColor(0.5 * self._vari[0], 0.5 * self._vari[1], 0.5 * self._vari[2])

    @property
    def teksti(self):
        return self._teksti

    @property
    def vari(self):
        return self._vari

    @property
    def voi_liikkua_vari(self):
        return self._voi_liikkua_vari

    @property
    def kantaman_sisalla_vari(self):
        return self._kantaman_sisalla_vari

    @property
    def valittu_kohteeksi_vari(self):
        return self._valittu_kohteeksi_vari

    def piirra_ruutu(self):
        brush = QtGui.QBrush(QtGui.QColor(self._vari[0], self._vari[1], self._vari[2]))
        self.setRect(self._koordinaatit.x * self._koko, self._koordinaatit.y * self._koko,
                     self._koko, self._koko)
        self.setBrush(brush)
        self.setZValue(-2)
        self._kayttoliittyma.scene.addItem(self)

    def paivita_grafiikka(self):
        pass

    def mousePressEvent(self, *args, **kwargs):
        if self._kayttoliittyma.valittu_yksikko is not None:
            if self._kayttoliittyma.valittu_yksikko.kyky1_valitsee_kohteita:
                self._kayttoliittyma.valittu_yksikko.kyky1_lisaa_kohde(self._ruutu)
            elif self._kayttoliittyma.valittu_yksikko.kyky2_valitsee_kohteita:
                pass
            elif self._ruutu in self._kayttoliittyma.valittu_yksikko.mahdolliset_ruudut and \
                    self._kayttoliittyma.valitsee_hyokkayksen_kohdetta is False:
                self._kayttoliittyma.valittu_yksikko.liiku_ruutuun(self._ruutu)


    def maarita_teksti(self, teksti):
        self._teksti.setPlainText(str(teksti))           # polunhaun testausta varten

    # muuta siten, että parametrina annetaan QColor
    def muuta_vari(self, vari):
        brush = QtGui.QBrush(vari)
        self.setBrush(brush)

    def palauta_vari(self):
        brush = QtGui.QBrush(QtGui.QColor(self._vari[0], self._vari[1], self._vari[2]))
        self.setBrush(brush)

    def aseta_tooltip(self, teksti):
        QtWidgets.QToolTip.setFont(Qt.QFont('SansSerif', 10))
        self.setToolTip(teksti)

    def paivita_tooltip(self):
        maasto = self._ruutu.maasto
        # määrittelee läpinäkyvyyden ja liikkumisen
        liikkuminen = "kyllä"
        lapinakyvyys = "kyllä"
        if maasto.liikkuminen is False:
            liikkuminen = "ei"
        if maasto.lapinakyvyys is False:
            lapinakyvyys = "ei"

        self.aseta_tooltip(self._ruutu.maasto.__str__())

    def voi_liikkua(self):
        brush = QtGui.QBrush(self._voi_liikkua_vari)
        self.setBrush(brush)
