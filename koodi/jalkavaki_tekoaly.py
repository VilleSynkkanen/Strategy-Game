from jalkavaki import Jalkavaki
from ajastin import Ajastin

class Jalkavaki_tekoaly(Jalkavaki):
    
    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        # tarvitaan (ainakin) grafiikan luontia varten
        self.__class__.__name__ = "Jalkavaki"
        super(Jalkavaki_tekoaly, self).__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt)

    '''
    -jos on kohteita kantamalla, valitsee niistä yhden, jonka viereen liikkuu pisteytyksen perusteella
        -heikompien/tiettyjen yksikkötyyppejen priorisaatio
        -ei mieluiten mene huonoon maastoon
    -vaihtoehtoisesti liikkuu hyvään maastoon, jos ei heikkoja vihollisia tarjolla
    
    eli siis pisteytykseen vaikuttaa:
    -mahdollisen vihollisen puolustus, elämä, tyyppi, ruudun maasto
    -maasto
    -läheiset omat yksiköt
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
        '''# etsi lähin vihollinen
        kantama = 1000
        lahin = None
        for vihollinen in self.kayttoliittyma.pelinohjain.kartta.pelaajan_yksikot:
            if self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.ruutu, vihollinen.ruutu) < kantama:
                kantama = self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(self.ruutu, vihollinen.ruutu)
                lahin = vihollinen'''

        # sanakirja, johon lisätään ruudut, avaimena pisteytys
        # jokaiselle ruudulle kutsutaan pistytysmetodi
        vaihtoehdot = {}
        self.laske_mahdolliset_ruudut()
        self.mahdolliset_ruudut.append(self.ruutu)  # lisätään, koska muuten ei tule lisättyä(?)
        for ruutu in self.mahdolliset_ruudut:
            vaihtoehdot[ruutu] = self.pisteyta_ruutu(ruutu, kohderuutu)

        # etsi korkein pistemäärä
        paras = self.ruutu
        for ruutu in vaihtoehdot:
            if vaihtoehdot[ruutu] > vaihtoehdot[paras]:
                paras = ruutu

        #print(vaihtoehdot)
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
        # alustava pisteytys testausta varten
        pisteet = 0
        for naapuri in ruutu.naapurit:
            if naapuri.yksikko is not None and naapuri.yksikko.omistaja != self.omistaja:
                pisteet += 3
                # tyypin, elämän tms. vaikutukset
                kerroin = 1
                if naapuri.__class__.__name__ == "Tykisto" or naapuri.yksikko.__class__.__name__ == "Parantaja":
                    kerroin = 1.5
                elamakerroin = 1 / (naapuri.yksikko.ominaisuudet.nyk_elama / naapuri.yksikko.ominaisuudet.max_elama)
                puolustuskerroin = 1 * (self.ominaisuudet.hyokkays / naapuri.yksikko.ominaisuudet.puolustus)
                kerroin *= elamakerroin * puolustuskerroin
                if naapuri.yksikko.vieressa_monta_vihollista(): # muuta: viereesä yksi vihollinen
                    kerroin *= 1.25
                pisteet *= kerroin
        # maaston puolustus ja hyökkäys
        # pisteet += (ruutu.maasto.hyokkayskerroin - 1) * 4
        # pisteet += (ruutu.maasto.puolustuskerroin - 1) * 4

        # kohderuudun lähestyminen
        polku, hinnat = self.kayttoliittyma.pelinohjain.polunhaku.hae_polkua(ruutu, kohderuutu)
        if hinnat is not False:
            etaisyys = self.kayttoliittyma.pelinohjain.polunhaku.laske_hinta(hinnat, kohderuutu)
            # ongelma: pelkän heuristiikan avulla ei päästä perille

            # alaspäin aukava paraabeli
            pistelisays = -0.06 * etaisyys*etaisyys + 10
            if pistelisays < 0:
                pistelisays = 0
            if etaisyys < 7:
                pistelisays *= etaisyys / 7
            if etaisyys < 4:
                pistelisays = 0

            pisteet += pistelisays
        # läheiset omat yksiköt

        return pisteet

    def valitse_ruutu(self):
        pass