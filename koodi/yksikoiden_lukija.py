import os

from yksikon_ominaisuudet import Yksikon_ominaisuudet

class Yksikoiden_lukija:

    def __init__(self):
        self.__yksikot = {}  # sanakirja, johon lisätään yksiköt (avain = yksikön nimi)
        tiedostot = os.scandir('yksikot/')

        # lukee jokaisesta tiedostosta yksikön tiedot
        # tietojen järjestyksellä ei ole väliä

        for tiedosto in tiedostot:
            lue = open(tiedosto, 'r')
            tyyppi = ""
            liikkumispisteet = 0
            max_elama = 0
            max_energia = 0
            hyokkays = 0
            puolustus = 0
            kantama = 0
            hinta = 0
            for rivi in lue:
                rivi = rivi.rstrip()
                rivi = rivi.split(':')
                i = 0
                while i < len(rivi):
                    rivi[i] = rivi[i].strip()
                    i += 1
                if rivi[0] == "TYYPPI":
                    tyyppi = rivi[1]
                elif rivi[0] == "LIIKKUMISPISTEET":
                    liikkumispisteet = int(rivi[1])
                elif rivi[0] == "MAKSIMIELAMA":
                    max_elama = int(rivi[1])
                elif rivi[0] == "MAKSIMIENERGIA":
                    max_energia = int(rivi[1])
                elif rivi[0] == "HYOKKAYS":
                    hyokkays = int(rivi[1])
                elif rivi[0] == "PUOLUSTUS":
                    puolustus = int(rivi[1])
                elif rivi[0] == "KANTAMA":
                    kantama = int(rivi[1])
                elif rivi[0] == "PISTEHINTA":
                    hinta = int(rivi[1])
                elif rivi[0] == "LOPPU":
                    break

            # luo uuden maasto-instanssin, johon tiedot säilötään
            # luotu maasto lisätään sanakirjaan, josta se voiddan myöhemmin lukea
            yksikko = Yksikon_ominaisuudet(tyyppi, liikkumispisteet, max_elama, max_elama, max_energia, max_energia,
                                           hyokkays, puolustus, kantama, hinta, [])
            self.__yksikot[tyyppi.lower()] = yksikko
            lue.close()  # muista sulkea aina

    @property
    def yksikot(self):
        return self.__yksikot
