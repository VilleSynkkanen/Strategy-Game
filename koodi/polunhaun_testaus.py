import unittest
from pelinohjain import Pelinohjain
from paavalikko import Paavalikko
import sys
from PyQt5.QtWidgets import QApplication
from yksikon_ominaisuudet import Yksikon_ominaisuudet
from yksikoiden_lukija import Yksikoiden_lukija


class Polunhaun_testaus(unittest.TestCase):

    def Testi(self):
        global app
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        polunhaku = pelinojain.polunhaku
        lukija = Yksikoiden_lukija()

        # lisätään yksiköitä siten, että tulee muutama blokattu paikka
        ominaisuudet = Yksikon_ominaisuudet("Jalkavaki", 1, 1, 1, 1, 1, 1, 1, 1, 1, None)
        kartta.lisaa_yksikko(ruudut[9][10], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")
        kartta.lisaa_yksikko(ruudut[7][9], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")
        kartta.lisaa_yksikko(ruudut[15][12], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")
        kartta.lisaa_yksikko(ruudut[6][4], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")

        # aloitusruutu
        aloitus = ruudut[10][8]

        # testataan 15 ruutuun vaadittava liike, 5 sellaista, joihin ei pääse liikkumaan (blokattu tai yksikkö ruudussa)

        # paikat, joihin pääsee
        hinta = self.ruutu_hinta(aloitus, ruudut[0][4], polunhaku)
        self.assertEqual(hinta, 19)

        hinta = self.ruutu_hinta(aloitus, ruudut[18][6], polunhaku)
        self.assertEqual(hinta, 14)

        hinta = self.ruutu_hinta(aloitus, ruudut[12][3], polunhaku)
        self.assertEqual(hinta, 12)

        hinta = self.ruutu_hinta(aloitus, ruudut[4][13], polunhaku)
        self.assertEqual(hinta, 13)

        hinta = self.ruutu_hinta(aloitus, ruudut[18][5], polunhaku)
        self.assertEqual(hinta, 13)

        hinta = self.ruutu_hinta(aloitus, ruudut[2][10], polunhaku)
        self.assertEqual(hinta, 12)

        hinta = self.ruutu_hinta(aloitus, ruudut[6][11], polunhaku)
        self.assertEqual(hinta, 9)

        hinta = self.ruutu_hinta(aloitus, ruudut[4][6], polunhaku)
        self.assertEqual(hinta, 9)

        hinta = self.ruutu_hinta(aloitus, ruudut[15][11], polunhaku)
        self.assertEqual(hinta, 8)

        hinta = self.ruutu_hinta(aloitus, ruudut[19][1], polunhaku)
        self.assertEqual(hinta, 18)

        # paikat,joihin ei pääse
        self.assertFalse(polunhaku.hae_polkua(aloitus, ruudut[7][10])[0])
        self.assertFalse(polunhaku.hae_polkua(aloitus, ruudut[6][5])[0])
        self.assertFalse(polunhaku.hae_polkua(aloitus, ruudut[16][14])[0])
        self.assertFalse(polunhaku.hae_polkua(aloitus, ruudut[3][3])[0])
        self.assertFalse(polunhaku.hae_polkua(aloitus, ruudut[14][10])[0])

    # kutsu tätä metodia vain ruuduille, joihin pääsee varmuudella
    def ruutu_hinta(self, aloitus, kohde, polunhaku):
        ruudut, hinnat = polunhaku.hae_polkua(aloitus, kohde)
        hinta = polunhaku.laske_hinta(hinnat, kohde)
        return hinta


if __name__ == "__main__":
    unittest.main()
