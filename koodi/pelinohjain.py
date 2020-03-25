from kartta import Kartta
from kartan_lukija import Kartan_lukija
from kayttoliittyma import Kayttoliittyma
from maaston_lukija import Maaston_lukija
from yksikoiden_lukija import Yksikoiden_lukija
from polunhaku import Polunhaku

class Pelinohjain:

    def __init__(self):
        # käyttöliittymä
        self.kayttoliittyma = Kayttoliittyma(self)

        self.vuoro = "PLR"      # PLR = pelaaja, COM = tietokone

        # kartan lukeminen
        self.kartan_lukija = Kartan_lukija()
        self.nimi, x, y, ruudut, yksikot = self.kartan_lukija.lue_kartta("testikentta.txt")
        self.koko = (x, y)
        self.kartta = Kartta(self.koko[0], self.koko[1], ruudut, self.kayttoliittyma)

        self.kayttoliittyma.aseta_scene_rect(self.koko[0], self.koko[1])

        # maastojen lukeminen
        self.maaston_lukija = Maaston_lukija()

        # yksiköiden lukeminen
        self.yksikoiden_lukija = Yksikoiden_lukija()

        # tehdään vasta koko kartan luomisen jälkeen, kun kaikki ruudut ovat paikallaan
        for ruutu in self.kartta.ruudut:
            ruutu.luo_maasto()
            ruutu.luo_grafiikka(self.kartta.ruudun_koko)

        # maastot täytyy luoda ensin, jotta saadaan naapurit, joihin liikkuminen on mahdollista
        for ruutu in self.kartta.ruudut:
            ruutu.etsi_naapurit()

        self.kartta.lisaa_yksikot(yksikot, self.yksikoiden_lukija.yksikot)

        # polunhaku
        self.polunhaku = Polunhaku()

    # laskee mahdolliset kohteet aloituksen ja liikkumispisteiden perusteella
    def laske_polut(self, aloitus, liikkuminen):
        mahdolliset_ruudut = []
        for ruutu in self.kartta.ruudut:
            # rajoitetaan haku vain alueelle, jolle liikkumispisteet riittävät
            if ruutu.maasto.liikkuminen and ruutu.yksikko == None and self.polunhaku.heuristiikka(aloitus, ruutu) <= liikkuminen:
                ruudut, hinnat = self.polunhaku.hae_polkua(aloitus, ruutu)
                if ruudut != False:
                    #polku = self.polunhaku.rakenna_polku(ruudut, aloitus, ruutu)
                    hinta = self.polunhaku.laske_hinta(hinnat, ruutu)
                    if hinta <= liikkuminen:
                        mahdolliset_ruudut.append(ruutu)
        return mahdolliset_ruudut

    def vuoron_alku(self):
        # lasketaan kaikkien yksiköiden mahdolliset polut
        self.kayttoliittyma.tyhjenna_valinta()
        self.kayttoliittyma.valitsee_hyokkayksen_kohdetta = False
        self.kartta.palauta_pelaajan_toimivat_yksikot()            # myöh: palauta vain ne, jotka eivät ole taintuneita
        for yksikko in self.kartta.pelaajan_yksikot:
            # jos on tehnyt jotain, 2 energiaa, muuten 1
            yksikko.saa_energiaa()
            if yksikko.liikkuminen_kaytetty or yksikko.hyokkays_kaytetty:
                yksikko.saa_energiaa()
            yksikko.kasittele_tilavaikutukset()     # siirrä vuoron loppuun jossain vaiheessa
            if not yksikko.onko_taintunut():
                yksikko.palauta_liikkumispisteet()
            yksikko.grafiikka.palauta_vari()
        for yksikko in self.kartta.tietokoneen_yksikot:
            yksikko.kasittele_tilavaikutukset()  # siirrä vuoron loppuun jossain vaiheessa
            yksikko.grafiikka.paivita_tooltip()