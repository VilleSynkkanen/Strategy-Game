from PyQt5 import QtWidgets, QtCore, QtGui, Qt

class Kayttoliittyma(QtWidgets.QMainWindow):
    '''
    Käyttöliittymä piirtää pelilaudan, napit ja tekstielementit
    '''
    def __init__(self, pelinohjain):
        super().__init__()
        self.__scene_size = 880       # kentän koko pikseleinä
        self.__pelinohjain = pelinohjain

        # toimintaan liittyviä muuttujia
        self.__valittu_yksikko = None
        self.__yksikon_tiedot_aktiivinen = False
        self.__valitsee_hyokkayksen_kohdetta = False

        self.setCentralWidget(QtWidgets.QWidget())  # QMainWindown must have a centralWidget to be able to add layouts
        self.__paa_layout = QtWidgets.QHBoxLayout()  # Horizontal main layout
        self.centralWidget().setLayout(self.__paa_layout)

        # set window
        self.setGeometry(0, 0, self.__scene_size + 420, self.__scene_size)
        self.setWindowTitle('Strategiapeli')
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

        # buttons
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

        self.__hyokkaa_nappi.setStyleSheet("font: 10pt Arial")
        self.__kyky1_nappi.setStyleSheet("font: 10pt Arial")
        self.__kyky2_nappi.setStyleSheet("font: 10pt Arial")
        self.__peru_valinta_nappi.setStyleSheet("font: 10pt Arial")
        self.__yksikon_tiedot_nappi.setStyleSheet("font: 10pt Arial")
        self.__edellinen_yksikko_nappi.setStyleSheet("font: 10pt Arial")
        self.__seuraava_yksikko_nappi.setStyleSheet("font: 10pt Arial")
        self.__paata_vuoro_nappi.setStyleSheet("font: 10pt Arial")
        self.__tallenna_peli_napi.setStyleSheet("font: 10pt Arial")

        # nappien yhdistäminen
        self.__hyokkaa_nappi.clicked.connect(self.__hyokkaa)
        self.__kyky1_nappi.clicked.connect(self.__kyky_1)
        self.__kyky2_nappi.clicked.connect(self.__kyky_2)
        self.__peru_valinta_nappi.clicked.connect(self.__peru_valinta)
        self.__paata_vuoro_nappi.clicked.connect(self.__paata_vuoro)
        self.__yksikon_tiedot_nappi.clicked.connect(self.__yksikon_tiedot)
        self.__edellinen_yksikko_nappi.clicked.connect(self.__edellinen_yksikko)
        self.__seuraava_yksikko_nappi.clicked.connect(self.__seuraava_yksikko)
        self.__tallenna_peli_napi.clicked.connect(self.__tallenna_peli)

        # add button widgets
        self.__nappi_layout.addWidget(self.__hyokkaa_nappi, 0, 0, 1, 2)
        self.__nappi_layout.addWidget(self.__kyky1_nappi, 1, 0)
        self.__nappi_layout.addWidget(self.__kyky2_nappi, 1, 1)
        self.__nappi_layout.addWidget(self.__peru_valinta_nappi, 2, 0)
        self.__nappi_layout.addWidget(self.__yksikon_tiedot_nappi, 2, 1)
        self.__nappi_layout.addWidget(self.__edellinen_yksikko_nappi, 3, 0)
        self.__nappi_layout.addWidget(self.__seuraava_yksikko_nappi, 3, 1)
        self.__nappi_layout.addWidget(self.__paata_vuoro_nappi, 4, 0)
        self.__nappi_layout.addWidget(self.__tallenna_peli_napi, 4, 1)

        # unit info
        self.__perustiedot = QtWidgets.QLabel("")
        self.__nappi_layout.addWidget(self.__perustiedot, 5, 0, 1, 1, alignment=QtCore.Qt.AlignTop)
        self.__perustiedot.setStyleSheet("font: 9pt Arial")
        self.__perustiedot.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # maaston info
        self.__maaston_tiedot = QtWidgets.QLabel("")
        self.__nappi_layout.addWidget(self.__maaston_tiedot, 5, 1, 1, 1, alignment=QtCore.Qt.AlignTop)
        self.__maaston_tiedot.setStyleSheet("font: 9pt Arial")
        self.__maaston_tiedot.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # game log test
        self.__peliloki = QtWidgets.QLabel("PELILOKI:\n", self)
        self.__nappi_layout.addWidget(self.__peliloki, 6, 0, 6, 2, alignment=QtCore.Qt.AlignTop)
        self.__peliloki.setStyleSheet("font: 9pt Arial")

        self.__ohjeteksti = QtWidgets.QLabel("OHJETEKSTI\n", self)
        self.__nappi_layout.addWidget(self.__ohjeteksti, 11, 0, 1, 0, alignment=QtCore.Qt.AlignTop)
        self.__ohjeteksti.setStyleSheet("font: 9pt Arial")

    @property
    def pelinohjain(self):
        return self.__pelinohjain

    @property
    def scene_size(self):
        return self.__scene_size

    @property
    def valittu_yksikko(self):
        return self.__valittu_yksikko

    @property
    def yksikon_tiedot_aktiivinen(self):
        return self.__yksikon_tiedot_aktiivinen

    @property
    def valitsee_hyokkayksen_kohdetta(self):
        return self.__valitsee_hyokkayksen_kohdetta

    @property
    def scene(self):
        return self.__scene

    def aseta_scene_rect(self, x, y):
        # rectin skaalauskertoimet
        if x > y:
            y /= x
            x = 1
        else:
            x /= y
            y = 1
        self.__scene.setSceneRect(0, 0, self.__scene_size * x, self.__scene_size * y)
        #self.setGeometry(0, 0, self.scene_size * x + 420, self.scene_size * y + 20)

        # keskelle liikuttaminen
        res_x = 1920
        res_y = 1080
        self.move((res_x / 2) - (self.frameSize().width() / 2),
                  (res_y / 2) - (self.frameSize().height() / 2))


    def valitse_yksikko(self, yksikko):
        self.tyhjenna_valinta()
        # valinnan muuttaminen
        self.__valittu_yksikko = yksikko

        liikuttu = "ei"
        hyokatty = "ei"
        if self.__valittu_yksikko.liikkuminen_kaytetty:
            liikuttu = "kyllä"
        if self.__valittu_yksikko.hyokkays_kaytetty:
            hyokatty = "kyllä"

        # näytä tiedot
        self.paivita_valitun_yksikon_tiedot()
        self.__paivita_kykynapit()

        # näytä peliloki
        self.__peliloki.setText("PELILOKI:\n")

        yksikko.grafiikka.muuta_varia(yksikko.grafiikka.pelaaja_valittu_vari)
        # vanhan valinnan värin muutos tehdään, kun valinta tyhjennetään (jos yksikkö ei voi tehdä mitään, väri on eri)
        for yks in self.__pelinohjain.kartta.pelaajan_yksikot:
            if yks != self.__valittu_yksikko:
                yks.grafiikka.palauta_vari()
        for ruutu in self.__pelinohjain.kartta.ruudut:
            ruutu.grafiikka.palauta_vari()

        # polkujen näyttäminen
        if not self.__valittu_yksikko.liikkuminen_kaytetty:
            self.__valittu_yksikko.laske_mahdolliset_ruudut()
        self.__valittu_yksikko.nayta_mahdolliset_ruudut()

    def __paivita_kykynapit(self):
        if self.__valittu_yksikko is not None:
            self.__kyky1_nappi.setText(self.__valittu_yksikko.kyky1_nappi_tiedot())
            self.__kyky2_nappi.setText(self.__valittu_yksikko.kyky2_nappi_tiedot())
        else:
            self.__kyky1_nappi.setText("KYKY 1")
            self.__kyky2_nappi.setText("KYKY 2")

    def paivita_valitun_yksikon_tiedot(self):
        liikuttu = "ei"
        hyokatty = "ei"
        if self.__valittu_yksikko.liikkuminen_kaytetty:
            liikuttu = "kyllä"
        if self.__valittu_yksikko.hyokkays_kaytetty:
            hyokatty = "kyllä"

        self.__perustiedot.setText("Perustiedot:\n" + self.__valittu_yksikko.ominaisuudet.__str__() +
                                 "\nLiikkuminen käytetty: " + liikuttu + "\n"
                                                                       "Hyökkäys käytetty: " + hyokatty)

        self.__maaston_tiedot.setText("Maaston tiedot:\n" + self.__valittu_yksikko.ruutu.maasto.__str__())

    def tyhjenna_valinta(self):
        if self.__valittu_yksikko is not None:
            if self.__valitsee_hyokkayksen_kohdetta is True:
                self.__valittu_yksikko.peru_hyokkayksen_kohteiden_nayttaminen()
            if self.__valittu_yksikko.kyky1_valitsee_kohteita:
                self.__valittu_yksikko.peru_kyky1()
            if self.__valittu_yksikko.kyky2_valitsee_kohteita:
                self.__valittu_yksikko.peru_kyky2()
            self.__valittu_yksikko.grafiikka.palauta_vari()
            self.__valittu_yksikko = None
            self.__yksikon_tiedot_aktiivinen = False
            self.__perustiedot.setText("")
            for ruutu in self.__pelinohjain.kartta.ruudut:
                ruutu.grafiikka.palauta_vari()

            # näytä peliloki
            self.__peliloki.setText("PELILOKI:\n")

            # päivitä napit
            self.__paivita_kykynapit()

    def __paata_vuoro(self):
        if self.__pelinohjain.vuoro == "PLR":
            self.__pelinohjain.vaihda_vuoroa()

    # nayttaa tarkemmat tiedot yksiköstä
    def __yksikon_tiedot(self):
        if self.__yksikon_tiedot_aktiivinen:
            self.__peliloki.setText("PELILOKI:\n")
            self.__yksikon_tiedot_aktiivinen = False
        elif self.__valittu_yksikko is not None:
            self.__peliloki.setText("YKSIKON TIEDOT:\n" + self.__valittu_yksikko.__str__())
            self.__yksikon_tiedot_aktiivinen = True

    def __edellinen_yksikko(self):
        if len(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot) == 0:
            return
        i = 0
        if self.__valittu_yksikko is None:
            self.valitse_yksikko(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot[len(self.__pelinohjain.kartta.
                                                                                         pelaajan_toimivat_yksikot) - 1])
        else:
            if self.__valitsee_hyokkayksen_kohdetta:
                self.__peru_valinta()
            indeksi = self.__pelinohjain.kartta.pelaajan_yksikot.index(self.__valittu_yksikko)
            while i < len(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot):
                if self.__valittu_yksikko not in self.__pelinohjain.kartta.pelaajan_toimivat_yksikot:
                    j = -1
                    if indeksi + j == -1:
                        self.valitse_yksikko(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot
                                             [len(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot) - 1])
                        return
                    valittu_yksikko = self.__pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    while valittu_yksikko not in self.__pelinohjain.kartta.pelaajan_toimivat_yksikot:
                        j -= 1
                        if indeksi + j == -1:
                            self.valitse_yksikko(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot
                                                 [len(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot) - 1])
                            return
                        valittu_yksikko = self.__pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    self.valitse_yksikko(valittu_yksikko)
                    return
                elif self.__pelinohjain.kartta.pelaajan_toimivat_yksikot[i] == self.__valittu_yksikko:
                    if i == 0:
                        self.valitse_yksikko(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot
                                             [len(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot) - 1])
                        break
                    else:
                        self.valitse_yksikko(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot[i - 1])
                i += 1

    def __seuraava_yksikko(self):
        if len(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot) == 0:
            return
        i = 0
        if self.__valittu_yksikko is None:
            self.valitse_yksikko(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
        else:
            if self.__valitsee_hyokkayksen_kohdetta:
                self.__peru_valinta()
            indeksi = self.__pelinohjain.kartta.pelaajan_yksikot.index(self.__valittu_yksikko)
            while i < len(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot):
                # jos ei toimivissa yksiköissä, etsitään seuraava yksikkö, joka on
                if self.__valittu_yksikko not in self.__pelinohjain.kartta.pelaajan_toimivat_yksikot:
                    j = 1
                    if indeksi + j == len(self.__pelinohjain.kartta.pelaajan_yksikot):
                        self.valitse_yksikko(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
                        return
                    valittu_yksikko = self.__pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    while valittu_yksikko not in self.__pelinohjain.kartta.pelaajan_toimivat_yksikot:
                        j += 1
                        if indeksi + j == len(self.__pelinohjain.kartta.pelaajan_yksikot):
                            self.valitse_yksikko(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
                            return
                        valittu_yksikko = self.__pelinohjain.kartta.pelaajan_yksikot[indeksi + j]
                    self.valitse_yksikko(valittu_yksikko)
                    return
                elif self.__pelinohjain.kartta.pelaajan_toimivat_yksikot[i] == self.__valittu_yksikko:
                    if i + 1 == len(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot):
                        self.valitse_yksikko(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot[0])
                    else:
                        self.valitse_yksikko(self.__pelinohjain.kartta.pelaajan_toimivat_yksikot[i + 1])
                        return
                i += 1

    def __tallenna_peli(self):
        pass

    def __peru_valinta(self):
        if self.__valitsee_hyokkayksen_kohdetta is True:
            self.peru_kohteen_valinta()
            self.__valittu_yksikko.nayta_mahdolliset_ruudut()
        elif self.__valittu_yksikko is not None:
            if self.__valittu_yksikko.kyky1_valitsee_kohteita:
                self.__valittu_yksikko.peru_kyky1()
            elif self.__valittu_yksikko.kyky2_valitsee_kohteita:
                self.__valittu_yksikko.peru_kyky2()
            else:
                self.tyhjenna_valinta()

    def __valitse_kohde(self):
        self.__valitsee_hyokkayksen_kohdetta = True
        # värjää mahdolliset kohteet, poistaa ruutujen värjäyksen
        self.__valittu_yksikko.peru_mahdollisten_ruutujen_nayttaminen()
        self.__valittu_yksikko.laske_hyokkayksen_kohteet(True)

    def peru_kohteen_valinta(self):
        self.__valittu_yksikko.peru_hyokkayksen_kohteiden_nayttaminen()
        self.__valitsee_hyokkayksen_kohdetta = False

    def __hyokkaa(self):
        # määrittelee valitaanko kohdetta vai perutaanko valinta
        if self.__valittu_yksikko is not None and self.__valitsee_hyokkayksen_kohdetta is False and \
                self.__valittu_yksikko.hyokkays_kaytetty is False:
            if self.__valittu_yksikko.kyky1_valitsee_kohteita:
                self.__valittu_yksikko.peru_kyky1()
            if self.__valittu_yksikko.kyky2_valitsee_kohteita:
                self.__valittu_yksikko.peru_kyky2()
            self.__valitse_kohde()
        elif self.__valitsee_hyokkayksen_kohdetta:
            self.peru_kohteen_valinta()
            self.__valittu_yksikko.nayta_mahdolliset_ruudut()

    def __kyky_1(self):
        valitse = True
        if self.__valittu_yksikko is not None and \
                self.__valittu_yksikko.ominaisuudet.nyk_energia >= self.__valittu_yksikko.kyky1_hinta:
            if not self.__valittu_yksikko.hyokkays_kaytetty:
                if self.__valitsee_hyokkayksen_kohdetta:
                    self.__valittu_yksikko.peru_hyokkayksen_kohteiden_nayttaminen()
                    self.__valitsee_hyokkayksen_kohdetta = False
                if self.__valittu_yksikko.kyky2_valitsee_kohteita:
                    self.__valittu_yksikko.peru_kyky2()
                elif self.__valittu_yksikko.kyky1_valitsee_kohteita:
                    self.__valittu_yksikko.peru_kyky1()
                    valitse = False
                if valitse:
                    self.__valittu_yksikko.kyky1()

    def __kyky_2(self):
        valitse = True
        if self.__valittu_yksikko is not None and \
                self.__valittu_yksikko.ominaisuudet.nyk_energia >= self.__valittu_yksikko.kyky2_hinta:
            if not self.__valittu_yksikko.hyokkays_kaytetty:
                if self.__valitsee_hyokkayksen_kohdetta:
                    self.__valittu_yksikko.peru_hyokkayksen_kohteiden_nayttaminen()
                    self.__valitsee_hyokkayksen_kohdetta = False
                if self.__valittu_yksikko.kyky1_valitsee_kohteita:
                    self.__valittu_yksikko.peru_kyky1()
                elif self.__valittu_yksikko.kyky2_valitsee_kohteita:
                    self.__valittu_yksikko.peru_kyky2()
                    valitse = False
                if valitse:
                    self.__valittu_yksikko.kyky2()
