from yksikkografiikka import Yksikkografiikka

class Yksikko:

    def __init__(self, omistaja, ruutu, kayttoliittyma):
        self.omistaja = omistaja
        self.ruutu = ruutu
        self.kayttoliittyma = kayttoliittyma
        self.grafiikka = None

        #self.luo_grafiikka()

        print(self.ruutu.koordinaatit.x, " ", self.ruutu.koordinaatit.y, " ", self.omistaja)

    def luo_grafiikka(self):
        self.grafiikka = Yksikkografiikka(self, self.ruutu.grafiikka.koko)