from PyQt5 import QtWidgets, QtCore, QtGui, Qt

class Kayttoliittyma(QtWidgets.QMainWindow):
    '''
    Käyttöliittymä piirtää pelilaudan, napit ja tekstielementit
    '''
    def __init__(self, pelinohjain):
        super().__init__()
        self._scene_size = 880       # kentän koko pikseleinä
        self._pelinohjain = pelinohjain

        # toimintaan liittyviä muuttujia
        self._valittu_yksikko = None
        self._yksikon_tiedot_aktiivinen = False
        self._valitsee_hyokkayksen_kohdetta = False

        self.setCentralWidget(QtWidgets.QWidget())  # QMainWindown must have a centralWidget to be able to add layouts
        self._paa_layout = QtWidgets.QHBoxLayout()  # Horizontal main layout
        self.centralWidget().setLayout(self._paa_layout)

        # set window
        self.setGeometry(0, 0, self._scene_size + 420, self._scene_size)
        self.setWindowTitle('Strategiapeli')
        self.show()

        # Add a scene for drawing 2d objects
        self._scene = QtWidgets.QGraphicsScene()

        # Add a view for showing the scene
        self._nakyma = QtWidgets.QGraphicsView(self._scene, self)
        self._nakyma.adjustSize()
        self._nakyma.show()
        self._paa_layout.addWidget(self._nakyma)
        # main_layout.addStretch()

        self._nappi_layout = QtWidgets.QGridLayout()
        self._paa_layout.addLayout(self._nappi_layout)

        # buttons
        self._hyokkaa_nappi = QtWidgets.QPushButton("HYÖKKÄÄ")
        self._hyokkaa_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self._kyky1_nappi = QtWidgets.QPushButton("KYKY 1")
        self._kyky1_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self._kyky2_nappi = QtWidgets.QPushButton("KYKY 2")
        self._kyky2_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self._peru_valinta_nappi = QtWidgets.QPushButton("PERU VALINTA")
        self._peru_valinta_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self._yksikon_tiedot_nappi = QtWidgets.QPushButton("YKSIKÖN TIEDOT")
        self._yksikon_tiedot_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self._edellinen_yksikko_nappi = QtWidgets.QPushButton("EDELLINEN YKSIKKÖ")
        self._edellinen_yksikko_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self._seuraava_yksikko_nappi = QtWidgets.QPushButton("SEURAAVA YKSIKKÖ")
        self._seuraava_yksikko_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self._paata_vuoro_nappi = QtWidgets.QPushButton("PÄÄTÄ VUORO")
        self._paata_vuoro_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self._tallenna_peli_napi = QtWidgets.QPushButton("TALLENNA PELI")
        self._tallenna_peli_napi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self._hyokkaa_nappi.setStyleSheet("font: 10pt Arial")
        self._kyky1_nappi.setStyleSheet("font: 10pt Arial")
        self._kyky2_nappi.setStyleSheet("font: 10pt Arial")
        self._peru_valinta_nappi.setStyleSheet("font: 10pt Arial")
        self._yksikon_tiedot_nappi.setStyleSheet("font: 10pt Arial")
        self._edellinen_yksikko_nappi.setStyleSheet("font: 10pt Arial")
        self._seuraava_yksikko_nappi.setStyleSheet("font: 10pt Arial")
        self._paata_vuoro_nappi.setStyleSheet("font: 10pt Arial")
        self._tallenna_peli_napi.setStyleSheet("font: 10pt Arial")

        # nappien yhdistäminen
        self._hyokkaa_nappi.clicked.connect(self.hyokkaa)
        self._kyky1_nappi.clicked.connect(self.kyky_1)
        self._kyky2_nappi.clicked.connect(self.kyky_2)
        self._peru_valinta_nappi.clicked.connect(self.peru_valinta)
        self._paata_vuoro_nappi.clicked.connect(self.paata_vuoro)
        self._yksikon_tiedot_nappi.clicked.connect(self.yksikon_tiedot)
        self._edellinen_yksikko_nappi.clicked.connect(self.edellinen_yksikko)
        self._seuraava_yksikko_nappi.clicked.connect(self.seuraava_yksikko)
        self._tallenna_peli_napi.clicked.connect(self.tallenna_peli)

        # add button widgets
        self._nappi_layout.addWidget(self._hyokkaa_nappi, 0, 0, 1, 2)
        self._nappi_layout.addWidget(self._kyky1_nappi, 1, 0)
        self._nappi_layout.addWidget(self._kyky2_nappi, 1, 1)
        self._nappi_layout.addWidget(self._peru_valinta_nappi, 2, 0)
        self._nappi_layout.addWidget(self._yksikon_tiedot_nappi, 2, 1)
        self._nappi_layout.addWidget(self._edellinen_yksikko_nappi, 3, 0)
        self._nappi_layout.addWidget(self._seuraava_yksikko_nappi, 3, 1)
        self._nappi_layout.addWidget(self._paata_vuoro_nappi, 4, 0)
        self._nappi_layout.addWidget(self._tallenna_peli_napi, 4, 1)

        # unit info
        self._perustiedot = QtWidgets.QLabel("")
        self._nappi_layout.addWidget(self._perustiedot, 5, 0, 1, 1, alignment=QtCore.Qt.AlignTop)
        self._perustiedot.setStyleSheet("font: 9pt Arial")
        self._perustiedot.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # maaston info
        self._maaston_tiedot = QtWidgets.QLabel("")
        self._nappi_layout.addWidget(self._maaston_tiedot, 5, 1, 1, 1, alignment=QtCore.Qt.AlignTop)
        self._maaston_tiedot.setStyleSheet("font: 9pt Arial")
        self._maaston_tiedot.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # game log test
        self._peliloki = QtWidgets.QLabel("PELILOKI:\n", self)
        self._nappi_layout.addWidget(self._peliloki, 6, 0, 6, 2, alignment=QtCore.Qt.AlignTop)
        self._peliloki.setStyleSheet("font: 9pt Arial")

        self._ohjeteksti = QtWidgets.QLabel("OHJETEKSTI\n", self)
        self._nappi_layout.addWidget(self._ohjeteksti, 11, 0, 1, 0, alignment=QtCore.Qt.AlignTop)
        self._ohjeteksti.setStyleSheet("font: 9pt Arial")

    @property
    def pelinohjain(self):
        return self._pelinohjain

    @property
    def scene_size(self):
        return self._scene_size

    @property
    def valittu_yksikko(self):
        return self._valittu_yksikko

    @property
    def yksikon_tiedot_aktiivinen(self):
        return self._yksikon_tiedot_aktiivinen

    @property
    def valitsee_hyokkayksen_kohdetta(self):
        return self._valitsee_hyokkayksen_kohdetta

    @property
    def scene(self):
        return self._scene

    def aseta_scene_rect(self, x, y):
        # rectin skaalauskertoimet
        if x > y:
            y /= x
            x = 1
        else:
            x /= y
            y = 1
        self._scene.setSceneRect(0, 0, self._scene_size * x, self._scene_size * y)
        #self.setGeometry(0, 0, self.scene_size * x + 420, self.scene_size * y + 20)

        # keskelle liikuttaminen
        res_x = 1920
        res_y = 1080
        self.move((res_x / 2) - (self.frameSize().width() / 2),
                  (res_y / 2) - (self.frameSize().height() / 2))


    def valitse_yksikko(self, yksikko):
        self.tyhjenna_valinta()
        # valinnan muuttaminen
        self._valittu_yksikko = yksikko

        liikuttu = "ei"
        hyokatty = "ei"
        if self._valittu_yksikko.liikkuminen_kaytetty:
            liikuttu = "kyllä"
        if self._valittu_yksikko.hyokkays_kaytetty:
            hyokatty = "kyllä"

        # näytä tiedot
        self.paivita_valitun_yksikon_tiedot()
        self.paivita_kykynapit()

        # näytä peliloki
        self._peliloki.setText("PELILOKI:\n")

        yksikko.grafiikka.muuta_varia(yksikko.grafiikka.pelaaja_valittu_vari)
        # vanhan valinnan värin muutos tehdään, kun valinta tyhjennetään (jos yksikkö ei voi tehdä mitään, väri on eri)
        for yks in self._pelinohjain.kartta.pelaajan_yksikot:
            if yks != self._valittu_yksikko:
                yks.grafiikka.palauta_vari()
        for ruutu in self._pelinohjain.kartta.ruudut:
            ruutu.grafiikka.palauta_vari()

        # polkujen näyttäminen
        if not self._valittu_yksikko.liikkuminen_kaytetty:
            self._valittu_yksikko.laske_mahdolliset_ruudut()
        self._valittu_yksikko.nayta_mahdolliset_ruudut()

    def paivita_kykynapit(self):
        if self._valittu_yksikko is not None:
            self._kyky1_nappi.setText(self._valittu_yksikko.kyky1_nappi_tiedot())
            self._kyky2_nappi.setText(self._valittu_yksikko.kyky2_nappi_tiedot())
        else:
            self._kyky1_nappi.setText("KYKY 1")
            self._kyky2_nappi.setText("KYKY 2")

    def paivita_valitun_yksikon_tiedot(self):
        liikuttu = "ei"
        hyokatty = "ei"
        if self._valittu_yksikko.liikkuminen_kaytetty:
            liikuttu = "kyllä"
        if self._valittu_yksikko.hyokkays_kaytetty:
            hyokatty = "kyllä"

        self._perustiedot.setText("Perustiedot:\n" + self._valittu_yksikko.ominaisuudet.__str__() +
                                 "\nLiikkuminen käytetty: " + liikuttu + "\n"
                                                                       "Hyökkäys käytetty: " + hyokatty)

        self._maaston_tiedot.setText("Maaston tiedot:\n" + self._valittu_yksikko.ruutu.maasto.__str__())

    def tyhjenna_valinta(self):
        if self._valittu_yksikko is not None:
            if self._valitsee_hyokkayksen_kohdetta is True:
                self._valittu_yksikko.peru_hyokkayksen_kohteiden_nayttaminen()
            if self._valittu_yksikko.kyky1_valitsee_kohteita:
                self._valittu_yksikko.peru_kyky1()
            if self._valittu_yksikko.kyky2_valitsee_kohteita:
                self._valittu_yksikko.peru_kyky2()
            self._valittu_yksikko.grafiikka.palauta_vari()
            self._valittu_yksikko = None
            self._yksikon_tiedot_aktiivinen = False
            self._perustiedot.setText("")
            for ruutu in self._pelinohjain.kartta.ruudut:
                ruutu.grafiikka.palauta_vari()

            # näytä peliloki
            self._peliloki.setText("PELILOKI:\n")

            # päivitä napit
            self.paivita_kykynapit()

    def paata_vuoro(self):
        if self._pelinohjain.vuoro == "PLR":
            self._pelinohjain.vaihda_vuoroa()

    # nayttaa tarkemmat tiedot yksiköstä
    def yksikon_tiedot(self):
        if self._yksikon_tiedot_aktiivinen:
            self._peliloki.setText("PELILOKI:\n")
            self._yksikon_tiedot_aktiivinen = False
        elif self._valittu_yksikko is not None:
            self._peliloki.setText("YKSIKON TIEDOT:\n" + self._valittu_yksikko.__str__())
            self._yksikon_tiedot_aktiivinen = True

    def edellinen_yksikko(self):
        if len(self._pelinohjain.kartta.pelaajan_toimivat_yksikot) == 0:
            return
        i = 0
        if self._valittu_yksikko is None:
            self.valitse_yksikko(self._pelinohjain.kartta.pelaajan_toimivat_yksikot[len(self._pelinohjain.kartta.
                                                                                        pelaajan_toimivat_yksikot) - 1])
        else:
            if self._valitsee_hyokkayksen_kohdetta:
                self.peru_valinta()
            indeksi = self._pelinohjain.kartta.pelaajan_yksikot.index(self._valittu_yksikko)
            while i < len(self._pelinohjain.kartta.pelaajan_toimivat_yksikot):
                if self._valittu_yksikko not in self._pelinohjain.kartta.pelaajan_toimivat_yksikot:
                    j = -1
                    if indeksi + j == -1:
                        self.valitse_yksikko(self._pelinohjain.kartta.pelaajan_toimivat_yksikot
                                             [len(self._pelinohjain.kartta.pelaajan_toimivat_yksikot) - 1])
                        return
                    valittu_yksikko = self._pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    while valittu_yksikko not in self._pelinohjain.kartta.pelaajan_toimivat_yksikot:
                        j -= 1
                        if indeksi + j == -1:
                            self.valitse_yksikko(self._pelinohjain.kartta.pelaajan_toimivat_yksikot
                                                 [len(self._pelinohjain.kartta.pelaajan_toimivat_yksikot) - 1])
                            return
                        valittu_yksikko = self._pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    self.valitse_yksikko(valittu_yksikko)
                    return
                elif self._pelinohjain.kartta.pelaajan_toimivat_yksikot[i] == self._valittu_yksikko:
                    if i == 0:
                        self.valitse_yksikko(self._pelinohjain.kartta.pelaajan_toimivat_yksikot
                                             [len(self._pelinohjain.kartta.pelaajan_toimivat_yksikot) - 1])
                        break
                    else:
                        self.valitse_yksikko(self._pelinohjain.kartta.pelaajan_toimivat_yksikot[i - 1])
                i += 1

    def seuraava_yksikko(self):
        if len(self._pelinohjain.kartta.pelaajan_toimivat_yksikot) == 0:
            return
        i = 0
        if self._valittu_yksikko is None:
            self.valitse_yksikko(self._pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
        else:
            if self._valitsee_hyokkayksen_kohdetta:
                self.peru_valinta()
            indeksi = self._pelinohjain.kartta.pelaajan_yksikot.index(self._valittu_yksikko)
            while i < len(self._pelinohjain.kartta.pelaajan_toimivat_yksikot):
                # jos ei toimivissa yksiköissä, etsitään seuraava yksikkö, joka on
                if self._valittu_yksikko not in self._pelinohjain.kartta.pelaajan_toimivat_yksikot:
                    j = 1
                    if indeksi + j == len(self._pelinohjain.kartta.pelaajan_yksikot):
                        self.valitse_yksikko(self._pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
                        return
                    valittu_yksikko = self._pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    while valittu_yksikko not in self._pelinohjain.kartta.pelaajan_toimivat_yksikot:
                        j += 1
                        if indeksi + j == len(self._pelinohjain.kartta.pelaajan_yksikot):
                            self.valitse_yksikko(self._pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
                            return
                        valittu_yksikko = self._pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    self.valitse_yksikko(valittu_yksikko)
                    return
                elif self._pelinohjain.kartta.pelaajan_toimivat_yksikot[i] == self._valittu_yksikko:
                    if i + 1 == len(self._pelinohjain.kartta.pelaajan_toimivat_yksikot):
                        self.valitse_yksikko(self._pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
                    else:
                        self.valitse_yksikko(self._pelinohjain.kartta.pelaajan_toimivat_yksikot[i + 1])
                        return
                i += 1

    def tallenna_peli(self):
        pass

    def peru_valinta(self):
        if self._valitsee_hyokkayksen_kohdetta is True:
            self.peru_kohteen_valinta()
            self._valittu_yksikko.nayta_mahdolliset_ruudut()
        elif self._valittu_yksikko is not None:
            if self._valittu_yksikko.kyky1_valitsee_kohteita:
                self._valittu_yksikko.peru_kyky1()
            elif self._valittu_yksikko.kyky2_valitsee_kohteita:
                self._valittu_yksikko.peru_kyky2()
            else:
                self.tyhjenna_valinta()

    def valitse_kohde(self):
        self._valitsee_hyokkayksen_kohdetta = True
        # värjää mahdolliset kohteet, poistaa ruutujen värjäyksen
        self._valittu_yksikko.peru_mahdollisten_ruutujen_nayttaminen()
        self._valittu_yksikko.laske_hyokkayksen_kohteet(True)

    def peru_kohteen_valinta(self):
        self._valittu_yksikko.peru_hyokkayksen_kohteiden_nayttaminen()
        self._valitsee_hyokkayksen_kohdetta = False

    def hyokkaa(self):
        # määrittelee valitaanko kohdetta vai perutaanko valinta
        if self._valittu_yksikko is not None and self._valitsee_hyokkayksen_kohdetta is False and \
                self._valittu_yksikko.hyokkays_kaytetty is False:
            if self._valittu_yksikko.kyky1_valitsee_kohteita:
                self._valittu_yksikko.peru_kyky1()
            if self._valittu_yksikko.kyky2_valitsee_kohteita:
                self._valittu_yksikko.peru_kyky2()
            self.valitse_kohde()
        elif self._valitsee_hyokkayksen_kohdetta:
            self.peru_kohteen_valinta()
            self._valittu_yksikko.nayta_mahdolliset_ruudut()

    def kyky_1(self):
        valitse = True
        if self._valittu_yksikko is not None and self._valittu_yksikko.ominaisuudet.nyk_energia >= self._valittu_yksikko.kyky1_hinta:
            if not self._valittu_yksikko.hyokkays_kaytetty:
                if self._valitsee_hyokkayksen_kohdetta:
                    self._valittu_yksikko.peru_hyokkayksen_kohteiden_nayttaminen()
                    self._valitsee_hyokkayksen_kohdetta = False
                if self._valittu_yksikko.kyky2_valitsee_kohteita:
                    self._valittu_yksikko.peru_kyky2()
                elif self._valittu_yksikko.kyky1_valitsee_kohteita:
                    self._valittu_yksikko.peru_kyky1()
                    valitse = False
                if valitse:
                    self._valittu_yksikko.kyky1()

    def kyky_2(self):
        valitse = True
        if self._valittu_yksikko is not None and \
                self._valittu_yksikko.ominaisuudet.nyk_energia >= self._valittu_yksikko.kyky2_hinta:
            if not self._valittu_yksikko.hyokkays_kaytetty:
                if self._valitsee_hyokkayksen_kohdetta:
                    self._valittu_yksikko.peru_hyokkayksen_kohteiden_nayttaminen()
                    self._valitsee_hyokkayksen_kohdetta = False
                if self._valittu_yksikko.kyky1_valitsee_kohteita:
                    self._valittu_yksikko.peru_kyky1()
                elif self._valittu_yksikko.kyky2_valitsee_kohteita:
                    self._valittu_yksikko.peru_kyky2()
                    valitse = False
                if valitse:
                    self._valittu_yksikko.kyky2()
