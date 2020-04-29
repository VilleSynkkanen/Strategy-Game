from tilavaikutus import Tilavaikutus
import os


class Pelitilanteen_lukija:

    def lue_pelitilanne(self, karttatiedot, yksikkotiedot):
        self.__lukeminen_onnistui = True
        self.__nimi_loydetty = False
        self.__yksikot_loydetty = False
        self.__kiilat_loydetty = False
        tiedosto = None
        omistajat = ["PLR", "COM"]
        tyypit = ["jalkavaki", "ratsuvaki", "jousimiehet", "tykisto", "parantaja"]
        tot_arvot = ["kylla", "ei"]
        x_koko = 0
        y_koko = 0
        try:
            tiedosto = open("pelitilanne/pelitilanne.txt", "r")
            nimi = None
            for rivi in tiedosto:
                rivi = rivi.lower()
                rivi = rivi.rstrip()
                rivi = rivi.split(":")
                if rivi[0] == "kentan nimi":
                    nimi = rivi[1].strip()
                    # nimen validius
                    validi = False
                    kartat = os.scandir('kartat/')
                    for kartta in kartat:
                        if kartta.name == nimi:
                            validi = True
                    if not validi:
                        self.__ei_validi(tiedosto)
                        return None, None, None
                    else:
                        self.__nimi_loydetty = True
                elif rivi[0] == "yksikot":
                    self.__yksikot_loydetty = True
                    # yksiköiden lukeminen
                    yksikot = []
                    rivi = tiedosto.readline()
                    rivi = rivi.lower()
                    rivi = rivi.rstrip()
                    rivi = rivi.split(",")
                    if nimi is None:
                        self.__ei_validi(tiedosto)
                        return None, None, None
                    x_koko = karttatiedot[nimi][0]
                    y_koko = karttatiedot[nimi][1]
                    while rivi[0][0] != "k":    # kiilat alkaa k:lla
                        # tietojen validiustarkastus
                        # koordinaattien täytyy olla kartan sisällä
                        if not 1 <= int(rivi[0]) <= x_koko or not 1 <= int(rivi[1]) <= y_koko:
                            self.__ei_validi(tiedosto)
                            return None, None, None
                        # omistajan täytyy olla plr tai com, yksikkötyypin täytyy olla oikae
                        if rivi[2].upper() not in omistajat or rivi[3] not in tyypit:
                            self.__ei_validi(tiedosto)
                            return None, None, None
                        # elämän ja energian täytyy olla yksikölle mahdollisissa rajoissa
                        max_elama = yksikkotiedot[rivi[3]][0].max_elama
                        max_energia = yksikkotiedot[rivi[3]][0].max_energia
                        if not 0 < int(rivi[4]) <= max_elama or not 0 <= int(rivi[5]) <= max_energia:
                            self.__ei_validi(tiedosto)
                            return None, None, None
                        # liikkumisen ja hyökkäyksen täytyy olla kyllä tai ei
                        if rivi[6] not in tot_arvot or rivi[7] not in tot_arvot:
                            self.__ei_validi(tiedosto)
                            return None, None, None
                        # hyökkäysvaikutuksen täytyy olla ei tai tilavaikutus
                        if rivi[8] != "ei":
                            uusi_rivi = rivi[8].split(":")
                            if uusi_rivi[0] != "tilavaikutus":
                                self.__ei_validi(tiedosto)
                                return None, None, None
                        #print(rivi)
                        # tallennetaan numerot tupleen
                        # x,y,omistaja,tyyppi,elämä,energia,liikkuminen,hyökkäys,taintuminen
                        yksikko = (int(rivi[0]) - 1, int(rivi[1]) - 1, rivi[2].upper(), rivi[3], int(rivi[4]), int(rivi[5]),
                                   rivi[6], rivi[7])
                        hyokkaysvaikutus = None
                        #print(yksikko)
                        if rivi[8] != "ei":
                            hyokkaysvaikutus = self.lue_vaikutus(rivi, 8)
                            if hyokkaysvaikutus is None:
                                self.__ei_validi(tiedosto)
                                return None, None, None
                            # hyökkäysvaikutuksen jälkeinen indeksi
                            i = 15
                        else:
                            # indeksi, jos hyökkäysvaikutusta ei ole
                            i = 9
                        tilavaikutukset = []
                        #print(rivi)
                        while i < len(rivi):
                            if rivi[i].split(":")[0] == "tilavaikutus":
                                tilavaikutus = self.lue_vaikutus(rivi, i)
                                if tilavaikutus is None:
                                    self.__ei_validi(tiedosto)
                                    return None, None, None
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
                        if not 0 < uusi[i] <= x_koko or not 0 < uusi[i + 1] <= y_koko:
                            self.__ei_validi(tiedosto)
                            return None, None, None
                        koord = (uusi[i] - 1, uusi[i + 1] - 1)
                        kiilat.append(koord)
                        i += 2
                    self.__kiilat_loydetty = True
                    # print(kiilat)
                    tiedosto.close()
                    if not self.__yksikot_loydetty or not self.__kiilat_loydetty or not self.__nimi_loydetty:
                        self.__ei_validi(tiedosto)
                        return None, None, None
                    return nimi, yksikot, kiilat
        except OSError:
            self.__ei_validi(tiedosto)
            return None, None, None
        except IndexError:
            self.__ei_validi(tiedosto)
            return None, None, None
        except ValueError:
            self.__ei_validi(tiedosto)
            return None, None, None
        except KeyError:
            self.__ei_validi(tiedosto)
            return None, None, None

    def lue_vaikutus(self, rivi, i):
        try:
            tot_arvot = ["kylla", "ei"]
            #print(rivi[i])
            rivi[i] = rivi[i].split(":")[1]
            # vaikutuksen validiuden tarkistus
            # kesto, hyokkays, puolustus, liikkuminen, verenvuoto, taintuminen, loppuvaikutus
            if int(rivi[i]) <= 0 or int(rivi[i + 4]) < 0 or rivi[i + 5].strip(";") not in tot_arvot:
                return None
            vaikutus = rivi[i + 6].split(":")
            if vaikutus[0] != "ei;" and vaikutus[0] != "tilavaikutus":
                return None
            taintuminen = False
            if rivi[i + 5].strip(";") == "kylla":
                taintuminen = True
            loppuvaikutus = None
            if rivi[i + 6].strip(";") != "ei":
                loppuvaikutus = self.lue_vaikutus(rivi, i + 6)
            tilavaikutus = Tilavaikutus(None, int(rivi[i]), int(rivi[i + 1]), int(rivi[i + 2]),
                                        int(rivi[i + 3]), int(rivi[i + 4]), taintuminen, loppuvaikutus)
            return tilavaikutus
        except ValueError:
            return None
        except IndexError:
            return None

    def __ei_validi(self, tiedosto):
        self.__lukeminen_onnistui = False
        if tiedosto is not None and not tiedosto.closed:
            tiedosto.close()

    @property
    def lukeminen_onnistui(self):
        return self.__lukeminen_onnistui
