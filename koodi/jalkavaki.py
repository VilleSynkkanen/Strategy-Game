from yksikko import Yksikko
from tilavaikutus import Tilavaikutus


class Jalkavaki(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        # pelkkä numero (ei prosentti/kerroin)
        # ottaa ensin vahinkoa, sitten paranee
        self.__parannus_hyokkayksessa = int(kyvyt["parannus_hyokkayksessa"])

        self.__kyky1_hinta = int(kyvyt["kyky1_hinta"])
        self.__kyky1_kesto = int(kyvyt["kyky1_kesto"])
        self.__kyky1_puolustus = int(kyvyt["kyky1_puolustus"])
        self.__kyky1_liikkuminen = int(kyvyt["kyky1_liikkuminen"])

        self.__kyky2_hinta = int(kyvyt["kyky2_hinta"])
        self.__kyky2_kantama = int(kyvyt["kyky2_kantama"])
        self.__kyky2_bonushyokkays = int(kyvyt["kyky2_bonushyokkays"])
        self.__kyky2_taintuminen_kesto = int(kyvyt["kyky2_taintuminen_kesto"])

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

    # kyky1 lisää tilavaikutuksen yksikölle
    def kyky1(self):
        super(Jalkavaki, self).kyky1()
        self.lisaa_tilavaikutus(self.kyky1_kesto, 0, self.kyky1_puolustus, self.kyky1_liikkuminen, 0, False)
        self.kayta_energiaa(self.kyky1_hinta)
        self.hyokatty()
        teksti = self.__class__.__name__ + self.omistaja_teksti + " käytti kilpiseinän"
        self.kayttoliittyma.lisaa_pelilokiin(teksti)

    # kyky2 antaa uuden vuoron, vähentää liikkumista ja nostaa hyökkäystä väliaikaisesti
    # lisäämällä yhden vuoron tilavaikutuksen ja lisää hyökkäykseen tilavaikutuksen
    def kyky2(self):
        liikkuminen = self.kyky2_kantama - self.ominaisuudet.liikkuminen
        self.lisaa_tilavaikutus(1, self.kyky2_bonushyokkays, 0, liikkuminen, 0, False)
        self.kayta_energiaa(self.kyky2_hinta)
        self.palauta_liikkumispisteet()
        if self.omistaja == "PLR":
            self.kayttoliittyma.valitse_yksikko(self)   # helpoin tapa "resetoida" vuoro
        self.hyokkays_vaikutus = Tilavaikutus(None, self.__kyky2_taintuminen_kesto, 0, 0, 0, 0, True)
        teksti = self.__class__.__name__ + self.omistaja_teksti + " käytti rynnäkön"
        self.kayttoliittyma.lisaa_pelilokiin(teksti)

    # hyökkäysvaikutus poistetaan vaikutusten käsittelyn yhteydessä
    def kasittele_tilavaikutukset(self):
        super(Jalkavaki, self).kasittele_tilavaikutukset()
        if self.hyokkays_vaikutus is not None:
            self.hyokkays_vaikutus = None

    def kyky1_voi_kayttaa(self):
        if self.ominaisuudet.nyk_energia >= self.__kyky1_hinta:
            return True
        return False

    def kyky2_voi_kayttaa(self):
        if self.ominaisuudet.nyk_energia >= self.__kyky2_hinta:
            return True
        return False

    def kyky1_nappi_tiedot(self):
        return "Kilpiseinä\n" + "Hinta: " + str(self.kyky1_hinta)

    def kyky2_nappi_tiedot(self):
        return "Rynnäkkö\n" + "Hinta: " + str(self.kyky2_hinta)

    def __str__(self):
        return "PASSIIVINEN KYKY:\n{}\n\nKYKY 1 (KILPISEINÄ):\n{}\n\nKYKY 2 (RYNNÄKKÖ):\n{}"\
            .format(self.passiivinen_kyky(), self.kyky1_tooltip_teksti(), self.kyky2_tooltip_teksti())

    def passiivinen_kyky(self):
        return "Vahingon aiheuttaminen hyökkäyksessä parantaa " + str(self.__parannus_hyokkayksessa)

    def kyky1_tooltip_teksti(self):
        return "Lisää puolustusta " + str(self.__kyky1_puolustus)  \
               + " ja vähentää liikumista " + str(-self.__kyky1_liikkuminen) + "\n" + str(self.__kyky1_kesto) \
               + " vuoron ajaksi"

    def kyky2_tooltip_teksti(self):
        return "Saa tällä vuorolla käyttämänsä liikkumisen takaisin.\n" \
               "Voi liikkua " + str(self.__kyky2_kantama) + " ruutua" \
               " ja hyökätä.\nSaa " + str(self.__kyky2_bonushyokkays) + \
               " hyökkäystä tämän vuoron ajaksi.\nHyökkäys tainnuttaa vihollisen " + str(self.__kyky2_taintuminen_kesto)\
                + " vuoron ajaksi."
