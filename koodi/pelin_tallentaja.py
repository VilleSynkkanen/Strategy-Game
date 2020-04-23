

class Pelin_tallentaja:

    def __init__(self, pelinohjain):
        self.__pelinohjain = pelinohjain

    def tallenna_peli(self):
        '''
        tallennettavat asiat:
        -kartan nimi
        -kiilat kartalla
        -yksiköt:
            -koordinaatit
            -omistaja
            -tyyppi
            -nykyinen elämä
            -nykyinen energia
            -liikkuminen käytetty
            -hyökkäys käytetty
            -hyökkäysvaikutus (jalkaväki)
            -tilavaikutukset
                -kesto
                -hyökkäys
                -puolustus
                -liikkuminen
                -verenvuoto
                -taintuminen
                -loppuvaikutus
        ei tallenneta:
        -vuorotilanne (tallennus mahdollinen vain pelaajan vuorolla)
        -muut yksikön tiedot (oletetaan, että pelaaja ei muokkaa asetustiedostoja)
        '''
        tiedosto = open("pelitilanne/pelitilanne.txt", "w")
        print(self.__pelinohjain.nimi)
        tiedosto.write("KENTAN NIMI: " + self.__pelinohjain.nimi)
        tiedosto.write("\nYKSIKOT:\n")
        kaikki_yksikot = []
        for yksikko in self.__pelinohjain.kartta.pelaajan_yksikot:
            kaikki_yksikot.append(yksikko)
        for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
            kaikki_yksikot.append(yksikko)

        # yksiköiden tallennus
        for yksikko in kaikki_yksikot:
            x = str(yksikko.ruutu.koordinaatit.x + 1)
            y = str(yksikko.ruutu.koordinaatit.y + 1)
            om = yksikko.omistaja
            tp = yksikko.__class__.__name__
            ela = str(yksikko.ominaisuudet.nyk_elama)
            ene = str(yksikko.ominaisuudet.nyk_energia)
            if yksikko.liikkuminen_kaytetty:
                liik = "kylla"
            else:
                liik = "ei"
            if yksikko.hyokkays_kaytetty:
                hyok = "kylla"
            else:
                hyok = "ei"
            tiedosto.write(x + "," + y + "," + om + "," + tp + "," + ela + "," + ene + "," + liik + "," + hyok)
            if yksikko.hyokkays_vaikutus is not None:
                self.__kirjoita_tilavaikutus(tiedosto, yksikko.hyokkays_vaikutus)
            else:
                tiedosto.write(",ei")
            for vaikutus in yksikko.ominaisuudet.tilavaikutukset:
                self.__kirjoita_tilavaikutus(tiedosto, vaikutus)
            tiedosto.write("\n")

        # kiilat
        tiedosto.write("KIILAT")
        for ruutu in self.__pelinohjain.kartta.ruudut:
            if ruutu.kiilat is not None:
                x = str(ruutu.koordinaatit.x + 1)
                y = str(ruutu.koordinaatit.y + 1)
                tiedosto.write(":" + x + "," + y)
        tiedosto.write("\n")

        tiedosto.write("LOPPU")
        tiedosto.close()
        self.__pelinohjain.kayttoliittyma.poistu_pelista()

    def __kirjoita_tilavaikutus(self, tiedosto, tilavaikutus, loppuvaikutus=False):
        if tilavaikutus.taintuminen:
            taintuminen = "kylla"
        else:
            taintuminen = "ei"
        if not loppuvaikutus:
            tiedosto.write(",")
        tiedosto.write("tilavaikutus:" + str(tilavaikutus.kesto) + "," + str(tilavaikutus.hyokkaysbonus)
                       + "," + str(tilavaikutus.puolustusbonus) + "," + str(tilavaikutus.liikkumisbonus)
                       + "," + str(tilavaikutus.verenvuoto) + "," + taintuminen)
        if tilavaikutus.loppuvaikutus is not None:
            tiedosto.write(",")
            self.__kirjoita_tilavaikutus(tiedosto, tilavaikutus.loppuvaikutus, True)
        else:
            tiedosto.write(",ei;")













