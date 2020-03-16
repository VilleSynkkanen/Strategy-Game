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
        self.ruudut_kantamalla = []

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

    def laske_hyokkayksen_kohteet(self, nayta):
        # implementoi line of sight sääntö
        self.hyokkayksen_kohteet = []
        for vihollinen in self.kayttoliittyma.pelinohjain.kartta.tietokoneen_yksikot:
            etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.ruutu, vihollinen.ruutu)
            if etaisyys <= self.ominaisuudet.kantama:
                self.hyokkayksen_kohteet.append(vihollinen)
        if not nayta:
            return
        self.nayta_hyokkayksen_kohteet()
        self.laske_kantaman_sisalla_olevat_ruudut()
        self.nayta_kantaman_sisalla_olevat_ruudut()

    def peru_hyokkayksen_kohteiden_nayttaminen(self):
        for vihollinen in self.hyokkayksen_kohteet:
            vihollinen.grafiikka.palauta_vari()
            vihollinen.grafiikka.paivita_tooltip()
        self.hyokkayksen_kohteet = []
        self.tyhjenna_ruudut_kantamalla()

    def laske_kantaman_sisalla_olevat_ruudut(self):
        self.ruudut_kantamalla = []
        for ruutu in self.kayttoliittyma.pelinohjain.kartta.ruudut:
            if self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.ruutu, ruutu) <= self.ominaisuudet.kantama:
                self.ruudut_kantamalla.append(ruutu)

    def nayta_kantaman_sisalla_olevat_ruudut(self):
        for ruutu in self.ruudut_kantamalla:
            ruutu.grafiikka.muuta_vari(ruutu.grafiikka.kantaman_sisalla_vari)

    def nayta_hyokkayksen_kohteet(self):
        for vihollinen in self.hyokkayksen_kohteet:
            vihollinen.grafiikka.muuta_varia(vihollinen.grafiikka.voi_hyokata_vari)
            # laskee odotetun vahingon ja näyttää sen tooltipissä
            hyok_vahinko, puol_vahinko = self.laske_vahinko(self, vihollinen, True)
            vihollinen.grafiikka.hyokkays_tootip(hyok_vahinko, puol_vahinko)

    def tyhjenna_hyokkayksen_kohteet(self):
        self.hyokkayksen_kohteet = []

    def peru_mahdollisten_ruutujen_nayttaminen(self):
        for ruutu in self.mahdolliset_ruudut:
            ruutu.grafiikka.palauta_vari()

    def tyhjenna_ruudut_kantamalla(self):
        for ruutu in self.ruudut_kantamalla:
            ruutu.grafiikka.palauta_vari()
        self.ruudut_kantamalla = []

    def liiku_ruutuun(self, ruutu):
        self.ruutu.liiku_pois()
        self.ruutu = ruutu
        ruutu.liiku_ruutuun(self)
        self.grafiikka.paivita_sijainti(self.ruutu)
        self.liikuttu()
        self.laske_hyokkayksen_kohteet(False)
        if len(self.hyokkayksen_kohteet) == 0:
            # poista yksiköistä, jotka voivat vielä tehdä jotain
            self.kayttoliittyma.pelinohjain.kartta.poista_toimivista_yksikoista(self)

    def liikuttu(self):
        self.peru_mahdollisten_ruutujen_nayttaminen()
        self.liikkuminen_kaytetty = True
        self.mahdolliset_ruudut = []
        self.kayttoliittyma.paivita_valitun_yksikon_tiedot()

    def palauta_liikkumispisteet(self):
        self.liikkuminen_kaytetty = False
        self.hyokkays_kaytetty = False
        self.grafiikka.palauta_vari()

    def hyokatty(self):
        # poista listoista kantamalla olevat ruudut ja mahdolliset kohteet
        self.tyhjenna_hyokkayksen_kohteet()
        self.tyhjenna_ruudut_kantamalla()
        self.hyokkays_kaytetty = True
        self.liikuttu()
        self.kayttoliittyma.paivita_valitun_yksikon_tiedot()
        # poista yksiköistä, jotka voivat vielä tehdä jotain
        self.kayttoliittyma.pelinohjain.kartta.poista_toimivista_yksikoista(self)

    def hyokkayksen_kohde(self, hyokkaaja):
        self.hyokkays(hyokkaaja)
        if hyokkaaja == self.kayttoliittyma.valittu_yksikko:
            for vihollinen in hyokkaaja.hyokkayksen_kohteet:
                vihollinen.grafiikka.palauta_vari()
            self.kayttoliittyma.peru_kohteen_valinta()
        hyokkaaja.hyokatty()

    def laske_vahinko(self, hyokkaaja, puolustaja, odotettu):
        # odotettu: bool, joka kertoo, palautetaanko odotettu vai todellinen vahinko
        # hyökkääjä = hyökkääjä
        hyokkays = hyokkaaja.ominaisuudet.hyokkays * hyokkaaja.ruutu.maasto.hyokkayskerroin * \
                   (0.5 * (hyokkaaja.ominaisuudet.nyk_elama / hyokkaaja.ominaisuudet.max_elama) + 0.5)
        puolustus = puolustaja.ominaisuudet.puolustus * puolustaja.ruutu.maasto.puolustuskerroin * \
                    (0.5 * (puolustaja.ominaisuudet.nyk_elama / puolustaja.ominaisuudet.max_elama) + 0.5)
        etaisyys = puolustaja.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(puolustaja.ruutu, hyokkaaja.ruutu)

        # aiheutettu vahinko = voima / vihollisen voima * perusvahinko, [min_vahinko, max_vahinko]
        # puolustettaessa voima = puolustus, hyökättäessä voima = hyökkäys
        # vahinko voi vaihdella +-15%
        # elämän vaikutus voimaan: kerroin = 0.5 * elämä + 0.5 (= 1, kun täysi elämä, 0.5, kun elämä 0)

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

        if odotettu:
            return int(hyokkaajan_vahinko), int(puolustajan_vahinko)

        hyokkaajan_vahinko_min = int(hyokkaajan_vahinko * (1 - satunnaisuuskerroin))
        hyokkaajan_vahinko_max = int(hyokkaajan_vahinko * (1 + satunnaisuuskerroin))

        puolustajan_vahinko_min = int(puolustajan_vahinko * (1 - satunnaisuuskerroin))
        puolustajan_vahinko_max = int(puolustajan_vahinko * (1 + satunnaisuuskerroin))

        hyokkaajan_vahinko = randrange(hyokkaajan_vahinko_min, hyokkaajan_vahinko_max + 1, 1)
        puolustajan_vahinko = randrange(puolustajan_vahinko_min, puolustajan_vahinko_max + 1, 1)

        return hyokkaajan_vahinko, puolustajan_vahinko

    # puolustautuminen
    def hyokkays(self, hyokkaaja):
        hyokkaajan_vahinko, puolustajan_vahinko = self.laske_vahinko(hyokkaaja, self, False)
        self.ota_vahinkoa(puolustajan_vahinko)
        hyokkaaja.ota_vahinkoa(hyokkaajan_vahinko)

    def ota_vahinkoa(self, vahinko):
        self.ominaisuudet.nyk_elama -= vahinko
        self.grafiikka.elamapalkki.paivita_koko()
        self.grafiikka.paivita_tooltip()
        self.tarkasta_tuhoutuminen()

    def tarkasta_tuhoutuminen(self):
        if self.ominaisuudet.nyk_elama <= 0:
            self.tuhoudu()

    def tuhoudu(self):
        # jos valittu yksikkö, poista käyttöliittymästä
        if self.kayttoliittyma.valittu_yksikko == self:
            self.kayttoliittyma.tyhjenna_valinta()
        # poista kartan listasta
        self.kayttoliittyma.pelinohjain.kartta.poista_yksikko(self)
        # poista ruudusta
        self.ruutu.poista_yksikko()
        # tuhoa elämäpalkki
        self.grafiikka.elamapalkki.poista()
        # tuhoa grafiikka
        self.grafiikka.poista()
        # poista viittaus ominaisuuksiin
        self.ominaisuudet = None
        # tuhoa yksikkö

        print("tuhottu")





