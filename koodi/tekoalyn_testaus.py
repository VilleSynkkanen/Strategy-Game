from tekoaly import Tekoaly
from paavalikko import Paavalikko
from pelinohjain import Pelinohjain
from yksikoiden_lukija import Yksikoiden_lukija
from PyQt5.QtWidgets import QApplication
import sys
import unittest

class Tekoalyn_testaus(unittest.TestCase):

    '''
    testit:
    -hyökkäyksen kohteen valinta (ei kykyjä)
    -ruudun pisteytys kantamalla olevien vihollisten perusteella
    -maaston pisteytys
    -kohteen lähestyminen
    -oman yksikön läheisyys
    -vihollisten välttely
    '''

    def kohteen_valinta_testi(self):
        # luo kartta, lisää yksikkö ja sen kantamalle (viereen) mahdolliset kohteet
        # kutsu funktiota, joka pisteyttää kohteet
        # viisi eri tilannetta
        global app
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        lukija = Yksikoiden_lukija()

        # tilanne 1: neljä eri jalkaväkeä, jokaisella eri elämä
        kartta.lisaa_yksikko(ruudut[1][1], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")

        kartta.lisaa_yksikko(ruudut[1][0], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[0][1], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[2][1], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[1][2], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")

        ruudut[1][0].yksikko.ominaisuudet.nyk_elama = 50
        ruudut[0][1].yksikko.ominaisuudet.nyk_elama = 60
        ruudut[2][1].yksikko.ominaisuudet.nyk_elama = 70
        ruudut[1][2].yksikko.ominaisuudet.nyk_elama = 80
        ruudut[1][1].yksikko.ominaisuudet.nyk_elama = 90

        paras_kohde, pisteet = Tekoaly.hyokkays_toiminto(ruudut[1][1].yksikko, True, True)
        self.assertEqual(paras_kohde.ruutu, ruudut[1][0])

        ruudut[1][0].yksikko.tuhoudu()
        ruudut[0][1].yksikko.tuhoudu()
        ruudut[2][1].yksikko.tuhoudu()
        ruudut[1][2].yksikko.tuhoudu()
        ruudut[1][1].yksikko.tuhoudu()

        # tilanne 2: jousimiehet, ratsuväki, tykistö, kaikilla täysi elämä ja sama puolustus = sama odotettu vahinko
        kartta.lisaa_yksikko(ruudut[1][1], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")

        kartta.lisaa_yksikko(ruudut[1][0], "jousimiehet", lukija.yksikot["jousimiehet"], "PLR")
        kartta.lisaa_yksikko(ruudut[0][1], "tykisto", lukija.yksikot["tykisto"], "PLR")
        kartta.lisaa_yksikko(ruudut[2][1], "ratsuvaki", lukija.yksikot["ratsuvaki"], "PLR")

        ruudut[1][0].yksikko.ominaisuudet.puolustus = 10
        ruudut[0][1].yksikko.ominaisuudet.puolustus = 10
        ruudut[2][1].yksikko.ominaisuudet.puolustus = 10

        paras_kohde, pisteet = Tekoaly.hyokkays_toiminto(ruudut[1][1].yksikko, True, True)
        self.assertEqual(paras_kohde.ruutu, ruudut[0][1])       # tykistön prio kerroin on korkein

        ruudut[1][0].yksikko.tuhoudu()
        ruudut[0][1].yksikko.tuhoudu()
        ruudut[2][1].yksikko.tuhoudu()
        ruudut[1][1].yksikko.tuhoudu()

        # tilanne 3: jalkaväkikohteita 4, toisella flanking, yhdellä flanking
        kartta.lisaa_yksikko(ruudut[1][1], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")
        kartta.lisaa_yksikko(ruudut[1][3], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")

        kartta.lisaa_yksikko(ruudut[1][0], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[0][1], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[2][1], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[1][2], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")

        paras_kohde, pisteet = Tekoaly.hyokkays_toiminto(ruudut[1][1].yksikko, True, True)
        self.assertEqual(paras_kohde.ruutu, ruudut[1][2])          # tämän vieressä on oma, joten se on paras vaihtoehto

        ruudut[1][1].yksikko.tuhoudu()
        ruudut[1][3].yksikko.tuhoudu()
        ruudut[1][0].yksikko.tuhoudu()
        ruudut[0][1].yksikko.tuhoudu()
        ruudut[2][1].yksikko.tuhoudu()
        ruudut[1][2].yksikko.tuhoudu()

        # tilanne 4: yksi kohde ei vieressä, muut ovat
        kartta.lisaa_yksikko(ruudut[1][1], "jousimiehet", lukija.yksikot["jousimiehet"], "COM")

        kartta.lisaa_yksikko(ruudut[1][0], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[0][1], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[2][1], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[1][3], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")

        ruudut[1][1].yksikko.ominaisuudet.hyokkays = 20     # tehdään, jotta vahinkojen suhde olisi > 1

        paras_kohde, pisteet = Tekoaly.hyokkays_toiminto(ruudut[1][1].yksikko, True, True)
        self.assertEqual(paras_kohde.ruutu, ruudut[1][3])

        ruudut[1][1].yksikko.tuhoudu()
        ruudut[1][0].yksikko.tuhoudu()
        ruudut[0][1].yksikko.tuhoudu()
        ruudut[2][1].yksikko.tuhoudu()
        ruudut[1][3].yksikko.tuhoudu()

        # tilanne 5: ei hyviä kohteita
        kartta.lisaa_yksikko(ruudut[1][1], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")

        kartta.lisaa_yksikko(ruudut[1][0], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[0][1], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[2][1], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[1][2], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")

        ruudut[1][0].yksikko.ominaisuudet.nyk_elama = 50
        ruudut[0][1].yksikko.ominaisuudet.nyk_elama = 60
        ruudut[2][1].yksikko.ominaisuudet.nyk_elama = 70
        ruudut[1][2].yksikko.ominaisuudet.nyk_elama = 80
        ruudut[1][1].yksikko.ominaisuudet.nyk_elama = 30

        paras_kohde, pisteet = Tekoaly.hyokkays_toiminto(ruudut[1][1].yksikko, True, True)
        self.assertEqual(paras_kohde, None)
        self.assertEqual(pisteet, 0)
