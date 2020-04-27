from yksikko import Yksikko
from tilavaikutus import Tilavaikutus
from math import sqrt
from random import randrange
from ajastin import Ajastin


class Parantaja(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        self.__inspiraatio_kantama = int(kyvyt["inspiraatio_kantama"])
        self.__inspiraatio_kerroin = kyvyt["inspiraatio_kerroin"]

        # kyky 1 tiedot
        self.__kyky1_hinta = int(kyvyt["kyky1_hinta"])
        self.__kyky1_kohteiden_maara = int(kyvyt["kyky1_kohteiden_maara"])
        self.__kyky1_kantama = int(kyvyt["kyky1_kantama"])
        self.__kyky1_parannuskerroin = int(kyvyt["kyky1_parannuskerroin"])

        # kyky 2 tiedot
        self.__kyky2_hinta = int(kyvyt["kyky2_hinta"])
        self.__kyky2_kesto = int(kyvyt["kyky2_kesto"])
        self.__kyky2_hyokkaysvahennys = int(kyvyt["kyky2_hyokkaysvahennys"])
        self.__kyky2_puolustusvahennys = int(kyvyt["kyky2_puolustusvahennys"])
        self.__kyky2_taintumisaika = int(kyvyt["kyky2_taintumisaika"])

    # propertyt

    @property
    def inspiraatio_kantama(self):
        return self.__inspiraatio_kantama

    @property
    def inspiraatio_kerroin(self):
        return self.__inspiraatio_kerroin

    @property
    def kyky1_hinta(self):
        return self.__kyky1_hinta

    @property
    def kyky1_kohteiden_maara(self):
        return self.__kyky1_kohteiden_maara

    @property
    def kyky1_kantama(self):
        return self.__kyky1_kantama

    @property
    def kyky1_parannuskerroin(self):
        return self.__kyky1_parannuskerroin

    @property
    def kyky2_hinta(self):
        return self.__kyky2_hinta

    @property
    def kyky2_kesto(self):
        return self.__kyky2_kesto

    @property
    def kyky2_hyokkaysvahennys(self):
        return self.__kyky2_hyokkaysvahennys

    @property
    def kyky2_puolustusvahennys(self):
        return self.__kyky2_puolustusvahennys

    # passiivinen tehty
    # kyky 1 tehty
    # kyky 2 tehty

    # parannuksen määrä = hyökkäys * parannuskerroin / sqrt(etäisyys + 1) (+-15% satunnaisuus)
    # kykyihin pätee näkyvyyssäännöt

    def kyky1_lisaa_kohde(self, ruutu, tekoaly=False):
        # lisätään kantaman päässä olevat ruudut, sitten käytetään kyky
        if ruutu in self.ruudut_kantamalla:
            self.kyky1_kohteet.append(ruutu)
            if not tekoaly:
                ruutu.grafiikka.muuta_vari(ruutu.grafiikka.valittu_kohteeksi_vari)
            for Ruutu in self.kayttoliittyma.pelinohjain.kartta.ruudut:
                if self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, Ruutu) <= self.kyky1_kantama and \
                        Ruutu not in self.kyky1_kohteet:
                    self.kyky1_kohteet.append(Ruutu)
                    if not tekoaly:
                        Ruutu.grafiikka.muuta_vari(Ruutu.grafiikka.valittu_kohteeksi_vari)
            if not tekoaly:
                Ajastin.aloita_ajastin(self.visualisointi_viive, self.__kayta_kyky1)
            else:
                self.__kayta_kyky1()

    def laske_kyky2_parannus(self, kohderuutu, ruutu):
        etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, kohderuutu)
        parannus = self.ominaisuudet.hyokkays * self.kyky1_parannuskerroin / sqrt(etaisyys + 1)
        return parannus

    def __kayta_kyky1(self):
        for ruutu in self.kyky1_kohteet:
            ruutu.grafiikka.palauta_vari()
            if ruutu.yksikko is not None and ruutu.yksikko.omistaja == self.omistaja:
                # etäisyys keskimmäisestä ruudusta
                parannus = self.laske_kyky2_parannus(self.kyky1_kohteet[0], ruutu)
                self.paranna_yksikko(ruutu.yksikko, parannus)
        self.peru_kyky1()
        self.kayta_energiaa(self.kyky1_hinta)
        self.hyokatty()
        teksti = self.__class__.__name__ + self.omistaja_teksti + " käytti alueparannuksen"
        self.kayttoliittyma.lisaa_pelilokiin(teksti)

    def paranna_yksikko(self, yksikko, maara):
        satunnaisuuskerroin = 0.15
        parannus_min = int(maara * (1 - satunnaisuuskerroin))
        parannus_max = int(maara * (1 + satunnaisuuskerroin))
        parannus = randrange(parannus_min, parannus_max + 1, 1)
        yksikko.parannu(parannus)

    def kyky2(self):
        self.kyky2_valitsee_kohteita = True
        self.laske_kantaman_sisalla_olevat_ruudut()
        self.nayta_kantaman_sisalla_olevat_ruudut()
        self.laske_hyokkayksen_kohteet(True)
        self.nayta_hyokkayksen_kohteet()

    def kayta_kyky2(self, kohde):
        kohde.hyokkays(self)
        if kohde is not None:
            # jos luo tilavaikutuksen, jolla ei ole "omistajaa", omistaja on None
            loppuvaikutus = Tilavaikutus(None , self.__kyky2_taintumisaika, 0, 0, 0, 0, True)
            kohde.lisaa_tilavaikutus(self.kyky2_kesto, -self.kyky2_hyokkaysvahennys, -self.kyky2_puolustusvahennys,
                                     0, 0, False, loppuvaikutus)
        self.peru_kyky2()
        self.kayta_energiaa(self.kyky2_hinta)
        self.hyokatty()
        teksti = self.__class__.__name__ + self.omistaja_teksti + " käytti kirouksen"
        self.kayttoliittyma.lisaa_pelilokiin(teksti)

    def kyky1_voi_kayttaa(self):
        if self.ominaisuudet.nyk_energia >= self.__kyky1_hinta:
            return True
        return False

    def kyky2_voi_kayttaa(self):
        if self.ominaisuudet.nyk_energia >= self.__kyky2_hinta:
            if len(self.hyokkayksen_kohteet) > 0:
                return True
        return False

    def kyky1_nappi_tiedot(self):
        return "Alueparannus\n" + "Hinta: " + str(self.kyky1_hinta)

    def kyky2_nappi_tiedot(self):
        return "Kirous\n" + "Hinta: " + str(self.kyky2_hinta)

    # inspiraatio: voi olla monta kerrallaan
    # ei voi inspiroida itseään
    # pystyy hyökkäämään, mutta on melko heikko

    def __str__(self):
        return "PASSIIVINEN KYKY:\n{}\n\nKYKY 1 (ALUEPARANNUS):\n{}\n\nKYKY 2 (KIROUS):\n{}"\
            .format(self.passiivinen_kyky(), self.kyky1_tooltip_teksti(), self.kyky2_tooltip_teksti())

    def passiivinen_kyky(self):
        return "Inspiroi " + str(self.__inspiraatio_kantama) + " ruudun kantamalla olevia omia yksiköitä\n" \
                                                               "(parantaa hyökkäystä ja puolustusta " + \
               str(int(100*(self.__inspiraatio_kerroin - 1))) + "%)"


    def kyky1_tooltip_teksti(self):
        return "Parantaa alueella olevia " \
               "yksiköitä. Alueen keskellä\nolevat yksiköt paranevat enemmän. Alueeseen\nkuuluvat " + str(self.__kyky1_kantama) + \
               " ruudun säteellä olevat ruudut\nvalitusta ruudusta"

    def kyky2_tooltip_teksti(self):
        return "Hyökkää vihollisen kimppuun ja kiroaa sen.\n" \
               "Kohteen hyökkäys vähenee " + str(self.__kyky2_hyokkaysvahennys) + " ja puolustus\nvähenee " \
               + str(self.__kyky2_puolustusvahennys) + " verran " + str(self.__kyky2_kesto) + \
               " vuoron ajaksi. Vihollinen taintuu\n" \
               + str(self.__kyky2_taintumisaika) + " vuoron ajaksi, kun kirous loppuu."
