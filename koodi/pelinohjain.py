from kartta import Kartta
from kartan_lukija import Kartan_lukija
from kayttoliittyma import Kayttoliittyma
from maaston_lukija import Maaston_lukija

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
            ruutu.etsi_naapurit()
            ruutu.luo_maasto()
            ruutu.luo_grafiikka(self.kartta.ruudun_koko)










