from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from elamapalkki import Elamapalkki

class Yksikkografiikka(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, luokka, ruutu, kayttoliittyma, omistaja, yksikko):
        super(Yksikkografiikka, self).__init__()
        # yksikön tyyppi luetaan sen luokan nimestä
        tyyppi = luokka.__class__.__name__
        self._yksikko = yksikko
        self._koko = ruutu.kartta.ruudun_koko
        self._ruutu = ruutu
        self._kayttoliittyma = kayttoliittyma
        self._omistaja = omistaja
        self._ylaosan_koko = 0.75        # alas jää 1 - ylaosan_koko ruutua elämänpalkille

        # eri tilanteissa käytettävien värien määrittely
        self._tietokoneen_vari = QtGui.QBrush(QtGui.QColor(180, 0, 0))
        self._pelaajan_vari = QtGui.QBrush(QtGui.QColor(0, 0, 180))
        self._pelaaja_valittu_vari = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        self._pelaaja_kaytetty_vari = QtGui.QBrush(QtGui.QColor(0, 0, 80))
        self._voi_hyokata_vari = QtGui.QBrush(QtGui.QColor(255, 0, 0))

        # brush
        if self._omistaja == "COM":
            self.muuta_varia(self._tietokoneen_vari)
        else:
            self.muuta_varia(self._pelaajan_vari)

        if tyyppi == "Jalkavaki":
            self.piirra_jalkavaki()
        elif tyyppi == "Ratsuvaki":
            self.piirra_ratsuvaki()
        elif tyyppi == "Jousimiehet":
            self.piirra_jousimiehet()
        elif tyyppi == "Tykisto":
            self.piirra_tykisto()
        elif tyyppi == "Parantaja":
            self.piirra_parantaja()

        # origin piste keskelle
        self.setTransformOriginPoint(self._koko / 2, self._koko / 2)

        self.setPos(self._ruutu.koordinaatit.x * self._koko, self._ruutu.koordinaatit.y * self._koko)
        self._kayttoliittyma.scene.addItem(self)

        # luo elämäpalkki
        self.elamapalkki = Elamapalkki(self._koko, self._ylaosan_koko, self._kayttoliittyma, self._yksikko)

        # luo tooltip
        self.paivita_tooltip()

    @property
    def yksikko(self):
        return self._yksikko

    @property
    def ruutu(self):
        return self._ruutu

    @property
    def omistaja(self):
        return self._omistaja

    @property
    def tietokoneen_vari(self):
        return self._tietokoneen_varis

    @property
    def pelaajan_vari(self):
        return self._pelaajan_vari

    @property
    def pelaaja_valittu_vari(self):
        return self._pelaaja_valittu_vari

    @property
    def pelaaja_kaytetty_vari(self):
        return self._pelaaja_kaytetty_vari

    @property
    def voi_hyokata_vari(self):
        return self._voi_hyokata_vari

    def piirra_jalkavaki(self):
        polygoni = QtGui.QPolygonF()

        a = self._koko

        r = self._koko / 4

        polygoni.append(QtCore.QPointF(r, 0))
        polygoni.append(QtCore.QPointF(2 * r, r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 0))
        polygoni.append(QtCore.QPointF(a, r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 2 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(a, 3 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, a * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(2 * r, 3 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, a * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, 3 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, 2 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, r * self._ylaosan_koko))

        self.setPolygon(polygoni)

    def piirra_ratsuvaki(self):
        polygoni = QtGui.QPolygonF()

        a = self._koko
        r = self._koko / 4

        polygoni.append(QtCore.QPointF(0, 3 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 0))
        polygoni.append(QtCore.QPointF(a, r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, a * self._ylaosan_koko))

        self.setPolygon(polygoni)

    def piirra_jousimiehet(self):
        polygoni = QtGui.QPolygonF()

        a = self._koko
        r = self._koko / 4

        polygoni.append(QtCore.QPointF(2 * r, 0))
        polygoni.append(QtCore.QPointF(a, 2 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 2 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, a * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, a * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, 2 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, 2 * r * self._ylaosan_koko))

        self.setPolygon(polygoni)

    def piirra_tykisto(self):
        polygoni = QtGui.QPolygonF()

        a = self._koko
        r = self._koko / 4

        polygoni.append(QtCore.QPointF(r, 0))
        polygoni.append(QtCore.QPointF(3 * r, 0))
        polygoni.append(QtCore.QPointF(3 * r, 2 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(a, 3 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, a * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, a * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, 3 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, 2 * r * self._ylaosan_koko))

        self.setPolygon(polygoni)

    def piirra_parantaja(self):
        polygoni = QtGui.QPolygonF()

        a = self._koko
        r = self._koko / 4

        polygoni.append(QtCore.QPointF(0, 0))
        polygoni.append(QtCore.QPointF(r, r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(a, 0))
        polygoni.append(QtCore.QPointF(a, a * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 3 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, 3 * r * self._ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, a * self._ylaosan_koko))

        self.setPolygon(polygoni)

    def muuta_varia(self, vari):        # vari = QColor
        brush = QtGui.QBrush(vari)
        self.setBrush(brush)

    def palauta_vari(self):
        # väri riippuu siitä, onko yksikkö vielä käytettävissä tällä vuorolla
        if self._yksikko not in self._kayttoliittyma.pelinohjain.kartta.pelaajan_toimivat_yksikot:
            if self._omistaja == "COM":
                brush = QtGui.QBrush(self._tietokoneen_vari)
            else:
                brush = QtGui.QBrush(self._pelaaja_kaytetty_vari)
        else:
            if self._omistaja == "COM":
                brush = QtGui.QBrush(self._tietokoneen_vari)
            else:
                brush = QtGui.QBrush(self._pelaajan_vari)
        self.setBrush(brush)

    def paivita_sijainti(self, ruutu):
        self._ruutu = ruutu
        self.setPos(self._ruutu.koordinaatit.x * self._koko, self._ruutu.koordinaatit.y * self._koko)
        self.elamapalkki.paivita_sijainti()

    def aseta_tooltip(self, teksti):
        QtWidgets.QToolTip.setFont(Qt.QFont('SansSerif', 10))
        self.setToolTip(teksti)

    def paivita_tooltip(self):
        if self._yksikko.ominaisuudet is not None:
            self.aseta_tooltip(self._yksikko.ominaisuudet.__str__())

    def hyokkays_tootip(self, hyokkaaja_vahinko, puolustaja_vahinko, tukibonus):
        self.aseta_tooltip(self._yksikko.__class__.__name__ + "\nElämä: " + str(self._yksikko.ominaisuudet.nyk_elama) +
                           "/" + str(self._yksikko.ominaisuudet.max_elama) + "\nPuolustus: "
                           + str(self._yksikko.ominaisuudet.puolustus) +
                           "\nOdotettu vahinko:\nHyökkääjä: " + str(hyokkaaja_vahinko) +
                           "\nPuolustaja: " + str(puolustaja_vahinko) + "\nTukibonus: " + tukibonus)

    def poista(self):
        self.elamapalkki = None
        polygoni = QtGui.QPolygonF()
        self.setPolygon(polygoni)

    def mousePressEvent(self, *args, **kwargs):
        if self._kayttoliittyma.valittu_yksikko is not None and \
                self._kayttoliittyma.valittu_yksikko.kyky1_valitsee_kohteita:
            self._kayttoliittyma.valittu_yksikko.kyky1_lisaa_kohde(self._yksikko.ruutu)
        elif self._kayttoliittyma.valittu_yksikko is not None and \
                self._kayttoliittyma.valittu_yksikko.kyky2_valitsee_kohteita:
            if self._yksikko.omistaja != self._kayttoliittyma.valittu_yksikko.omistaja:
                self._kayttoliittyma.valittu_yksikko.kayta_kyky2(self._yksikko)
        elif self._yksikko.omistaja == "PLR" and self._kayttoliittyma.valitsee_hyokkayksen_kohdetta is False:
            self._kayttoliittyma.valitse_yksikko(self._yksikko)
        elif self._yksikko.omistaja == "COM" and self._yksikko.kayttoliittyma.valitsee_hyokkayksen_kohdetta and \
                self._yksikko in self._kayttoliittyma.valittu_yksikko.hyokkayksen_kohteet:
            self._yksikko.hyokkayksen_kohde(self._kayttoliittyma.valittu_yksikko)
