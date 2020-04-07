from jalkavaki import Jalkavaki
from ajastin import Ajastin
from math import sqrt

class Jalkavaki_tekoaly(Jalkavaki):
    
    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        # tarvitaan (ainakin) grafiikan luontia varten
        self.__class__.__name__ = "Jalkavaki"
        super(Jalkavaki_tekoaly, self).__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt)

        # priorisaatio ruudun/hyökkäyksen kohteen päättämisessä
        self.tykisto_prio = 1.5
        self.parantaja_prio = 1.4
        self.jousimies_prio = 1.2
        self.ratsuvaki_prio = 1.1
        self.jalkavaki_prio = 1

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
            vaihtoehdot[ruutu] = self.pisteyta_ruutu(ruutu, kohderuutu)

        # etsi korkein pistemäärä
        paras = self.ruutu
        for ruutu in vaihtoehdot:
            if vaihtoehdot[ruutu] > vaihtoehdot[paras]:
                paras = ruutu

        # liiku ruutuun
        if paras != self.ruutu:
            self.liiku_ruutuun(paras)

    def hyokkays_toiminto(self):
        self.laske_hyokkayksen_kohteet(False)
        paras_suhde = 1
        paras_kohde = None
        for vihollinen in self.hyokkayksen_kohteet:
            hyok_vahinko, puol_vahinko, flanking = self.laske_vahinko(self, vihollinen, True)
            suhde = hyok_vahinko / puol_vahinko
            if suhde < 1:
                paras_suhde = suhde
                paras_kohde = vihollinen
        if paras_suhde < 1:
            paras_kohde.hyokkayksen_kohde(self)

    def pisteyta_ruutu(self, ruutu, kohderuutu):
        # aluksi 10 pistettä, muokataan kertoimien avulla
        pisteet = 10
        # lasketaan mahdolliset kohteet ja käydään ne läpi for-loopilla
        viholliset = self.kantamalla_olevat_viholliset(ruutu)
        suurin_kerroin = 1
        for yksikko in viholliset:
            kerroin = 1
            # priorisoitavat tyypit
            if yksikko.__class__.__name__ == "Tykisto":
                kerroin *= self.tykisto_prio
            elif yksikko.__class__.__name__ == "Parantaja":
                kerroin *= self.parantaja_prio
            elif yksikko.__class__.__name__ == "Jousimiehet":
                kerroin *= self.jousimies_prio
            elif yksikko.__class__.__name__ == "Ratsuvaki":
                kerroin *= self.ratsuvaki_prio
            elif yksikko.__class__.__name__ == "Jalkavaki":
                kerroin *= self.jalkavaki_prio

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
            if yksikko.vieressa_monta_vihollista(True): # muuta: viereesä yksi vihollinen
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

        # lasketaan, lähestytäänkö kohderuutua liikuttaessa ruutuun (vaikutus vähäisempi hyvin lähellä)
        polku, hinnat = self.kayttoliittyma.pelinohjain.polunhaku.hae_polkua(ruutu, kohderuutu)
        if hinnat is not False:
            etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.laske_hinta(hinnat, kohderuutu)
            if etaisyys <= 25:
                kerroin = -0.7 * etaisyys + 5
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
        return pisteet
