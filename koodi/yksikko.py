from yksikkografiikka import Yksikkografiikka
from yksikon_ominaisuudet import Yksikon_ominaisuudet
from random import randrange

class Yksikko:

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        self.omistaja = omistaja
        self.ruutu = ruutu
        self.kayttoliittyma = kayttoliittyma
        self.grafiikka = None
        self.ominaisuudet = self.luo_ominaisuudet(ominaisuudet)

        # ruudut, joihin liikkuminen on mahdollista tällä vuorolla
        self.mahdolliset_ruudut = []

        # mahdolliset hyökkäyskohteet
        self.hyokkayksen_kohteet = []

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

    def laske_hyokkayksen_kohteet(self):
        # implementoi line of sight sääntö
        for vihollinen in self.kayttoliittyma.pelinohjain.kartta.tietokoneen_yksikot:
            etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.ruutu, vihollinen.ruutu)
            if etaisyys <= self.ominaisuudet.kantama:
                self.hyokkayksen_kohteet.append(vihollinen)
        self.nayta_hyokkayksen_kohteet()

    def peru_hyokkayksen_kohteiden_nayttaminen(self):
        for vihollinen in self.hyokkayksen_kohteet:
            vihollinen.grafiikka.palauta_vari()
        self.hyokkayksen_kohteet = []

    def nayta_hyokkayksen_kohteet(self):
        for vihollinen in self.hyokkayksen_kohteet:
            vihollinen.grafiikka.muuta_varia(vihollinen.grafiikka.voi_hyokata_vari)

    def tyhjenna_hyokkayksen_kohteet(self):
        self.hyokkayksen_kohteet = []

    def peru_mahdollisten_ruutujen_nayttaminen(self):
        for ruutu in self.mahdolliset_ruudut:
            ruutu.grafiikka.palauta_vari()

    def liiku_ruutuun(self, ruutu):
        self.ruutu.liiku_pois()
        self.ruutu = ruutu
        ruutu.liiku_ruutuun(self)
        self.grafiikka.paivita_sijainti(self.ruutu)
        self.liikuttu()

    def liikuttu(self):
        self.peru_mahdollisten_ruutujen_nayttaminen()
        self.liikkuminen_kaytetty = True
        self.mahdolliset_ruudut = []

    def palauta_liikkumispisteet(self):
        self.liikkuminen_kaytetty = False
        self.hyokkays_kaytetty = False

    def hyokatty(self):
        self.tyhjenna_hyokkayksen_kohteet()
        self.hyokkays_kaytetty = True
        self.liikuttu()

    def hyokkayksen_kohde(self, hyokkaaja):
        self.laske_vahinko(hyokkaaja)
        if hyokkaaja == self.kayttoliittyma.valittu_yksikko:
            for vihollinen in hyokkaaja.hyokkayksen_kohteet:
                vihollinen.grafiikka.palauta_vari()
            self.kayttoliittyma.peru_kohteen_valinta()
        hyokkaaja.hyokatty()

    def laske_vahinko(self, hyokkaaja):
        # hyökkääjä = hyökkääjä
        # puolustaja = self
        hyokkays = hyokkaaja.ominaisuudet.hyokkays * hyokkaaja.ruutu.maasto.hyokkayskerroin * \
                    (hyokkaaja.ominaisuudet.nyk_elama / hyokkaaja.ominaisuudet.max_elama)
        puolustus = self.ominaisuudet.puolustus * self.ruutu.maasto.puolustuskerroin * \
                    (self.ominaisuudet.nyk_elama / self.ominaisuudet.max_elama)
        etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.ruutu, hyokkaaja.ruutu)

        # aiheutettu vahinko = voima / vihollisen voima * perusvahinko, [min_vahinko, max_vahinko]
        # puolustettaessa voima = puolustus, hyökättäessä voima = hyökkäys
        # vahinko voi vaihdella +-15%

        perusvahinko = 10
        min_vahinko = 2
        max_vahinko = 40
        satunnaisuuskerroin = 0.15

        if etaisyys == 1:
            hyokkaajan_vahinko = (puolustus / hyokkays) * perusvahinko
            if hyokkaajan_vahinko < min_vahinko:
                hyokkaajan_vahinko = min_vahinko
            elif hyokkaajan_vahinko > max_vahinko:
                hyokkaajan_vahinko = max_vahinko
        else:
            hyokkaajan_vahinko = 0

        puolustajan_vahinko = (hyokkays / puolustus) * perusvahinko
        if puolustajan_vahinko < min_vahinko:
            puolustajan_vahinko = min_vahinko
        elif puolustajan_vahinko > max_vahinko:
            puolustajan_vahinko = max_vahinko

        hyokkaajan_vahinko_min = int(hyokkaajan_vahinko * (1 - satunnaisuuskerroin))
        hyokkaajan_vahinko_max = int(hyokkaajan_vahinko * (1 + satunnaisuuskerroin))

        puolustajan_vahinko_min = int(puolustajan_vahinko * (1 - satunnaisuuskerroin))
        puolustajan_vahinko_max = int(puolustajan_vahinko * (1 + satunnaisuuskerroin))

        hyokkaajan_vahinko = randrange(hyokkaajan_vahinko_min, hyokkaajan_vahinko_max + 1, 1)
        puolustajan_vahinko = randrange(puolustajan_vahinko_min, puolustajan_vahinko_max + 1, 1)

        self.ota_vahinkoa(puolustajan_vahinko)
        hyokkaaja.ota_vahinkoa(hyokkaajan_vahinko)

    def ota_vahinkoa(self, vahinko):
        self.ominaisuudet.nyk_elama -= vahinko
        self.grafiikka.elamapalkki.paivita_koko()
        self.grafiikka.paivita_tooltip()



