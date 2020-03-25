import os
from maasto import Maasto

class Maaston_lukija:

    def __init__(self):
        self._maastot = {}                   #sanakirja, johon lisätään maastot (avain = maaston nimi)
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
                rivi = rivi.rstrip()
                rivi = rivi.split(':')
                i = 0
                while i < len(rivi):
                    rivi[i] = rivi[i].strip()
                    i += 1
                if rivi[0] == "TYYPPI":
                    tyyppi = rivi[1]
                elif rivi[0] == "LIIKKUMINEN":
                    if rivi[1] == "ei":
                        liikkuminen = False
                elif rivi[0] == "LIIKKUMISEN HINTA":
                    liikkumisen_hinta = int(rivi[1])
                elif rivi[0] == "HYOKKAYSKERROIN":
                    hyokkayskerroin = float(rivi[1])
                elif rivi[0] == "PUOLUSTUSKERROIN":
                    puolustuskerroin = float(rivi[1])
                elif rivi[0] == "LAPINAKYVYYS":
                    if rivi[1] == "ei":
                        lapinakyvyys = False
                elif rivi[0] == "VARI":
                    rivi[1] = rivi[1].split(",")
                    i = 0
                    while i < len(rivi[1]):
                        rivi[1][i] = int(rivi[1][i].strip())
                        i += 1
                    vari = rivi[1]
                elif rivi[0] == "LOPPU":
                    break

            # luo uuden maasto-instanssin, johon tiedot säilötään
            # luotu maasto lisätään sanakirjaan, josta se voiddan myöhemmin lukea
            maasto = Maasto(tyyppi, liikkuminen, liikkumisen_hinta, hyokkayskerroin, puolustuskerroin,
                            vari, lapinakyvyys)
            self._maastot[tyyppi] = maasto
            lue.close() # muista sulkea aina

    @property
    def maastot(self):
        return self._maastot
