from tilavaikutus import Tilavaikutus
import re


class Pelitilanteen_lukija:

    def lue_pelitilanne(self):
        tiedosto = open("pelitilanne/pelitilanne.txt", "r")
        nimi = None
        for rivi in tiedosto:
            rivi = rivi.lower()
            rivi = rivi.rstrip()
            rivi = rivi.split(":")
            if rivi[0] == "kentan nimi":
                nimi = rivi[1].strip()
            elif rivi[0] == "yksikot":
                # yksiköiden lukeminen
                yksikot = []
                rivi = tiedosto.readline()
                rivi = rivi.lower()
                rivi = rivi.rstrip()
                rivi = rivi.split(",")
                while rivi[0][0] != "k":    # kiilat alkaa k:lla
                    #print(rivi)
                    # tallennetaan numerot tupleen
                    # x,y,omistaja,tyyppi,elämä,energia,liikkuminen,hyökkäys,taintuminen
                    yksikko = (int(rivi[0]) - 1, int(rivi[1]) - 1, rivi[2].upper(), rivi[3], int(rivi[4]), int(rivi[5]),
                               rivi[6], rivi[7])
                    hyokkaysvaikutus = None
                    #print(yksikko)
                    if rivi[8] != "ei":
                        rivi[8] = rivi[8].split(":")[1]  # muutetaan tilavaikutuksen ensimmäinen alkio pelkäksi kestoksi
                        hyokkaysvaikutus = self.lue_vaikutus(rivi, 8)
                        # hyökkäysvaikutuksen jälkeinen indeksi
                        i = 15
                    else:
                        # indeksi, jos hyökkäysvaikutusta ei ole
                        i = 9
                    tilavaikutukset = []
                    print(rivi)
                    while i < len(rivi):
                        if rivi[i].split(":")[0] == "tilavaikutus":
                            tilavaikutus = self.lue_vaikutus(rivi, i)
                            tilavaikutukset.append(tilavaikutus)
                            i += 7
                        else:
                            break
                    tiedot = (yksikko, hyokkaysvaikutus, tilavaikutukset)
                    yksikot.append(tiedot)
                    rivi = tiedosto.readline()
                    rivi = rivi.lower()
                    rivi = rivi.rstrip()
                    rivi = rivi.split(",")
                # kiilojen lukeminen
                uusi = []
                for elem in rivi:
                    elem = elem.split(":")
                    for alkio in elem:
                        if alkio != "kiilat":
                            uusi.append(int(alkio))
                kiilat = []
                i = 0
                while i + 1 < len(uusi):
                    koord = (uusi[i], uusi[i + 1])
                    kiilat.append(koord)
                    i += 2
                print(kiilat)

                tiedosto.close()
                return nimi, yksikot, kiilat

    def lue_vaikutus(self, rivi, i):
        rivi[i] = rivi[i].split(":")[1]
        taintuminen = False
        if rivi[i + 5].strip(";") == "kylla":
            taintuminen = True
        loppuvaikutus = None
        if rivi[i + 6].strip(";") != "ei":
            loppuvaikutus = self.lue_vaikutus(rivi, i + 6)
        tilavaikutus = Tilavaikutus(None, int(rivi[i]), int(rivi[i + 1]), int(rivi[i + 2]),
                                    int(rivi[i + 3]), int(rivi[i + 4]), taintuminen, loppuvaikutus)
        return tilavaikutus
