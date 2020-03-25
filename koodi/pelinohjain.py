from kartta import Kartta
from kartan_lukija import Kartan_lukija
from kayttoliittyma import Kayttoliittyma
from maaston_lukija import Maaston_lukija
from yksikoiden_lukija import Yksikoiden_lukija
from polunhaku import Polunhaku
from time import sleep


class Pelinohjain:

    def __init__(self):
        # käyttöliittymä
        self._kayttoliittyma = Kayttoliittyma(self)

        self._vuoro = "PLR"      # PLR = pelaaja, COM = tietokone
        self._viive = 0.1

        # kartan lukeminen
        self._kartan_lukija = Kartan_lukija()
        self._nimi, x, y, ruudut, yksikot = self._kartan_lukija.lue_kartta("testikentta.txt")
        self._koko = (x, y)
        self._kartta = Kartta(self._koko[0], self._koko[1], ruudut, self._kayttoliittyma)

        self._kayttoliittyma.aseta_scene_rect(self._koko[0], self._koko[1])

        # maastojen lukeminen
        self._maaston_lukija = Maaston_lukija()

        # yksiköiden lukeminen
        self._yksikoiden_lukija = Yksikoiden_lukija()

        # tehdään vasta koko kartan luomisen jälkeen, kun kaikki ruudut ovat paikallaan
        for ruutu in self._kartta.ruudut:
            ruutu.luo_maasto()
            ruutu.luo_grafiikka(self._kartta.ruudun_koko)

        # maastot täytyy luoda ensin, jotta saadaan naapurit, joihin liikkuminen on mahdollista
        for ruutu in self._kartta.ruudut:
            ruutu.etsi_naapurit()

        self._kartta.lisaa_yksikot(yksikot, self._yksikoiden_lukija.yksikot)

        # polunhaku
        self._polunhaku = Polunhaku()

    @property
    def kayttoliittyma(self):
        return self._kayttoliittyma

    @property
    def vuoro(self):
        return self._vuoro

    @property
    def kartta(self):
        return self._kartta

    @property
    def koko(self):
        return self._koko

    @property
    def yksikoiden_lukija(self):
        return self._yksikoiden_lukija

    @property
    def maaston_lukija(self):
        return self._maaston_lukija

    @property
    def polunhaku(self):
        return self._polunhaku

    # laskee mahdolliset kohteet aloituksen ja liikkumispisteiden perusteella
    def laske_polut(self, aloitus, liikkuminen):
        mahdolliset_ruudut = []
        for ruutu in self._kartta.ruudut:
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
        if self._vuoro == "PLR":
            self.tietokoneen_vuoron_alku()
        elif self._vuoro == "COM":
            self.pelaajan_vuoron_alku()

    def pelaajan_vuoron_alku(self):
        # tietokoneen vuoron loppu
        for yksikko in self._kartta.tietokoneen_yksikot:
            # jos on tehnyt jotain, 2 energiaa, muuten 1
            yksikko.saa_energiaa()
            if yksikko.liikkuminen_kaytetty or yksikko.hyokkays_kaytetty:
                yksikko.saa_energiaa()
            yksikko.kasittele_tilavaikutukset()
            yksikko.grafiikka.paivita_tooltip()

        # pelaajan vuoron alku
        print("PLR")
        self._vuoro = "PLR"
        self._kayttoliittyma.tyhjenna_valinta()
        self._kayttoliittyma._valitsee_hyokkayksen_kohdetta = False
        self._kartta.palauta_pelaajan_toimivat_yksikot()            # myöh: palauta vain ne, jotka eivät ole taintuneita
        for yksikko in self._kartta.pelaajan_yksikot:
            if not yksikko.onko_taintunut():
                yksikko.palauta_liikkumispisteet()
            yksikko.grafiikka.palauta_vari()

    def tietokoneen_vuoron_alku(self):
        # pelaajan vuoron loppu
        self._kayttoliittyma.tyhjenna_valinta()
        self._kayttoliittyma._valitsee_hyokkayksen_kohdetta = False
        for yksikko in self._kartta.pelaajan_yksikot:
            # jos on tehnyt jotain, 2 energiaa, muuten 1
            yksikko.saa_energiaa()
            if yksikko.liikkuminen_kaytetty or yksikko.hyokkays_kaytetty:
                yksikko.saa_energiaa()
            yksikko.kasittele_tilavaikutukset()
            yksikko.grafiikka.paivita_tooltip()

        # tietokoneen vuoron alku
        self.tietokoneen_vuoro()

    def tietokoneen_vuoro(self):
        print("COM")
        self._vuoro = "COM"
        sleep(self._viive)
        self.vaihda_vuoroa()


