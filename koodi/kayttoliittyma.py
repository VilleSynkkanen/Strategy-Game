from PyQt5 import QtWidgets, QtCore, QtGui, Qt

class Kayttoliittyma(QtWidgets.QMainWindow):
    '''
    The class GUI handles the drawing of the board and buttons
    '''
    def __init__(self, pelinohjain):
        super().__init__()
        self.scene_size = 880       #kentän koko pikseleinä
        self.pelinohjain = pelinohjain

        # toimintaan liittyviä muuttujia
        self.valittu_yksikko = None
        self.yksikon_tiedot_aktiivinen = False


        self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
        main_layout = QtWidgets.QHBoxLayout()  # Horizontal main layout
        self.centralWidget().setLayout(main_layout)

        # set window
        self.setGeometry(0, 0, self.scene_size + 420, self.scene_size)
        self.setWindowTitle('Strategiapeli')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()

        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        main_layout.addWidget(self.view)
        # main_layout.addStretch()

        nappi_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(nappi_layout)

        # buttons
        button1 = QtWidgets.QPushButton("HYÖKKÄÄ")
        button1.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button2 = QtWidgets.QPushButton("KYKY 1")
        button2.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button3 = QtWidgets.QPushButton("KYKY 2")
        button3.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        peru_valinta_nappi = QtWidgets.QPushButton("PERU VALINTA")
        peru_valinta_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        yksikon_tiedot_nappi = QtWidgets.QPushButton("YKSIKÖN TIEDOT")
        yksikon_tiedot_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        edellinen_yksikko_nappi = QtWidgets.QPushButton("EDELLINEN YKSIKKÖ")
        edellinen_yksikko_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        seuraava_yksikko_nappi = QtWidgets.QPushButton("SEURAAVA YKSIKKÖ")
        seuraava_yksikko_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        paata_vuoro_nappi = QtWidgets.QPushButton("PÄÄTÄ VUORO")
        paata_vuoro_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        tallenna_peli_napi = QtWidgets.QPushButton("TALLENNA PELI")
        tallenna_peli_napi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        button1.setStyleSheet("font: 10pt Arial")
        button2.setStyleSheet("font: 10pt Arial")
        button3.setStyleSheet("font: 10pt Arial")
        peru_valinta_nappi.setStyleSheet("font: 10pt Arial")
        yksikon_tiedot_nappi.setStyleSheet("font: 10pt Arial")
        edellinen_yksikko_nappi.setStyleSheet("font: 10pt Arial")
        seuraava_yksikko_nappi.setStyleSheet("font: 10pt Arial")
        paata_vuoro_nappi.setStyleSheet("font: 10pt Arial")
        tallenna_peli_napi.setStyleSheet("font: 10pt Arial")

        # nappien yhdistäminen
        peru_valinta_nappi.clicked.connect(self.peru_valinta)
        paata_vuoro_nappi.clicked.connect(self.paata_vuoro)
        yksikon_tiedot_nappi.clicked.connect(self.yksikon_tiedot)
        edellinen_yksikko_nappi.clicked.connect(self.edellinen_yksikko)
        seuraava_yksikko_nappi.clicked.connect(self.seuraava_yksikko)
        tallenna_peli_napi.clicked.connect(self.tallenna_peli)

        # add button widgets
        nappi_layout.addWidget(button1, 0, 0, 1, 2)
        nappi_layout.addWidget(button2, 1, 0)
        nappi_layout.addWidget(button3, 1, 1)
        nappi_layout.addWidget(peru_valinta_nappi, 2, 0)
        nappi_layout.addWidget(yksikon_tiedot_nappi, 2, 1)
        nappi_layout.addWidget(edellinen_yksikko_nappi, 3, 0)
        nappi_layout.addWidget(seuraava_yksikko_nappi, 3, 1)
        nappi_layout.addWidget(paata_vuoro_nappi, 4, 0)
        nappi_layout.addWidget(tallenna_peli_napi, 4, 1)

        # unit info
        self.perustiedot = QtWidgets.QLabel("")
        nappi_layout.addWidget(self.perustiedot, 5, 0, 1, 1)
        self.perustiedot.setStyleSheet("font: 10pt Arial")
        self.perustiedot.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        # game log test
        self.peliloki = QtWidgets.QLabel("PELILOKI:\n", self)
        nappi_layout.addWidget(self.peliloki,6, 0, 6, 2, alignment=QtCore.Qt.AlignTop)
        self.peliloki.setStyleSheet("font: 10pt Arial")

        ohjeteksti = QtWidgets.QLabel("OHJETEKSTI\n", self)
        nappi_layout.addWidget(ohjeteksti, 11, 0, 1, 0, alignment=QtCore.Qt.AlignTop)
        ohjeteksti.setStyleSheet("font: 10pt Arial")

    def set_scene_rect(self, x, y):
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
        # valinnan muuttaminen
        self.valittu_yksikko = yksikko

        # näytä tiedot
        self.perustiedot.setText("Perustiedot:\n" + self.valittu_yksikko.ominaisuudet.__str__())

        # näytä peliloki
        self.peliloki.setText("PELILOKI:\n")

        yksikko.grafiikka.muuta_varia(yksikko.grafiikka.pelaaja_valittu_vari)
        for yks in self.pelinohjain.kartta.pelaajan_yksikot:
            if yks != self.valittu_yksikko:
                yks.grafiikka.muuta_varia(yks.grafiikka.pelaajan_vari)
        for ruutu in self.pelinohjain.kartta.ruudut:
            ruutu.grafiikka.palauta_vari()

        # polkujen näyttäminen
        if not self.valittu_yksikko.liikkuminen_kaytetty:
            self.valittu_yksikko.laske_mahdolliset_ruudut()
        self.valittu_yksikko.nayta_mahdolliset_ruudut()

    def tyhjenna_valinta(self):
        if self.valittu_yksikko is not None:
            self.valittu_yksikko.grafiikka.palauta_vari()
            self.valittu_yksikko = None
            self.perustiedot.setText("")
            for ruutu in self.pelinohjain.kartta.ruudut:
                ruutu.grafiikka.palauta_vari()

            # näytä peliloki
            self.peliloki.setText("PELILOKI:\n")


    def paata_vuoro(self):
        self.pelinohjain.vuoron_alku()

    # nayttaa tarkemmat tiedot yksiköstä
    def yksikon_tiedot(self):
        if self.yksikon_tiedot_aktiivinen:
            self.peliloki.setText("PELILOKI:\n")
            self.yksikon_tiedot_aktiivinen = False
        elif self.valittu_yksikko is not None:
            self.peliloki.setText("YKSIKON TIEDOT:\n")
            self.yksikon_tiedot_aktiivinen = True

    # kutsu vain, jos yksiköitä on ainakin yksi
    def edellinen_yksikko(self):
        i = 0
        if self.valittu_yksikko is None:
            self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_yksikot[len(self.pelinohjain.kartta.pelaajan_yksikot) - 1])
            print("none")
        else:
            while i < len(self.pelinohjain.kartta.pelaajan_yksikot):
                if self.pelinohjain.kartta.pelaajan_yksikot[i] == self.valittu_yksikko:
                    print(i)
                    if i == 0:
                        self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_yksikot
                                             [len(self.pelinohjain.kartta.pelaajan_yksikot) - 1])
                        break
                    else:
                        self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_yksikot[i - 1])
                i += 1

    def seuraava_yksikko(self):
        i = 0
        if self.valittu_yksikko is None:
            self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_yksikot[0])
        else:
            while i < len(self.pelinohjain.kartta.pelaajan_yksikot):
                if self.pelinohjain.kartta.pelaajan_yksikot[i] == self.valittu_yksikko:
                    if i + 1 == len(self.pelinohjain.kartta.pelaajan_yksikot):
                        self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_yksikot[0])
                    else:
                        self.valitse_yksikko(self.pelinohjain.kartta.pelaajan_yksikot[i + 1])
                        break
                i += 1

    def tallenna_peli(self):
        pass

    def peru_valinta(self):
        if self.valittu_yksikko is not None:
            self.tyhjenna_valinta()

    def hyokkaa(self):
        pass

    def kyky_1(self):
        pass

    def kyky_2(self):
        pass
