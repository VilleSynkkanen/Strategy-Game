from tekoaly import Tekoaly
from tykisto import Tykisto

class Tykisto_tekoaly(Tykisto):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        self.__class__.__name__ = "Tykisto"
        super(Tykisto_tekoaly, self).__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt)

        # priorisaatio ruudun/hyökkäyksen kohteen päättämisessä
        self.__tykisto_prio = 1.2
        self.__parantaja_prio = 1.3
        self.__jousimies_prio = 1.2
        self.__ratsuvaki_prio = 1.1
        self.__jalkavaki_prio = 1
        self.__max_elamakerroin = 2.5
        self.__min_puolustuskerroin = 1
        self.__max_puolustuskerroin = 1
        self.__min_maastokerroin = 1
        self.__max_maastokerroin = 1
        self.__flanking_kerroin = 1

        # maaston pisteytys
        self.__oma_maastokerroin_hyokkays = 0.75
        self.__oma_maastokerroin_puolustus = 0.25

        # etäisyys kohteesta pisteytys
        self.__kulmakerroin = -0.016
        self.__max_lahestymisbonus = 5
        self.__max_etaisyys_kohteesta = (self.__max_lahestymisbonus - 1) / (-self.__kulmakerroin)

        # etäisyys omasta pisteytys
        self.__oma_lahestymisbonus = 1.01
        self.__oma_max_kantama = 7
        self.__laheisyys_bonus_yksikot = 2

        # ei kohteita nykyisessä ruudussa
        self.__kohteita_kerroin = 0.1
        self.__ei_kohteita_bonus = 10

        # etäisyys vihollisista
        self.__etaisyys_vihollisista_eksp = 2

        # kyvyt
        self.__kyky2_kohde = None
        self.__kyky2_prio = 2.5

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
            self.kyky1()
        elif paras_kohde == "KYKY2":
            self.kyky2(True)
            self.kayta_kyky2(self.__kyky2_kohde)
        else:
            paras_kohde.hyokkayksen_kohde(self)

    # returnaa pisteet ja parhaan kohderuudun
    def pisteyta_kyky1(self):
        return 0

    # käyttää kyvyn 2 aina kun mahdollista (hyvin korkeat pisteet)
    def pisteyta_kyky2(self):
        # muutetaan hyökkäys ja kantama väliaikaisesti
        self.__kyky2_kohde = None
        # tekoäly = True
        self.kyky2(True)
        # etsitään paras kohde
        self.__kyky2_kohde = Tekoaly.hyokkays_toiminto(self, True)
        self.ominaisuudet.hyokkays = self.alkuperainen_hyok
        self.ominaisuudet.kantama = self.alkuperainen_kant
        if self.__kyky2_kohde is not None:
            return self.__kyky2_prio * Tekoaly.pisteyta_pelkka_kohde(self, self.__kyky2_kohde)
        else:
            return 0

    def pisteyta_ruutu(self, ruutu, kohderuutu):
        # jos tykistöllä on hyökkäyksen kohteita, vähennetään pisteitä, muussa tapauksessa lisätään
        self.laske_hyokkayksen_kohteet(False)
        ei_kohteita = False
        if len(self.hyokkayksen_kohteet) == 0 and ruutu != self.ruutu:
            ei_kohteita = True

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

        # ei kohteita nykyisessä ruudussa
        if ei_kohteita:
            pisteet *= self.__ei_kohteita_bonus
        else:
            pisteet *= self.__kohteita_kerroin

        return pisteet
