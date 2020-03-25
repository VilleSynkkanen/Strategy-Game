import os
from koordinaatit import Koordinaatit

class Kartan_lukija:

    def __init__(self):
        self.__kartat = {}  # sanakirja, johon lisätään validit kartat (avain = kartan nimi)
        '''
        tallentaa lukemansa tiedot kaksiulotteiseen listaan (ruuduista), jossa
        jokainen jäsen on maaston tyyppi
        
        toinen lista yksiköistä 
        '''

    @property
    def kartat(self):
        return self.__kartat

    def lue_kartta(self, nimi):
        kartan_nimi = ""
        ruudut = []
        yksikot_sanakirja = {}
        x = 0
        y = 0
        tiedosto = open('kartat/' + nimi, 'r')
        for rivi in tiedosto:
            rivi = rivi.rstrip()
            rivi = rivi.split(':')
            i = 0
            while i < len(rivi):
                rivi[i] = rivi[i].strip()
                i += 1
            if rivi[0] == "NIMI":
                nimi = rivi[1]
            elif rivi[0] == "KOKO":     #koko tulee olla ennen  ruutuja
                rivi[1] = rivi[1].split('*')
                x = int(rivi[1][0])
                y = int(rivi[1][1])
                ruudut = [["tasanko" for i in range(y)] for j in range(x)]
            elif rivi[0] == "RUUDUT":
                koordinaatit = tiedosto.readline()
                koordinaatit = koordinaatit.split(':')
                while koordinaatit[0] != "RUUDUTLOPPU":
                    # lukee ruudut, jotka on annettu listana ja lisää ne annettuun kaksiulotteiseen listaan ja palauttaa sen
                    tyyppi = koordinaatit[0].lower()
                    i = 1
                    while i < len(koordinaatit):
                        koordinaatit[i] = koordinaatit[i].strip()
                        koordinaatit[i] = koordinaatit[i].split(",")
                        koordinaatit[i][0] = int(koordinaatit[i][0]) - 1    # vähennetään 1, koska koodissa koordinaatit
                        koordinaatit[i][1] = int(koordinaatit[i][1]) - 1    # alkavat nollasta
                        ruudut[koordinaatit[i][0]][koordinaatit[i][1]] = tyyppi  # listaan lisäys (tyyppi)
                        i += 1
                    koordinaatit = tiedosto.readline()
                    koordinaatit = koordinaatit.split(':')
                    if koordinaatit[0].strip() == "RUUDUTLOPPU":
                        break

            # yksiköt tallennetaan koordinaatti, omistaja -tupleina listaan, joka lisätään sanakirjaan
            elif rivi[0] == "YKSIKOT":
                yksikot = tiedosto.readline()
                yksikot = yksikot.split(':')
                while yksikot[0] != "RUUDUTLOPPU":
                    tyyppi = yksikot[0].lower()
                    i = 1
                    lista = []
                    while i < len(yksikot):
                        yksikot[i] = yksikot[i].strip()
                        yksikot[i] = yksikot[i].split(",")
                        yksikot[i][0] = int(yksikot[i][0]) - 1
                        yksikot[i][1] = int(yksikot[i][1]) - 1
                        yksikko = (Koordinaatit(yksikot[i][0],  yksikot[i][1]), yksikot[i][2])
                        lista.append(yksikko)
                        i += 1
                    yksikot_sanakirja[tyyppi] = lista
                    yksikot = tiedosto.readline()
                    yksikot = yksikot.split(':')
                    if yksikot[0].strip() == "YKSIKOTLOPPU":
                        break
            elif rivi[0] == "LOPPU":
                tiedosto.close()
                return kartan_nimi, x, y, ruudut, yksikot_sanakirja
