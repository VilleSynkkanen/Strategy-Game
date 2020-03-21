from kiilagrafiikka import Kiilagrafiikka

class Kiilat:

    def __init__(self, bonus, bonus_ratsuvaki, ruutu, kayttoliittyma):
        self.puolustusbonus = bonus
        self.puolustusbonus_ratsuvaki = bonus_ratsuvaki
        self.ruutu = ruutu
        self.kayttoliittyma = kayttoliittyma
        self.kiilagrafiikka = Kiilagrafiikka(self.ruutu)