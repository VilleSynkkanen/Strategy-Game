from kartta import Kartta
from kartan_lukija import Kartan_lukija
from kayttoliittyma import Kayttoliittyma

class Pelinohjain:

    def __init__(self):
        # käyttöliittymä
        self.kayttoliittyma = Kayttoliittyma(self)

        self.vuoro = "PLR"      # PLR = pelaaja, COM = tietokone

        # kartan lukeminen
        self.kartan_lukija = Kartan_lukija()
        ruudut = self.kartan_lukija.lue_kartta()
        self.koko = (self.kartan_lukija.koko_x(), self.kartan_lukija.koko_y())
        self.kartta = Kartta(self.koko[0], self.koko[1], ruudut, self.kayttoliittyma)







