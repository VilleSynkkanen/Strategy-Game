import unittest
from pelinohjain import Pelinohjain
from paavalikko import Paavalikko
from yksikoiden_lukija import Yksikoiden_lukija
import sys
from PyQt5.QtWidgets import QApplication
from yksikon_ominaisuudet import Yksikon_ominaisuudet
from yksikko import Yksikko
from random import randrange
from tilavaikutus import Tilavaikutus

class Laskennan_testaus(unittest.TestCase):

    '''
    testataan ohjelman eri laskennallisia osioita
    -vahingon laskenta eri tilanteissa (eri maastot, kiilat, kantamat tms.)
    -tilavaikutusten vaikutus + käsittely
    -vahingon ottaminen
    -parannus
    '''

    def vahingon_laskenta_testi(self):
        global app
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        lukija = Yksikoiden_lukija()

        # lisätään yksiköitä siten, että tulee muutama blokattu paikka
        kartta.lisaa_yksikko(ruudut[9][10], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")
        kartta.lisaa_yksikko(ruudut[7][9], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")
        kartta.lisaa_yksikko(ruudut[15][12], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")
        kartta.lisaa_yksikko(ruudut[6][4], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")

        # tyyppi, liikkuminen, max_elama, nyk_elama, max_energia, nyk_energia, hyokkays, puolustus,
        # kantama, hinta, tilavaikutukset

        # luodaan kaksi jalkaväkeä (pelaaja ja tietokone),
        # tietokone: hyökkäys, puolustus, kantama = 10
        # pelaaja: hyökkäys, puolustus, kantama = 8
        ominaisuudet_tiet = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 100, 10, 10, 10, 10, 10, 10, None)
        ominaisuudet_pel = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 100, 8, 8, 8, 8, 8, 8, None)

        # tilanne 1: molemmat tasangolla, vierekkäin
        tie = ruudut[13][6]
        pel = ruudut[13][7]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(tiet_yks, pel_yks)

        # tilanne 2: toinen kukkulalla, toinen tasangolla
        tie = ruudut[2][3]
        pel = ruudut[1][3]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(pel_yks, tiet_yks)

        # 3: toinen sillalla, toinen tasangolla
        tie = ruudut[8][6]
        pel = ruudut[8][7]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(tiet_yks, pel_yks)

        # 4: molemmat pellolla
        tie = ruudut[2][9]
        pel = ruudut[2][10]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(pel_yks, tiet_yks)

        # 5: toinen vuoristossa, toinen tasangolla
        tie = ruudut[16][6]
        pel = ruudut[16][7]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(pel_yks, tiet_yks)

        # 6: toinen kiiloissa, molemmat tasangolla
        tie = ruudut[15][14]
        pel = ruudut[16][14]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        pel.luo_kiilat(1.15, 1.5)
        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(tiet_yks, pel_yks)

        # 7: flank, molemmat vuoristossa
        tie = ruudut[18][6]
        pel = ruudut[17][6]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(tiet_yks, pel_yks)

        # 8: pidempi kantama, molemmat tasangolla
        tie = ruudut[0][15]
        pel = ruudut[3][15]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(pel_yks, tiet_yks)

        # 9: minimi ja maksimi testaus, molemmat tasangolla
        ominaisuudet_tiet = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 100, 100, 100, 100, 100, 100, 100, None)
        ominaisuudet_pel = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 100, 2, 2, 2, 2, 2, 2, None)

        tie = ruudut[0][5]
        pel = ruudut[0][4]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(tiet_yks, pel_yks)

        # 10: vajaa elämä molemmilla
        ominaisuudet_tiet = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 50, 10, 10, 10, 10, 10, 10, None)
        ominaisuudet_pel = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 70, 8, 8, 8, 8, 8, 8, None)

        tie = ruudut[7][15]
        pel = ruudut[8][15]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(pel_yks, tiet_yks)

        # 11: vajaa elämä toisella
        ominaisuudet_tiet = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 50, 10, 10, 10, 10, 10, 10, None)
        ominaisuudet_pel = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 100, 8, 8, 8, 8, 8, 8, None)

        tie = ruudut[0][0]
        pel = ruudut[0][1]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko
        self.vahingon_laskenta(pel_yks, tiet_yks)

        # 12: molemmat tasangolla, satunnaisuuden testaus (monta kertaa), muuten tilanne 1
        ominaisuudet_tiet = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 100, 10, 10, 10, 10, 10, 10, None)
        ominaisuudet_pel = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 100, 8, 8, 8, 8, 8, 8, None)

        tie = ruudut[13][6]
        pel = ruudut[13][7]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko

        i = 0
        # 1000 toistoa
        while i < 1000:
            i += 1
            self.vahingon_laskenta(tiet_yks, pel_yks, False)

    def tilavaikutukset_testi(self):
        # testataan, muuttaako tilavaikutus ominaisuuksia odotetusti ja loppuuko se oikeaan aikaan
        global app
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        lukija = Yksikoiden_lukija()

        ominaisuudet = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 100, 10, 10, 10, 10, 10, 10, None)
        kartta.lisaa_yksikko(ruudut[0][0], "jalkavaki", (ominaisuudet, lukija.yksikot["jalkavaki"][1]), "COM")

        yksikko = ruudut[0][0].yksikko
        om = yksikko.ominaisuudet

        # kesto, hyokkays, puolustus, liikkuminen, verenvuoto, taintuminen, loppuvaikutus=None
        loppuvaikutus = Tilavaikutus(None, 1, 0, 0, 0, 0, True)
        yksikko.lisaa_tilavaikutus(2, 2, -2, 1, 2, False, loppuvaikutus)

        # ominaisuudet heti tilavaikutuksen lisäämisen jäkeen
        self.assertEqual(om.hyokkays, 10 + 2)
        self.assertEqual(om.puolustus, 10 - 2)
        self.assertEqual(om.liikkuminen, 1 + 1)
        self.assertFalse(yksikko.onko_taintunut())
        self.assertEqual(om.nyk_elama, 100)

        # ensimmäisen käsittelyn jälkeen
        yksikko.kasittele_tilavaikutukset()
        self.assertEqual(om.hyokkays, 10 + 2)
        self.assertEqual(om.puolustus, 10 - 2)
        self.assertEqual(om.liikkuminen, 1 + 1)
        self.assertFalse(yksikko.onko_taintunut())
        self.assertEqual(om.nyk_elama, 98)

        # toisen käsittelyn jälkeen (loppuvaikutus tulee voimaan, edellinen poistuu)
        yksikko.kasittele_tilavaikutukset()
        self.assertEqual(om.hyokkays, 10)
        self.assertEqual(om.puolustus, 10)
        self.assertEqual(om.liikkuminen, 1)
        self.assertTrue(yksikko.onko_taintunut())
        self.assertEqual(om.nyk_elama, 96)

        # kolmannen käsittelyn jälkeen (kaikki vaikutukset poistuneet)
        yksikko.kasittele_tilavaikutukset()
        self.assertEqual(om.hyokkays, 10)
        self.assertEqual(om.puolustus, 10)
        self.assertEqual(om.liikkuminen, 1)
        self.assertFalse(yksikko.onko_taintunut())
        self.assertEqual(om.nyk_elama, 96)

    def vahingon_ottaminen_testi(self):
        global app
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        lukija = Yksikoiden_lukija()

        # yksinkertainen ota_vahinkoa-metodin testi
        # 2 tilannetta: yksikkö kuolee/ei kuole

        vahinko = 50

        ominaisuudet_tiet = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 50, 10, 10, 10, 10, 10, 10, None)
        ominaisuudet_pel = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 99, 8, 8, 8, 8, 8, 8, None)

        tie = ruudut[0][0]
        pel = ruudut[0][1]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")

        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko

        tiet_yks.ota_vahinkoa(vahinko)

        # tuhoutunut, jos ominaisuudet on none
        self.assertIsNone(tiet_yks.ominaisuudet)

        pel_yks.ota_vahinkoa(vahinko)
        self.assertEqual(pel_yks.ominaisuudet.nyk_elama, 99 - vahinko)

    def parannus_testi(self):
        global app
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        lukija = Yksikoiden_lukija()

        # yksinkertainen parannus-metodin testi
        # 2 tilannetta: menee yli/ei mene yli

        parannus = 10

        ominaisuudet_tiet = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 50, 10, 10, 10, 10, 10, 10, None)
        ominaisuudet_pel = Yksikon_ominaisuudet("Jalkavaki", 1, 100, 99, 8, 8, 8, 8, 8, 8, None)

        tie = ruudut[0][0]
        pel = ruudut[0][1]
        kartta.lisaa_yksikko(tie, "jalkavaki", (ominaisuudet_tiet, lukija.yksikot["jalkavaki"][1]), "COM")
        kartta.lisaa_yksikko(pel, "jalkavaki", (ominaisuudet_pel, lukija.yksikot["jalkavaki"][1]), "PLR")
        tiet_yks = tie.yksikko
        pel_yks = pel.yksikko

        tiet_yks.parannu(parannus)
        self.assertEqual(tiet_yks.ominaisuudet.nyk_elama, 50 + parannus)
        pel_yks.parannu(parannus)
        self.assertEqual(pel_yks.ominaisuudet.nyk_elama, pel_yks.ominaisuudet.max_elama)

    def vahingon_laskenta(self, hyokkaaja, puolustaja, odotettu=True):
        # perustuu tällä hetkellä kovakoodattuihin arvoihin
        # voi joutua muuttamaan myöhemmin
        perusvahinko = 10
        min_vahinko = 2
        max_vahinko = 40
        satunnaisuuskerroin = 0.15
        flanking_kerroin = 1.15

        # saadut arvot
        if odotettu:
            odotettu_hyok, odotettu_puol, flank = Yksikko.laske_vahinko(hyokkaaja, puolustaja, odotettu)
        else:
            odotettu_hyok, odotettu_puol = Yksikko.laske_vahinko(hyokkaaja, puolustaja, odotettu)

        # halutut arvot
        hyok = hyokkaaja.ominaisuudet.hyokkays * hyokkaaja.ruutu.maasto.hyokkayskerroin * \
                   (0.5 * (hyokkaaja.ominaisuudet.nyk_elama / hyokkaaja.ominaisuudet.max_elama) + 0.5)
        puol = puolustaja.ominaisuudet.puolustus * puolustaja.ruutu.maasto.puolustuskerroin * \
                    (0.5 * (puolustaja.ominaisuudet.nyk_elama / puolustaja.ominaisuudet.max_elama) + 0.5)
        etaisyys = puolustaja.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(puolustaja.ruutu, hyokkaaja.ruutu)

        flanking = False
        if etaisyys == 1:
            flanking = puolustaja.vieressa_monta_vihollista()
        if flanking:
            hyok *= flanking_kerroin

        if puolustaja.ruutu.kiilat is not None:
            if hyokkaaja.__class__.__name__ == "Ratsuvaki":
                puol *= puolustaja.ruutu.kiilat.puolustusbonus_ratsuvaki
            else:
                puol *= puolustaja.ruutu.kiilat.puolustusbonus

        if etaisyys == 1:
            hyokkaajan_vahinko = (puol / hyok) * perusvahinko
            if hyokkaajan_vahinko < min_vahinko:
                hyokkaajan_vahinko = min_vahinko
            elif hyokkaajan_vahinko > max_vahinko:
                hyokkaajan_vahinko = max_vahinko
        else:
            hyokkaajan_vahinko = 0

        puolustajan_vahinko = (hyok / puol) * perusvahinko
        if puolustajan_vahinko < min_vahinko:
            puolustajan_vahinko = min_vahinko
        elif puolustajan_vahinko > max_vahinko:
            puolustajan_vahinko = max_vahinko

        if not odotettu:
            # satunnaisuustestaus
            hyokkaajan_vahinko_min = int(hyokkaajan_vahinko * (1 - satunnaisuuskerroin))
            hyokkaajan_vahinko_max = int(hyokkaajan_vahinko * (1 + satunnaisuuskerroin))

            puolustajan_vahinko_min = int(puolustajan_vahinko * (1 - satunnaisuuskerroin))
            puolustajan_vahinko_max = int(puolustajan_vahinko * (1 + satunnaisuuskerroin))

            hyokkaajan_vahinko = randrange(hyokkaajan_vahinko_min, hyokkaajan_vahinko_max + 1, 1)
            puolustajan_vahinko = randrange(puolustajan_vahinko_min, puolustajan_vahinko_max + 1, 1)

            self.assertGreaterEqual(int(odotettu_hyok), hyokkaajan_vahinko_min)
            self.assertLessEqual(int(odotettu_hyok), hyokkaajan_vahinko_max)
            self.assertGreaterEqual(int(odotettu_puol), puolustajan_vahinko_min)
            self.assertLessEqual(int(odotettu_puol), puolustajan_vahinko_max)
        else:
            self.assertEqual(flanking, flank)
            self.assertEqual(int(odotettu_hyok), int(hyokkaajan_vahinko))
            self.assertEqual(int(odotettu_puol), int(puolustajan_vahinko))


if __name__ == "__main__":
    unittest.main()
