from kartta import Kartta
from kartan_lukija import Kartan_lukija
from kayttoliittyma import Kayttoliittyma
from maaston_lukija import Maaston_lukija
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

        self.kayttoliittyma.set_scene_rect(self.koko[0], self.koko[1])

        # maastojen lukeminen
        self.maaston_lukija = Maaston_lukija()

        # tehdään vasta koko kartan luomisen jälkeen, kun kaikki ruudut ovat paikallaan
        for ruutu in self.kartta.ruudut:
            ruutu.luo_maasto()
            ruutu.luo_grafiikka(self.kartta.ruudun_koko)

        # maastot täytyy luoda ensin, jotta saadaan naapurit, joihin liikkuminen on mahdollista
        for ruutu in self.kartta.ruudut:
            ruutu.etsi_naapurit()


        # polunhaku
        self.polunhaku = Polunhaku()

    def polunhaku_testi(self, aloitus):
        for ruutu in self.kartta.ruudut:
            if ruutu.maasto.liikkuminen:
                ruudut, hinnat = self.polunhaku.hae_polkua(aloitus, ruutu)
                #polku = self.polunhaku.rakenna_polku(ruudut, aloitus, ruutu)
                hinta = self.polunhaku.laske_hinta(hinnat, ruutu)
                ruutu.grafiikka.maarita_teksti(hinta)






