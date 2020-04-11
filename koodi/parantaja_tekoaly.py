from parantaja import Parantaja
from tekoaly import Tekoaly


class Parantaja_tekoaly(Parantaja):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        self.__class__.__name__ = "Parantaja"
        super(Parantaja_tekoaly, self).__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt)

        # priorisaatio ruudun/hyökkäyksen kohteen päättämisessä
        self.__tykisto_prio = 1.25
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
        self.__oma_maastokerroin_hyokkays = 0.1
        self.__oma_maastokerroin_puolustus = 0.4

        # etäisyys kohteesta pisteytys
        self.__kulmakerroin = -0.04
        self.__max_lahestymisbonus = 2
        self.__max_etaisyys_kohteesta = (self.__max_lahestymisbonus - 1) / (-self.__kulmakerroin)

        # etäisyys omasta pisteytys
        self.__oma_lahestymisbonus = 1.1
        self.__oma_max_kantama = 3
        self.__laheisyys_bonus_yksikot = 2

        # etäisyys vihollisista
        self.__etaisyys_vihollisista_eksp = 4

        # kyvyt
        self.__kyky1_prio_kerroin = 175
        self.__kyky1_jalkavaki_prio = 1
        self.__kyky1_ratsuvaki_prio = 1.1
        self.__kyky1_jousimiehet_prio = 1.2
        self.__kyky1_parantaja_prio = 1.4
        self.__kyky1_tykisto_prio = 1.3

        self.__kyky1_kohde = None

        self.__kyky2_kohde = None
        self.__kyky2_elama_potenssi = 2
        self.__kyky2_voima_kerroin = 0.1

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
            self.kyky1_lisaa_kohde(self.__kyky1_kohde, True)
        elif paras_kohde == "KYKY2":
            self.kayta_kyky2(self.__kyky2_kohde)
        else:
            paras_kohde.hyokkayksen_kohde(self)

    def pisteyta_kyky1(self):
        self.__kyky1_kohde = None
        # käydään läpi kaikki mahdolliset ruudut ja pisteytetään ne
        self.laske_kantaman_sisalla_olevat_ruudut()
        vaihtoehdot = {}
        vaihtoehdot[self.ruutu] = self.__pisteyta_ruutu_kyky2(self.ruutu)
        for ruutu in self.ruudut_kantamalla:
            vaihtoehdot[ruutu] = self.__pisteyta_ruutu_kyky2(ruutu)

        paras = self.ruutu
        for ruutu in vaihtoehdot:
            if vaihtoehdot[ruutu] > vaihtoehdot[paras]:
                paras = ruutu
        self.__kyky1_kohde = paras
        return vaihtoehdot[paras]

    def __pisteyta_ruutu_kyky2(self, ruutu):
        # pisteytyksessä lasketaan painotettu parannusmäärä
        # haetaan ruudut etsimällä annetun ruudun naapurit ja niiden naapurit
        alue = []
        alue.append(self.ruutu)
        for alkio in self.kayttoliittyma.pelinohjain.kartta.ruudut:
            if self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, alkio) <= self.kyky1_kantama:
                alue.append(alkio)
        pisteet = 0
        for paikka in alue:
            if paikka.yksikko is not None and paikka.yksikko.omistaja == "COM":
                puuttuva_elama = paikka.yksikko.ominaisuudet.puuttuva_elama()
                parannus = self.laske_kyky2_parannus(ruutu, paikka)
                if parannus > puuttuva_elama:
                    parannus = puuttuva_elama
                if paikka.yksikko.__class__.__name__ == "Tykisto":
                    parannus *= self.__kyky1_jalkavaki_prio
                elif paikka.yksikko.__class__.__name__ == "Parantaja":
                    parannus *= self.__kyky1_parantaja_prio
                elif paikka.yksikko.__class__.__name__ == "Jousimiehet":
                    parannus *= self.__kyky1_jousimiehet_prio
                elif paikka.yksikko.__class__.__name__ == "Ratsuvaki":
                    parannus *= self.__kyky1_ratsuvaki_prio
                elif paikka.yksikko.__class__.__name__ == "Jalkavaki":
                    parannus *= self.__kyky1_jalkavaki_prio
                pisteet += parannus
        return pisteet * self.__kyky1_prio_kerroin

    def pisteyta_kyky2(self):
        # muutetaan hyökkäys ja kantama väliaikaisesti
        self.__kyky2_kohde = None
        # etsitään paras kohde
        pisteet, self.__kyky2_kohde = self.__kyky2_pisteytys()
        return pisteet

    # mitä voimakkaampi yksikkö, sitä enemmän pisteitä
    def __kyky2_pisteytys(self):
        vaihtoehdot = {}
        self.laske_hyokkayksen_kohteet(False)
        for vihollinen in self.hyokkayksen_kohteet:
            hyok_vahinko, puol_vahinko, flanking = self.laske_vahinko(self, vihollinen, True)
            kerroin = (puol_vahinko + 0.001) / (hyok_vahinko + 0.001)
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
            elamakerroin = (vihollinen.ominaisuudet.nyk_elama / vihollinen.ominaisuudet.max_elama) ** self.__kyky2_elama_potenssi
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

        # etäisyys vihollisista
        kerroin = Tekoaly.pisteyta_vihollisten_valttely(self, ruutu)
        pisteet *= kerroin

        return pisteet