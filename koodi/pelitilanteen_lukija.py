from tilavaikutus import Tilavaikutus


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
                while rivi[0] != "kiilat":
                    #print(rivi)
                    # tallennetaan numerot tupleen
                    # x,y,omistaja,tyyppi,elämä,energia,liikkuminen,hyökkäys,taintuminen
                    yksikko = (int(rivi[0]) - 1, int(rivi[1]) - 1, rivi[2].upper(), rivi[3], int(rivi[4]), int(rivi[5]),
                               rivi[6], rivi[7])
                    hyokkaysvaikutus = None
                    #print(yksikko)
                    if rivi[8] != "ei":
                        rivi[8] = rivi[8].split(":")[1]  # muutetaan tilavaikutuksen ensimmäinen alkio pelkäksi kestoksi
                        taintuminen = False
                        if rivi[13].strip(";") == "kylla":
                            taintuminen = True
                        hyokkaysvaikutus = Tilavaikutus(None, int(rivi[8]), int(rivi[9]), int(rivi[10]), int(rivi[11]),
                                                        int(rivi[12]), taintuminen, None)  # ei impl loppuvaikutusta
                        # hyökkäysvaikutuksen jälkeinen indeksi
                        i = 15
                    else:
                        # indeksi, jos hyökkäysvaikutusta ei ole
                        i = 9
                    tilavaikutukset = []
                    while i < len(rivi):
                        if rivi[i].split(":")[0] == "tilavaikutus":
                            rivi[i] = rivi[i].split(":")[1]
                            taintuminen = False
                            if rivi[i + 6].strip(";") == "kylla":
                                taintuminen = True
                            tilavaikutus = Tilavaikutus(None, int(rivi[i]), int(rivi[i+1]), int(rivi[i+2]),
                                                            int(rivi[i+3]),int(rivi[i+4]), taintuminen, None)
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
                tiedosto.close()
                return nimi, yksikot
