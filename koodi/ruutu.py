from koordinaatit import Koordinaatit
from maasto import Maasto
from ruutugrafiikka import Ruutugrafiikka

class Ruutu:

    def __init__(self, koordinaatit, koko, tyyppi, kayttoliittyma):
        self.kayttoliittyma = kayttoliittyma
        self.koordinaatit = koordinaatit
        self.grafiikka = self.luo_grafiikka(tyyppi, koko)
        self.maasto = self.luo_maasto(tyyppi)
        self.naapurit = []      # toteutus???

    def luo_grafiikka(self, tyyppi, koko):
        grafiikka = Ruutugrafiikka(self.koordinaatit, koko, self.kayttoliittyma)
        return grafiikka

    def luo_maasto(self, tyyppi):
        return Maasto()     # placeholder
