from kiilagrafiikka import Kiilagrafiikka

class Kiilat:

    def __init__(self, bonus, bonus_ratsuvaki, ruutu, kayttoliittyma):
        self._puolustusbonus = bonus
        self._puolustusbonus_ratsuvaki = bonus_ratsuvaki
        self._ruutu = ruutu
        self._kayttoliittyma = kayttoliittyma
        self._kiilagrafiikka = Kiilagrafiikka(self._ruutu)

    def tuhoa(self):
        # poista grafiikka
        self._kiilagrafiikka.poista()
        self._kiilagrafiikka = None
        # poista ruudusta
        self._ruutu.kiilat = None

    @property
    def puolustusbonus(self):
        return self._puolustusbonus

    @property
    def puolustusbonus_ratsuvaki(self):
        return self._puolustusbonus_ratsuvaki
