from yksikkografiikka import Yksikkografiikka
from yksikon_ominaisuudet import Yksikon_ominaisuudet
from tilavaikutus import Tilavaikutus
from random import randrange

class Yksikko:

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        self.__omistaja = omistaja
        self.__ruutu = ruutu
        self.__kayttoliittyma = kayttoliittyma
        self.__grafiikka = None
        self.__ominaisuudet = self.__luo_ominaisuudet(ominaisuudet)

        # ruudut, joihin liikkuminen on mahdollista tällä vuorolla
        self.__mahdolliset_ruudut = []

        # mahdolliset hyökkäyskohteet
        self.__hyokkayksen_kohteet = []
        self.__ruudut_kantamalla = []

        self.__liikkuminen_kaytetty = False
        self.__hyokkays_kaytetty = False

        # niille yksiköille, joiden kyky 1 valitsee kohteiksi ruutuja
        self.__kyky1_valitsee_kohteita = False
        self.__kyky1_kohteet = []

        self.__kyky2_valitsee_kohteita = False
        self.__visualisointi_viive = 200

        # hyökkäyksessä aiheutettava tilavaikutus
        self.__hyokkays_vaikutus = None


    # propertyt vain luku-muuttujia varten
    @property
    def hyokkays_vaikutus(self):
        return self.__hyokkays_vaikutus

    @hyokkays_vaikutus.setter
    def hyokkays_vaikutus(self, arvo):
        self.__hyokkays_vaikutus = arvo

    @property
    def visualisointi_viive(self):
        return self.__visualisointi_viive

    @property
    def liikkuminen_kaytetty(self):
        return self.__liikkuminen_kaytetty

    @property
    def hyokkays_kaytetty(self):
        return self.__hyokkays_kaytetty

    @property
    def omistaja(self):
        return self.__omistaja

    @property
    def ruutu(self):
        return self.__ruutu

    @property
    def kayttoliittyma(self):
        return self.__kayttoliittyma

    @property
    def grafiikka(self):
        return self.__grafiikka

    @property
    def ominaisuudet(self):
        return self.__ominaisuudet

    @property
    def kyky1_valitsee_kohteita(self):
        return self.__kyky1_valitsee_kohteita

    @kyky1_valitsee_kohteita.setter
    def kyky1_valitsee_kohteita(self, arvo):
        self.__kyky1_valitsee_kohteita = arvo

    @property
    def kyky1_kohteet(self):
        return self.__kyky1_kohteet

    @property
    def mahdolliset_ruudut(self):
        return self.__mahdolliset_ruudut

    @property
    def hyokkayksen_kohteet(self):
        return self.__hyokkayksen_kohteet

    @property
    def ruudut_kantamalla(self):
        return self.__ruudut_kantamalla

    @property
    def kyky2_valitsee_kohteita(self):
        return self.__kyky2_valitsee_kohteita

    @kyky2_valitsee_kohteita.setter
    def kyky2_valitsee_kohteita(self, arvo):
        self.__kyky2_valitsee_kohteita = arvo

    def __str__(self):
        pass

    def luo_grafiikka(self):
        self.__grafiikka = Yksikkografiikka(self, self.__ruutu, self.__kayttoliittyma, self.__omistaja, self)

    def __luo_ominaisuudet(self, ominaisuudet):
        # luo ominaisuudet annetun ominaisuus-instanssin perusteella
        om = Yksikon_ominaisuudet(ominaisuudet.tyyppi, ominaisuudet.liikkuminen, ominaisuudet.max_elama,
                                  ominaisuudet.nyk_elama, ominaisuudet.max_energia, ominaisuudet.nyk_energia,
                                  ominaisuudet.hyokkays, ominaisuudet.puolustus, ominaisuudet.kantama,
                                  ominaisuudet.hinta, ominaisuudet.tilavaikutukset)
        return om

    def laske_mahdolliset_ruudut(self):
        self.__mahdolliset_ruudut = self.__kayttoliittyma.pelinohjain.laske_polut(self.__ruutu,
                                                                                  self.__ominaisuudet.liikkuminen)

    def nayta_mahdolliset_ruudut(self):
        for ruutu in self.__mahdolliset_ruudut:
            ruutu.grafiikka.voi_liikkua()

    def __tyhjenna_mahdolliset_ruudut(self):
        self.__mahdolliset_ruudut = []

    def laske_hyokkayksen_kohteet(self, nayta):
        # laskee kantamalla olevat ruudut ja lisää kohteisiin niissä olevat viholliset
        self.__hyokkayksen_kohteet = []
        self.laske_kantaman_sisalla_olevat_ruudut()
        for ruutu in self.__ruudut_kantamalla:
            if ruutu.yksikko is not None and ruutu.yksikko.omistaja != self.__omistaja:
                self.__hyokkayksen_kohteet.append(ruutu.yksikko)
        if not nayta:
            return
        self.nayta_hyokkayksen_kohteet()
        self.nayta_kantaman_sisalla_olevat_ruudut()

    # eroaa laske_kantaman_sisalla_olevat_ruudut siten, että ruutu voi olla mikä tahansa ja tyhjiä ruutuja ei lasketa
    def kantamalla_olevat_viholliset(self, ruutu):
        viholliset_kantamalla = []
        for kohde in self.__kayttoliittyma.pelinohjain.kartta.ruudut:
            if kohde.yksikko is not None and kohde.yksikko.omistaja != self.__omistaja and \
                    self.__kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, kohde) \
                    <= self.__ominaisuudet.kantama:
                if self.__kayttoliittyma.pelinohjain.kartta.nakyvyys(ruutu, kohde) \
                        or self.__class__.__name__ == "Tykisto":
                    viholliset_kantamalla.append(kohde.yksikko)
        return viholliset_kantamalla

    def peru_hyokkayksen_kohteiden_nayttaminen(self):
        for vihollinen in self.__hyokkayksen_kohteet:
            vihollinen.grafiikka.palauta_vari()
            vihollinen.grafiikka.paivita_tooltip()
        self.__hyokkayksen_kohteet = []
        self.tyhjenna_ruudut_kantamalla()

    def laske_kantaman_sisalla_olevat_ruudut(self):
        self.__ruudut_kantamalla = []
        for ruutu in self.__kayttoliittyma.pelinohjain.kartta.ruudut:
            if self.__kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.__ruutu, ruutu) <= self.__ominaisuudet.kantama:
                if self.__kayttoliittyma.pelinohjain.kartta.nakyvyys(self.__ruutu, ruutu):
                    self.__ruudut_kantamalla.append(ruutu)
                elif self.__class__.__name__ == "Tykisto" and self.__kyky2_valitsee_kohteita is False:
                    self.__ruudut_kantamalla.append(ruutu)

    def nayta_kantaman_sisalla_olevat_ruudut(self):
        for ruutu in self.__ruudut_kantamalla:
            ruutu.grafiikka.muuta_vari(ruutu.grafiikka.kantaman_sisalla_vari)

    def nayta_hyokkayksen_kohteet(self, vari=True):
        for vihollinen in self.__hyokkayksen_kohteet:
            if vari:
                vihollinen.grafiikka.muuta_varia(vihollinen.grafiikka.voi_hyokata_vari)
            # laskee odotetun vahingon ja näyttää sen tooltipissä
            hyok_vahinko, puol_vahinko, flanking = self.laske_vahinko(self, vihollinen, True)
            tukibonus = "ei"
            if flanking is True:
                tukibonus = "kyllä"
            if self.__class__.__name__ != "Ratsuvaki" or not self.kyky2_valitsee_kohteita:
                vihollinen.grafiikka.hyokkays_tootip(hyok_vahinko, puol_vahinko, tukibonus)

    def __tyhjenna_hyokkayksen_kohteet(self):
        self.__hyokkayksen_kohteet = []

    def peru_mahdollisten_ruutujen_nayttaminen(self):
        for ruutu in self.__mahdolliset_ruudut:
            ruutu.grafiikka.palauta_vari()

    def tyhjenna_ruudut_kantamalla(self):
        for ruutu in self.__ruudut_kantamalla:
            ruutu.grafiikka.palauta_vari()
        self.__ruudut_kantamalla = []

    def liiku_ruutuun(self, ruutu):
        self.__ruutu.liiku_pois()
        self.__ruutu = ruutu
        ruutu.liiku_ruutuun(self)
        self.__grafiikka.paivita_sijainti(self.__ruutu)
        self.liikuttu()
        self.laske_hyokkayksen_kohteet(False)
        teksti = self.__class__.__name__ + \
                 " liikkui ruutuun (" + str(ruutu.koordinaatit.x) + ", " + str(ruutu.koordinaatit.y) + ")"
        self.kayttoliittyma.lisaa_pelilokiin(teksti)
        if self.omistaja == "PLR":
            self.kayttoliittyma.paivita_nappien_aktiivisuus()
            if len(self.__hyokkayksen_kohteet) == 0 or self.__hyokkays_kaytetty:
                # poista yksiköistä, jotka voivat vielä tehdä jotain
                self.__kayttoliittyma.pelinohjain.kartta.poista_toimivista_yksikoista(self)

    def liikuttu(self):
        self.peru_mahdollisten_ruutujen_nayttaminen()
        self.__liikkuminen_kaytetty = True
        self.__mahdolliset_ruudut = []
        if self == self.__kayttoliittyma.valittu_yksikko:
            self.__kayttoliittyma.paivita_valitun_yksikon_tiedot()

    def palauta_liikkumispisteet(self):
        self.__liikkuminen_kaytetty = False
        self.__hyokkays_kaytetty = False
        self.__grafiikka.palauta_vari()

    def vieressa_monta_vihollista(self, yksi=False):
        viholliset = 0
        for ruutu in self.__ruutu.naapurit:
            if ruutu.yksikko is not None and ruutu.yksikko.omistaja != self.__omistaja:
                viholliset += 1
        if viholliset > 1 or viholliset == 1 and yksi == True:
            return True
        return False

    def hyokatty(self):
        # poista listoista kantamalla olevat ruudut ja mahdolliset kohteet
        self.__tyhjenna_hyokkayksen_kohteet()
        self.tyhjenna_ruudut_kantamalla()
        self.__hyokkays_kaytetty = True
        # ratsuväen passiivinen kyky
        if self.__class__.__name__ != "Ratsuvaki":
            self.liikuttu()
        else:
            if not self.__liikkuminen_kaytetty:
                self.laske_mahdolliset_ruudut()
                self.nayta_mahdolliset_ruudut()
        if self == self.__kayttoliittyma.valittu_yksikko:
            self.__kayttoliittyma.paivita_valitun_yksikon_tiedot()
        # poista yksiköistä, jotka voivat vielä tehdä jotain
        self.__kayttoliittyma.pelinohjain.kartta.poista_toimivista_yksikoista(self)

    def hyokkayksen_kohde(self, hyokkaaja):
        self.hyokkays(hyokkaaja)
        if hyokkaaja == self.__kayttoliittyma.valittu_yksikko:
            for vihollinen in hyokkaaja.hyokkayksen_kohteet:
                vihollinen.grafiikka.palauta_vari()
            self.__kayttoliittyma.peru_kohteen_valinta()
        # jos hyökkäykseen liittyy tilavaikutus, se lisätään hyökkäyksen jälkeen
        if hyokkaaja.hyokkays_vaikutus is not None:
            v = hyokkaaja.hyokkays_vaikutus
            self.lisaa_tilavaikutus(v.kesto, v.hyokkaysbonus, v.puolustusbonus, v.liikkumisbonus,
                                    v.verenvuoto, v.taintuminen)
        hyokkaaja.hyokatty()

    @staticmethod
    def laske_vahinko(hyokkaaja, puolustaja, odotettu):
        # odotettu: bool, joka kertoo, palautetaanko odotettu vai todellinen vahinko
        # hyökkääjä = hyökkääjä
        hyokkays = hyokkaaja.ominaisuudet.hyokkays * hyokkaaja.ruutu.maasto.hyokkayskerroin * \
                   (0.5 * (hyokkaaja.ominaisuudet.nyk_elama / hyokkaaja.ominaisuudet.max_elama) + 0.5)
        puolustus = puolustaja.ominaisuudet.puolustus * puolustaja.ruutu.maasto.puolustuskerroin * \
                    (0.5 * (puolustaja.ominaisuudet.nyk_elama / puolustaja.ominaisuudet.max_elama) + 0.5)
        etaisyys = puolustaja.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(puolustaja.ruutu, hyokkaaja.ruutu)

        # aiheutettu vahinko = voima / vihollisen voima * perusvahinko, [min_vahinko, max_vahinko]
        # puolustettaessa voima = puolustus, hyökättäessä voima = hyökkäys
        # vahinko voi vaihdella +-15%
        # elämän vaikutus voimaan: kerroin = 0.5 * elämä + 0.5 (= 1, kun täysi elämä, 0.5, kun elämä 0)
        # flanking bonus: +15% hyökkäys

        perusvahinko = 10
        min_vahinko = 2
        max_vahinko = 40
        satunnaisuuskerroin = 0.15
        flanking_kerroin = 1.15

        # flanking
        flanking = False
        if etaisyys == 1:
            flanking = puolustaja.vieressa_monta_vihollista()
        if flanking:
            hyokkays *= flanking_kerroin

        # jousimiesten bonus
        if hyokkaaja.__class__.__name__ == "Jousimiehet":
            if puolustaja.__class__.__name__ == "Jalkavaki" or puolustaja.__class__.__name__ == "Ratsuvaki":
                hyokkays *= hyokkaaja.jalka_ratsu_vahinko_hyokkays

        # inspiraatio
        hyokkays *= hyokkaaja.__inspiraatio_bonus()
        puolustus *= puolustaja.__inspiraatio_bonus()

        # kiilat
        if puolustaja.ruutu.kiilat is not None:
            if hyokkaaja.__class__.__name__ == "Ratsuvaki":
                puolustus *= puolustaja.ruutu.kiilat.puolustusbonus_ratsuvaki
            else:
                puolustus *= puolustaja.ruutu.kiilat.puolustusbonus

        # tykistö vs tykistö 33 % vahingosta:
        if puolustaja.__class__.__name__ == "Tykisto" and hyokkaaja.__class__.__name__ == "Tykisto":
            perusvahinko /= 3

        # jos puolustaja ja hyökkääjä samalla puolella, hyökkääjä ei ota vahinkoa
        # mahdollista tykistö kyky 1 kohdalla
        if etaisyys == 1 and puolustaja.omistaja != hyokkaaja.omistaja:
            hyokkaajan_vahinko = (puolustus / hyokkays) * perusvahinko
            if hyokkaajan_vahinko < min_vahinko:
                hyokkaajan_vahinko = min_vahinko
            elif hyokkaajan_vahinko > max_vahinko:
                hyokkaajan_vahinko = max_vahinko
        else:
            hyokkaajan_vahinko = 0

        puolustajan_vahinko = (hyokkays / puolustus) * perusvahinko
        if puolustajan_vahinko < min_vahinko:
            puolustajan_vahinko = min_vahinko
        elif puolustajan_vahinko > max_vahinko:
            puolustajan_vahinko = max_vahinko

        if odotettu:
            return int(hyokkaajan_vahinko), int(puolustajan_vahinko), flanking

        hyokkaajan_vahinko_min = int(hyokkaajan_vahinko * (1 - satunnaisuuskerroin))
        hyokkaajan_vahinko_max = int(hyokkaajan_vahinko * (1 + satunnaisuuskerroin))

        puolustajan_vahinko_min = int(puolustajan_vahinko * (1 - satunnaisuuskerroin))
        puolustajan_vahinko_max = int(puolustajan_vahinko * (1 + satunnaisuuskerroin))

        hyokkaajan_vahinko = randrange(hyokkaajan_vahinko_min, hyokkaajan_vahinko_max + 1, 1)
        puolustajan_vahinko = randrange(puolustajan_vahinko_min, puolustajan_vahinko_max + 1, 1)

        return hyokkaajan_vahinko, puolustajan_vahinko

    # puolustautuminen
    def hyokkays(self, hyokkaaja):
        hyokkaajan_vahinko, puolustajan_vahinko = self.laske_vahinko(hyokkaaja, self, False)
        self.ota_vahinkoa(puolustajan_vahinko)
        hyokkaaja.ota_vahinkoa(hyokkaajan_vahinko)
        teksti1 = hyokkaaja.__class__.__name__ + " hyokkasi " + self.__class__.__name__ + " kimppuun:"
        teksti2 = "Hyökkääjä otti " + str(hyokkaajan_vahinko) + " vahinkoa ja puolustaja otti " \
                  + str(puolustajan_vahinko) + " vahinkoa"
        self.kayttoliittyma.lisaa_pelilokiin(teksti1)
        self.kayttoliittyma.lisaa_pelilokiin(teksti2)
        # jalkaväen passiivinen kyky
        if hyokkaaja.__class__.__name__ == "Jalkavaki":
            hyokkaaja.parannu(hyokkaaja.parannus_hyokkayksessa)

    def ota_vahinkoa(self, vahinko):
        self.__ominaisuudet.nyk_elama -= vahinko
        self.__grafiikka.elamapalkki.paivita_koko()
        self.__grafiikka.paivita_tooltip()
        self.__tarkasta_tuhoutuminen()

    def parannu(self, maara):
        self.__ominaisuudet.nyk_elama += maara
        if self.__ominaisuudet.nyk_elama > self.__ominaisuudet.max_elama:
            self.__ominaisuudet.nyk_elama = self.__ominaisuudet.max_elama
        self.__grafiikka.elamapalkki.paivita_koko()
        self.__grafiikka.paivita_tooltip()
        print("Parannus: ", maara)

    # saa yhden energian
    def saa_energiaa(self):
        if self.__ominaisuudet.nyk_energia < self.__ominaisuudet.max_energia:
            self.__ominaisuudet.nyk_energia += 1

    def kayta_energiaa(self, maara):
        self.__ominaisuudet.nyk_energia -= maara

    def lisaa_tilavaikutus(self, kesto, hyokkays, puolustus, liikkuminen, verenvuoto, taintuminen, loppuvaikutus=None):
        if self.__ominaisuudet is not None:
            vaikutus = Tilavaikutus(self, kesto, hyokkays, puolustus, liikkuminen, verenvuoto, taintuminen, loppuvaikutus)
            self.__ominaisuudet.tilavaikutukset.append(vaikutus)
            self.grafiikka.elamapalkki.paivita_tilavaikutukset()
            teksti = self.__class__.__name__ + " sai tilavaikutuksen"
            self.kayttoliittyma.lisaa_pelilokiin(teksti)

    def muuta_hyokkaysta(self, maara):
        if self.ominaisuudet is not None:
            self.__ominaisuudet.hyokkays += maara

    def muuta_puolustusta(self, maara):
        if self.ominaisuudet is not None:
            self.__ominaisuudet.puolustus += maara

    def muuta_liikkumista(self, maara):
        if self.ominaisuudet is not None:
            self.__ominaisuudet.liikkuminen += maara

    def onko_taintunut(self):
        for vaikutus in self.__ominaisuudet.tilavaikutukset:
            if vaikutus.taintuminen:
                return True
        return False

    def kasittele_tilavaikutukset(self):
        for vaikutus in self.__ominaisuudet.tilavaikutukset:
            # ota vahinkoa verenvuodosta
            if vaikutus.verenvuoto > 0:
                self.ota_vahinkoa(vaikutus.verenvuoto)
            vaikutus.vahenna_kestoa()
            # jos vaikutus loppu, poista vaikutukset
            if vaikutus.kesto <= 0:
                self.muuta_hyokkaysta(-vaikutus.hyokkaysbonus)
                self.muuta_puolustusta(-vaikutus.puolustusbonus)
                self.muuta_liikkumista(-vaikutus.liikkumisbonus)
                self.__ominaisuudet.tilavaikutukset.remove(vaikutus)
                teksti = self.__class__.__name__ + " tilavaikutus loppui"
                self.kayttoliittyma.lisaa_pelilokiin(teksti)
                if vaikutus.loppuvaikutus is not None:
                    v = vaikutus.loppuvaikutus
                    self.lisaa_tilavaikutus(v.kesto, v.hyokkaysbonus, v.puolustusbonus, v.liikkumisbonus,
                                            v.verenvuoto, v.taintuminen)
                    #print("loppuvaikutus")
        self.grafiikka.elamapalkki.paivita_tilavaikutukset()

    def __inspiraatio_bonus(self):
        # käy läpi kaikki yksiköt ja tarkistaa, onko parantaja inspiraation kantamalla, jos on, lisätään bonusta
        bonus = 1
        for yksikko in self.__kayttoliittyma.pelinohjain.kartta.pelaajan_yksikot:
            if yksikko.__class__.__name__ == "Parantaja" and yksikko != self and \
                    self.__kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.__ruutu, yksikko.ruutu) <= \
                    yksikko.inspiraatio_kantama and yksikko.omistaja == self.__omistaja:
                bonus *= yksikko.inspiraatio_kerroin
        return bonus

    def __tarkasta_tuhoutuminen(self):
        if self.__ominaisuudet.nyk_elama <= 0:
            self.__tuhoudu()

    def __tuhoudu(self):
        # poistaa kaikki olemassa olevat viittaukset yksikköön ja piilottaa sen graafiset komponentit
        # jos valittu yksikkö, poista käyttöliittymästä
        teksti = self.__class__.__name__ + " tuhoutui"
        self.kayttoliittyma.lisaa_pelilokiin(teksti)
        if self.__kayttoliittyma.valittu_yksikko == self:
            self.__kayttoliittyma.tyhjenna_valinta()
        # poista kartan listasta
        self.__kayttoliittyma.pelinohjain.kartta.poista_yksikko(self)
        # poista ruudusta
        self.__ruutu.poista_yksikko()
        # tuhoa elämäpalkki
        self.__grafiikka.elamapalkki.poista()
        # tuhoa grafiikka
        self.__grafiikka.poista()
        # poista viittaus ominaisuuksiin
        self.__ominaisuudet = None

    def kyky1(self):
        luokat = ["Jousimiehet", "Parantaja", "Tykisto"]
        if self.__class__.__name__ in luokat:
            # aloittaa kohteiden valitsemisen
            self.__kyky1_kohteet = []
            self.__kyky1_valitsee_kohteita = True
            self.peru_mahdollisten_ruutujen_nayttaminen()
            self.laske_hyokkayksen_kohteet(False)
            self.nayta_kantaman_sisalla_olevat_ruudut()
            self.kayttoliittyma.paivita_peru_nappi()
            if self.__class__.__name__ != "Parantaja":
                # jos jousimies tai tykistö, lasketaan odotettu vahinko kantamalla oleville yksiköille
                alkuperainen_hyok = self.ominaisuudet.hyokkays
                self.ominaisuudet.hyokkays *= self.kyky1_hyokkayskerroin
                # näytä kohteet, jotta tooltip tulee näkyviin, ei värjäämistä
                self.nayta_hyokkayksen_kohteet(False)
                self.ominaisuudet.hyokkays = alkuperainen_hyok


    def kyky2(self):
        pass

    def kyky1_nappi_tiedot(self):
        pass

    def kyky2_nappi_tiedot(self):
        pass

    def peru_kyky1(self):
        self.__kyky1_kohteet = []
        self.__kyky1_valitsee_kohteita = False
        self.tyhjenna_ruudut_kantamalla()
        self.nayta_mahdolliset_ruudut()
        self.kayttoliittyma.paivita_peru_nappi()

    def peru_kyky2(self):
        self.__kyky2_valitsee_kohteita = False
        self.tyhjenna_ruudut_kantamalla()
        self.peru_hyokkayksen_kohteiden_nayttaminen()
        self.nayta_mahdolliset_ruudut()
        self.kayttoliittyma.paivita_peru_nappi()

    def pystyy_toimimaan(self):
        if self.__ominaisuudet.nyk_energia < self.kyky1_hinta and \
                self.__ominaisuudet.nyk_energia < self.kyky2_hinta and self.__liikkuminen_kaytetty:
            return False
        elif self.__liikkuminen_kaytetty and self.__hyokkays_kaytetty:
            return False
        else:
            return True
