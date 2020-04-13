from jousimiehet import Jousimiehet
from tekoaly import Tekoaly


class Jousimiehet_tekoaly(Jousimiehet):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        self.__class__.__name__ = "Jousimiehet"
        super(Jousimiehet_tekoaly, self).__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt)

        # priorisaatio ruudun/hyökkäyksen kohteen päättämisessä
        self.__tykisto_prio = 1.2
        self.__parantaja_prio = 1.2
        self.__jousimies_prio = 1.1
        self.__ratsuvaki_prio = 1
        self.__jalkavaki_prio = 1
        self.__max_elamakerroin = 1.25

        # seuraavat vaikuttavat pelkästään liikkumiseen
        self.__min_puolustuskerroin = 0.8
        self.__max_puolustuskerroin = 1.2
        self.__min_maastokerroin = 0.8
        self.__max_maastokerroin = 1.2
        self.__flanking_kerroin = 1

        # maaston pisteytys
        self.__oma_maastokerroin_hyokkays = 0.2
        self.__oma_maastokerroin_puolustus = 0.2

        # etäisyys kohteesta pisteytys
        self.__kulmakerroin = -0.04
        self.__max_lahestymisbonus = 2
        self.__max_etaisyys_kohteesta = (self.__max_lahestymisbonus - 1) / (-self.__kulmakerroin)

        # etäisyys omasta pisteytys
        self.__oma_lahestymisbonus = 1.025
        self.__oma_max_kantama = 4
        self.__laheisyys_bonus_yksikot = 2

        # etäisyys vihollisista
        self.__etaisyys_vihollisista_eksp = 2

        # kyvyt
        self.__kyky1_prio = 0.9

        self.__kyky2_prio = 1000
        self.__kyky2_etaisyys_max = 4
        self.__kyky2_ratsuvaki_painotus = 2

    @property
    def tykisto_prio(self):
        return self.__tykisto_prio

    @property
    def parantaja_prio(self):
        return self.__parantaja_prio

    @property
    def jousimies_prio(self):
        return self.__jousimies_prio

    @property
    def ratsuvaki_prio(self):
        return self.__ratsuvaki_prio

    @property
    def jalkavaki_prio(self):
        return self.__jalkavaki_prio

    @property
    def max_elamakerroin(self):
        return self.__max_elamakerroin

    @property
    def min_puolustuskerroin(self):
        return self.__min_puolustuskerroin

    @property
    def max_puolustuskerroin(self):
        return self.__max_puolustuskerroin

    @property
    def min_maastokerroin(self):
        return self.__min_maastokerroin

    @property
    def max_maastokerroin(self):
        return self.__max_maastokerroin

    @property
    def flanking_kerroin(self):
        return self.__flanking_kerroin

    @property
    def oma_maastokerroin_hyokkays(self):
        return self.__oma_maastokerroin_hyokkays

    @property
    def oma_maastokerroin_puolustus(self):
        return self.__oma_maastokerroin_puolustus

    @property
    def kulmakerroin(self):
        return self.__kulmakerroin

    @property
    def max_etaisyys_kohteesta(self):
        return self.__max_etaisyys_kohteesta

    @property
    def max_lahestymisbonus(self):
        return self.__max_lahestymisbonus

    @property
    def oma_lahestymisbonus(self):
        return self.__oma_lahestymisbonus

    @property
    def oma_max_kantama(self):
        return self.__oma_max_kantama

    @property
    def laheisyys_bonus_yksikot(self):
        return self.__laheisyys_bonus_yksikot

    @property
    def etaisyys_vihollisista_eksp(self):
        return self.__etaisyys_vihollisista_eksp

    def liike(self, kohderuutu):
        Tekoaly.liike(self, kohderuutu)

    def hyokkays_toiminto(self):
        # katsotaan ensin, mahdolliset hyökkäyksen kohteet ja tallennetaan ne sanakirjaan
        paras_kohde = Tekoaly.hyokkays_toiminto(self)

        if paras_kohde is None:
            pass
        elif paras_kohde == "KYKY1":
            self.kyky1_hyokkays()
            self.kyky1_kohteet = []
        elif paras_kohde == "KYKY2":
            self.kyky2()
        else:
            paras_kohde.hyokkayksen_kohde(self)

    def pisteyta_kyky1(self):
        self.kyky1_kohteet = []
        # katsotaan ruudut, joissa on vihollisia
        # arvioidaan jokainen ruutu ja sen naapurit

        vaihtoehdot = {}
        for ruutu in self.ruudut_kantamalla:
            kohteet, pisteet = self.__pisteyta_ruutu_kyky1(ruutu)
            # tallennetaan tiedot tupleen ja lisätään se sanakirjaan
            tiedot = (pisteet, kohteet)
            vaihtoehdot[ruutu] = tiedot

        korkeimmat_pisteet = 0
        paras_kohde = None
        for vaihtoehto in vaihtoehdot:
            if vaihtoehdot[vaihtoehto][0] > korkeimmat_pisteet:
                korkeimmat_pisteet = vaihtoehdot[vaihtoehto][0]
                paras_kohde = vaihtoehdot[vaihtoehto][1]

        self.kyky1_kohteet = paras_kohde
        return korkeimmat_pisteet * self.__kyky1_prio

    # returnaa ruudun pisteet ja kohteiden määrn mukaisesti parhaat kohteet
    def __pisteyta_ruutu_kyky1(self, ruutu):
        pisteet = 0
        if ruutu.yksikko is not None and ruutu.yksikko.omistaja == "PLR":
            pisteet += Tekoaly.pisteyta_pelkka_kohde(self, ruutu.yksikko)
        naapurit = {}
        #self.laske_kantaman_sisalla_olevat_ruudut()
        for naapuri in ruutu.naapurit:
            if naapuri.yksikko is not None and naapuri.yksikko.omistaja == "PLR" and naapuri in self.ruudut_kantamalla:
                naapurit[naapuri] = Tekoaly.pisteyta_pelkka_kohde(self, naapuri.yksikko)
            else:
                naapurit[naapuri] = 0
        # lajitellaan naapurit
        lajiteltu = sorted(naapurit.items(), key=lambda x: x[1], reverse=True)
        #print(lajiteltu)
        kohteet = [ruutu]

        # lisätään parhaat naapurit kohteisiin ja lisätään niiden pisteet
        for kohde in lajiteltu:
            if len(kohteet) < self.kyky1_kohteiden_maara:
                kohteet.append(kohde[0])
                pisteet += kohde[1]

        return kohteet, pisteet

    def pisteyta_kyky2(self):
        # perustuu lähellä olevien vihollisten määrään, ratsuväkipainotus
        # jos on jo kiilat, ei laiteta uusia
        if self.ruutu.kiilat is not None:
            return 0
        viholliset = 0
        for vihollinen in self.kayttoliittyma.pelinohjain.kartta.pelaajan_yksikot:
            if self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(vihollinen.ruutu, self.ruutu) <= self.__kyky2_etaisyys_max:
                if vihollinen.__class__.__name__ == "Ratsuvaki":
                    viholliset += self.__kyky2_ratsuvaki_painotus
                else:
                    viholliset += 1
        #print("VIH: ", viholliset)
        return self.__kyky2_prio * viholliset

    def pisteyta_ruutu(self, ruutu, kohderuutu):
        # pisteytys vihollisten perusteella
        pisteet = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruutu, self)

        # maaston puolustus ja hyökkäys
        maastokerroin_oma = Tekoaly.pisteyta_liikuttava_maasto(self, ruutu)
        pisteet *= maastokerroin_oma

        # kohteen lähestyminen
        kerroin = Tekoaly.pisteyta_kohteen_lahestyminen(self, ruutu, kohderuutu)
        pisteet *= kerroin

        # läheinen oma yksikkö
        etaisyyskerroin = Tekoaly.pisteyta_oman_yksikon_laheisyys(self, ruutu)
        pisteet *= etaisyyskerroin

        # etäisyys vihollisista
        kerroin = Tekoaly.pisteyta_vihollisten_valttely(self, ruutu)
        pisteet *= kerroin
        return pisteet
