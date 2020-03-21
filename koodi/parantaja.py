from yksikko import Yksikko
from math import sqrt
from random import randrange

class Parantaja(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        self.inspiraatio_kantama = 3
        self.inspiraatio_kerroin = 1.15

        self.kyky1_kohteiden_maara = 1
        self.kyky1_kantama = 2
        self.kyky1_parannuskerroin = 3
        self.kyky1_keskimmainen_ruutu = None

    # passiivinen tehty
    # kyky 1 tehty

    # parannuksen määrä = hyökkäys * parannuskerroin / sqrt(etäisyys + 1) (+-15% satunnaisuus)
    # kykyihin pätee näkyvyyssäännöt

    def kyky1_lisaa_kohde(self, ruutu):
        # lisätään kantaman päässä olevat ruudut, sitten käytetään kyky
        if ruutu in self.ruudut_kantamalla:
            self.kyky1_kohteet.append(ruutu)
            for Ruutu in self.kayttoliittyma.pelinohjain.kartta.ruudut:
                if self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, Ruutu) <= self.kyky1_kantama and \
                        Ruutu not in self.kyky1_kohteet:
                    self.kyky1_kohteet.append(Ruutu)
            self.kayta_kyky1()

    def kayta_kyky1(self):
        for ruutu in self.kyky1_kohteet:
            if ruutu.yksikko is not None and ruutu.yksikko.omistaja == self.omistaja:
                # etäisyys keskimmäisestä ruudusta
                etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.kyky1_kohteet[0], ruutu)
                parannus = self.ominaisuudet.hyokkays * self.kyky1_parannuskerroin / sqrt(etaisyys + 1)
                self.paranna_yksikko(ruutu.yksikko, parannus)
        self.peru_kyky1()
        self.hyokatty()

    def paranna_yksikko(self, yksikko, maara):
        satunnaisuuskerroin = 0.15
        parannus_min = int(maara * (1 - satunnaisuuskerroin))
        parannus_max = int(maara * (1 + satunnaisuuskerroin))
        parannus = randrange(parannus_min, parannus_max + 1, 1)
        yksikko.parannu(parannus)

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
