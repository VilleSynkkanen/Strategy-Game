from PyQt5 import QtTest


class Tekoalyn_ohjain:

    def __init__(self, pelinohjain):
        self.__pelinohjain = pelinohjain

        # priorisaatio kohderuudun päättämisessä
        self.tykisto_prio = 1.5
        self.parantaja_prio = 1.4
        self.jousimies_prio = 1.2
        self.ratsuvaki_prio = 1.1
        self.jalkavaki_prio = 1

        # liikkumisjärjestys
        self.__liikkumisjarjestys = ["Ratsuvaki", "Jalkavaki", "Jousimiehet", "Parantaja", "Tykisto"]
        self.__hyokkaysjarjestys = ["Tykisto", "Jousimiehet", "Ratsuvaki", "Parantaja", "Jalkavaki"]

    # tekoäly: aggressiivinen, lähestyy kohdealuetta
    # yksikön oma tekoäly hoitaa tarkemmat päätökset
    # pieni pistebonus kohdealuetta kohdi liikkumisessa
    # priorisoi alueen valinnassa tärkeitä yksiköitä

    # määritellään kohderuutu, jota kohti liikkumiseen yksiköt saavat lisäpisteitä
    def paata_kohdealue(self):
        x = 0
        y = 0
        maara = 0
        # kohderuutu saadaan laskemalla pelaajan yksiköiden koordinaattien painotettu keskiarvo
        for yksikko in self.__pelinohjain.kartta.pelaajan_yksikot:
            kerroin = 1
            # priorisoitavat tyypit
            if yksikko.__class__.__name__ == "Tykisto":
                kerroin *= self.tykisto_prio
            elif yksikko.__class__.__name__ == "Parantaja":
                kerroin *= self.parantaja_prio
            elif yksikko.__class__.__name__ == "Jousimiehet":
                kerroin *= self.jousimies_prio
            elif yksikko.__class__.__name__ == "Ratsuvaki":
                kerroin *= self.ratsuvaki_prio
            elif yksikko.__class__.__name__ == "Jalkavaki":
                kerroin *= self.jalkavaki_prio

            x += kerroin * yksikko.ruutu.koordinaatit.x
            y += kerroin * yksikko.ruutu.koordinaatit.y
            maara += kerroin
        if maara > 0:
            x /= maara
            y /= maara
            x = int(x)
            y = int(y)

            # jos kohderuudussa ei ole pelaajan yksikköä, etsitään sitä lähin ruutu, jossa on
            if self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y].yksikko is not None and \
                    self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y].yksikko.omistaja == "PLR":
                return self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y]
            else:
                return self.__etsi_lahin_vihollinen(self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y])

        return self.__pelinohjain.kartta.pelaajan_yksikot[0].ruutu

    def __etsi_lahin_vihollinen(self, ruutu):
        pienin_etaisyys = 1000
        lahin_ruutu = None
        for vihollinen in self.__pelinohjain.kartta.pelaajan_yksikot:
            etaisyys = self.__pelinohjain.polunhaku.heuristiikka(ruutu, vihollinen.ruutu)
            if etaisyys < pienin_etaisyys:
                pienin_etaisyys = etaisyys
                lahin_ruutu = vihollinen.ruutu
        return lahin_ruutu

    def __lajittele_listat(self, toiminto):
        # lajittelu liikkumista ja hyökkäystä varten
        # listan järjestys määrittelee yksiköiden toimintajärjestyksen
        uusi_lista = []
        if toiminto == "liikkuminen":
            i = 0
            while i < len(self.__liikkumisjarjestys):
                for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
                    if yksikko.__class__.__name__ == self.__liikkumisjarjestys[i]:
                        uusi_lista.append(yksikko)
                i += 1
        elif toiminto == "hyokkays":
            i = 0
            while i < len(self.__hyokkaysjarjestys):
                for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
                    if yksikko.__class__.__name__ == self.__hyokkaysjarjestys[i]:
                        uusi_lista.append(yksikko)
                i += 1
        self.__pelinohjain.kartta.tietokoneen_yksikot = uusi_lista

    def ohjaa_yksikoita(self):
        # ensin määritellään kohdealue, sitten liikutetaan kaikkia yksiköitä, minkä jälkeen hyökätään
        kohderuutu = self.paata_kohdealue()
        self.__lajittele_listat("liikkuminen")
        for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
            if not yksikko.liikkuminen_kaytetty:
                yksikko.liike(kohderuutu)
                QtTest.QTest.qWait(self.__pelinohjain.viive)
        self.__lajittele_listat("hyokkays")
        for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
            if not yksikko.hyokkays_kaytetty:
                yksikko.hyokkays_toiminto()
                QtTest.QTest.qWait(self.__pelinohjain.viive)
        for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
            # ratsuväki voi liikkua hyökkäyksen jälkeen, jos se ei liikkunut ennen sitä
            if yksikko.__class__.__name__ == "Ratsuvaki" and not yksikko.liikkuminen_kaytetty \
                    and yksikko.ominaisuudet is not None:       # tarkistetaan, ettei ole kuollut
                yksikko.liike(kohderuutu)
                QtTest.QTest.qWait(self.__pelinohjain.viive)
                # joissain tapauksissa hyökkäys voi jäädä käyttämättä, joten tarkistetaan kohteet vielä kerran
                if not yksikko.hyokkays_kaytetty:
                    yksikko.hyokkays_toiminto()
                    QtTest.QTest.qWait(self.__pelinohjain.viive)
