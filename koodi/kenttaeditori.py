from PyQt5 import QtWidgets, QtTest
from kartta import Kartta
from kentan_tallentaja import Kentan_tallentaja
from kartan_lukija import Kartan_lukija


class Kenttaeditori(QtWidgets.QMainWindow):

    def __init__(self, paavalikko):
        super().__init__()
        self.__scene_size = paavalikko.scene_size       # kentän koko pikseleinä
        self.__paavalikko = paavalikko
        self.__viive = 1500             # tallennuksen onnistumisen ja päävalikkoon palaamisen välinen viive

        self.setCentralWidget(QtWidgets.QWidget())
        self.__paa_layout = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.__paa_layout)

        # ikkuna
        self.setGeometry(0, 0, self.__scene_size + 420, self.__scene_size + 20)
        self.setWindowTitle('Strategiapeli')
        self.show()

        # scene
        self.__scene = QtWidgets.QGraphicsScene()

        # näkymä
        self.__nakyma = QtWidgets.QGraphicsView(self.__scene, self)
        self.__nakyma.adjustSize()
        self.__nakyma.show()
        self.__paa_layout.addWidget(self.__nakyma)

        self.__nappi_layout = QtWidgets.QGridLayout()
        self.__paa_layout.addLayout(self.__nappi_layout)

        # widgetit
        self.__uusi_ohje = QtWidgets.QLabel("SYÖTÄ UUDEN\nKENTÄN PITUUS\nJA LEVEYS\nVÄLILYÖNNILLÄ\nEROTETTUNA")
        self.__uusi_ohje.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__muokkaa_ohje = QtWidgets.QLabel("SYÖTÄ MUOKATTAVAN\nKENTÄN NIMI\nILMAN\nTIEDOSTOPÄÄTETTÄ")
        self.__muokkaa_ohje.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__uusi_kentta_nappi = QtWidgets.QPushButton("UUSI KENTTÄ")
        self.__uusi_kentta_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__muokkaa_vanhaa_nappi = QtWidgets.QPushButton("MUOKKAA KENTTÄÄ")
        self.__muokkaa_vanhaa_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__vaihda_nappien_sisalto = QtWidgets.QPushButton("VAIHDA\nYKSIKÖT/MAASTOT")
        self.__vaihda_nappien_sisalto.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__poistu_nappi = QtWidgets.QPushButton("POISTU EDITORISTA")
        self.__poistu_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__tasanko_nappi = QtWidgets.QPushButton("TASANKO")
        self.__tasanko_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__kukkula_nappi = QtWidgets.QPushButton("KUKKULA")
        self.__kukkula_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__pelto_nappi = QtWidgets.QPushButton("PELTO")
        self.__pelto_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__vuoristo_nappi = QtWidgets.QPushButton("VUORISTO")
        self.__vuoristo_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__silta_nappi = QtWidgets.QPushButton("SILTA")
        self.__silta_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__joki_nappi = QtWidgets.QPushButton("JOKI")
        self.__joki_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.__koko = QtWidgets.QLineEdit()
        self.__koko.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__nimi = QtWidgets.QLineEdit()
        self.__nimi.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.__uusi_ohje.setStyleSheet("font: 10pt Arial")
        self.__muokkaa_ohje.setStyleSheet("font: 10pt Arial")
        self.__uusi_kentta_nappi.setStyleSheet("font: 10pt Arial")
        self.__muokkaa_vanhaa_nappi.setStyleSheet("font: 10pt Arial")
        self.__poistu_nappi.setStyleSheet("font: 10pt Arial")
        self.__vaihda_nappien_sisalto.setStyleSheet("font: 10pt Arial")
        self.__tasanko_nappi.setStyleSheet("font: 10pt Arial")
        self.__kukkula_nappi.setStyleSheet("font: 10pt Arial")
        self.__pelto_nappi.setStyleSheet("font: 10pt Arial")
        self.__vuoristo_nappi.setStyleSheet("font: 10pt Arial")
        self.__silta_nappi.setStyleSheet("font: 10pt Arial")
        self.__joki_nappi.setStyleSheet("font: 10pt Arial")
        self.__koko.setStyleSheet("font: 10pt Arial")
        self.__nimi.setStyleSheet("font: 10pt Arial")

        self.__vaihda_nappien_sisalto.setEnabled(False)
        self.__tasanko_nappi.setEnabled(False)
        self.__kukkula_nappi.setEnabled(False)
        self.__pelto_nappi.setEnabled(False)
        self.__vuoristo_nappi.setEnabled(False)
        self.__silta_nappi.setEnabled(False)
        self.__joki_nappi.setEnabled(False)

        self.__nappi_layout.addWidget(self.__uusi_ohje, 0, 0)
        self.__nappi_layout.addWidget(self.__muokkaa_ohje, 0, 1)
        self.__nappi_layout.addWidget(self.__koko, 1, 0)
        self.__nappi_layout.addWidget(self.__nimi, 1, 1)
        self.__nappi_layout.addWidget(self.__uusi_kentta_nappi, 2, 0)
        self.__nappi_layout.addWidget(self.__muokkaa_vanhaa_nappi, 2, 1)
        self.__nappi_layout.addWidget(self.__vaihda_nappien_sisalto, 3, 0)
        self.__nappi_layout.addWidget(self.__poistu_nappi, 3, 1)
        self.__nappi_layout.addWidget(self.__tasanko_nappi, 4, 0)
        self.__nappi_layout.addWidget(self.__kukkula_nappi, 4, 1)
        self.__nappi_layout.addWidget(self.__pelto_nappi, 5, 0)
        self.__nappi_layout.addWidget(self.__vuoristo_nappi, 5, 1)
        self.__nappi_layout.addWidget(self.__silta_nappi, 6, 0)
        self.__nappi_layout.addWidget(self.__joki_nappi, 6, 1)

        self.__uusi_kentta_nappi.clicked.connect(self.__lue_koko)
        self.__muokkaa_vanhaa_nappi.clicked.connect(self.__lue_kentan_nimi)
        self.__vaihda_nappien_sisalto.clicked.connect(self.__muuta_nappien_toiminnot)
        self.__poistu_nappi.clicked.connect(self.__poistu)
        self.__tasanko_nappi.clicked.connect(self.valitse_tasanko)
        self.__pelto_nappi.clicked.connect(self.valitse_pelto)
        self.__vuoristo_nappi.clicked.connect(self.valitse_vuoristo)
        self.__kukkula_nappi.clicked.connect(self.valitse_kukkula)
        self.__silta_nappi.clicked.connect(self.valitse_silta)
        self.__joki_nappi.clicked.connect(self.valitse_joki)

        self.__kartan_lukija = Kartan_lukija()

        self.__koko_x = 0
        self.__koko_y = 0

        self.__kartta = None

        # voi olla maasto tai yksikkö
        self.__valittu_elementti = None
        self.__valittu_omistaja = None

        # käyttöliittymän muutokset
        self.__editoi_kenttaa = False
        self.__muokkaa_vanhaa = False

        # ikkunan keskittäminen
        res_x = self.paavalikko.kayttoliittyman_lukija.x
        res_y = self.paavalikko.kayttoliittyman_lukija.y
        self.move(int(res_x / 2) - int(self.frameSize().width() / 2),
                  int(res_y / 2) - int(self.frameSize().height() / 2))

    @property
    def scene(self):
        return self.__scene

    @property
    def paavalikko(self):
        return self.__paavalikko

    @property
    def koko_x(self):
        return self.__koko_x

    @property
    def koko_y(self):
        return self.__koko_y

    @property
    def scene_size(self):
        return self.__scene_size

    @property
    def valittu_elementti(self):
        return self.__valittu_elementti

    @property
    def kartta(self):
        return self.__kartta

    @property
    def valittu_omistaja(self):
        return self.__valittu_omistaja

    def __aseta_scene_rect(self, x, y):
        # rectin skaalauskertoimet
        if x > y:
            y /= x
            x = 1
        else:
            x /= y
            y = 1
        self.__scene.setSceneRect(0, 0, self.__scene_size * x, self.__scene_size * y)

        # keskelle liikuttaminen
        res_x = self.paavalikko.kayttoliittyman_lukija.x
        res_y = self.paavalikko.kayttoliittyman_lukija.y
        self.move(int(res_x / 2) - int(self.frameSize().width() / 2),
                  int(res_y / 2) - int(self.frameSize().height() / 2))

    def __lue_koko(self):
        try:
            text = self.__koko.text().split(" ")
            self.__koko_x = int(text[0])
            self.__koko_y = int(text[1])
            self.__piirra_tyhja_kartta()
        except ValueError:
            self.__koko.setText("")
        except IndexError:
            self.__koko.setText("")

    def __lue_kentan_nimi(self):
        nimi = self.__nimi.text()
        validi = Kentan_tallentaja.tarkista_nimi(nimi)
        nimi += ".txt"
        # jos on false, nimen mukainen kenttä löytyi
        if validi is False:
            nimi, x, y, ruudut, yksikot = self.__kartan_lukija.lue_kartta(nimi)
            koko = (x, y)
            self.__koko_x = koko[0]
            self.__koko_y = koko[1]
            self.__kartta = Kartta(koko[0], koko[1], ruudut, self)
            self.__aseta_scene_rect(koko[0], koko[1])

            # luodaan maastot ja lisätään yksiköt vasta koko kartan luomisen jälkeen, kun kaikki ruudut ovat paikallaan
            for ruutu in self.__kartta.ruudut:
                ruutu.luo_maasto()
                ruutu.luo_grafiikka()
                ruutu.etsi_kartta()

            self.__kartta.lisaa_yksikot(yksikot, self.__paavalikko.yksikoiden_lukija.yksikot)
            self.__editoi_kenttaa = True
            self.__muokkaa_vanhaa = True
            self.__editoi_kenttaa_napit(self.__editoi_kenttaa)
        else:
            pass

    # piirtää tyhjän kartan, jonka mitat ovat koko_x ja koko_y
    def __piirra_tyhja_kartta(self):
        self.__tyhjenna_kartta()
        ruudut = [["tasanko" for i in range(self.__koko_y)] for j in range(self.__koko_x)]
        self.__kartta = Kartta(self.__koko_x, self.__koko_y, ruudut, self)

        for ruutu in self.__kartta.ruudut:
            ruutu.luo_maasto(True)
            ruutu.luo_grafiikka(True)
            ruutu.etsi_kartta()

        self.__aseta_scene_rect(self.__koko_x, self.__koko_y)

        # nappien muutokset
        self.__editoi_kenttaa = True
        self.__editoi_kenttaa_napit(self.__editoi_kenttaa)

    def __editoi_kenttaa_napit(self, editoi):
        # muuttaa käyttöliittymää sen perusteella, editoidaanko kenttää vai ei
        if editoi:
            self.__uusi_kentta_nappi.setText("TALLENNA KENTTÄ")
            self.__uusi_kentta_nappi.clicked.disconnect(self.__lue_koko)
            self.__uusi_kentta_nappi.clicked.connect(self.__tallenna_kentta)
            self.__uusi_ohje.setText("SYÖTÄ TALLENNETTAVAN\nKENTÄN NIMI")
            self.__koko.setText("")

            self.__muokkaa_vanhaa_nappi.setText("TYHJENNÄ KENTTÄ")
            self.__muokkaa_vanhaa_nappi.clicked.disconnect(self.__lue_kentan_nimi)
            self.__muokkaa_vanhaa_nappi.clicked.connect(self.__tyhjenna_kartta)
            self.__muokkaa_ohje.setText("")
            self.__nimi.setText("")
            self.__vaihda_nappien_sisalto.setEnabled(True)
            self.__tasanko_nappi.setEnabled(True)
            self.__kukkula_nappi.setEnabled(True)
            self.__pelto_nappi.setEnabled(True)
            self.__vuoristo_nappi.setEnabled(True)
            self.__silta_nappi.setEnabled(True)
            self.__joki_nappi.setEnabled(True)
            if self.__muokkaa_vanhaa is True:
                self.__uusi_kentta_nappi.setText("TALLENNA KENTTÄ")
                self.__uusi_ohje.setText("TALLENNA VANHAN\nKENTÄN PÄÄLLE\nSYÖTTÄMÄLLÄ\nVANHAN KENTÄN"
                                         "\nNIMI TAI\nSYÖTÄ UUSI NIMI")
        else:
            self.__uusi_kentta_nappi.setText("UUSI KENTTÄ")
            self.__uusi_kentta_nappi.clicked.disconnect(self.__tallenna_kentta)
            self.__uusi_kentta_nappi.clicked.connect(self.__lue_koko)
            self.__uusi_ohje.setText("SYÖTÄ UUDEN\nKENTÄN PITUUS\nJA LEVEYS\nVÄLILYÖNNILLÄ\nEROTETTUNA")
            self.__koko.setText("")

            self.__muokkaa_vanhaa_nappi.setText("MUOKKAA KENTTÄÄ")
            self.__muokkaa_vanhaa_nappi.clicked.disconnect(self.__tyhjenna_kartta)
            self.__muokkaa_vanhaa_nappi.clicked.connect(self.__lue_kentan_nimi)
            self.__muokkaa_ohje.setText("SYÖTÄ MUOKATTAVAN\nKENTÄN NIMI\nILMAN\nTIEDOSTOPÄÄTETTÄ")
            self.__nimi.setText("")
            self.__vaihda_nappien_sisalto.setEnabled(False)
            self.__tasanko_nappi.setEnabled(False)
            self.__kukkula_nappi.setEnabled(False)
            self.__pelto_nappi.setEnabled(False)
            self.__vuoristo_nappi.setEnabled(False)
            self.__silta_nappi.setEnabled(False)
            self.__joki_nappi.setEnabled(False)

    def __tyhjenna_kartta(self):
        if self.kartta is not None:
            self.kartta.tyhjenna()
        if self.__editoi_kenttaa:
            self.__editoi_kenttaa = False
            self.__editoi_kenttaa_napit(self.__editoi_kenttaa)

    def valitse_tasanko(self):
        self.__valittu_elementti = "tasanko"
        print(self.__valittu_elementti)

    def valitse_kukkula(self):
        self.__valittu_elementti = "kukkula"
        print(self.__valittu_elementti)

    def valitse_pelto(self):
        self.__valittu_elementti = "pelto"
        print(self.__valittu_elementti)

    def valitse_vuoristo(self):
        self.__valittu_elementti = "vuoristo"
        print(self.__valittu_elementti)

    def valitse_joki(self):
        self.__valittu_elementti = "joki"
        print(self.__valittu_elementti)

    def valitse_silta(self):
        self.__valittu_elementti = "silta"
        print(self.__valittu_elementti)

    def valitse_ratsuvaki(self):
        self.__valittu_elementti = "ratsuvaki"
        print(self.__valittu_elementti)

    def valitse_jousimiehet(self):
        self.__valittu_elementti = "jousimiehet"
        print(self.__valittu_elementti)

    def valitse_parantaja(self):
        self.__valittu_elementti = "parantaja"
        print(self.__valittu_elementti)

    def valitse_tykisto(self):
        self.__valittu_elementti = "tykisto"
        print(self.__valittu_elementti)

    def valitse_jalkavaki(self):
        self.__valittu_elementti = "jalkavaki"
        print(self.__valittu_elementti)

    def valitse_poista_yksikko(self):
        self.__valittu_elementti = "poista"
        print(self.__valittu_elementti)

    def __tallenna_kentta(self):
        tallenna_paalle = False
        if self.__muokkaa_vanhaa is True:
            tallenna_paalle = True
        self.kartta.etsi_yksikot()
        onnistui = Kentan_tallentaja.tallenna_kentta(self.kartta, self.__koko.text(), tallenna_paalle)
        if onnistui:
            self.__uusi_ohje.setText("TALLENNUS ONNISTUI")
            QtTest.QTest.qWait(self.__viive)
            self.__tyhjenna_kartta()
        else:
            self.__uusi_ohje.setText("NIMI KÄYTÖSSÄ")
            QtTest.QTest.qWait(self.__viive)
            self.__uusi_ohje.setText("SYÖTÄ TALLENNETTAVAN\nKENTÄN NIMI")
            self.__koko.setText("")

    def __poistu(self):
        self.__tyhjenna_kartta()
        self.paavalikko.show()
        self.paavalikko.kartan_lukija.lue_kaikki_kartat()
        self.hide()

    def __muuta_nappien_toiminnot(self):
        # vaihtaa maastojen ja yksiköiden lisäyksen välillä
        if self.__valittu_omistaja is None:
            tyyppi = "pelaaja"
        elif self.__valittu_omistaja == "PLR":
            tyyppi = "tietokone"
        else:
            tyyppi = "maastot"
        if tyyppi == "maastot":
            self.__valittu_omistaja = None
            self.__tasanko_nappi.setText("TASANKO")
            self.__pelto_nappi.setText("PELTO")
            self.__vuoristo_nappi.setText("VUORISTO")
            self.__kukkula_nappi.setText("KUKKULA")
            self.__silta_nappi.setText("SILTA")
            self.__joki_nappi.setText("JOKI")
            self.__tasanko_nappi.clicked.connect(self.valitse_tasanko)
            self.__pelto_nappi.clicked.connect(self.valitse_pelto)
            self.__vuoristo_nappi.clicked.connect(self.valitse_vuoristo)
            self.__kukkula_nappi.clicked.connect(self.valitse_kukkula)
            self.__silta_nappi.clicked.connect(self.valitse_silta)
            self.__joki_nappi.clicked.connect(self.valitse_joki)
            self.__tasanko_nappi.clicked.disconnect(self.valitse_jalkavaki)
            self.__pelto_nappi.clicked.disconnect(self.valitse_ratsuvaki)
            self.__vuoristo_nappi.clicked.disconnect(self.valitse_jousimiehet)
            self.__kukkula_nappi.clicked.disconnect(self.valitse_tykisto)
            self.__silta_nappi.clicked.disconnect(self.valitse_parantaja)
            self.__joki_nappi.clicked.disconnect(self.valitse_poista_yksikko)
        elif tyyppi == "pelaaja":
            self.__valittu_omistaja = "PLR"
            self.__tasanko_nappi.setText("JALKAVÄKI (PEL)")
            self.__pelto_nappi.setText("RATSUVÄKI (PEL)")
            self.__vuoristo_nappi.setText("JOUSIMIEHET (PEL)")
            self.__kukkula_nappi.setText("TYKISTÖ (PEL)")
            self.__silta_nappi.setText("PARANTAJA (PEL)")
            self.__joki_nappi.setText("POISTA YKSIKKÖ")
            self.__tasanko_nappi.clicked.connect(self.valitse_jalkavaki)
            self.__pelto_nappi.clicked.connect(self.valitse_ratsuvaki)
            self.__vuoristo_nappi.clicked.connect(self.valitse_jousimiehet)
            self.__kukkula_nappi.clicked.connect(self.valitse_tykisto)
            self.__silta_nappi.clicked.connect(self.valitse_parantaja)
            self.__joki_nappi.clicked.connect(self.valitse_poista_yksikko)
            self.__tasanko_nappi.clicked.disconnect(self.valitse_tasanko)
            self.__pelto_nappi.clicked.disconnect(self.valitse_pelto)
            self.__vuoristo_nappi.clicked.disconnect(self.valitse_vuoristo)
            self.__kukkula_nappi.clicked.disconnect(self.valitse_kukkula)
            self.__silta_nappi.clicked.disconnect(self.valitse_silta)
            self.__joki_nappi.clicked.disconnect(self.valitse_joki)
        elif tyyppi == "tietokone":
            self.__valittu_omistaja = "COM"
            self.__tasanko_nappi.setText("JALKAVÄKI (TIET)")
            self.__pelto_nappi.setText("RATSUVÄKI (TIET)")
            self.__vuoristo_nappi.setText("JOUSIMIEHET (TIET)")
            self.__kukkula_nappi.setText("TYKISTÖ (TIET)")
            self.__silta_nappi.setText("PARANTAJA (TIET)")
            self.__joki_nappi.setText("POISTA YKSIKKÖ")
            self.__tasanko_nappi.clicked.connect(self.valitse_jalkavaki)
            self.__pelto_nappi.clicked.connect(self.valitse_ratsuvaki)
            self.__vuoristo_nappi.clicked.connect(self.valitse_jousimiehet)
            self.__kukkula_nappi.clicked.connect(self.valitse_tykisto)
            self.__silta_nappi.clicked.connect(self.valitse_parantaja)
            self.__joki_nappi.clicked.connect(self.valitse_poista_yksikko)
