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

    def maaston_pisteytys(self):
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        lukija = Yksikoiden_lukija()

        kartta.lisaa_yksikko(ruudut[1][1], "jousimiehet", lukija.yksikot["jousimiehet"], "COM")

        # pisteytetään silta < tasanko < kukkula ja tarkistetaan järjestys
        silta_p = Tekoaly.pisteyta_liikuttava_maasto(ruudut[1][1].yksikko, ruudut[4][6])
        kukkula_p = Tekoaly.pisteyta_liikuttava_maasto(ruudut[1][1].yksikko, ruudut[3][3])
        tasanko_p = Tekoaly.pisteyta_liikuttava_maasto(ruudut[1][1].yksikko, ruudut[0][0])
        self.assertGreater(kukkula_p, tasanko_p)
        self.assertGreater(tasanko_p, silta_p)

    def kohteen_lahestyminen(self):
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        lukija = Yksikoiden_lukija()

        # pisteytetään kaksi ruutua, joista toinen on lähempänä kohdetta
        kartta.lisaa_yksikko(ruudut[1][1], "jousimiehet", lukija.yksikot["jousimiehet"], "COM")
        kohderuutu = ruudut[10][10]
        kauempana_p = Tekoaly.pisteyta_kohteen_lahestyminen(ruudut[1][1].yksikko, ruudut[0][0], kohderuutu)
        lahempana_p = Tekoaly.pisteyta_kohteen_lahestyminen(ruudut[1][1].yksikko, ruudut[1][2], kohderuutu)
        self.assertGreater(lahempana_p, kauempana_p)

    def oman_yksikon_laheisyys(self):
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        lukija = Yksikoiden_lukija()

        # pisteytetään kaksi ruutua, joista toinen on lähempänä omia
        # jousimiehet tarvitsevat läheisyysbonukseen 2 läheistä yksikköä
        kartta.lisaa_yksikko(ruudut[1][1], "jousimiehet", lukija.yksikot["jousimiehet"], "COM")
        kohderuutu = ruudut[10][10]
        kauempana_p = Tekoaly.pisteyta_oman_yksikon_laheisyys(ruudut[1][1].yksikko, ruudut[1][2])
        lahempana_p = Tekoaly.pisteyta_oman_yksikon_laheisyys(ruudut[1][1].yksikko, ruudut[4][3])
        self.assertGreater(lahempana_p, kauempana_p)

    def vihollisen_valttely(self):
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        lukija = Yksikoiden_lukija()

        # pisteytetään kaksi ruutua, joista toinen on lähempänä vihollisia
        # perustuu siihen, että jousimiesten kantama on 4
        kartta.lisaa_yksikko(ruudut[13][7], "jousimiehet", lukija.yksikot["jousimiehet"], "COM")
        lahempana_p = Tekoaly.pisteyta_vihollisten_valttely(ruudut[13][7].yksikko, ruudut[13][8])
        kauempana_p = Tekoaly.pisteyta_vihollisten_valttely(ruudut[13][7].yksikko, ruudut[14][6])
        self.assertLess(lahempana_p, kauempana_p)

    def ruudun_pisteytys_vihollisen_perusteella(self):
        # vaikuttavat asiat (testataan jokainen tapaus):
        # 1. priorisoitavat tyypit
        # 2. elämän vaikutus
        # 3. puolustuksen vaikutus
        # 4. ruudun maasto
        # 5. flankkays
        # 6. kiilat
        # 7. monta yksikköä, kahdella ruudulla samat pisteet
        app = QApplication(sys.argv)
        paavalikko = Paavalikko()
        pelinojain = Pelinohjain("testikentta.txt", paavalikko)
        kartta = pelinojain.kartta
        ruudut = kartta.ruudut_koordinaateilla
        lukija = Yksikoiden_lukija()

        # tapaus 1 toisessa vaihtoehdossa tykistö lähellä, toisessa jalkaväki, molemmilla sama puolustus:
        kartta.lisaa_yksikko(ruudut[0][0], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")

        kartta.lisaa_yksikko(ruudut[2][0], "tykisto", lukija.yksikot["tykisto"], "PLR")
        kartta.lisaa_yksikko(ruudut[0][2], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")

        ruudut[2][0].yksikko.ominaisuudet.puolustus = 10
        ruudut[0][2].yksikko.ominaisuudet.puolustus = 10

        pisteet_1 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[1][0], ruudut[0][0].yksikko)
        pisteet_2 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[0][1], ruudut[0][0].yksikko)
        self.assertGreater(pisteet_1, pisteet_2)

        ruudut[2][0].yksikko.tuhoudu()
        ruudut[0][2].yksikko.tuhoudu()

        # tapaus 2: ainoa ero vihollisen elämässä
        kartta.lisaa_yksikko(ruudut[2][0], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")
        kartta.lisaa_yksikko(ruudut[0][2], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")

        ruudut[2][0].yksikko.ominaisuudet.nyk_elama = 50
        ruudut[0][2].yksikko.ominaisuudet.nyk_elama = 60

        pisteet_1 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[1][0], ruudut[0][0].yksikko)
        pisteet_2 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[0][1], ruudut[0][0].yksikko)
        self.assertGreater(pisteet_1, pisteet_2)

        # tapaus 3: toisella suurempi puolustus
        ruudut[2][0].yksikko.ominaisuudet.nyk_elama = 60
        ruudut[0][2].yksikko.ominaisuudet.nyk_elama = 60
        ruudut[2][0].yksikko.ominaisuudet.puolustus = 5
        ruudut[0][2].yksikko.ominaisuudet.puolustus = 10

        pisteet_1 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[1][0], ruudut[0][0].yksikko)
        pisteet_2 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[0][1], ruudut[0][0].yksikko)
        self.assertGreater(pisteet_1, pisteet_2)

        # tapaus 4: toisella ruudun maasto suotuisampi
        kartta.lisaa_yksikko(ruudut[2][3], "jalkavaki", lukija.yksikot["jalkavaki"], "PLR")

        ruudut[2][0].yksikko.ominaisuudet.nyk_elama = 60
        ruudut[0][2].yksikko.ominaisuudet.nyk_elama = 60
        ruudut[2][3].yksikko.ominaisuudet.nyk_elama = 60
        ruudut[2][0].yksikko.ominaisuudet.puolustus = 10
        ruudut[0][2].yksikko.ominaisuudet.puolustus = 10
        ruudut[2][3].yksikko.ominaisuudet.puolustus = 10

        pisteet_1 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[1][3], ruudut[0][0].yksikko)
        pisteet_2 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[0][1], ruudut[0][0].yksikko)
        self.assertLess(pisteet_1, pisteet_2)

        # tapaus 5: flankkays
        kartta.lisaa_yksikko(ruudut[0][3], "jalkavaki", lukija.yksikot["jalkavaki"], "COM")

        pisteet_1 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[1][0], ruudut[0][0].yksikko)
        pisteet_2 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[0][1], ruudut[0][0].yksikko)
        self.assertLess(pisteet_1, pisteet_2)

        ruudut[0][3].yksikko.tuhoudu()

        # tapaus 6: kiilat
        ruudut[0][2].luo_kiilat(1.1, 1.5)

        pisteet_1 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[1][0], ruudut[0][0].yksikko)
        pisteet_2 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[0][1], ruudut[0][0].yksikko)
        self.assertGreater(pisteet_1, pisteet_2)

        ruudut[0][2].poista_kiilat()

        # tapaus 7: kaksi yhtä hyvää vaihtoehtoa
        pisteet_1 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[1][0], ruudut[0][0].yksikko)
        pisteet_2 = Tekoaly.pisteyta_kantamalla_olevat_viholliset(ruudut[0][1], ruudut[0][0].yksikko)
        self.assertEqual(pisteet_1, pisteet_2)
