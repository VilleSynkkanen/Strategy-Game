from koordinaatit import Koordinaatit
from ruutu import Ruutu
from math import sqrt

class Kartta:

    def __init__(self, x, y, ruudut, kayttoliittyma):
        self.kayttoliittyma = kayttoliittyma
        self.ruudun_koko = 44
        # ruudut = tavallinen lista, ruudut_koordinaateilla = 2d-lista (näkemisen laskemiseen tms.)
        self.ruudut, self.ruudut_koordinaateilla = self.luo_ruudut(x, y, ruudut)
        self.pelaajan_yksikot = []
        self.tietokoneen_yksikot = []
        self.pelaajan_toimivat_yksikot = []

    def luo_ruudut(self, x, y, ruudut):
        lista = []
        koord_lista = [[None for i in range(y)] for j in range(x)]
        for i in range(0, x, 1):
            for j in range(0, y, 1):
                koordinaatit = Koordinaatit(i, j)
                ruutu = Ruutu(koordinaatit, self.ruudun_koko, ruudut[i][j], self.kayttoliittyma)   # placeholder tyyppi
                lista.append(ruutu)
        for ruutu in lista:
            x_koord = ruutu.koordinaatit.x
            y_koord = ruutu.koordinaatit.y
            koord_lista[x_koord][y_koord] = ruutu
        return lista, koord_lista

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
        self.palauta_pelaajan_toimivat_yksikot()

    def poista_yksikko(self, yksikko):
        if yksikko.omistaja == "COM":
            for Yksikko in self.tietokoneen_yksikot:
                if Yksikko == yksikko:
                    self.tietokoneen_yksikot.remove(yksikko)
        elif yksikko.omistaja == "PLR":
            for Yksikko in self.pelaajan_yksikot_yksikot:
                if Yksikko == yksikko:
                    self.pelaajan_yksikot.remove(yksikko)
                    if yksikko in self.pelaajan_toimivat_yksikot:
                        self.pelaajan_toimivat_yksikot.remove(yksikko)

    def poista_toimivista_yksikoista(self, yksikko):
        # hyökkäyksen kohteiden määrän tarkistus tehdään ennen, kuin kutsutaan tätä metodia
        if not yksikko.pystyy_toimimaan():
            self.pelaajan_toimivat_yksikot.remove(yksikko)

    def palauta_pelaajan_toimivat_yksikot(self):
        self.pelaajan_toimivat_yksikot = []
        for yksikko in self.pelaajan_yksikot:
            self.pelaajan_toimivat_yksikot.append(yksikko)

    def nakyvyys(self, alku, loppu):
        # algoritmi: edetään step * pituus verran pisteiden välistä suoraa ja tarkistetaan, onko se ruudussa, joka ei
        # ole läpinäkyvä, aloitetaan/lopetetaan ruudun keskeltä/keskelle
        x_alku = alku.koordinaatit.x
        y_alku = alku.koordinaatit.y
        x_loppu = loppu.koordinaatit.x
        y_loppu = loppu.koordinaatit.y
        x_muutos = x_loppu - x_alku
        y_muutos = y_loppu - y_alku
        muutos = sqrt(x_muutos*x_muutos + y_muutos*y_muutos)
        step = 0.1
        # mitä pidempi etäisyys, sitä lyhyempi step
        if muutos != 0:
            step = 0.1 / sqrt(x_muutos*x_muutos + y_muutos*y_muutos)
        toistot = 0
        nyk = [x_alku, y_alku]
        koord_x = nyk[0]
        koord_y = nyk[1]
        while toistot < 1 / step:
            toistot += 1
            nyk[0] += step * x_muutos
            nyk[1] += step * y_muutos
            # tarkistetaan, onko ruutu vaihtunut:
            ero_x = nyk[0] - koord_x
            ero_y = nyk[1] - koord_y
            if ero_x > 0.5:
                koord_x += 1
            elif ero_x < -0.5:
                koord_x -=1
            if ero_y > 0.5:
                koord_y += 1
            elif ero_y < -0.5:
                koord_y -= 1
            if self.ruudut_koordinaateilla[koord_x][koord_y].maasto.lapinakyvyys is False and \
                    self.ruudut_koordinaateilla[koord_x][koord_y] != alku and \
                    self.ruudut_koordinaateilla[koord_x][koord_y] != loppu:
                return False
        return True