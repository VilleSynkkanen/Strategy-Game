from yksikkografiikka import Yksikkografiikka

class Yksikko:

    def __init__(self, omistaja, ruutu, kayttoliittyma):
        self.omistaja = omistaja
        self.ruutu = ruutu
        self.kayttoliittyma = kayttoliittyma
        self.grafiikka = None

    def luo_grafiikka(self):
        self.grafiikka = Yksikkografiikka(self, self.ruutu, self.kayttoliittyma, self.omistaja)

    def luo_ominaisuudet(self):
        pass