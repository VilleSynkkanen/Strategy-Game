from koordinaatit import Koordinaatit
from ruutu import Ruutu

class Kartta:

    def __init__(self, x, y, ruudut, kayttoliittyma):
        self.kayttoliittyma = kayttoliittyma
        self.ruudun_koko = 44
        self.ruudut = self.luo_ruudut(x, y, ruudut)

    def luo_ruudut(self, x, y, ruudut):
        lista = []
        for i in range(0, x, 1):
            for j in range(0, y, 1):
                koordinaatit = Koordinaatit(i, j)
                ruutu = Ruutu(koordinaatit, self.ruudun_koko, "tasanko", self.kayttoliittyma)   # placeholder tyyppi
                lista.append(ruutu)
        return lista