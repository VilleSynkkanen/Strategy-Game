import os

class Kentan_tallentaja:

    @staticmethod
    def tallenna_kentta(kartta, nimi, tallenna_paalle=False):
        validi_nimi = Kentan_tallentaja.tarkista_nimi(nimi)
        if not validi_nimi and tallenna_paalle is False:
            return False
        else:
            '''
            tallennettavat asiat:
            -nimi
            -koko (lue ruudut koordinaateilla-listasta)
            -ruudut (lue ruuduista ja lajittele)
            -yksiköt: lue yksiköistä tyyppi kerrallaan (lisää yhteen listaan ja lajittele)
            '''
            tied_nimi = nimi + ".txt"
            tiedosto = open("kartat/" + tied_nimi, "w")
            x = len(kartta.ruudut_koordinaateilla)
            y = len(kartta.ruudut_koordinaateilla[0])
            print(x, y)
            tiedosto.write("NIMI: " + nimi + "\n")
            tiedosto.write("KOKO: " + str(x) + "*" + str(y) + "\n")
            tiedosto.write("RUUDUT:")
            ruudut = Kentan_tallentaja.lajittele_ruudut(kartta.ruudut)
            ruututyyppi = " "
            for ruutu in ruudut:
                if ruututyyppi == ruutu.tyyppi:
                    tiedosto.write(" : "
                                   + str(ruutu.koordinaatit.x + 1) + "," + str(ruutu.koordinaatit.y + 1))
                else:
                    tiedosto.write("\n" + ruutu.tyyppi + ": "
                                   + str(ruutu.koordinaatit.x + 1) + "," + str(ruutu.koordinaatit.y + 1))
                    ruututyyppi = ruutu.tyyppi
            tiedosto.write("\nRUUDUTLOPPU\n")
            tiedosto.write("YKSIKOT:")
            yksikot = Kentan_tallentaja.lajittele_yksikot(kartta.pelaajan_yksikot, kartta.tietokoneen_yksikot)
            yksikkotyyppi = " "
            for yksikko in yksikot:
                if yksikkotyyppi == yksikko.__class__.__name__.lower():
                    tiedosto.write(" : "
                                   + str(yksikko.ruutu.koordinaatit.x + 1) + "," + str(yksikko.ruutu.koordinaatit.y + 1) +
                                   "," + yksikko.omistaja)
                else:
                    tiedosto.write("\n" + yksikko.__class__.__name__.lower() + ": "
                                   + str(yksikko.ruutu.koordinaatit.x + 1) + "," + str(yksikko.ruutu.koordinaatit.y + 1) +
                                   "," + yksikko.omistaja)
                    yksikkotyyppi = yksikko.__class__.__name__.lower()
            tiedosto.write("\nYKSIKOTLOPPU\n")
            tiedosto.write("LOPPU")
            tiedosto.close()
            return True

    @staticmethod
    def tarkista_nimi(nimi):
        tiedostot = os.scandir('kartat/')
        nimi += ".txt"
        for tiedosto in tiedostot:
            if tiedosto.name == nimi:
                return False
        return True

    @staticmethod
    def lajittele_ruudut(ruudut):
        # lajittelee kaikki ruudut, jotka eivät ole tasankoja
        uusi = []
        jarjestys = ["kukkula", "pelto", "vuoristo", "joki", "silta"]
        i = 0
        while i < len(jarjestys):
            for ruutu in ruudut:
                if ruutu.tyyppi == jarjestys[i]:
                    uusi.append(ruutu)
            i += 1
        return uusi

    @staticmethod
    def lajittele_yksikot(pelaajan, tietokoneen):
        uusi = []
        jarjestys = ["jalkavaki", "ratsuvaki", "jousimiehet", "tykisto", "parantaja"]
        i = 0
        while i < len(jarjestys):
            for pel in pelaajan:
                tyyppi = pel.__class__.__name__.lower()
                if tyyppi == jarjestys[i]:
                    uusi.append(pel)
            for tie in tietokoneen:
                tyyppi = tie.__class__.__name__.lower()
                if tyyppi == jarjestys[i]:
                    uusi.append(tie)
            i += 1
        return uusi
