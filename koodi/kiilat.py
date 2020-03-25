from kiilagrafiikka import Kiilagrafiikka


class Kiilat:

    def __init__(self, bonus, bonus_ratsuvaki, ruutu, kayttoliittyma):
        self.__puolustusbonus = bonus
        self.__puolustusbonus_ratsuvaki = bonus_ratsuvaki
        self.__ruutu = ruutu
        self.__kayttoliittyma = kayttoliittyma
        self.__kiilagrafiikka = Kiilagrafiikka(self.__ruutu)

    def tuhoa(self):
        # poista grafiikka
        self.__kiilagrafiikka.poista()
        self.__kiilagrafiikka = None
        # poista ruudusta
        self.__ruutu.poista_kiilat()

    @property
    def puolustusbonus(self):
        return self.__puolustusbonus

    @property
    def puolustusbonus_ratsuvaki(self):
        return self.__puolustusbonus_ratsuvaki
