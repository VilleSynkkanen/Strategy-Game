import os

from yksikon_ominaisuudet import Yksikon_ominaisuudet

class Yksikoiden_lukija:

    def __init__(self):
        self.__yksikot = {}  # sanakirja, johon lisätään yksiköt (avain = yksikön nimi)
        lue = None
        self.__lukeminen_onnistui = True
        self.__luettu_maara = 0
        try:
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
                kyvyt = {}
                for rivi in lue:
                    rivi = rivi.lower()
                    print(rivi)
                    rivi = rivi.rstrip()
                    rivi = rivi.split(':')
                    i = 0
                    while i < len(rivi):
                        rivi[i] = rivi[i].strip()
                        i += 1
                    if rivi[0] == "tyyppi":
                        tyyppi = rivi[1]
                    elif rivi[0] == "liikkumispisteet":
                        liikkumispisteet = int(rivi[1])
                    elif rivi[0] == "maksimielama":
                        max_elama = int(rivi[1])
                    elif rivi[0] == "maksimienergia":
                        max_energia = int(rivi[1])
                    elif rivi[0] == "hyokkays":
                        hyokkays = int(rivi[1])
                    elif rivi[0] == "puolustus":
                        puolustus = int(rivi[1])
                    elif rivi[0] == "kantama":
                        kantama = int(rivi[1])
                    elif rivi[0] == "pistehinta":
                        hinta = int(rivi[1])
                    elif rivi[0] == "kyvyt":
                        # jokaisella tyypillä eri kykyihin liittyvät muuttujat, joten käytetään eri metodeita lukemiseen
                        # numerot tallennetaan sanakirjaan
                        kyvyt = self.__lue_kyvyt(lue)
                        if kyvyt is False:
                            self.__lukeminen_onnistui = False
                            lue.close()
                            return
                    elif rivi[0] == "loppu":
                        break

                # luo uuden yksikkö-instanssin, johon tiedot säilötään
                # luotu yksikkö lisätään sanakirjaan, josta se voiddan myöhemmin lukea
                # instanssi on tuple, jossa 1. jäsen on ominaisuudet-instanssi ja toinen kyvyt-sanakirja
                yksikko = (Yksikon_ominaisuudet(tyyppi, liikkumispisteet, max_elama, max_elama, max_energia, max_energia,
                                               hyokkays, puolustus, kantama, hinta, []), kyvyt)
                self.__yksikot[tyyppi.lower()] = yksikko
                self.__luettu_maara += 1
                lue.close()  # muista sulkea aina

            print(self.__luettu_maara)
            if self.__luettu_maara < 5:
                self.__lukeminen_onnistui = False

        except IndexError:
            self.__lukeminen_onnistui = False
            if lue is not None and not lue.closed:
                lue.close()
            return
        except ValueError:
            self.__lukeminen_onnistui = False
            if lue is not None and not lue.closed:
                lue.close()
            return
        except OSError:
            self.__lukeminen_onnistui = False
            if lue is not None and not lue.closed:
                lue.close()
            return

    @property
    def yksikot(self):
        return self.__yksikot

    @property
    def lukeminen_onnistui(self):
        return self.__lukeminen_onnistui

    def __lue_kyvyt(self, tiedosto):
        try:
            kyvyt = {}
            rivi = tiedosto.readline()
            rivi = rivi.lower()
            rivi = rivi.rstrip()
            rivi = rivi.split(':')
            while rivi[0] != "loppu":
                kyvyt[rivi[0]] = float(rivi[1])
                rivi = tiedosto.readline()
                rivi = rivi.lower()
                rivi = rivi.rstrip()
                rivi = rivi.split(':')
            return kyvyt
        except ValueError:
            return False
