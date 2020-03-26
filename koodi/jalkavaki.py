from yksikko import  Yksikko

class Jalkavaki(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        # pelkkä numero (ei prosentti/kerroin)
        # ottaa ensin vahinkoa, sitten paranee
        self.__parannus_hyokkayksessa = 2

        self.__kyky1_hinta = kyvyt["kyky1_hinta"]
        self.__kyky1_kesto = kyvyt["kyky1_kesto"]
        self.__kyky1_puolustus = kyvyt["kyky1_puolustus"]
        self.__kyky1_liikkuminen = kyvyt["kyky1_liikkuminen"]

        self.__kyky2_hinta = kyvyt["kyky2_hinta"]
        self.__kyky2_kantama = kyvyt["kyky2_kantama"]
        self.__kyky2_bonushyokkays = kyvyt["kyky2_bonushyokkays"]
        self.__kyky2_taintuminen_kesto = kyvyt["kyky2_taintuminen_kesto"]


    # propertyt

    @property
    def parannus_hyokkayksessa(self):
        return self.__parannus_hyokkayksessa

    @property
    def kyky1_hinta(self):
        return self.__kyky1_hinta

    @property
    def kyky1_kesto(self):
        return self.__kyky1_kesto

    @property
    def kyky1_puolustus(self):
        return self.__kyky1_puolustus

    @property
    def kyky1_liikkuminen(self):
        return self.__kyky1_liikkuminen

    @property
    def kyky2_hinta(self):
        return self.__kyky2_hinta

    @property
    def kyky2_kantama(self):
        return self.__kyky2_kantama

    @property
    def kyky2_bonushyokkays(self):
        return self.__kyky2_bonushyokkays

    @property
    def kyky2_taintuminen_kesto(self):
        return self.__kyky2_taintuminen_kesto

    # passiivinen tehty
    # kyky 1 tehty
    # kyky 2 tehty

    def kyky1(self):
        super(Jalkavaki, self).kyky1()
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

    def kyky1_nappi_tiedot(self):
        return "Kilpiseinä\n" + "Hinta: " + str(self.kyky1_hinta)

    def kyky2_nappi_tiedot(self):
        return "Rynnäkkö\n" + "Hinta: " + str(self.kyky2_hinta)

    def __str__(self):
        return "-Passiivinen kyky: vahingon aiheuttaminen\n " \
               " hyökkäyksessä parantaa hieman\n" \
               "-Kyky 1 (kilpiseinä): Parantaa puolustusta\n" \
               " X vuoron ajaksi, vähentää liikkumispisteitä\n" \
               "-Kyky 2 (rynnäkkö): Valitsee kohteen enintään\n" \
               " Y ruudun päässä. Liikkuu kohteen viereen\n" \
               " ja hyökkää sen kimppuun. Tekee bonusvahinkoa\n" \
               " ja tainnuttaa yksikön 1 vuoron ajaksi"
