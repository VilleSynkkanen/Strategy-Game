from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from elamapalkki import Elamapalkki


class Yksikkografiikka(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, luokka, ruutu, kayttoliittyma, omistaja, yksikko):
        super(Yksikkografiikka, self).__init__()
        # yksikön tyyppi luetaan sen luokan nimestä
        tyyppi = luokka.__class__.__name__
        self.__yksikko = yksikko
        self.__koko = ruutu.grafiikka.koko
        self.__ruutu = ruutu
        self.__kayttoliittyma = kayttoliittyma
        self.__omistaja = omistaja
        self.__ylaosan_koko = 0.75        # ruudun alaosaan jää 1 - ylaosan_koko ruutua elämänpalkille

        # eri tilanteissa käytettävien värien määrittely
        self.__tietokoneen_vari = QtGui.QBrush(QtGui.QColor(180, 0, 0))
        self.__pelaajan_vari = QtGui.QBrush(QtGui.QColor(0, 0, 180))
        self.__pelaaja_valittu_vari = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        self.__pelaaja_kaytetty_vari = QtGui.QBrush(QtGui.QColor(0, 0, 80))
        self.__voi_hyokata_vari = QtGui.QBrush(QtGui.QColor(255, 0, 0))

        # brush
        if self.__omistaja == "COM":
            self.muuta_varia(self.__tietokoneen_vari)
        else:
            self.muuta_varia(self.__pelaajan_vari)

        if tyyppi == "Jalkavaki":
            self.__piirra_jalkavaki()
        elif tyyppi == "Ratsuvaki":
            self.__piirra_ratsuvaki()
        elif tyyppi == "Jousimiehet":
            self.__piirra_jousimiehet()
        elif tyyppi == "Tykisto":
            self.__piirra_tykisto()
        elif tyyppi == "Parantaja":
            self.__piirra_parantaja()

        # origin piste keskelle
        self.setTransformOriginPoint(self.__koko / 2, self.__koko / 2)
        self.setPos(self.__ruutu.koordinaatit.x * self.__koko, self.__ruutu.koordinaatit.y * self.__koko)
        self.__kayttoliittyma.scene.addItem(self)

        # luo elämäpalkki
        self.__elamapalkki = Elamapalkki(self.__koko, self.__ylaosan_koko, self.__kayttoliittyma, self.__yksikko)

        # luo tooltip
        self.paivita_tooltip()

    @property
    def yksikko(self):
        return self.__yksikko

    @property
    def ruutu(self):
        return self.__ruutu

    @property
    def omistaja(self):
        return self.__omistaja

    @property
    def tietokoneen_vari(self):
        return self.__tietokoneen_vari

    @property
    def pelaajan_vari(self):
        return self.__pelaajan_vari

    @property
    def pelaaja_valittu_vari(self):
        return self.__pelaaja_valittu_vari

    @property
    def pelaaja_kaytetty_vari(self):
        return self.__pelaaja_kaytetty_vari

    @property
    def voi_hyokata_vari(self):
        return self.__voi_hyokata_vari

    @property
    def elamapalkki(self):
        return self.__elamapalkki

    def __piirra_jalkavaki(self):
        polygoni = QtGui.QPolygonF()

        a = self.__koko

        r = self.__koko / 4

        polygoni.append(QtCore.QPointF(r, 0))
        polygoni.append(QtCore.QPointF(2 * r, r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 0))
        polygoni.append(QtCore.QPointF(a, r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 2 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(a, 3 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, a * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(2 * r, 3 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, a * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, 3 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, 2 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, r * self.__ylaosan_koko))

        self.setPolygon(polygoni)

    def __piirra_ratsuvaki(self):
        polygoni = QtGui.QPolygonF()

        a = self.__koko
        r = self.__koko / 4

        polygoni.append(QtCore.QPointF(0, 3 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 0))
        polygoni.append(QtCore.QPointF(a, r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, a * self.__ylaosan_koko))

        self.setPolygon(polygoni)

    def __piirra_jousimiehet(self):
        polygoni = QtGui.QPolygonF()

        a = self.__koko
        r = self.__koko / 4

        polygoni.append(QtCore.QPointF(2 * r, 0))
        polygoni.append(QtCore.QPointF(a, 2 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 2 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, a * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, a * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, 2 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, 2 * r * self.__ylaosan_koko))

        self.setPolygon(polygoni)

    def __piirra_tykisto(self):
        polygoni = QtGui.QPolygonF()

        a = self.__koko
        r = self.__koko / 4

        polygoni.append(QtCore.QPointF(r, 0))
        polygoni.append(QtCore.QPointF(3 * r, 0))
        polygoni.append(QtCore.QPointF(3 * r, 2 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(a, 3 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, a * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, a * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, 3 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, 2 * r * self.__ylaosan_koko))

        self.setPolygon(polygoni)

    def __piirra_parantaja(self):
        polygoni = QtGui.QPolygonF()

        a = self.__koko
        r = self.__koko / 4

        polygoni.append(QtCore.QPointF(0, 0))
        polygoni.append(QtCore.QPointF(r, r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(a, 0))
        polygoni.append(QtCore.QPointF(a, a * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 3 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, 3 * r * self.__ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, a * self.__ylaosan_koko))

        self.setPolygon(polygoni)

    def muuta_varia(self, vari):        # vari = QColor
        brush = QtGui.QBrush(vari)
        self.setBrush(brush)

    def palauta_vari(self):
        # väri riippuu siitä, onko yksikkö vielä käytettävissä tällä vuorolla
        if self.__yksikko not in self.__kayttoliittyma.pelinohjain.kartta.pelaajan_toimivat_yksikot:
            if self.__omistaja == "COM":
                brush = QtGui.QBrush(self.__tietokoneen_vari)
            else:
                brush = QtGui.QBrush(self.__pelaaja_kaytetty_vari)
        else:
            if self.__omistaja == "COM":
                brush = QtGui.QBrush(self.__tietokoneen_vari)
            else:
                brush = QtGui.QBrush(self.__pelaajan_vari)
        self.setBrush(brush)

    def paivita_sijainti(self, ruutu):
        self.__ruutu = ruutu
        self.setPos(self.__ruutu.koordinaatit.x * self.__koko, self.__ruutu.koordinaatit.y * self.__koko)
        self.__elamapalkki.paivita_sijainti()

    def __aseta_tooltip(self, teksti):
        QtWidgets.QToolTip.setFont(Qt.QFont('SansSerif', 10))
        self.setToolTip(teksti)

    def paivita_tooltip(self):
        if self.__yksikko.ominaisuudet is not None:
            self.__aseta_tooltip(self.__yksikko.ominaisuudet.__str__())

    def hyokkays_tootip(self, hyokkaaja_vahinko, puolustaja_vahinko, tukibonus):
        self.__aseta_tooltip(self.__yksikko.__class__.__name__ + "\nElämä: " + str(self.__yksikko.ominaisuudet.nyk_elama) +
                           "/" + str(self.__yksikko.ominaisuudet.max_elama) + "\nPuolustus: "
                             + str(self.__yksikko.ominaisuudet.puolustus) +
                           "\nOdotettu vahinko:\nHyökkääjä: " + str(hyokkaaja_vahinko) +
                           "\nPuolustaja: " + str(puolustaja_vahinko) + "\nTukibonus: " + tukibonus)

    def poista(self):
        self.__elamapalkki = None
        polygoni = QtGui.QPolygonF()
        self.setPolygon(polygoni)

    def mousePressEvent(self, *args, **kwargs):
        # toiminnallisuus pelitilanteessa
        if self.__kayttoliittyma.__class__.__name__ == "Kayttoliittyma":
            if self.__kayttoliittyma.pelinohjain.vuoro == "PLR":
                if self.__kayttoliittyma.valittu_yksikko is not None and \
                        self.__kayttoliittyma.valittu_yksikko.kyky1_valitsee_kohteita:
                    self.__kayttoliittyma.valittu_yksikko.kyky1_lisaa_kohde(self.__yksikko.ruutu)
                elif self.__kayttoliittyma.valittu_yksikko is not None and \
                        self.__kayttoliittyma.valittu_yksikko.kyky2_valitsee_kohteita:
                    if self.__yksikko.omistaja != self.__kayttoliittyma.valittu_yksikko.omistaja:
                        self.__kayttoliittyma.valittu_yksikko.kayta_kyky2(self.__yksikko)
                elif self.__yksikko.omistaja == "PLR" and self.__kayttoliittyma.valitsee_hyokkayksen_kohdetta is False:
                    self.__kayttoliittyma.valitse_yksikko(self.__yksikko)
                elif self.__kayttoliittyma.valittu_yksikko is not None and self.__yksikko.omistaja == "COM" \
                        and self.__yksikko.kayttoliittyma.valitsee_hyokkayksen_kohdetta and \
                        self.__yksikko in self.__kayttoliittyma.valittu_yksikko.hyokkayksen_kohteet:
                    self.__yksikko.hyokkayksen_kohde(self.__kayttoliittyma.valittu_yksikko)
        # toiminnallisuus kenttäeditorissa
        else:
            if self.__kayttoliittyma.valittu_elementti is not None:
                maastot = ["tasanko", "kukkula", "pelto", "vuoristo", "silta", "joki"]
                if self.__kayttoliittyma.valittu_elementti in maastot:
                    self.__yksikko.kayttoliittyma.kartta.korvaa_ruutu(self.__yksikko.ruutu,
                                                                      self.__kayttoliittyma.valittu_elementti)
                elif self.__kayttoliittyma.valittu_elementti == "poista":
                    self.yksikko.tuhoudu()
                    self.__kayttoliittyma.kartta.poista_yksikko(self)
