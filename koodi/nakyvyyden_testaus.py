import unittest
from pelinohjain import Pelinohjain
from paavalikko import Paavalikko
import sys
from PyQt5.QtWidgets import QApplication


class Nakyvyyden_testaus(unittest.TestCase):

    # testi perustuu testikenttä-karttaan
    # testattavat näkyvyydet on tarkistettu käsin ja sen perusteella määritelty, pitäisikö niiden olla True vai False
    def Testi(self):
        global app
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla

        # testataan näkyvyydet eri ruuduista toisiin ruutuihin
        # 15 True, 15 False
        # valittuna erilaisia tilanteita (lähellä kaukana, näkyy juuri ja juuri, erilaiset maastot tms.)
        self.assertTrue(kartta.nakyvyys(ruudut[2][3], ruudut[6][10]))
        self.assertTrue(kartta.nakyvyys(ruudut[16][5], ruudut[11][10]))
        self.assertTrue(kartta.nakyvyys(ruudut[4][13], ruudut[10][2]))
        self.assertTrue(kartta.nakyvyys(ruudut[16][5], ruudut[11][10]))
        self.assertTrue(kartta.nakyvyys(ruudut[17][5], ruudut[11][7]))
        self.assertTrue(kartta.nakyvyys(ruudut[15][13], ruudut[10][2]))
        self.assertTrue(kartta.nakyvyys(ruudut[4][2], ruudut[2][10]))
        self.assertTrue(kartta.nakyvyys(ruudut[8][0], ruudut[8][11]))
        self.assertTrue(kartta.nakyvyys(ruudut[19][0], ruudut[0][12]))
        self.assertTrue(kartta.nakyvyys(ruudut[18][5], ruudut[19][6]))
        self.assertTrue(kartta.nakyvyys(ruudut[15][12], ruudut[17][6]))
        self.assertTrue(kartta.nakyvyys(ruudut[15][10], ruudut[5][13]))
        self.assertTrue(kartta.nakyvyys(ruudut[15][0], ruudut[7][6]))
        self.assertTrue(kartta.nakyvyys(ruudut[19][0], ruudut[18][15]))
        self.assertTrue(kartta.nakyvyys(ruudut[5][1], ruudut[8][11]))

        self.assertFalse(kartta.nakyvyys(ruudut[2][2], ruudut[6][10]))
        self.assertFalse(kartta.nakyvyys(ruudut[17][5], ruudut[11][9]))
        self.assertFalse(kartta.nakyvyys(ruudut[9][10], ruudut[5][13]))
        self.assertFalse(kartta.nakyvyys(ruudut[3][14], ruudut[10][2]))
        self.assertFalse(kartta.nakyvyys(ruudut[16][5], ruudut[14][8]))
        self.assertFalse(kartta.nakyvyys(ruudut[15][12], ruudut[14][8]))
        self.assertFalse(kartta.nakyvyys(ruudut[6][11], ruudut[12][8]))
        self.assertFalse(kartta.nakyvyys(ruudut[2][2], ruudut[7][6]))
        self.assertFalse(kartta.nakyvyys(ruudut[16][7], ruudut[17][5]))
        self.assertFalse(kartta.nakyvyys(ruudut[4][14], ruudut[3][12]))
        self.assertFalse(kartta.nakyvyys(ruudut[5][1], ruudut[12][15]))
        self.assertFalse(kartta.nakyvyys(ruudut[3][13], ruudut[15][12]))
        self.assertFalse(kartta.nakyvyys(ruudut[19][5], ruudut[15][11]))
        self.assertFalse(kartta.nakyvyys(ruudut[13][3], ruudut[11][11]))
        self.assertFalse(kartta.nakyvyys(ruudut[19][6], ruudut[2][3]))

if __name__ == "__main__":
    unittest.main()
