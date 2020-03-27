from yksikko import  Yksikko

class Ratsuvaki(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()

        # kyky 1 tiedot
        self.__kyky1_hinta = int(kyvyt["kyky1_hinta"])
        self.__kyky1_kesto = int(kyvyt["kyky1_kesto"])
        self.__kyky1_puolustusvahennys = int(kyvyt["kyky1_puolustusvahennys"])
        self.__kyky1_hyokkaysbonus = int(kyvyt["kyky1_hyokkaysbonus"])

        # kyky 2 tiedot
        self.__kyky2_hinta = int(kyvyt["kyky2_hinta"])
        self.__kyky2_kantama = int(kyvyt["kyky2_kantama"])
        self.__kyky2_puolustusvahennys = int(kyvyt["kyky2_puolustusvahennys"])
        self.__kyky2_kesto = int(kyvyt["kyky2_kesto"])

        # kykyä 2 varten
        self.__alkuperainen_kant = self.ominaisuudet.kantama

    # propertyt

    @property
    def kyky1_hinta(self):
        return self.__kyky1_hinta

    @property
    def kyky1_kesto(self):
        return self.__kyky1_kesto

    @property
    def kyky1_puolustusvahennys(self):
        return self.__kyky1_puolustusvahennys

    @property
    def kyky1_hyokkaysbonus(self):
        return self.__kyky1_hyokkaysbonus

    @property
    def kyky2_hinta(self):
        return self.__kyky2_hinta

    @property
    def kyky2_kantama(self):
        return self.__kyky2_kantama

    @property
    def kyky2_puolustusvahennys(self):
        return self.__kyky2_puolustusvahennys

    @property
    def kyky2_kesto(self):
        return self.__kyky2_kesto

    # passiivinen tehty
    # kyky 1 tehty
    # kyky 2 tehty

    def kyky1(self):
        super(Ratsuvaki, self).kyky1()
        self.lisaa_tilavaikutus(self.kyky1_kesto, self.kyky1_hyokkaysbonus, -self.kyky1_puolustusvahennys,
                                0, 0, False)
        self.kayta_energiaa(self.kyky1_hinta)
        self.hyokatty()

    def kyky2(self):
        self.__alkuperainen_kant = self.ominaisuudet.kantama
        self.ominaisuudet.kantama = self.kyky2_kantama
        self.kyky2_valitsee_kohteita = True
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
        self.ominaisuudet.kantama = self.__alkuperainen_kant

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

    def __str__(self):
        return "PASSIIVINEN KYKY:\n{}\nKYKY 1 (KOLMIOKIILA):\n{}\nKYKY 2 (TIEDUSTELU):\n{}"\
            .format(self.passiivinen_kyky(), self.kyky1_tooltip_teksti(), self.kyky2_tooltip_teksti())

    def passiivinen_kyky(self):
        return "Voi liikkua myös kyvyn käyttämisen/hyökkäyksen jälkeen\n"

    def kyky1_tooltip_teksti(self):
        return ""

    def kyky2_tooltip_teksti(self):
        return ""
