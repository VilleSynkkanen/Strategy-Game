import os
from maasto import Maasto

class Maaston_lukija:

    def __init__(self):
        self.__maastot = {}                   #sanakirja, johon lisätään maastot (avain = maaston nimi)
        lue = None
        self.__lukeminen_onnistui = True
        self.__luettu_maara = 0
        try:
            tiedostot = os.scandir('maastot/')

            # lukee jokaisesta tiedostosta maaston tiedot
            # tietojen järjestyksellä ei ole väliä

            for tiedosto in tiedostot:
                lue = open(tiedosto, 'r')
                tyyppi = ""
                liikkuminen = True
                liikkumisen_hinta = 1
                hyokkayskerroin = 1
                puolustuskerroin = 1
                vari = []
                lapinakyvyys = True
                for rivi in lue:
                    rivi = rivi.lower()
                    rivi = rivi.rstrip()
                    rivi = rivi.split(':')
                    i = 0
                    while i < len(rivi):
                        rivi[i] = rivi[i].strip()
                        i += 1
                    if rivi[0] == "tyyppi":
                        tyyppi = rivi[1]
                    elif rivi[0] == "liikkuminen":
                        if rivi[1] == "ei":
                            liikkuminen = False
                    elif rivi[0] == "liikkumisen hinta":
                        liikkumisen_hinta = int(rivi[1])
                    elif rivi[0] == "hyokkayskerroin":
                        hyokkayskerroin = float(rivi[1])
                    elif rivi[0] == "puolustuskerroin":
                        puolustuskerroin = float(rivi[1])
                    elif rivi[0] == "lapinakyvyys":
                        if rivi[1] == "ei":
                            lapinakyvyys = False
                    elif rivi[0] == "vari":
                        rivi[1] = rivi[1].split(",")
                        i = 0
                        while i < len(rivi[1]):
                            rivi[1][i] = int(rivi[1][i].strip())
                            i += 1
                        vari = rivi[1]
                    elif rivi[0] == "loppu":
                        break

                # luo uuden maasto-instanssin, johon tiedot säilötään
                # luotu maasto lisätään sanakirjaan, josta se voiddan myöhemmin lukea
                maasto = Maasto(tyyppi, liikkuminen, liikkumisen_hinta, hyokkayskerroin, puolustuskerroin,
                                vari, lapinakyvyys)
                self.__maastot[tyyppi] = maasto
                self.__luettu_maara += 1
                lue.close() # muista sulkea aina
            if self.__luettu_maara < 6:
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
    def maastot(self):
        return self.__maastot

    @property
    def lukeminen_onnistui(self):
        return self.__lukeminen_onnistui
