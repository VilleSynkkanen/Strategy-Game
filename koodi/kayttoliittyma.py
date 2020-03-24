from PyQt5 import QtWidgets, QtCore, QtGui, Qt

class Kayttoliittyma(QtWidgets.QMainWindow):
    '''
    Käyttöliittymä piirtää pelilaudan, napit ja tekstielementit
    '''
    def __init__(self, pelinohjain):
        super().__init__()
        self.scene_size = 880       #kentän koko pikseleinä
        self.pelinohjain = pelinohjain

        # toimintaan liittyviä muuttujia
        self.valittu_yksikko = None
        self.yksikon_tiedot_aktiivinen = False
        self.valitsee_hyokkayksen_kohdetta = False

        self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
        self.paa_layout = QtWidgets.QHBoxLayout()  # Horizontal main layout
        self.centralWidget().setLayout(self.paa_layout)

        # set window
        self.setGeometry(0, 0, self.scene_size + 420, self.scene_size)
        self.setWindowTitle('Strategiapeli')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()

        # Add a view for showing the scene
        self.nakyma = QtWidgets.QGraphicsView(self.scene, self)
        self.nakyma.adjustSize()
        self.nakyma.show()
        self.paa_layout.addWidget(self.nakyma)
        # main_layout.addStretch()

        self.nappi_layout = QtWidgets.QGridLayout()
        self.paa_layout.addLayout(self.nappi_layout)

        # buttons
        self.hyokkaa_nappi = QtWidgets.QPushButton("HYÖKKÄÄ")
        self.hyokkaa_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.kyky1_nappi = QtWidgets.QPushButton("KYKY 1")
        self.kyky1_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.kyky2_nappi = QtWidgets.QPushButton("KYKY 2")
        self.kyky2_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.peru_valinta_nappi = QtWidgets.QPushButton("PERU VALINTA")
        self.peru_valinta_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.yksikon_tiedot_nappi = QtWidgets.QPushButton("YKSIKÖN TIEDOT")
        self.yksikon_tiedot_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.edellinen_yksikko_nappi = QtWidgets.QPushButton("EDELLINEN YKSIKKÖ")
        self.edellinen_yksikko_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.seuraava_yksikko_nappi = QtWidgets.QPushButton("SEURAAVA YKSIKKÖ")
        self.seuraava_yksikko_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.paata_vuoro_nappi = QtWidgets.QPushButton("PÄÄTÄ VUORO")
        self.paata_vuoro_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.tallenna_peli_napi = QtWidgets.QPushButton("TALLENNA PELI")
        self.tallenna_peli_napi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.hyokkaa_nappi.setStyleSheet("font: 10pt Arial")
        self.kyky1_nappi.setStyleSheet("font: 10pt Arial")
        self.kyky2_nappi.setStyleSheet("font: 10pt Arial")
        self.peru_valinta_nappi.setStyleSheet("font: 10pt Arial")
        self.yksikon_tiedot_nappi.setStyleSheet("font: 10pt Arial")
        self.edellinen_yksikko_nappi.setStyleSheet("font: 10pt Arial")
        self.seuraava_yksikko_nappi.setStyleSheet("font: 10pt Arial")
        self.paata_vuoro_nappi.setStyleSheet("font: 10pt Arial")
        self.tallenna_peli_napi.setStyleSheet("font: 10pt Arial")

        # nappien yhdistäminen
        self.hyokkaa_nappi.clicked.connect(self.hyokkaa)
        self.kyky1_nappi.clicked.connect(self.kyky_1)
        self.kyky2_nappi.clicked.connect(self.kyky_2)
        self.peru_valinta_nappi.clicked.connect(self.peru_valinta)
        self.paata_vuoro_nappi.clicked.connect(self.paata_vuoro)
        self.yksikon_tiedot_nappi.clicked.connect(self.yksikon_tiedot)
        self.edellinen_yksikko_nappi.clicked.connect(self.edellinen_yksikko)
        self.seuraava_yksikko_nappi.clicked.connect(self.seuraava_yksikko)
        self.tallenna_peli_napi.clicked.connect(self.tallenna_peli)

        # add button widgets
        self.nappi_layout.addWidget(self.hyokkaa_nappi, 0, 0, 1, 2)
        self.nappi_layout.addWidget(self.kyky1_nappi, 1, 0)
        self.nappi_layout.addWidget(self.kyky2_nappi, 1, 1)
        self.nappi_layout.addWidget(self.peru_valinta_nappi, 2, 0)
        self.nappi_layout.addWidget(self.yksikon_tiedot_nappi, 2, 1)
        self.nappi_layout.addWidget(self.edellinen_yksikko_nappi, 3, 0)
        self.nappi_layout.addWidget(self.seuraava_yksikko_nappi, 3, 1)
        self.nappi_layout.addWidget(self.paata_vuoro_nappi, 4, 0)
        self.nappi_layout.addWidget(self.tallenna_peli_napi, 4, 1)

        # unit info
        self.perustiedot = QtWidgets.QLabel("")
        self.nappi_layout.addWidget(self.perustiedot, 5, 0, 1, 1, alignment=QtCore.Qt.AlignTop)
        self.perustiedot.setStyleSheet("font: 9pt Arial")
        self.perustiedot.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # maaston info
        self.maaston_tiedot = QtWidgets.QLabel("")
        self.nappi_layout.addWidget(self.maaston_tiedot, 5, 1, 1, 1, alignment=QtCore.Qt.AlignTop)
        self.maaston_tiedot.setStyleSheet("font: 9pt Arial")
        self.maaston_tiedot.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # game log test
        self.peliloki = QtWidgets.QLabel("PELILOKI:\n", self)
        self.nappi_layout.addWidget(self.peliloki,6, 0, 6, 2, alignment=QtCore.Qt.AlignTop)
        self.peliloki.setStyleSheet("font: 9pt Arial")

        self.ohjeteksti = QtWidgets.QLabel("OHJETEKSTI\n", self)
        self.nappi_layout.addWidget(self.ohjeteksti, 11, 0, 1, 0, alignment=QtCore.Qt.AlignTop)
        self.ohjeteksti.setStyleSheet("font: 9pt Arial")

    def aseta_scene_rect(self, x, y):
        # rectin skaalauskertoimet
        if x > y:
            y /= x
            x = 1
        else:
            x /= y
            y = 1
        self.scene.setSceneRect(0, 0, self.scene_size * x, self.scene_size * y)
        #self.setGeometry(0, 0, self.scene_size * x + 420, self.scene_size * y + 20)

        # keskelle liikuttaminen
        res_x = 1920
        res_y = 1080
        self.move((res_x / 2) - (self.frameSize().width() / 2),
                  (res_y / 2) - (self.frameSize().height() / 2))


    def valitse_yksikko(self, yksikko):
        self.tyhjenna_valinta()
        # valinnan muuttaminen
        self.valittu_yksikko = yksikko

        liikuttu = "ei"
        hyokatty = "ei"
        if self.valittu_yksikko.liikkuminen_kaytetty:
            liikuttu = "kyllä"
        if self.valittu_yksikko.hyokkays_kaytetty:
            hyokatty = "kyllä"

        # näytä tiedot
        self.paivita_valitun_yksikon_tiedot()
        self.paivita_kykynapit()

        # näytä peliloki
        self.peliloki.setText("PELILOKI:\n")

        yksikko.grafiikka.muuta_varia(yksikko.grafiikka.pelaaja_valittu_vari)
        # vanhan valinnan värin muutos tehdään, kun valinta tyhjennetään (jos yksikkö ei voi tehdä mitään, väri on eri)
        for yks in self.pelinohjain.kartta.pelaajan_yksikot:
            if yks != self.valittu_yksikko:
                yks.grafiikka.palauta_vari()
        for ruutu in self.pelinohjain.kartta.ruudut:
            ruutu.grafiikka.palauta_vari()

        # polkujen näyttäminen
        if not self.valittu_yksikko.liikkuminen_kaytetty:
            self.valittu_yksikko.laske_mahdolliset_ruudut()
        self.valittu_yksikko.nayta_mahdolliset_ruudut()

    def paivita_kykynapit(self):
        if self.valittu_yksikko is not None:
            self.kyky1_nappi.setText(self.valittu_yksikko.kyky1_nappi_tiedot())
            self.kyky2_nappi.setText(self.valittu_yksikko.kyky2_nappi_tiedot())
        else:
            self.kyky1_nappi.setText("KYKY 1")
            self.kyky2_nappi.setText("KYKY 2")

    def paivita_valitun_yksikon_tiedot(self):
        liikuttu = "ei"
        hyokatty = "ei"
        if self.valittu_yksikko.liikkuminen_kaytetty:
            liikuttu = "kyllä"
        if self.valittu_yksikko.hyokkays_kaytetty:
            hyokatty = "kyllä"

        self.perustiedot.setText("Perustiedot:\n" + self.valittu_yksikko.ominaisuudet.__str__() +
                                 "\nLiikkuminen käytetty: " + liikuttu + "\n"
                                                                       "Hyökkäys käytetty: " + hyokatty)

        self.maaston_tiedot.setText("Maaston tiedot:\n" + self.valittu_yksikko.ruutu.maasto.__str__())

    def tyhjenna_valinta(self):
        if self.valittu_yksikko is not None:
            if self.valitsee_hyokkayksen_kohdetta is True:
                self.valittu_yksikko.peru_hyokkayksen_kohteiden_nayttaminen()
                self.valittu_yksikko.grafiikka.palauta_vari()
            if self.valittu_yksikko.kyky1_valitsee_kohteita:
                self.valittu_yksikko.peru_kyky1()
            if self.valittu_yksikko.kyky2_valitsee_kohteita:
                self.valittu_yksikko.peru_kyky2()
            self.valittu_yksikko = None
            self.yksikon_tiedot_aktiivinen = False
            self.perustiedot.setText("")
            for ruutu in self.pelinohjain.kartta.ruudut:
                ruutu.grafiikka.palauta_vari()

            # näytä peliloki
            self.peliloki.setText("PELILOKI:\n")

            # päivitä napit
            self.paivita_kykynapit()

    def paata_vuoro(self):
        self.pelinohjain.vuoron_alku()

    # nayttaa tarkemmat tiedot yksiköstä
    def yksikon_tiedot(self):
        if self.yksikon_tiedot_aktiivinen:
            self.peliloki.setText("PELILOKI:\n")
            self.yksikon_tiedot_aktiivinen = False
        elif self.valittu_yksikko is not None:
            self.peliloki.setText("YKSIKON TIEDOT:\n" + self.valittu_yksikko.__str__())
            self.yksikon_tiedot_aktiivinen = True

    def edellinen_yksikko(self):
        if len(self.pelinohjain.kartta.pelaajan_toimivat_yksikot) == 0:
            return
        i = 0
        if self.valittu_yksikko is None:
            self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_toimivat_yksikot[len(self.pelinohjain.kartta.
                                                                                    pelaajan_toimivat_yksikot) - 1])
        else:
            if self.valitsee_hyokkayksen_kohdetta:
                self.peru_valinta()
            indeksi = self.pelinohjain.kartta.pelaajan_yksikot.index(self.valittu_yksikko)
            while i < len(self.pelinohjain.kartta.pelaajan_toimivat_yksikot):
                if self.valittu_yksikko not in self.pelinohjain.kartta.pelaajan_toimivat_yksikot:
                    j = -1
                    if indeksi + j == -1:
                        self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_toimivat_yksikot
                                             [len(self.pelinohjain.kartta.pelaajan_toimivat_yksikot) - 1])
                        return
                    valittu_yksikko = self.pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    while valittu_yksikko not in self.pelinohjain.kartta.pelaajan_toimivat_yksikot:
                        j -= 1
                        if indeksi + j == -1:
                            self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_toimivat_yksikot
                                                 [len(self.pelinohjain.kartta.pelaajan_toimivat_yksikot) - 1])
                            return
                        valittu_yksikko = self.pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    self.valitse_yksikko(valittu_yksikko)
                    return
                elif self.pelinohjain.kartta.pelaajan_toimivat_yksikot[i] == self.valittu_yksikko:
                    if i == 0:
                        self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_toimivat_yksikot
                                             [len(self.pelinohjain.kartta.pelaajan_toimivat_yksikot) - 1])
                        break
                    else:
                        self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_toimivat_yksikot[i - 1])
                i += 1

    def seuraava_yksikko(self):
        if len(self.pelinohjain.kartta.pelaajan_toimivat_yksikot) == 0:
            return
        i = 0
        if self.valittu_yksikko is None:
            self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
        else:
            if self.valitsee_hyokkayksen_kohdetta:
                self.peru_valinta()
            indeksi = self.pelinohjain.kartta.pelaajan_yksikot.index(self.valittu_yksikko)
            while i < len(self.pelinohjain.kartta.pelaajan_toimivat_yksikot):
                # jos ei toimivissa yksiköissä, etsitään seuraava yksikkö, joka on
                if self.valittu_yksikko not in self.pelinohjain.kartta.pelaajan_toimivat_yksikot:
                    j = 1
                    if indeksi + j == len(self.pelinohjain.kartta.pelaajan_yksikot):
                        self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
                        return
                    valittu_yksikko = self.pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    while valittu_yksikko not in self.pelinohjain.kartta.pelaajan_toimivat_yksikot:
                        j += 1
                        if indeksi + j == len(self.pelinohjain.kartta.pelaajan_yksikot):
                            self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
                            return
                        valittu_yksikko = self.pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    self.valitse_yksikko(valittu_yksikko)
                    return
                elif self.pelinohjain.kartta.pelaajan_toimivat_yksikot[i] == self.valittu_yksikko:
                    if i + 1 == len(self.pelinohjain.kartta.pelaajan_toimivat_yksikot):
                        self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
                    else:
                        self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_toimivat_yksikot[i + 1])
                        return
                i += 1

    def tallenna_peli(self):
        pass

    def peru_valinta(self):
        if self.valitsee_hyokkayksen_kohdetta is True:
            self.peru_kohteen_valinta()
            self.valittu_yksikko.nayta_mahdolliset_ruudut()
        elif self.valittu_yksikko is not None:
            if self.valittu_yksikko.kyky1_valitsee_kohteita:
                self.valittu_yksikko.peru_kyky1()
            elif self.valittu_yksikko.kyky2_valitsee_kohteita:
                self.valittu_yksikko.peru_kyky2()
            else:
                self.tyhjenna_valinta()

    def valitse_kohde(self):
        self.valitsee_hyokkayksen_kohdetta = True
        # värjää mahdolliset kohteet, poistaa ruutujen värjäyksen
        self.valittu_yksikko.peru_mahdollisten_ruutujen_nayttaminen()
        self.valittu_yksikko.laske_hyokkayksen_kohteet(True)

    def peru_kohteen_valinta(self):
        self.valittu_yksikko.peru_hyokkayksen_kohteiden_nayttaminen()
        self.valitsee_hyokkayksen_kohdetta = False

    def hyokkaa(self):
        # määrittelee valitaanko kohdetta vai perutaanko valinta
        if self.valittu_yksikko is not None and self.valitsee_hyokkayksen_kohdetta is False and \
                self.valittu_yksikko.hyokkays_kaytetty is False:
            self.valitse_kohde()
        elif self.valitsee_hyokkayksen_kohdetta:
            self.peru_kohteen_valinta()
            self.valittu_yksikko.nayta_mahdolliset_ruudut()

    def kyky_1(self):
        valitse = True
        if self.valittu_yksikko is not None and self.valittu_yksikko.ominaisuudet.nyk_energia >= self.valittu_yksikko.kyky1_hinta:
            if not self.valittu_yksikko.hyokkays_kaytetty:
                if self.valittu_yksikko.kyky2_valitsee_kohteita:
                    self.valittu_yksikko.peru_kyky2()
                elif self.valittu_yksikko.kyky1_valitsee_kohteita:
                    self.valittu_yksikko.peru_kyky1()
                    valitse = False
                if valitse:
                    self.valittu_yksikko.kyky1()

    def kyky_2(self):
        valitse = True
        if self.valittu_yksikko is not None and self.valittu_yksikko.ominaisuudet.nyk_energia >= self.valittu_yksikko.kyky2_hinta:
            if not self.valittu_yksikko.hyokkays_kaytetty:
                if self.valittu_yksikko.kyky1_valitsee_kohteita:
                    self.valittu_yksikko.peru_kyky1()
                elif self.valittu_yksikko.kyky2_valitsee_kohteita:
                    self.valittu_yksikko.peru_kyky2()
                    valitse = False
                if valitse:
                    self.valittu_yksikko.kyky2()