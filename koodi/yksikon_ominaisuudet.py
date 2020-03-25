class Yksikon_ominaisuudet:

    def __init__(self, tyyppi, liikkuminen, max_elama, nyk_elama, max_energia, nyk_energia, hyokkays, puolustus, kantama, hinta, tilavaikutukset):
        self._tyyppi = tyyppi
        self._liikkuminen = liikkuminen
        self._max_elama = max_elama
        self._nyk_elama = nyk_elama
        self._max_energia = max_energia
        self._nyk_energia = 0
        self._hyokkays = hyokkays
        self._puolustus = puolustus
        self._kantama = kantama
        self._hinta = hinta
        self._tilavaikutukset = []

    @property
    def tyyppi(self):
        return self._tyyppi

    @property
    def liikkuminen(self):
        return self._liikkuminen

    @liikkuminen.setter
    def liikkuminen(self, arvo):
        self._liikkuminen = arvo

    @property
    def max_elama(self):
        return self._max_elama

    @property
    def nyk_elama(self):
        return self._nyk_elama

    @nyk_elama.setter
    def nyk_elama(self, arvo):
        self._nyk_elama = arvo

    @property
    def max_energia(self):
        return self._max_energia

    @property
    def nyk_energia(self):
        return self._nyk_energia

    @nyk_energia.setter
    def nyk_energia(self, arvo):
        self._nyk_energia = arvo

    @property
    def hyokkays(self):
        return self._hyokkays

    @hyokkays.setter
    def hyokkays(self, arvo):
        self._hyokkays = arvo

    @property
    def puolustus(self):
        return self._puolustus

    @puolustus.setter
    def puolustus(self, arvo):
        self._puolustus = arvo

    @property
    def kantama(self):
        return self._kantama

    @kantama.setter
    def kantama(self, arvo):
        self._kantama = arvo

    @property
    def hinta(self):
        return self._hinta

    @property
    def tilavaikutukset(self):
        return self._tilavaikutukset

    def __str__(self):
        return "Tyyppi: {}\nLiikkuminen: {}\nElämä: {}/{}\nEnergia: {}/{}\nHyökkäys: {}\nPuolustus: {}\nKantama: {}"\
            .format(self._tyyppi, self._liikkuminen, self._nyk_elama, self._max_elama, self._nyk_energia, self._max_energia,
                    self._hyokkays, self._puolustus, self._kantama)