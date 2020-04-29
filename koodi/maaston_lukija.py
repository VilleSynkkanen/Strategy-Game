import os
from maasto import Maasto


class Maaston_lukija:

    def __init__(self):
        # sanakirja, johon lisätään maastot (avain = maaston nimi)
        self.__maastot = {}
        lue = None
        self.__lukeminen_onnistui = True
        self.__luettu_maara = 0
        maastotyypit = ["kukkula", "pelto", "vuoristo", "joki", "silta", "tasanko"]
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
                tyyppi_loydetty = False
                liikkuminen_loydetty = False
                liikkumisen_hinta_loydetty = False
                hyokkayskerroin_loydetty = False
                puolustuskerroin_loydetty = False
                vari_loydetty = False
                lapinakyvyys_loydetty = False
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
                        if tyyppi not in maastotyypit:
                            self.__ei_validi(lue)
                            return
                        tyyppi_loydetty = True
                    elif rivi[0] == "liikkuminen":
                        if rivi[1] == "ei":
                            liikkuminen = False
                        liikkuminen_loydetty = True
                    elif rivi[0] == "liikkumisen hinta":
                        liikkumisen_hinta = int(rivi[1])
                        if liikkumisen_hinta <= 0:
                            self.__ei_validi(lue)
                            return
                        liikkumisen_hinta_loydetty = True
                    elif rivi[0] == "hyokkayskerroin":
                        hyokkayskerroin = float(rivi[1])
                        if hyokkayskerroin <= 0:
                            self.__ei_validi(lue)
                            return
                        hyokkayskerroin_loydetty = True
                    elif rivi[0] == "puolustuskerroin":
                        puolustuskerroin = float(rivi[1])
                        if puolustuskerroin <= 0:
                            self.__ei_validi(lue)
                            return
                        puolustuskerroin_loydetty = True
                    elif rivi[0] == "lapinakyvyys":
                        if rivi[1] == "ei":
                            lapinakyvyys = False
                        lapinakyvyys_loydetty = True
                    elif rivi[0] == "vari":
                        rivi[1] = rivi[1].split(",")
                        i = 0
                        while i < len(rivi[1]):
                            rivi[1][i] = int(rivi[1][i].strip())
                            if rivi[1][i] < 0 or rivi[1][i] > 255:
                                self.__ei_validi(lue)
                                return
                            i += 1
                        vari = rivi[1]
                        vari_loydetty = True
                    elif rivi[0] == "loppu":
                        break

                # tietojen validiuden tarkistus
                if not tyyppi_loydetty or not liikkuminen_loydetty or not liikkumisen_hinta_loydetty or \
                        not hyokkayskerroin_loydetty or not puolustuskerroin_loydetty or not vari_loydetty or \
                        not lapinakyvyys_loydetty:
                    self.__ei_validi(lue)
                    return

                # luo uuden maasto-instanssin, johon tiedot säilötään
                # luotu maasto lisätään sanakirjaan, josta se voidaan myöhemmin lukea
                maasto = Maasto(tyyppi, liikkuminen, liikkumisen_hinta, hyokkayskerroin, puolustuskerroin,
                                vari, lapinakyvyys)
                self.__maastot[tyyppi] = maasto
                self.__luettu_maara += 1
                lue.close()
            # tarkistetaan, että kaikki tiedostot tulee luettua
            if self.__luettu_maara < 6:
                self.__ei_validi(lue)
        except IndexError:
            self.__ei_validi(lue)
            return
        except ValueError:
            self.__ei_validi(lue)
            return
        except OSError:
            self.__ei_validi(lue)
            return

    @property
    def maastot(self):
        return self.__maastot

    @property
    def lukeminen_onnistui(self):
        return self.__lukeminen_onnistui

    def __ei_validi(self, tiedosto):
        self.__lukeminen_onnistui = False
        if tiedosto is not None and not tiedosto.closed:
            tiedosto.close()
