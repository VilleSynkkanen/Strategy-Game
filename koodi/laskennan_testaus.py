import unittest
from pelinohjain import Pelinohjain
import sys
from PyQt5.QtWidgets import QApplication


class Laskennan_testaus(unittest.TestCase):

    '''
    testataan ohjelman eri laskennallisia osioita
    -vahingon laskenta eri tilanteissa (eri maastot, kiilat tms.)
    -tilavaikutusten vaikutus + käsittely
    -vahingon ottaminen
    -parannus
    '''


    def vahingon_laskenta_testi(self):
        global app
        app = QApplication(sys.argv)
        pelinojain = Pelinohjain()

    def tilavaikutukset_testi(self):
        global app
        app = QApplication(sys.argv)
        pelinojain = Pelinohjain()

    def vahingon_ottaminen_testi(self):
        global app
        app = QApplication(sys.argv)
        pelinojain = Pelinohjain()

    def parannus_testi(self):
        global app
        app = QApplication(sys.argv)
        pelinojain = Pelinohjain()


if __name__ == "__main__":
    unittest.main()
