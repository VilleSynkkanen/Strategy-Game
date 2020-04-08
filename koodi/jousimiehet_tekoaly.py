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
        Tekoaly.liike(self, kohderuutu)

    def hyokkays_toiminto(self):
        # katsotaan ensin, mahdolliset hyökkäyksen kohteet ja tallennetaan ne sanakirjaan
        paras_kohde = Tekoaly.hyokkays_toiminto(self)

        if paras_kohde is None:
            pass
        elif paras_kohde == "KYKY1":
            self.kyky1()
        elif paras_kohde == "KYKY2":
            self.kyky2()
        else:
            paras_kohde.hyokkayksen_kohde(self)

    def pisteyta_kyky1(self):
        return 0

    def pisteyta_kyky2(self):
        return 0

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

        # lisäys jousimiehille: pysy niin kaukana vihollisista kuin kantama sallii
        kerroin = 1
        for vihollinen in self.kayttoliittyma.pelinohjain.kartta.pelaajan_yksikot:
            polku, hinnat = self.kayttoliittyma.pelinohjain.polunhaku.hae_polkua(ruutu, vihollinen.ruutu, False)
            if hinnat is not False:
                etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.laske_hinta(hinnat, vihollinen.ruutu)
                if etaisyys < self.ominaisuudet.kantama:
                    kerroin = (etaisyys / self.ominaisuudet.kantama)**2
        pisteet *= kerroin
        return pisteet
