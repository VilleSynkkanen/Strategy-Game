class Yksikon_ominaisuudet:

    def __init__(self, tyyppi, liikkuminen, max_elama, nyk_elama, max_energia, nyk_energia, hyokkays, puolustus, kantama, hinta, tilavaikutukset):
        self.__tyyppi = tyyppi
        self.__liikkuminen = liikkuminen
        self.__max_elama = max_elama
        self.__nyk_elama = nyk_elama
        self.__max_energia = max_energia
        self.__nyk_energia = 0
        self.__hyokkays = hyokkays
        self.__puolustus = puolustus
        self.__kantama = kantama
        self.__hinta = hinta
        self.__tilavaikutukset = []

    @property
    def tyyppi(self):
        return self.__tyyppi

    @property
    def liikkuminen(self):
        return self.__liikkuminen

    @liikkuminen.setter
    def liikkuminen(self, arvo):
        self.__liikkuminen = arvo

    @property
    def max_elama(self):
        return self.__max_elama

    @property
    def nyk_elama(self):
        return self.__nyk_elama

    @nyk_elama.setter
    def nyk_elama(self, arvo):
        self.__nyk_elama = arvo

    @property
    def max_energia(self):
        return self.__max_energia

    @property
    def nyk_energia(self):
        return self.__nyk_energia

    @nyk_energia.setter
    def nyk_energia(self, arvo):
        self.__nyk_energia = arvo

    @property
    def hyokkays(self):
        return self.__hyokkays

    @hyokkays.setter
    def hyokkays(self, arvo):
        self.__hyokkays = arvo

    @property
    def puolustus(self):
        return self.__puolustus

    @puolustus.setter
    def puolustus(self, arvo):
        self.__puolustus = arvo

    @property
    def kantama(self):
        return self.__kantama

    @kantama.setter
    def kantama(self, arvo):
        self.__kantama = arvo

    @property
    def hinta(self):
        return self.__hinta

    @property
    def tilavaikutukset(self):
        return self.__tilavaikutukset

    def __str__(self):
        return "Tyyppi: {}\nLiikkuminen: {}\nElämä: {}/{}\nEnergia: {}/{}\nHyökkäys: {}\nPuolustus: {}\nKantama: {}"\
            .format(self.__tyyppi, self.__liikkuminen, self.__nyk_elama, self.__max_elama, self.__nyk_energia, self.__max_energia,
                    self.__hyokkays, self.__puolustus, self.__kantama)