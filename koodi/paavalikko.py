from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from kenttaeditori import Kenttaeditori
from pelinohjain import Pelinohjain
from maaston_lukija import Maaston_lukija
from yksikoiden_lukija import Yksikoiden_lukija
from kartan_lukija import Kartan_lukija
from kayttoliittyman_lukija import Kayttoliittyman_lukija
from pelaa_valikko import Pelaa_valikko
from pelitilanteen_lukija import Pelitilanteen_lukija
import sys


class Paavalikko(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Paavalikko, self).__init__()
        self.__kayttoliittyman_lukija = Kayttoliittyman_lukija()
        if self.__kayttoliittyman_lukija.koko != 0:
            self.__scene_size = self.__kayttoliittyman_lukija.koko
        else:
            self.__scene_size = 880
        self.setCentralWidget(QtWidgets.QWidget())  # QMainWindown must have a centralWidget to be able to add layouts
        self.__paa_layout = QtWidgets.QVBoxLayout()  # Vertical main layout
        self.centralWidget().setLayout(self.__paa_layout)

        self.setGeometry(0, 0, self.__scene_size + 360, self.__scene_size + 20)
        self.setWindowTitle('Strategiapeli')
        self.show()

        self.__virheteksti = QtWidgets.QLabel("")
        self.__virheteksti_kartat = QtWidgets.QLabel("")
        self.__virheteksti_lataus = QtWidgets.QLabel("")
        self.__jatka_nappi = QtWidgets.QPushButton("JATKA PELIÄ")
        self.__jatka_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__pelaa_nappi = QtWidgets.QPushButton("PELAA")
        self.__pelaa_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__kenttaeditori_nappi = QtWidgets.QPushButton("KENTTÄEDITORI")
        self.__kenttaeditori_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__poistu_nappi = QtWidgets.QPushButton("POISTU")
        self.__poistu_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.__virheteksti.setStyleSheet("font: 20pt Arial")
        self.__jatka_nappi.setStyleSheet("font: 10pt Arial")
        self.__virheteksti_kartat.setStyleSheet("font: 20pt Arial")
        self.__virheteksti_lataus.setStyleSheet("font: 20pt Arial")
        self.__pelaa_nappi.setStyleSheet("font: 10pt Arial")
        self.__kenttaeditori_nappi.setStyleSheet("font: 10pt Arial")
        self.__poistu_nappi.setStyleSheet("font: 10pt Arial")

        # nappien yhdistäminen
        self.__jatka_nappi.clicked.connect(self.__jatka)
        self.__pelaa_nappi.clicked.connect(self.__pelaa)
        self.__kenttaeditori_nappi.clicked.connect(self.__kenttaeditori)
        self.__poistu_nappi.clicked.connect(self.__poistu)

        # nappi widgetit
        self.__paa_layout.addWidget(self.__virheteksti, 1)
        self.__paa_layout.addWidget(self.__virheteksti_kartat, 1)
        self.__paa_layout.addWidget(self.__virheteksti_lataus, 1)
        self.__paa_layout.addWidget(self.__jatka_nappi, 2)
        self.__paa_layout.addWidget(self.__pelaa_nappi, 2)
        self.__paa_layout.addWidget(self.__kenttaeditori_nappi, 2)
        self.__paa_layout.addWidget(self.__poistu_nappi, 2)

        # kenttäeditori
        self.kenttaeditori = None
        self.__pelaa_valikko = None

        self.__virheelliset_kartat = []

        # tiedostojen lukijat
        self.__maastojen_lukija = Maaston_lukija()
        self.__yksikoiden_lukija = Yksikoiden_lukija()
        self.__kartan_lukija = Kartan_lukija(self)
        self.kartan_lukija.lue_kaikki_kartat()
        self.__pelitilanteen_lukija = Pelitilanteen_lukija()
        self.lue_tallennus()
        self.__pelinohjain = None
        #print(self.__tilanne)

        # virheet
        if not self.__kayttoliittyman_lukija.lukeminen_onnistui:
            self.__virhe_lukemisessa("kayttoliittyma")
        if not self.__yksikoiden_lukija.lukeminen_onnistui:
            self.__virhe_lukemisessa("yksikot")
        if not self.__maastojen_lukija.lukeminen_onnistui:
            self.__virhe_lukemisessa("maastot")
        self.__nayta_virheelliset_kartat()

        # keskelle liikuttaminen
        if self.kayttoliittyman_lukija.x != 0 and self.kayttoliittyman_lukija.y != 0:
            res_x = self.kayttoliittyman_lukija.x
            res_y = self.kayttoliittyman_lukija.y
        else:
            res_x = 1920
            res_y = 1080
        self.move(int(res_x / 2) - int(self.frameSize().width() / 2),
                  int(res_y / 2) - int(self.frameSize().height() / 2))

    @property
    def maastojen_lukija(self):
        return self.__maastojen_lukija

    @property
    def yksikoiden_lukija(self):
        return self.__yksikoiden_lukija

    @property
    def kartan_lukija(self):
        return self.__kartan_lukija

    @property
    def kayttoliittyman_lukija(self):
        return self.__kayttoliittyman_lukija

    @property
    def scene_size(self):
        return self.__scene_size

    @property
    def pelaa_valikko(self):
        return self.__pelaa_valikko

    def lisaa_virheellinen_kartta(self, nimi):
        self.__virheelliset_kartat.append(nimi)

    def __kriittinen_virhe(self):
        self.__pelaa_nappi.setEnabled(False)
        self.__kenttaeditori_nappi.setEnabled(False)

    def __virhe_lukemisessa(self, tyyppi):
        if tyyppi == "kayttoliittyma":
            self.__kriittinen_virhe()
            self.__virheteksti.setText("Käyttöliittymän tietojen lukemisessa tapahtui virhe.\n"
                                       "Korjaa tiedosto ja avaa ohjelma uudestaan")
        elif tyyppi == "yksikot":
            self.__kriittinen_virhe()
            self.__virheteksti.setText("Yksiköiden tietojen lukemisessa tapahtui virhe.\n"
                                       "Korjaa tiedosto ja avaa ohjelma uudestaan")
        elif tyyppi == "maastot":
            self.__kriittinen_virhe()
            self.__virheteksti.setText("Maastojen tietojen lukemisessa tapahtui virhe.\n"
                                       "Korjaa tiedosto ja avaa ohjelma uudestaan")
        elif tyyppi == "tilanne":
            self.__jatka_nappi.setEnabled(False)
            self.__virheteksti_lataus.setText("Pelitilanteen lukeminen epäonnistui")

    def __nayta_virheelliset_kartat(self):
        if len(self.__virheelliset_kartat) > 0:
            teksti = "Virheelliset kartat:\n"
            for kartta in self.__virheelliset_kartat:
                teksti += kartta + "\n"
            self.__virheteksti_kartat.setText(teksti)

    def __jatka(self):
        # luodaan pelinohjain ja kartta ilman yksiköitä
        self.__pelinohjain = Pelinohjain(self.__kartan_nimi, self, False)
        #print(self.__tilanne[0])

        # lisätään yksiköt, muutetaan niiden elämä ja energia sopivaksi, lisätään tilavaikutukset
        for yksikko in self.__tilanne:
            tiedot = yksikko[0]
            #print(tiedot)
            x = tiedot[0]
            y = tiedot[1]
            self.__pelinohjain.kartta.lisaa_yksikko(self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y], tiedot[3],
                                                self.yksikoiden_lukija.yksikot[tiedot[3]], tiedot[2])
            self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y].yksikko.ominaisuudet.nyk_elama = tiedot[4]
            self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y].yksikko.ominaisuudet.nyk_energia = tiedot[5]
            if tiedot[6] == "kylla":
                self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y].yksikko.liikuttu()
            if tiedot[7] == "kylla":
                self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y].yksikko.hyokatty()
            # tilavaikutusten lisäys
            hyokkaysvaikutus = yksikko[1]
            vaikutukset = yksikko[2]
            self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y].yksikko.hyokkays_vaikutus = hyokkaysvaikutus
            for v in vaikutukset:
                self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y].yksikko.lisaa_tilavaikutus(v.kesto,
                    v.hyokkaysbonus, v.puolustusbonus, v.liikkumisbonus, v.verenvuoto, v.taintuminen, v.loppuvaikutus)

        self.__pelinohjain.kartta.etsi_yksikot()
        self.__pelinohjain.kartta.palauta_pelaajan_toimivat_yksikot()
        self.__pelinohjain.kartta.tarkista_toimivat_yksikot()
        for yksikko in self.__pelinohjain.kartta.pelaajan_yksikot:
            yksikko.grafiikka.palauta_vari()
            yksikko.grafiikka.elamapalkki.paivita_koko()
            yksikko.grafiikka.elamapalkki.paivita_tilavaikutukset()
            yksikko.grafiikka.paivita_tooltip()
        for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
            yksikko.grafiikka.elamapalkki.paivita_koko()
            yksikko.grafiikka.elamapalkki.paivita_tilavaikutukset()
            yksikko.grafiikka.paivita_tooltip()
        self.__pelinohjain.kayttoliittyma.tyhjenna_valinta()
        self.__pelinohjain.kayttoliittyma.laita_napit_kayttoon()
        self.__pelinohjain.kayttoliittyma.paivita_nappien_aktiivisuus()

        # kiilojen lisäys
        for kiila in self.__kiilat:
            x = kiila[0]
            y = kiila[1]
            tiedot = self.yksikoiden_lukija.yksikot["jousimiehet"][1]
            print(tiedot)
            self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y].luo_kiilat(
                float(tiedot['kyky2_bonus']), float(tiedot['kyky2_bonus_ratsuvaki']))
            #print(tiedot['kyky2_bonus'], ",", tiedot['kyky2_bonus_ratsuvaki'])



    def __pelaa(self):
        if self.__pelaa_valikko is None:
            self.__pelaa_valikko = Pelaa_valikko(self)
        self.__pelaa_valikko.show()
        self.hide()

    def __kenttaeditori(self):
        if self.kenttaeditori is None:
            self.kenttaeditori = Kenttaeditori(self)
        self.kenttaeditori.show()
        self.hide()

    def __poistu(self):
        sys.exit()

    def lue_tallennus(self):
        if self.__pelitilanteen_lukija.lue_pelitilanne(self.__kartan_lukija.kartat, self.__yksikoiden_lukija.yksikot) \
                is not None:
            self.__kartan_nimi, self.__tilanne, self.__kiilat = self.__pelitilanteen_lukija.lue_pelitilanne\
                (self.__kartan_lukija.kartat, self.__yksikoiden_lukija.yksikot)
            self.__jatka_nappi.setEnabled(True)
        else:
            self.__jatka_nappi.setEnabled(False)
        if not self.__pelitilanteen_lukija.lukeminen_onnistui:
            self.__virhe_lukemisessa("tilanne")
        else:
            self.__virheteksti_lataus.setText("")

    def poista_pelinohjain(self):
        self.__pelinohjain.kayttoliittyma.deleteLater()
        self.__pelinohjain = None
