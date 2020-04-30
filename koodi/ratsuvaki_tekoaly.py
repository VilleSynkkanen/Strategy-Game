from ratsuvaki import Ratsuvaki
from tekoaly import Tekoaly


class Ratsuvaki_tekoaly(Ratsuvaki):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        self.__class__.__name__ = "Ratsuvaki"
        super(Ratsuvaki_tekoaly, self).__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt)

        # priorisaatio ruudun/hyökkäyksen kohteen päättämisessä
        self.__tykisto_prio = 1.25
        self.__parantaja_prio = 1.25
        self.__jousimies_prio = 1.2
        self.__ratsuvaki_prio = 1.1
        self.__jalkavaki_prio = 1
        self.__max_elamakerroin = 1.75

        # seuraavat muuttujat vaikuttavat pelkästään liikkumiseen vihollisen viereen
        self.__min_puolustuskerroin = 0.5
        self.__max_puolustuskerroin = 2
        self.__min_maastokerroin = 0.75
        self.__max_maastokerroin = 1.5
        self.__flanking_kerroin = 1.3

        # maaston pisteytys
        self.__oma_maastokerroin_hyokkays = 0.4
        self.__oma_maastokerroin_puolustus = 0.1

        # etäisyys kohteesta pisteytys
        self.__kulmakerroin = -0.04
        self.__max_lahestymisbonus = 2
        self.__max_etaisyys_kohteesta = (self.__max_lahestymisbonus - 1) / (-self.__kulmakerroin)

        # etäisyys omasta pisteytys
        self.__oma_lahestymisbonus = 1.05
        self.__oma_max_kantama = 3
        self.__laheisyys_bonus_yksikot = 1

        # kyvyt
        self.__kyky1_vihollinen_etaisyys = self.ominaisuudet.liikkuminen
        self.__kyky1_viholliset_min = 1
        self.__kyky1_prio_kerroin = 5
        self.__kyky1_prio_potenssi = 2

        self.__kyky2_kohde = None
        self.__kyky2_elama_potenssi = 2
        self.__kyky2_voima_kerroin = 0.012

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
        # etsitään ensin mahdolliset hyökkäyksen kohteet ja tallennetaan ne sanakirjaan
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

    def pisteyta_kyky1(self):
        # mitä enemmän elämää yksiköllä on, sitä suuremmat pisteet
        # lisäksi vihollisten läheisyys lisää pisteitä
        viholliset = 0
        for vihollinen in self.kayttoliittyma.pelinohjain.kartta.pelaajan_yksikot:
            if self.__kyky1_vihollinen_etaisyys <= \
                    self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.ruutu, vihollinen.ruutu):
                viholliset += 1
        if viholliset < self.__kyky1_viholliset_min:
            return 0
        else:
            return self.__kyky1_prio_kerroin * \
                   ((self.ominaisuudet.nyk_elama / self.ominaisuudet.max_elama)**self.__kyky1_prio_potenssi)

    def pisteyta_kyky2(self):
        # muutetaan hyökkäys ja kantama väliaikaisesti
        self.__kyky2_kohde = None
        self.kyky2(True)
        # etsitään paras kohde
        pisteet, self.__kyky2_kohde = self.__kyky2_pisteytys()
        self.ominaisuudet.kantama = self.alkuperainen_kant
        return pisteet

    # mitä voimakkaampi yksikkö, sitä enemmän pisteitä
    def __kyky2_pisteytys(self):
        vaihtoehdot = {}
        self.laske_hyokkayksen_kohteet(False)
        for vihollinen in self.hyokkayksen_kohteet:
            kerroin = 10
            # priorisoitavat tyypit
            if vihollinen.__class__.__name__ == "Tykisto":
                kerroin *= self.tykisto_prio
            elif vihollinen.__class__.__name__ == "Parantaja":
                kerroin *= self.parantaja_prio
            elif vihollinen.__class__.__name__ == "Jousimiehet":
                kerroin *= self.jousimies_prio
            elif vihollinen.__class__.__name__ == "Ratsuvaki":
                kerroin *= self.ratsuvaki_prio
            elif vihollinen.__class__.__name__ == "Jalkavaki":
                kerroin *= self.jalkavaki_prio

            # elämän vaikutus
            elamakerroin = (vihollinen.ominaisuudet.nyk_elama / vihollinen.ominaisuudet.max_elama)**self.__kyky2_elama_potenssi
            kerroin *= elamakerroin

            # hyökkäyksen ja puolustuksen vaikutus
            voimakerroin = (vihollinen.ominaisuudet.hyokkays + vihollinen.ominaisuudet.puolustus) * self.__kyky2_voima_kerroin
            kerroin *= voimakerroin
            vaihtoehdot[vihollinen] = kerroin

        # määritellään korkeimmat pisteet ja paras kohde
        korkeimmat_pisteet = 0
        paras_kohde = None
        for vaihtoehto in vaihtoehdot:
            # puolustajan vahingon täytyy olla suurempi tai yhtä suuri kuin hyökkääjän, jotta hyökkäys tapahtuisi
            if vaihtoehdot[vaihtoehto] > korkeimmat_pisteet:
                korkeimmat_pisteet = vaihtoehdot[vaihtoehto]
                paras_kohde = vaihtoehto
        return korkeimmat_pisteet, paras_kohde

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
