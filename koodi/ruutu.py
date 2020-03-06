from koordinaatit import Koordinaatit
from maasto import Maasto
from ruutugrafiikka import Ruutugrafiikka

class Ruutu:

    def __init__(self, koordinaatit, koko, tyyppi, kayttoliittyma):
        self.tyyppi = tyyppi
        self.kayttoliittyma = kayttoliittyma
        self.koordinaatit = koordinaatit
        self.grafiikka = None
        self.kartta = None  # etsitään myöhemmin
        self.maasto = None  # luodaan myöhemmin
        self.naapurit = []  # etsitään myöhemmin

    def luo_grafiikka(self, koko):
        self.grafiikka = Ruutugrafiikka(self.koordinaatit, koko, self.kayttoliittyma, self.maasto.vari, self)

    def luo_maasto(self):
        maastot = self.kayttoliittyma.pelinohjain.maaston_lukija.maastot
        ominaisuudet = maastot[self.tyyppi]
        self.maasto = Maasto(ominaisuudet.tyyppi, ominaisuudet.liikkuminen, ominaisuudet.liikkumisen_hinta,
                             ominaisuudet.hyokkayskerroin, ominaisuudet.puolustuskerroin, ominaisuudet.vari,
                             ominaisuudet.lapinakyvyys)

    def etsi_naapurit(self):
        self.kartta = self.kayttoliittyma.pelinohjain.kartta

        # suunnat naapureiden löytämistä varten
        pohjoinen = (self.koordinaatit.x, self.koordinaatit.y + 1)
        ita = (self.koordinaatit.x + 1, self.koordinaatit.y)
        etela = (self.koordinaatit.x, self.koordinaatit.y - 1)
        lansi = (self.koordinaatit.x - 1, self.koordinaatit.y)
        naapuri_koordinaatit = (pohjoinen, ita, etela, lansi)

        self.naapurit = []
        for ruutu in self.kartta.ruudut:
            if (ruutu.koordinaatit.x, ruutu.koordinaatit.y) in naapuri_koordinaatit and ruutu.maasto.liikkuminen == True:
                self.naapurit.append(ruutu)


