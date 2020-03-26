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
        self.__tyyppi = tyyppi
        self.__kayttoliittyma = kayttoliittyma
        self.__koordinaatit = koordinaatit
        self.__grafiikka = None
        self.__kartta = None  # etsitään myöhemmin
        self.__maasto = None  # luodaan myöhemmin
        self.__naapurit = []  # etsitään myöhemmin
        self.__yksikko = None
        self.__kiilat = None

    @property
    def tyyppi(self):
        return self.__tyyppi

    @property
    def kayttoliittyma(self):
        return self.__kayttoliittyma

    @property
    def koordinaatit(self):
        return self.__koordinaatit

    @property
    def grafiikka(self):
        return self.__grafiikka

    @property
    def kartta(self):
        return self.__kartta

    @property
    def maasto(self):
        return self.__maasto

    @property
    def naapurit(self):
        return self.__naapurit

    @property
    def yksikko(self):
        return self.__yksikko

    @property
    def kiilat(self):
        return self.__kiilat

    def lisaa_yksikko(self, tyyppi, omistaja, ominaisuudet):
        if tyyppi == "jalkavaki":
            self.__yksikko = Jalkavaki(omistaja, self, self.__kayttoliittyma, ominaisuudet[0], ominaisuudet[1])
        elif tyyppi == "ratsuvaki":
            self.__yksikko = Ratsuvaki(omistaja, self, self.__kayttoliittyma, ominaisuudet[0], ominaisuudet[1])
        elif tyyppi == "jousimiehet":
            self.__yksikko = Jousimiehet(omistaja, self, self.__kayttoliittyma, ominaisuudet[0], ominaisuudet[1])
        elif tyyppi == "tykisto":
            self.__yksikko = Tykisto(omistaja, self, self.__kayttoliittyma, ominaisuudet[0], ominaisuudet[1])
        elif tyyppi == "parantaja":
            self.__yksikko = Parantaja(omistaja, self, self.__kayttoliittyma, ominaisuudet[0], ominaisuudet[1])
        return self.__yksikko

    def luo_grafiikka(self, koko):
        self.__grafiikka = Ruutugrafiikka(self.__koordinaatit, koko, self.__kayttoliittyma, self.__maasto.vari, self)

    def luo_maasto(self):
        maastot = self.__kayttoliittyma.pelinohjain.maaston_lukija.maastot
        ominaisuudet = maastot[self.__tyyppi]
        self.__maasto = Maasto(ominaisuudet.tyyppi, ominaisuudet.liikkuminen, ominaisuudet.liikkumisen_hinta,
                               ominaisuudet.hyokkayskerroin, ominaisuudet.puolustuskerroin, ominaisuudet.vari,
                               ominaisuudet.lapinakyvyys)

    def etsi_naapurit(self):
        self.__kartta = self.__kayttoliittyma.pelinohjain.kartta

        # suunnat naapureiden löytämistä varten
        pohjoinen = (self.__koordinaatit.x, self.__koordinaatit.y + 1)
        ita = (self.__koordinaatit.x + 1, self.__koordinaatit.y)
        etela = (self.__koordinaatit.x, self.__koordinaatit.y - 1)
        lansi = (self.__koordinaatit.x - 1, self.__koordinaatit.y)
        naapuri_koordinaatit = (pohjoinen, ita, etela, lansi)

        self.__naapurit = []
        for ruutu in self.__kartta.ruudut:
            if (ruutu.koordinaatit.x, ruutu.koordinaatit.y) in naapuri_koordinaatit:
                self.__naapurit.append(ruutu)

    def vapaat_naapurit(self):
        vapaat = []
        for naapuri in self.__naapurit:
            if naapuri.yksikko is None and naapuri.maasto.liikkuminen:
                vapaat.append(naapuri)
        return vapaat

    def luo_kiilat(self, bonus, bonus_ratsuvaki):
        self.__kiilat = Kiilat(bonus, bonus_ratsuvaki, self, self.__kayttoliittyma)

    def liiku_pois(self):
        self.__yksikko = None

    def liiku_ruutuun(self, yksikko):
        self.__yksikko = yksikko

    def poista_yksikko(self):
        self.__yksikko = None

    def poista_kiilat(self):
        self.__kiilat = None
