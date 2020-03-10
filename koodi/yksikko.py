from yksikkografiikka import Yksikkografiikka
from yksikon_ominaisuudet import Yksikon_ominaisuudet

class Yksikko:

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        self.omistaja = omistaja
        self.ruutu = ruutu
        self.kayttoliittyma = kayttoliittyma
        self.grafiikka = None
        self.ominaisuudet = self.luo_ominaisuudet(ominaisuudet)

        # ruudut, joihin liikkuminen on mahdollista tällä vuorolla
        self.mahdolliset_ruudut = []

        self.liikkuminen_kaytetty = False
        self.hyokkays_kaytetty = False

    def luo_grafiikka(self):
        self.grafiikka = Yksikkografiikka(self, self.ruutu, self.kayttoliittyma, self.omistaja, self)

    def luo_ominaisuudet(self, ominaisuudet):
        # luo ominaisuudet annetun ominaisuus-instanssin perusteella
        om = Yksikon_ominaisuudet(ominaisuudet.tyyppi, ominaisuudet.liikkuminen, ominaisuudet.max_elama,
                                  ominaisuudet.nyk_elama, ominaisuudet.max_energia, ominaisuudet.nyk_energia,
                                  ominaisuudet.hyokkays, ominaisuudet.puolustus, ominaisuudet.kantama, ominaisuudet.hinta,
                                  ominaisuudet.tilavaikutukset)
        return om

    def laske_mahdolliset_ruudut(self):
        self.mahdolliset_ruudut = self.kayttoliittyma.pelinohjain.laske_polut(self.ruutu, self.ominaisuudet.liikkuminen)

    def nayta_mahdolliset_ruudut(self):
        for ruutu in self.mahdolliset_ruudut:
            ruutu.grafiikka.voi_liikkua()

    def tyhjenna_mahdolliset_ruudut(self):
        self.mahdolliset_ruudut = []

    def liiku_ruutuun(self, ruutu):
        self.ruutu.liiku_pois()
        self.ruutu = ruutu
        ruutu.liiku_ruutuun(self)
        self.grafiikka.paivita_sijainti(self.ruutu)
        self.liikuttu()

    def liikuttu(self):
        for ruutu in self.mahdolliset_ruudut:
            ruutu.grafiikka.palauta_vari()
        self.liikkuminen_kaytetty = True
        self.mahdolliset_ruudut = []

    def palauta_liikkumispisteet(self):
        self.liikkuminen_kaytetty = False

    def hyokatty(self):
        pass