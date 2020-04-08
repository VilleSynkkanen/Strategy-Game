from jalkavaki import Jalkavaki
from ajastin import Ajastin
from math import sqrt

class Jalkavaki_tekoaly(Jalkavaki):
    
    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        # tarvitaan (ainakin) grafiikan luontia varten
        self.__class__.__name__ = "Jalkavaki"
        super(Jalkavaki_tekoaly, self).__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt)

        # priorisaatio ruudun/hyökkäyksen kohteen päättämisessä
        self.__tykisto_prio = 1.5
        self.__parantaja_prio = 1.4
        self.__jousimies_prio = 1.2
        self.__ratsuvaki_prio = 1.1
        self.__jalkavaki_prio = 1

        # kykyjen pisteytys
        self.__kyky1_etaisyys_raja = 4
        self.__kyky1_viholliset_min = 2

    '''
    -jos on kohteita kantamalla, valitsee niistä yhden, jonka viereen liikkuu pisteytyksen perusteella
        -heikompien/tiettyjen yksikkötyyppejen priorisaatio
        -ei mieluiten mene huonoon maastoon
    -vaihtoehtoisesti liikkuu hyvään maastoon, jos ei heikkoja vihollisia tarjolla
    
    eli siis pisteytykseen vaikuttaa:
    -mahdollisen vihollisen puolustus, elämä, tyyppi, ruudun maasto
    -maasto
    (-läheiset omat yksiköt) jos toimii hyvin
    -pääsy lähemmäs vihollista
    
    mahdollisia apukeinoja: 
    -ylempi voima, joka päättää, mitä kohti liikutaan, mahdollisesti useita vaihtoehtoja
        -päättää, ollanko aggressiivisia vai passiivisia, mahdollinen säätö tiedostojen kautta
        -alue, jota kohti liikutaan
        -yksiköiden päätöksenteko hoitaa yksityiskohdat
        
    ensin katsotaan, halutaanko liikkua johonkin
    mahdollisen liikkumisen jälkeen katsotaan, halutaanko käyttää kykyjä tai hyökätä
    '''

    def liike(self, kohderuutu):
        # sanakirja, johon lisätään ruudut, avaimena pisteytys
        # jokaiselle ruudulle kutsutaan pistytysmetodi
        vaihtoehdot = {}
        self.laske_mahdolliset_ruudut()
        self.mahdolliset_ruudut.append(self.ruutu)  # lisätään, koska muuten ei tule lisättyä
        for ruutu in self.mahdolliset_ruudut:
            vaihtoehdot[ruutu] = self.__pisteyta_ruutu(ruutu, kohderuutu)
        #print(vaihtoehdot)

        # etsi korkein pistemäärä
        paras = self.ruutu
        for ruutu in vaihtoehdot:
            if vaihtoehdot[ruutu] > vaihtoehdot[paras]:
                paras = ruutu

        # liiku ruutuun
        if paras != self.ruutu:
            self.liiku_ruutuun(paras)

    '''
    Kohteen/kyvyn valintaan vaikuttaa:
    -kohteiden tyyppi (priorisaatiokertoimet)
    -odotettujen vahinkojen suhde (suurempi parempi)
    -onko mahdollista käyttää kyky: jokaisella kyvyllä oma pisteytys
    '''

    def hyokkays_toiminto(self):
        # katsotaan ensin, mahdolliset hyökkäyksen kohteet ja tallennetaan ne sanakirjaan
        vaihtoehdot = {}
        self.laske_hyokkayksen_kohteet(False)
        for vihollinen in self.hyokkayksen_kohteet:
            hyok_vahinko, puol_vahinko, flanking = self.laske_vahinko(self, vihollinen, True)
            suhde = puol_vahinko / hyok_vahinko
            vaihtoehdot[vihollinen] = suhde

        kyky1_pisteet = 0
        kyky2_pisteet = 0
        # katsotaan voidaanko kykyjä käyttää, jos voidaan, pisteytetään ne
        if self.ominaisuudet.nyk_energia >= self.kyky1_hinta:
            kyky1_pisteet = self.__pisteyta_kyky1()
            vaihtoehdot["KYKY1"] = kyky1_pisteet
        if self.ominaisuudet.nyk_energia >= self.kyky2_hinta:
            kyky2_pisteet = self.__pisteyta_kyky2()
            vaihtoehdot["KYKY2"] = kyky2_pisteet

        korkeimmat_pisteet = 0
        paras_kohde = None
        for vaihtoehto in vaihtoehdot:
            # puolustajan vahingon täytyy olla suurempi tai yhtä suuri kuin hyökkääjän, jotta hyökkäys tapahtuisi
            if vaihtoehdot[vaihtoehto] > korkeimmat_pisteet and vaihtoehdot[vaihtoehto] >= 1:
                korkeimmat_pisteet = vaihtoehdot[vaihtoehto]
                paras_kohde = vaihtoehto    # voi olla yksikkö tai merkkijono

        if paras_kohde is None:
            pass
        elif paras_kohde == "KYKY1":
            self.kyky1()
        elif paras_kohde == "KYKY2":
            self.kyky2()
        else:
            paras_kohde.hyokkayksen_kohde(self)

    # pisteytetään sen perusteella, kuinka paljon vihollisia on lähellä yksikköä
    # täytyy olla vähintään self.__kyky1_viholliset_min vihollista
    def __pisteyta_kyky1(self):
        etaisyydella = 0
        for vihollinen in self.kayttoliittyma.pelinohjain.kartta.pelaajan_yksikot:
            etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.ruutu, vihollinen.ruutu)
            if etaisyys <= self.__kyky1_etaisyys_raja:
                etaisyydella += 0.5
        if etaisyydella < self.__kyky1_viholliset_min:
            etaisyydella = 0
        return etaisyydella

    # pisteytys: jos kyky2 kantama sisällä on parempi kohde kuin vieressö oleva, enemmän pisteitä
    def __pisteyta_kyky2(self):
        # implementoi pisteytys
        return 0


    def __pisteyta_ruutu(self, ruutu, kohderuutu):
        # aluksi 10 pistettä, muokataan kertoimien avulla
        pisteet = 10
        # lasketaan mahdolliset kohteet ja käydään ne läpi for-loopilla
        viholliset = self.kantamalla_olevat_viholliset(ruutu)
        suurin_kerroin = 1
        for yksikko in viholliset:
            kerroin = 1
            # priorisoitavat tyypit
            if yksikko.__class__.__name__ == "Tykisto":
                kerroin *= self.__tykisto_prio
            elif yksikko.__class__.__name__ == "Parantaja":
                kerroin *= self.__parantaja_prio
            elif yksikko.__class__.__name__ == "Jousimiehet":
                kerroin *= self.__jousimies_prio
            elif yksikko.__class__.__name__ == "Ratsuvaki":
                kerroin *= self.__ratsuvaki_prio
            elif yksikko.__class__.__name__ == "Jalkavaki":
                kerroin *= self.__jalkavaki_prio

            # elämän vaikutus
            elamakerroin = 1 / sqrt(yksikko.ominaisuudet.nyk_elama / yksikko.ominaisuudet.max_elama)
            if elamakerroin > 2:
                elamakerroin = 2
            kerroin *= elamakerroin

            # puolustuksen vaikutus
            puolustuskerroin = 1 * (self.ominaisuudet.hyokkays / yksikko.ominaisuudet.puolustus)
            if puolustuskerroin > 2.5:
                puolustuskerroin = 2
            elif puolustuskerroin < 0.5:
                puolustuskerroin = 0.5
            kerroin *= puolustuskerroin

            # ruudun maasto
            maastokerroin = 1
            maastokerroin *= 1 / sqrt(yksikko.ruutu.maasto.hyokkayskerroin)
            maastokerroin *= 1 / sqrt(yksikko.ruutu.maasto.puolustuskerroin)
            if maastokerroin > 1.5:
                maastokerroin = 1.5
            elif maastokerroin < 0.7:
                maastokerroin = 0.7
            kerroin *= maastokerroin

            # flankkays
            if yksikko.vieressa_monta_vihollista(True):
                kerroin *= 1.25

            # suurimman kertoimen määrittely
            if kerroin > suurin_kerroin:
                suurin_kerroin = kerroin
        pisteet *= suurin_kerroin

        # maaston puolustus ja hyökkäys
        maastokerroin_oma = 1
        # jos kerroin huonompi kuin 1, vähennetään, jos parempi, niin lisätään
        maastokerroin_oma += 1.2 * (ruutu.maasto.hyokkayskerroin - 1)
        maastokerroin_oma += 1.2 * (ruutu.maasto.puolustuskerroin - 1)
        pisteet *= maastokerroin_oma

        # lasketaan, lähestytäänkö kohderuutua liikuttaessa ruutuun
        # lasketaan hinta ilman blokkausta (oletetaan, että tilanne muuttuu)
        polku, hinnat = self.kayttoliittyma.pelinohjain.polunhaku.hae_polkua(ruutu, kohderuutu, False)
        if hinnat is not False:
            etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.laske_hinta(hinnat, kohderuutu)
            if etaisyys <= 25:
                kerroin = -0.02 * etaisyys + 1.5
            else:
                kerroin = 1
            pisteet *= kerroin
        # läheinen oma yksikkö (hyvin pieni prioriteettilisäys)
        etaisyyskerroin = 1
        for yksikko in self.kayttoliittyma.pelinohjain.kartta.tietokoneen_yksikot:
            etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, yksikko.ruutu)
            if 0 < etaisyys < 3:
                etaisyyskerroin = 1.01
        pisteet *= etaisyyskerroin
        #print(pisteet)
        return pisteet
