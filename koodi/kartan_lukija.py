import os
from koordinaatit import Koordinaatit

class Kartan_lukija:

    def __init__(self, paavalikko=None):
        self.__kartat = {}  # sanakirja, johon lisätään validit kartat (avain = kartan nimi)
        self.__paavalikko = paavalikko
        '''
        tallentaa lukemansa tiedot kaksiulotteiseen listaan (ruuduista), jossa
        jokainen jäsen on maaston tyyppi
        
        toinen lista yksiköistä 
        '''

    @property
    def kartat(self):
        return self.__kartat

    def lue_kaikki_kartat(self):
        tiedostot = os.scandir('kartat/')
        for kartta in tiedostot:
            try:
                kartan_nimi, x, y, ruudut, yksikot_sanakirja = self.lue_kartta(kartta.name)
                if kartan_nimi is not False:
                    self.__kartat[kartta.name] = (x, y, ruudut, yksikot_sanakirja)
                else:
                    if self.__paavalikko is not None:
                        self.__paavalikko.lisaa_virheellinen_kartta(kartta.name)
            except TypeError:
                if self.__paavalikko is not None:
                    self.__paavalikko.lisaa_virheellinen_kartta(kartta.name)

    def lue_kartta(self, nimi):
        maastot = ["kukkula", "pelto", "vuoristo", "joki", "silta", "tasanko"]
        yksikkotyypit = ["jalkavaki", "ratsuvaki", "jousimiehet", "tykisto", "parantaja"]
        omistajat = ["plr", "com"]
        tiedosto = None
        try:
            kartan_nimi = ""
            ruudut = []
            yksikot_sanakirja = {}
            x = 0
            y = 0
            nimi_loydetty = False
            koko_loydetty = False
            ruudut_loydetty = False
            yksikot_loydetty = False
            tiedosto = open('kartat/' + nimi, 'r')
            for rivi in tiedosto:
                rivi = rivi.lower()
                rivi = rivi.rstrip()
                rivi = rivi.split(':')
                i = 0
                while i < len(rivi):
                    rivi[i] = rivi[i].strip()
                    i += 1
                if rivi[0] == "nimi":
                    nimi = rivi[1]
                    nimi_loydetty = True
                elif rivi[0] == "koko":     #koko tulee olla ennen  ruutuja
                    rivi[1] = rivi[1].split('*')
                    x = int(rivi[1][0])
                    y = int(rivi[1][1])
                    if x <= 0 or y <= 0:
                        if tiedosto is not None and not tiedosto.closed:
                            tiedosto.close()
                        return False, 0, 0, None, None
                    koko_loydetty = True
                    ruudut = [["tasanko" for i in range(y)] for j in range(x)]
                elif rivi[0] == "ruudut":
                    koordinaatit = tiedosto.readline()
                    koordinaatit = koordinaatit.lower()
                    koordinaatit = koordinaatit.split(':')
                    while koordinaatit[0] != "ruudutloppu":
                        # lukee ruudut, jotka on annettu listana ja lisää ne annettuun kaksiulotteiseen listaan ja palauttaa sen
                        tyyppi = koordinaatit[0].lower()
                        # tyypin validiuden tarkistus
                        if tyyppi not in maastot:
                            if tiedosto is not None and not tiedosto.closed:
                                tiedosto.close()
                            return False, 0, 0, None, None
                        i = 1
                        while i < len(koordinaatit):
                            koordinaatit[i] = koordinaatit[i].strip()
                            koordinaatit[i] = koordinaatit[i].split(",")
                            koordinaatit[i][0] = int(koordinaatit[i][0]) - 1    # vähennetään 1, koska koodissa koordinaatit
                            koordinaatit[i][1] = int(koordinaatit[i][1]) - 1    # alkavat nollasta
                            if koordinaatit[i][0] < 0 or koordinaatit[i][1] < 0:
                                if tiedosto is not None and not tiedosto.closed:
                                    tiedosto.close()
                                return False, 0, 0, None, None
                            ruudut[koordinaatit[i][0]][koordinaatit[i][1]] = tyyppi  # listaan lisäys (tyyppi)
                            i += 1
                        koordinaatit = tiedosto.readline()
                        koordinaatit = koordinaatit.lower()
                        koordinaatit = koordinaatit.split(':')
                        if koordinaatit[0].strip() == "ruudutloppu":
                            ruudut_loydetty = True
                            break

                # yksiköt tallennetaan koordinaatti, omistaja -tupleina listaan, joka lisätään sanakirjaan
                elif rivi[0] == "yksikot":
                    yksikot = tiedosto.readline()
                    yksikot = yksikot.lower()
                    yksikot = yksikot.split(':')
                    while yksikot[0] != "ruudutloppu":
                        tyyppi = yksikot[0].lower()
                        # tyypin validiuden tarkistus
                        if tyyppi not in yksikkotyypit:
                            if tiedosto is not None and not tiedosto.closed:
                                tiedosto.close()
                            return False, 0, 0, None, None
                        i = 1
                        lista = []
                        while i < len(yksikot):
                            yksikot[i] = yksikot[i].strip()
                            yksikot[i] = yksikot[i].split(",")
                            yksikot[i][0] = int(yksikot[i][0]) - 1
                            yksikot[i][1] = int(yksikot[i][1]) - 1
                            if yksikot[i][0] < 0 or yksikot[i][1] < 0:
                                if tiedosto is not None and not tiedosto.closed:
                                    tiedosto.close()
                                return False, 0, 0, None, None
                            # omistajan validiuden tarkistus
                            if yksikot[i][2].lower() not in omistajat:
                                if tiedosto is not None and not tiedosto.closed:
                                    tiedosto.close()
                                return False, 0, 0, None, None
                            yksikko = (Koordinaatit(yksikot[i][0],  yksikot[i][1]), yksikot[i][2].upper())
                            lista.append(yksikko)
                            i += 1
                        yksikot_sanakirja[tyyppi] = lista
                        yksikot = tiedosto.readline()
                        yksikot = yksikot.lower()
                        yksikot = yksikot.split(':')
                        if yksikot[0].strip() == "yksikotloppu":
                            yksikot_loydetty = True
                            break
                elif rivi[0] == "loppu":
                    tiedosto.close()
                    # tietojen validiuden tarkistus
                    if not nimi_loydetty or not ruudut_loydetty or not yksikot_loydetty or not koko_loydetty:
                        return False, 0, 0, None, None
                    else:
                        return kartan_nimi, x, y, ruudut, yksikot_sanakirja
        except OSError:
            if tiedosto is not None and not tiedosto.closed:
                tiedosto.close()
            return False, 0, 0, None, None
        except ValueError:
            if tiedosto is not None and not tiedosto.closed:
                tiedosto.close()
            return False, 0, 0, None, None
        except IndexError:
            if tiedosto is not None and not tiedosto.closed:
                tiedosto.close()
            return False, 0, 0, None, None
