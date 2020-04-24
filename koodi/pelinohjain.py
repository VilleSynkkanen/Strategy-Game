from kartta import Kartta
from kartan_lukija import Kartan_lukija
from kayttoliittyma import Kayttoliittyma
from maaston_lukija import Maaston_lukija
from yksikoiden_lukija import Yksikoiden_lukija
from polunhaku import Polunhaku
from tekoalyn_ohjain import Tekoalyn_ohjain
from pelin_tallentaja import Pelin_tallentaja
from ajastin import Ajastin
from PyQt5 import QtCore


class Pelinohjain:

    def __init__(self, kartan_nimi, paavalikko, luo_yksikot=True):
        # käyttöliittymä
        self.__paavalikko = paavalikko
        self.__tallentaja = Pelin_tallentaja(self)
        self.__kayttoliittyma = Kayttoliittyma(self)

        self.__vuoro = "PLR"      # PLR = pelaaja, COM = tietokone
        self.__viive = paavalikko.kayttoliittyman_lukija.viive     # ms

        # kartan lukeminen
        self.__kartan_lukija = Kartan_lukija()
        self.__nimi, x, y, ruudut, yksikot = self.__kartan_lukija.lue_kartta(kartan_nimi)
        self.__koko = (x, y)
        self.__nimi = kartan_nimi
        #print(ruudut)
        self.__kartta = Kartta(self.__koko[0], self.__koko[1], ruudut, self.__kayttoliittyma)

        self.__kayttoliittyma.aseta_scene_rect(self.__koko[0], self.__koko[1])

        # lukeminen
        self.__maaston_lukija = Maaston_lukija()
        self.__yksikoiden_lukija = Yksikoiden_lukija()

        # tehdään vasta koko kartan luomisen jälkeen, kun kaikki ruudut ovat paikallaan
        for ruutu in self.__kartta.ruudut:
            ruutu.luo_maasto()
            ruutu.luo_grafiikka(self.__kartta.ruudun_koko)

        # maastot täytyy luoda ensin, jotta saadaan naapurit, joihin liikkuminen on mahdollista
        for ruutu in self.__kartta.ruudut:
            ruutu.etsi_naapurit()

        if luo_yksikot:
            self.__kartta.lisaa_yksikot(yksikot, self.__yksikoiden_lukija.yksikot)

        # polunhaku
        self.__polunhaku = Polunhaku()

        # tekoälyn ohjain
        self.__tekoalyn_ohjain = Tekoalyn_ohjain(self)

        # nappien alkutila
        self.kayttoliittyma.paivita_nappien_aktiivisuus()

        # ohjetekstin alkutila
        self.__kayttoliittyma.muuta_ohjeteksti("PELAAJAN VUORO\n")

    @property
    def paavalikko(self):
        return self.__paavalikko

    @property
    def kayttoliittyma(self):
        return self.__kayttoliittyma

    @property
    def tallentaja(self):
        return self.__tallentaja

    @property
    def viive(self):
        return self.__viive

    @property
    def vuoro(self):
        return self.__vuoro

    @property
    def nimi(self):
        return self.__nimi

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
        return self.__polunhaku

    # laskee mahdolliset kohteet aloituksen ja liikkumispisteiden perusteella
    def laske_polut(self, aloitus, liikkuminen):
        mahdolliset_ruudut = []
        for ruutu in self.__kartta.ruudut:
            # rajoitetaan haku vain alueelle, jolle liikkumispisteet riittävät
            if ruutu.maasto.liikkuminen and ruutu.yksikko is None \
                    and self.__polunhaku.heuristiikka(aloitus, ruutu) <= liikkuminen:
                ruudut, hinnat = self.__polunhaku.hae_polkua(aloitus, ruutu)
                if ruudut is not False:
                    hinta = self.__polunhaku.laske_hinta(hinnat, ruutu)
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
        if len(self.__kartta.pelaajan_yksikot) != 0:
            self.__kayttoliittyma.laita_napit_kayttoon()
            self.__kayttoliittyma.tyhjenna_valinta()
            self.__kayttoliittyma.__valitsee_hyokkayksen_kohdetta = False
            self.__kartta.palauta_pelaajan_toimivat_yksikot()
            self.__kayttoliittyma.muuta_ohjeteksti("PELAAJAN VUORO\n")
            for yksikko in self.__kartta.pelaajan_yksikot:
                if not yksikko.onko_taintunut():
                    yksikko.palauta_liikkumispisteet()
                yksikko.grafiikka.palauta_vari()
            self.kayttoliittyma.paivita_nappien_aktiivisuus()
        else:
            self.kayttoliittyma.havio()
            # implementoi häviäminen

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
        self.__kayttoliittyma.muuta_ohjeteksti("TIETOKONEEN VUORO\n")
        for yksikko in self.__kartta.tietokoneen_yksikot:
            if not yksikko.onko_taintunut():
                yksikko.palauta_liikkumispisteet()
        self.__tietokoneen_vuoro()

    def __tietokoneen_vuoro(self):
        #print("COM")
        self.__vuoro = "COM"
        self.__kayttoliittyma.poista_napit_kaytosta()

        self.__tekoalyn_ohjain.ohjaa_yksikoita()

        # 1. arg = viive, 2. arg = viiveen jälkeen kutsuttava metodi
        Ajastin.aloita_ajastin(self.__viive, self.vaihda_vuoroa)

    def tarkista_voitto(self):
        if len(self.kartta.tietokoneen_yksikot) == 0:
            self.kayttoliittyma.voitto()
