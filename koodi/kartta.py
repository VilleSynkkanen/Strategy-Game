from koordinaatit import Koordinaatit
from ruutu import Ruutu

class Kartta:

    def __init__(self, x, y, ruudut, kayttoliittyma):
        self.kayttoliittyma = kayttoliittyma
        self.ruudun_koko = 44
        self.ruudut = self.luo_ruudut(x, y, ruudut)
        self.pelaajan_yksikot = []
        self.tietokoneen_yksikot = []

    def luo_ruudut(self, x, y, ruudut):
        lista = []
        for i in range(0, x, 1):
            for j in range(0, y, 1):
                koordinaatit = Koordinaatit(i, j)
                ruutu = Ruutu(koordinaatit, self.ruudun_koko, ruudut[i][j], self.kayttoliittyma)   # placeholder tyyppi
                lista.append(ruutu)
        return lista

    def lisaa_yksikot(self, yksikot, ominaisuudet):
        # yksikot = yksiköiden sijainnit
        # ominaisuudet = yksiköiden ominaisuudet (luettu tiedostoista)

        # lisää ominaisuudet yksiköihin

        for elementti in yksikot:
            # elementti = yksikön tyyppi
            for yksikko in yksikot[elementti]:
                for ruutu in self.ruudut:
                    if yksikko[0].x == ruutu.koordinaatit.x and yksikko[0].y == ruutu.koordinaatit.y:
                        luotu_yksikko = ruutu.lisaa_yksikko(elementti, yksikko[1], ominaisuudet[elementti])
                        if luotu_yksikko.omistaja == "PLR":
                            self.pelaajan_yksikot.append(luotu_yksikko)
                        elif luotu_yksikko.omistaja == "COM":
                            self.tietokoneen_yksikot.append(luotu_yksikko)

