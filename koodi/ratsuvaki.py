from yksikko import  Yksikko

class Ratsuvaki(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()

        # kyky 1 tiedot
        self._kyky1_hinta = 6
        self._kyky1_kesto = 3
        self._kyky1_puolustusvahennys = 2
        self._kyky1_hyokkaysbonus = 4

        # kyky 2 tiedot
        self._kyky2_hinta = 5
        self._kyky2_kantama = 3
        self._kyky2_puolustusvahennys = 2
        self._kyky2_kesto = 2

        # kykyä 2 varten
        self._alkuperainen_kant = self._ominaisuudet.kantama

    # propertyt

    @property
    def kyky1_hinta(self):
        return self._kyky1_hinta

    @property
    def kyky1_kesto(self):
        return self._kyky1_kesto

    @property
    def kyky1_puolustusvahennys(self):
        return self._kyky1_puolustusvahennys

    @property
    def kyky1_hyokkaysbonus(self):
        return self._kyky1_hyokkaysbonus

    @property
    def kyky2_hinta(self):
        return self._kyky2_hinta

    @property
    def kyky2_kantama(self):
        return self._kyky2_kantama

    @property
    def kyky2_puolustusvahennys(self):
        return self._kyky2_puolustusvahennys

    @property
    def kyky2_kesto(self):
        return self._kyky2_kesto

    # passiivinen tehty
    # kyky 1 tehty
    # kyky 2 tehty

    def kyky1(self):
        super(Ratsuvaki, self).kyky1()
        self.lisaa_tilavaikutus(self._kyky1_kesto, self._kyky1_hyokkaysbonus, -self._kyky1_puolustusvahennys,
                                0, 0, False)
        self.kayta_energiaa(self.kyky1_hinta)
        self.hyokatty()

    def kyky2(self):
        self._alkuperainen_kant = self._ominaisuudet.kantama
        self._ominaisuudet.kantama = self._kyky2_kantama
        self._kyky2_valitsee_kohteita = True
        self.peru_mahdollisten_ruutujen_nayttaminen()
        self.laske_kantaman_sisalla_olevat_ruudut()
        self.nayta_kantaman_sisalla_olevat_ruudut()
        self.laske_hyokkayksen_kohteet(True)
        self.nayta_hyokkayksen_kohteet()

    def kayta_kyky2(self, kohde):
        kohde.lisaa_tilavaikutus(self.kyky2_kesto, 0, -self.kyky2_puolustusvahennys, 0, 0, False)
        self.peru_kyky2()
        self.kayta_energiaa(self.kyky2_hinta)
        self.hyokatty()

    def peru_kyky2(self):
        super(Ratsuvaki, self).peru_kyky2()
        self._ominaisuudet.kantama = self._alkuperainen_kant

    def kyky1_nappi_tiedot(self):
        return "Kolmiokiila\n" + "Hinta: " + str(self.kyky1_hinta)

    def kyky2_nappi_tiedot(self):
        return "Tiedustelu\n" + "Hinta: " + str(self.kyky2_hinta)

    def __str__(self):
        return "-Passiivinen kyky: voi liikkua myös\n" \
               " kyvyn käyttämisen/hyökkäyksen jälkeen\n" \
               "-Kyky 1(kolmiokiila): Menee kiilaan 3 vuoron\n" \
               " ajaksi. Kiilassa ollessaan puolustus vähenee\n" \
               " hiukan, mutta vahinko kasvaa merkittävästi\n"\
               "-Kyky 2(tiedustelu): Merkitsee kohteen.\n" \
               " Kohteen puolustus kärsii 2 vuoron ajan."
