from yksikko import  Yksikko

class Jalkavaki(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        # pelkkä numero (ei prosentti/kerroin)
        # ottaa ensin vahinkoa, sitten paranee
        self.parannus_hyokkayksessa = 2

        self.kyky1_hinta = 6
        self.kyky1_kesto = 3
        self.kyky1_puolustus = 3
        self.kyky1_liikkuminen = -1

        self.kyky2_hinta = 7
        self.kyky2_kantama = 2
        self.kyky2_bonushyokkays = 2
        self.kyky2_taintuminen_kesto = 1

    # passiivinen tehty
    # kyky 1 tehty
    # kyky 2 tehty

    def kyky1(self):
        self.lisaa_tilavaikutus(self.kyky1_kesto, 0, self.kyky1_puolustus, self.kyky1_liikkuminen, 0, False)
        self.kayta_energiaa(self.kyky1_hinta)
        self.hyokatty()

    # voi käyttää myös pelkkään liikkumiseen
    # ensin valitaan ruutu, siten hyökkäyksen kohde
    # käytännössä antaa uuden vuoron, vähentää liikkumista ja nostaa hyökkäystä väliaikaisesti
    # lisäämällä yhden vuoron tilavaikutuksen
    def kyky2(self):
        liikkuminen = self.kyky2_kantama - self.ominaisuudet.liikkuminen
        self.lisaa_tilavaikutus(1, self.kyky2_bonushyokkays, 0, liikkuminen, 0, False)
        self.kayta_energiaa(self.kyky2_hinta)
        self.palauta_liikkumispisteet()
        self.kayttoliittyma.valitse_yksikko(self)   # helpoin tapa "resetoida" vuoro

    def __str__(self):
        return "-Passiivinen kyky: vahingon aiheuttaminen\n " \
               " hyökkäyksessä parantaa hieman\n" \
               "-Kyky 1 (kilpiseinä): Parantaa puolustusta\n" \
               " X vuoron ajaksi, vähentää liikkumispisteitä\n" \
               "-Kyky 2 (rynnäkkö): Valitsee kohteen enintään\n" \
               " Y ruudun päässä. Liikkuu kohteen viereen\n" \
               " ja hyökkää sen kimppuun. Tekee bonusvahinkoa\n" \
               " ja tainnuttaa yksikön 1 vuoron ajaksi"