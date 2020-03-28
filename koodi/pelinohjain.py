from kartta import Kartta
from kartan_lukija import Kartan_lukija
from kayttoliittyma import Kayttoliittyma
from maaston_lukija import Maaston_lukija
from yksikoiden_lukija import Yksikoiden_lukija
from polunhaku import Polunhaku
from ajastin import Ajastin
from PyQt5 import QtCore


class Pelinohjain:

    def __init__(self):
        # käyttöliittymä
        self.__kayttoliittyma = Kayttoliittyma(self)

        self.__vuoro = "PLR"      # PLR = pelaaja, COM = tietokone
        self.__viive = 10     # ms

        # kartan lukeminen
        self.__kartan_lukija = Kartan_lukija()
        self.__nimi, x, y, ruudut, yksikot = self.__kartan_lukija.lue_kartta("testikentta.txt")
        self.__koko = (x, y)
        self.__kartta = Kartta(self.__koko[0], self.__koko[1], ruudut, self.__kayttoliittyma)

        self.__kayttoliittyma.aseta_scene_rect(self.__koko[0], self.__koko[1])

        # maastojen lukeminen
        self.__maaston_lukija = Maaston_lukija()

        # yksiköiden lukeminen
        self.__yksikoiden_lukija = Yksikoiden_lukija()

        # tehdään vasta koko kartan luomisen jälkeen, kun kaikki ruudut ovat paikallaan
        for ruutu in self.__kartta.ruudut:
            ruutu.luo_maasto()
            ruutu.luo_grafiikka(self.__kartta.ruudun_koko)

        # maastot täytyy luoda ensin, jotta saadaan naapurit, joihin liikkuminen on mahdollista
        for ruutu in self.__kartta.ruudut:
            ruutu.etsi_naapurit()

        self.__kartta.lisaa_yksikot(yksikot, self.__yksikoiden_lukija.yksikot)

        # polunhaku
        self._polunhaku = Polunhaku()

        # nappien alkutila
        self.kayttoliittyma.paivita_nappien_aktiivisuus()

    @property
    def kayttoliittyma(self):
        return self.__kayttoliittyma

    @property
    def ajastin(self):
        return self.__ajastin

    @property
    def vuoro(self):
        return self.__vuoro

    @property
    def kartta(self):
        return self.__kartta

    @property
    def koko(self):
        return self.__koko

    @property
    def yksikoiden_lukija(self):
        return self.__yksikoiden_lukija

    @property
    def maaston_lukija(self):
        return self.__maaston_lukija

    @property
    def polunhaku(self):
        return self._polunhaku

    # laskee mahdolliset kohteet aloituksen ja liikkumispisteiden perusteella
    def laske_polut(self, aloitus, liikkuminen):
        mahdolliset_ruudut = []
        for ruutu in self.__kartta.ruudut:
            # rajoitetaan haku vain alueelle, jolle liikkumispisteet riittävät
            if ruutu.maasto.liikkuminen and ruutu.yksikko is None \
                    and self._polunhaku.heuristiikka(aloitus, ruutu) <= liikkuminen:
                ruudut, hinnat = self._polunhaku.hae_polkua(aloitus, ruutu)
                if ruudut is not False:
                    hinta = self._polunhaku.laske_hinta(hinnat, ruutu)
                    if hinta <= liikkuminen:
                        mahdolliset_ruudut.append(ruutu)
        return mahdolliset_ruudut

    def vaihda_vuoroa(self):
        if self.__vuoro == "PLR":
            self.__tietokoneen_vuoron_alku()
        elif self.__vuoro == "COM":
            self.__pelaajan_vuoron_alku()

    def __pelaajan_vuoron_alku(self):
        # tietokoneen vuoron loppu
        for yksikko in self.__kartta.tietokoneen_yksikot:
            # jos on tehnyt jotain, 2 energiaa, muuten 1
            yksikko.saa_energiaa()
            if yksikko.liikkuminen_kaytetty or yksikko.hyokkays_kaytetty:
                yksikko.saa_energiaa()
            yksikko.kasittele_tilavaikutukset()
            yksikko.grafiikka.paivita_tooltip()

        # pelaajan vuoron alku
        #print("PLR")
        self.__vuoro = "PLR"
        self.__kayttoliittyma.laita_napit_kayttoon()
        self.kayttoliittyma.paivita_nappien_aktiivisuus()
        self.__kayttoliittyma.tyhjenna_valinta()
        self.__kayttoliittyma.__valitsee_hyokkayksen_kohdetta = False
        self.__kartta.palauta_pelaajan_toimivat_yksikot()
        for yksikko in self.__kartta.pelaajan_yksikot:
            if not yksikko.onko_taintunut():
                yksikko.palauta_liikkumispisteet()
            yksikko.grafiikka.palauta_vari()

    def __tietokoneen_vuoron_alku(self):
        # pelaajan vuoron loppu
        self.__kayttoliittyma.tyhjenna_valinta()
        self.__kayttoliittyma.__valitsee_hyokkayksen_kohdetta = False
        for yksikko in self.__kartta.pelaajan_yksikot:
            # jos on tehnyt jotain, 2 energiaa, muuten 1
            yksikko.saa_energiaa()
            if yksikko.liikkuminen_kaytetty or yksikko.hyokkays_kaytetty:
                yksikko.saa_energiaa()
            yksikko.kasittele_tilavaikutukset()
            yksikko.grafiikka.paivita_tooltip()

        # tietokoneen vuoron alku
        self.__tietokoneen_vuoro()

    def __tietokoneen_vuoro(self):
        #print("COM")
        self.__vuoro = "COM"
        self.__kayttoliittyma.poista_napit_kaytosta()

        # 1. arg = viive, 2. arg = viiveen jälkeen kutsuttava metodi
        Ajastin.aloita_ajastin(self.__viive, self.vaihda_vuoroa)
