from kiilagrafiikka import Kiilagrafiikka

class Kiilat:

    def __init__(self, bonus, bonus_ratsuvaki, ruutu, kayttoliittyma):
        self.puolustusbonus = bonus
        self.puolustusbonus_ratsuvaki = bonus_ratsuvaki
        self.ruutu = ruutu
        self.kayttoliittyma = kayttoliittyma
        self.kiilagrafiikka = Kiilagrafiikka(self.ruutu)

    def tuhoa(self):
        # poista grafiikka
        self.kiilagrafiikka.poista()
        self.kiilagrafiikka = None
        # poista ruudusta
        self.ruutu.kiilat = None