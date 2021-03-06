from jalkavaki import Jalkavaki
from tekoaly import  Tekoaly
from PyQt5 import QtTest


class Jalkavaki_tekoaly(Jalkavaki):
    
    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        self.__class__.__name__ = "Jalkavaki"
        super(Jalkavaki_tekoaly, self).__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt)

        # priorisaatio ruudun/hyökkäyksen kohteen päättämisessä
        self.__tykisto_prio = 1.5
        self.__parantaja_prio = 1.4
        self.__jousimies_prio = 1.2
        self.__ratsuvaki_prio = 1.1
        self.__jalkavaki_prio = 1
        self.__max_elamakerroin = 1.5
        self.__min_puolustuskerroin = 0.5
        self.__max_puolustuskerroin = 2.5
        self.__min_maastokerroin = 0.75
        self.__max_maastokerroin = 1.5
        self.__flanking_kerroin = 1.25

        # maaston pisteytys
        self.__oma_maastokerroin_hyokkays = 0.4
        self.__oma_maastokerroin_puolustus = 0.4

        # etäisyys kohteesta pisteytys
        self.__kulmakerroin = -0.04
        self.__max_lahestymisbonus = 2
        self.__max_etaisyys_kohteesta = (self.__max_lahestymisbonus - 1) / (-self.__kulmakerroin)

        # etäisyys omasta pisteytys
        self.__oma_lahestymisbonus = 1.01
        self.__oma_max_kantama = 4
        self.__laheisyys_bonus_yksikot = 2

        # kykyjen pisteytys
        self.__kyky1_etaisyys_raja = 4
        self.__kyky1_viholliset_min = 2

        # kykyä 2 varten
        self.__kohderuutu = None
        self.__kyky2_ruutu = None
        self.__kyky2_prio = 0.05
        self.__kyky2_ei_vihollista_kerroin = 0.1

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

    def liike(self, kohderuutu):
        # arvioidaan paras kohde liikkumiselle
        self.__kohderuutu = kohderuutu
        Tekoaly.liike(self, kohderuutu)

    def hyokkays_toiminto(self):
        # katsotaan ensin, mahdolliset hyökkäyksen kohteet ja kyvyt ja tallennetaan ne sanakirjaan
        paras_kohde = Tekoaly.hyokkays_toiminto(self)
        if paras_kohde is None:
            pass
        elif paras_kohde == "KYKY1":
            self.kyky1()
        elif paras_kohde == "KYKY2":
            self.kyky2()
            self.liiku_ruutuun(self.__kyky2_ruutu)
            QtTest.QTest.qWait(self.kayttoliittyma.pelinohjain.viive)
            kohde = Tekoaly.hyokkays_toiminto(self, True)
            if kohde is not None:
                kohde.hyokkayksen_kohde(self)
        else:
            paras_kohde.hyokkayksen_kohde(self)

    # pisteytetään sen perusteella, kuinka paljon vihollisia on lähellä yksikköä
    # täytyy olla vähintään self.__kyky1_viholliset_min vihollista
    def pisteyta_kyky1(self):
        etaisyydella = 0
        for vihollinen in self.kayttoliittyma.pelinohjain.kartta.pelaajan_yksikot:
            etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.ruutu, vihollinen.ruutu)
            if etaisyys <= self.__kyky1_etaisyys_raja:
                etaisyydella += 0.5
        if etaisyydella < self.__kyky1_viholliset_min:
            etaisyydella = 0
        return etaisyydella

    # pisteytys sen perusteella, minkä vihollisyksiköiden viereen voidaan liikkua, jos kyky käytetään
    def pisteyta_kyky2(self):
        self.__kyky2_ruutu = None
        # muutetaan liikkuminen väliaikaisesti, sitten pisteytetään ruudut
        alkuperainen = self.ominaisuudet.liikkuminen
        self.ominaisuudet.liikkuminen = self.kyky2_kantama
        self.laske_mahdolliset_ruudut()
        vaihtoehdot = {}
        vaihtoehdot[self.ruutu] = self.pisteyta_ruutu(self.ruutu, self.__kohderuutu)
        for ruutu in self.mahdolliset_ruudut:
            vaihtoehdot[ruutu] = self.pisteyta_ruutu(ruutu, self.__kohderuutu)
        paras = self.ruutu
        for ruutu in vaihtoehdot:
            if vaihtoehdot[ruutu] > vaihtoehdot[paras]:
                paras = ruutu

        self.ominaisuudet.liikkuminen = alkuperainen
        self.__kohderuutu = None
        self.__kyky2_ruutu = paras
        viholliset = False
        for ruutu in self.__kyky2_ruutu.naapurit:
            if ruutu.yksikko is not None and ruutu.yksikko.omistaja == "PLR":
                viholliset = True
        # jos kohteen vieressä ei ole vihollisia, vähennetään pistemäärää
        if not viholliset:
            vaihtoehdot[paras] *= self.__kyky2_ei_vihollista_kerroin
        return vaihtoehdot[paras] * self.__kyky2_prio

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

        return pisteet
