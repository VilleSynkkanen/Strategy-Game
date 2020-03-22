from yksikko import  Yksikko

class Ratsuvaki(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()

        # kyky 1 tiedot
        self.kyky1_hinta = 6
        self.kyky1_kesto = 3
        self.kyky1_puolustusvahennys = 2
        self.kyky1_hyokkaysbonus = 4

        # kyky 2 tiedot
        self.kyky2_hinta = 5
        self.kyky2_kantama = 3
        self.kyky2_puolustusvahennys = 2
        self.kyky2_kesto = 2

        # kykyä 2 varten
        self.alkuperainen_kant = self.ominaisuudet.kantama

    # passiivinen tehty
    # kyky 1 tehty
    # kyky 2 tehty

    def kyky1(self):
        self.lisaa_tilavaikutus(self.kyky1_kesto, self.kyky1_hyokkaysbonus, -self.kyky1_puolustusvahennys, 0, 0, False)
        self.kayta_energiaa(self.kyky1_hinta)
        self.hyokatty()

    def kyky2(self):
        self.alkuperainen_kant = self.ominaisuudet.kantama
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
        self.ominaisuudet.kantama = self.alkuperainen_kant

    def __str__(self):
        return "-Passiivinen kyky: voi liikkua myös\n" \
               " kyvyn käyttämisen/hyökkäyksen jälkeen\n" \
               "-Kyky 1(kolmiokiila): Menee kiilaan 3 vuoron\n" \
               " ajaksi. Kiilassa ollessaan puolustus vähenee\n" \
               " hiukan, mutta vahinko kasvaa merkittävästi\n"\
               "-Kyky 2(tiedustelu): Merkitsee kohteen.\n" \
               " Kohteen puolustus kärsii 2 vuoron ajan."
