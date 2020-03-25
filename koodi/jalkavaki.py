from yksikko import  Yksikko

class Jalkavaki(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        # pelkkä numero (ei prosentti/kerroin)
        # ottaa ensin vahinkoa, sitten paranee
        self._parannus_hyokkayksessa = 2

        self._kyky1_hinta = 6
        self._kyky1_kesto = 3
        self._kyky1_puolustus = 3
        self._kyky1_liikkuminen = -1

        self._kyky2_hinta = 7
        self._kyky2_kantama = 2
        self._kyky2_bonushyokkays = 2
        self._kyky2_taintuminen_kesto = 1

    # propertyt

    @property
    def parannus_hyokkayksessa(self):
        return self._parannus_hyokkayksessa

    @property
    def kyky1_hinta(self):
        return self._kyky1_hinta

    @property
    def kyky1_kesto(self):
        return self._kyky1_kesto

    @property
    def kyky1_puolustus(self):
        return self._kyky1_puolustus

    @property
    def kyky1_liikkuminen(self):
        return self._kyky1_liikkuminen

    @property
    def kyky2_hinta(self):
        return self._kyky2_hinta

    @property
    def kyky2_kantama(self):
        return self._kyky2_kantama

    @property
    def kyky2_bonushyokkays(self):
        return self._kyky2_bonushyokkays

    @property
    def kyky2_taintuminen_kesto(self):
        return self._kyky2_taintuminen_kesto

    # passiivinen tehty
    # kyky 1 tehty
    # kyky 2 tehty

    def kyky1(self):
        super(Jalkavaki, self).kyky1()
        self.lisaa_tilavaikutus(self._kyky1_kesto, 0, self._kyky1_puolustus, self._kyky1_liikkuminen, 0, False)
        self.kayta_energiaa(self._kyky1_hinta)
        self.hyokatty()

    # voi käyttää myös pelkkään liikkumiseen
    # ensin valitaan ruutu, siten hyökkäyksen kohde
    # käytännössä antaa uuden vuoron, vähentää liikkumista ja nostaa hyökkäystä väliaikaisesti
    # lisäämällä yhden vuoron tilavaikutuksen
    def kyky2(self):
        liikkuminen = self._kyky2_kantama - self._ominaisuudet.liikkuminen
        self.lisaa_tilavaikutus(1, self._kyky2_bonushyokkays, 0, liikkuminen, 0, False)
        self.kayta_energiaa(self._kyky2_hinta)
        self.palauta_liikkumispisteet()
        self._kayttoliittyma.valitse_yksikko(self)   # helpoin tapa "resetoida" vuoro

    def kyky1_nappi_tiedot(self):
        return "Kilpiseinä\n" + "Hinta: " + str(self._kyky1_hinta)

    def kyky2_nappi_tiedot(self):
        return "Rynnäkkö\n" + "Hinta: " + str(self._kyky2_hinta)

    def __str__(self):
        return "-Passiivinen kyky: vahingon aiheuttaminen\n " \
               " hyökkäyksessä parantaa hieman\n" \
               "-Kyky 1 (kilpiseinä): Parantaa puolustusta\n" \
               " X vuoron ajaksi, vähentää liikkumispisteitä\n" \
               "-Kyky 2 (rynnäkkö): Valitsee kohteen enintään\n" \
               " Y ruudun päässä. Liikkuu kohteen viereen\n" \
               " ja hyökkää sen kimppuun. Tekee bonusvahinkoa\n" \
               " ja tainnuttaa yksikön 1 vuoron ajaksi"