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

        # maastojen lukeminen
        self.maaston_lukija = Maaston_lukija()

        # tehdään vasta koko kartan luomisen jälkeen, kun kaikki ruudut ovat paikallaan
        for ruutu in self.kartta.ruudut:
            ruutu.luo_maasto()
            ruutu.luo_grafiikka(self.kartta.ruudun_koko)

        # maastot täytyy luoda ensin, jotta saadaan naapurit, joihin liikkuminen on mahdollista
        for ruutu in self.kartta.ruudut:
            ruutu.etsi_naapurit()


        # polunhaku testi
        self.polunhaku = Polunhaku(self.kartta.ruudut)

        #print(self.kartta.ruudut[3].koordinaatit.x, " ", self.kartta.ruudut[3].koordinaatit.y)
        #print(self.kartta.ruudut[40].koordinaatit.x, " ", self.kartta.ruudut[40].koordinaatit.y)

        came, cost = self.polunhaku.a_star_search(self.kartta.ruudut[3], self.kartta.ruudut[250])

        path = self.polunhaku.reconstruct_path(came, self.kartta.ruudut[3], self.kartta.ruudut[250])
        for ruutu in path:
            print("x:", ruutu.koordinaatit.x + 1, "y:", ruutu.koordinaatit.y + 1)










