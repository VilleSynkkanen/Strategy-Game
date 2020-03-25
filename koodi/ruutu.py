from koordinaatit import Koordinaatit
from maasto import Maasto
from ruutugrafiikka import Ruutugrafiikka
from yksikko import Yksikko
from jalkavaki import  Jalkavaki
from ratsuvaki import  Ratsuvaki
from jousimiehet import  Jousimiehet
from tykisto import Tykisto
from parantaja import Parantaja
from kiilat import Kiilat


class Ruutu:

    def __init__(self, koordinaatit, koko, tyyppi, kayttoliittyma):
        self._tyyppi = tyyppi
        self._kayttoliittyma = kayttoliittyma
        self._koordinaatit = koordinaatit
        self._grafiikka = None
        self._kartta = None  # etsitään myöhemmin
        self._maasto = None  # luodaan myöhemmin
        self._naapurit = []  # etsitään myöhemmin
        self._yksikko = None
        self._kiilat = None

    @property
    def tyyppi(self):
        return self._tyyppi

    @property
    def kayttoliittyma(self):
        return self._kayttoliittyma

    @property
    def koordinaatit(self):
        return self._koordinaatit

    @property
    def grafiikka(self):
        return self._grafiikka

    @property
    def kartta(self):
        return self._kartta

    @property
    def maasto(self):
        return self._maasto

    @property
    def naapurit(self):
        return self._naapurit

    @property
    def yksikko(self):
        return self._yksikko

    @property
    def kiilat(self):
        return self._kiilat

    def lisaa_yksikko(self, tyyppi, omistaja, ominaisuudet):
        if tyyppi == "jalkavaki":
            self._yksikko = Jalkavaki(omistaja, self, self._kayttoliittyma, ominaisuudet)
        elif tyyppi == "ratsuvaki":
            self._yksikko = Ratsuvaki(omistaja, self, self._kayttoliittyma, ominaisuudet)
        elif tyyppi == "jousimiehet":
            self._yksikko = Jousimiehet(omistaja, self, self._kayttoliittyma, ominaisuudet)
        elif tyyppi == "tykisto":
            self._yksikko = Tykisto(omistaja, self, self._kayttoliittyma, ominaisuudet)
        elif tyyppi == "parantaja":
            self._yksikko = Parantaja(omistaja, self, self._kayttoliittyma, ominaisuudet)
        return self._yksikko

    def luo_grafiikka(self, koko):
        self._grafiikka = Ruutugrafiikka(self._koordinaatit, koko, self._kayttoliittyma, self._maasto.vari, self)

    def luo_maasto(self):
        maastot = self._kayttoliittyma.pelinohjain.maaston_lukija.maastot
        ominaisuudet = maastot[self._tyyppi]
        self._maasto = Maasto(ominaisuudet.tyyppi, ominaisuudet.liikkuminen, ominaisuudet.liikkumisen_hinta,
                              ominaisuudet.hyokkayskerroin, ominaisuudet.puolustuskerroin, ominaisuudet.vari,
                              ominaisuudet.lapinakyvyys)

    def etsi_naapurit(self):
        self._kartta = self._kayttoliittyma.pelinohjain.kartta

        # suunnat naapureiden löytämistä varten
        pohjoinen = (self._koordinaatit.x, self._koordinaatit.y + 1)
        ita = (self._koordinaatit.x + 1, self._koordinaatit.y)
        etela = (self._koordinaatit.x, self._koordinaatit.y - 1)
        lansi = (self._koordinaatit.x - 1, self._koordinaatit.y)
        naapuri_koordinaatit = (pohjoinen, ita, etela, lansi)

        self._naapurit = []
        for ruutu in self._kartta.ruudut:
            if (ruutu.koordinaatit.x, ruutu.koordinaatit.y) in naapuri_koordinaatit:
                self._naapurit.append(ruutu)

    def vapaat_naapurit(self):
        vapaat = []
        for naapuri in self._naapurit:
            if naapuri.yksikko is None and naapuri.maasto.liikkuminen:
                vapaat.append(naapuri)
        return vapaat

    def luo_kiilat(self, bonus, bonus_ratsuvaki):
        self._kiilat = Kiilat(bonus, bonus_ratsuvaki, self, self._kayttoliittyma)

    def liiku_pois(self):
        self._yksikko = None

    def liiku_ruutuun(self, yksikko):
        self._yksikko = yksikko

    def poista_yksikko(self):
        self._yksikko = None
