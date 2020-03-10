class Yksikon_ominaisuudet:

    def __init__(self, tyyppi, liikkuminen, max_elama, nyk_elama, max_energia, nyk_energia, hyokkays, puolustus, kantama, hinta, tilavaikutukset):
        self.tyyppi = tyyppi
        self.liikkuminen = liikkuminen
        self.max_elama = max_elama
        self.nyk_elama = nyk_elama
        self.max_energia = max_energia
        self.nyk_energia = nyk_energia
        self.hyokkays = hyokkays
        self.puolustus = puolustus
        self.kantama = kantama
        self.hinta = hinta
        self.tilavaikutukset = tilavaikutukset

    def __str__(self):
        return "Tyyppi: {}\nLiikkuminen: {}\nElämä: {}/{}\nEnergia: {}/{}\nHyökkäys: {}\nPuolustus: {}\nKantama: {}"\
            .format(self.tyyppi, self.liikkuminen, self.nyk_elama, self.max_elama, self.nyk_energia, self.max_energia,
                    self.hyokkays, self.puolustus, self.kantama)

