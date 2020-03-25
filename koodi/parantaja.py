from yksikko import Yksikko
from math import sqrt
from random import randrange

class Parantaja(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        self._inspiraatio_kantama = 3
        self._inspiraatio_kerroin = 1.15

        # kyky 1 tiedot
        self._kyky1_hinta = 6
        self._kyky1_kohteiden_maara = 1
        self._kyky1_kantama = 2
        self._kyky1_parannuskerroin = 3

        # kyky 2 tiedot
        self._kyky2_hinta = 6
        self._kyky2_kesto = 3
        self._kyky2_hyokkaysvahennys = 3
        self._kyky2_puolustusvahennys = 3

    # propertyt

    @property
    def inspiraatio_kantama(self):
        return self._inspiraatio_kantama

    @property
    def inspiraatio_kerroin(self):
        return self._inspiraatio_kerroin

    @property
    def kyky1_hinta(self):
        return self._kyky1_hinta

    @property
    def kyky1_kohteiden_maara(self):
        return self._kyky1_kohteiden_maara

    @property
    def kyky1_kantama(self):
        return self._kyky1_kantama

    @property
    def kyky1_parannuskerroin(self):
        return self._kyky1_parannuskerroin

    @property
    def kyky2_hinta(self):
        return self._kyky2_hinta

    @property
    def kyky2_kesto(self):
        return self._kyky2_kesto

    @property
    def kyky2_hyokkaysvahennys(self):
        return self._kyky2_hyokkaysvahennys

    @property
    def kyky2_puolustusvahennys(self):
        return self._kyky2_puolustusvahennys

    # passiivinen tehty
    # kyky 1 tehty
    # kyky 2 tehty

    # parannuksen määrä = hyökkäys * parannuskerroin / sqrt(etäisyys + 1) (+-15% satunnaisuus)
    # kykyihin pätee näkyvyyssäännöt

    def kyky1_lisaa_kohde(self, ruutu):
        # lisätään kantaman päässä olevat ruudut, sitten käytetään kyky
        if ruutu in self._ruudut_kantamalla:
            self._kyky1_kohteet.append(ruutu)
            for Ruutu in self._kayttoliittyma.pelinohjain.kartta.ruudut:
                if self._kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, Ruutu) <= self._kyky1_kantama and \
                        Ruutu not in self._kyky1_kohteet:
                    self._kyky1_kohteet.append(Ruutu)
            self.kayta_kyky1()

    def kayta_kyky1(self):
        for ruutu in self._kyky1_kohteet:
            if ruutu.yksikko is not None and ruutu.yksikko.omistaja == self._omistaja:
                # etäisyys keskimmäisestä ruudusta
                etaisyys = self._kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self._kyky1_kohteet[0], ruutu)
                parannus = self._ominaisuudet.hyokkays * self._kyky1_parannuskerroin / sqrt(etaisyys + 1)
                self.paranna_yksikko(ruutu.yksikko, parannus)
        self.peru_kyky1()
        self.kayta_energiaa(self._kyky1_hinta)
        self.hyokatty()

    def paranna_yksikko(self, yksikko, maara):
        satunnaisuuskerroin = 0.15
        parannus_min = int(maara * (1 - satunnaisuuskerroin))
        parannus_max = int(maara * (1 + satunnaisuuskerroin))
        parannus = randrange(parannus_min, parannus_max + 1, 1)
        yksikko.parannu(parannus)

    def kyky2(self):
        self._kyky2_valitsee_kohteita = True
        self.laske_kantaman_sisalla_olevat_ruudut()
        self.nayta_kantaman_sisalla_olevat_ruudut()
        self.laske_hyokkayksen_kohteet(True)
        self.nayta_hyokkayksen_kohteet()

    def kayta_kyky2(self, kohde):
        kohde.hyokkays(self)
        kohde.lisaa_tilavaikutus(self._kyky2_kesto, -self._kyky2_hyokkaysvahennys, -self._kyky2_puolustusvahennys, 0, 0, False)
        self.peru_kyky2()
        self.kayta_energiaa(self._kyky2_hinta)
        self.hyokatty()

    def kyky1_nappi_tiedot(self):
        return "Alueparannus\n" + "Hinta: " + str(self._kyky1_hinta)

    def kyky2_nappi_tiedot(self):
        return "Kirous\n" + "Hinta: " + str(self._kyky2_hinta)

    # inspiraatio: voi olla monta kerrallaan
    # ei voi inspiroida itseään
    # pystyy hyökkäämään, mutta on hyvin heikko
    def __str__(self):
        return "-Passiivinen kyky: inspiroi läheisiä\n" \
               " yksiköitä (parantaa hyökkäystä ja puolustusta)\n" \
               "-Kyky 1(alueparannus): parantaa alueella olevia\n" \
               " yksiköitä tietyn määrän X (alue = 2 ruudun etäisyys)\n" \
               "-Kyky 2(kirous): kiroaa yhden vihollisyksikön.\n" \
               " Vihollisen puolustus ja hyökkäys ovat\n" \
               " heikompia X vuoron ajan. Vihollinen taintuu\n" \
               " yhden vuoron ajaksi, kun kirous loppuu."