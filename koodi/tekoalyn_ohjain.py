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

    # säätö: aggressiivinen, lähestyy kohdealuetta
    # yksikön oma tekoäly hoitaa tarkemmat päätökset
    # pieni pistebonus kohdealuetta kohdi liikkumisessa
    # priorisoi alueen valinnassa tärkeitä yksiköitä

    def paata_kohdealue(self):
        x = 0
        y = 0
        maara = 0
        for yksikko in self.__pelinohjain.kartta.pelaajan_yksikot:
            kerroin = 0
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
        # lajittelu liikkumista varten
        uusi_lista = []
        if toiminto == "liikkuminen":
            for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
                pass
        # lajittelu hyökkäystä varten

        #self.__pelinohjain.kartta.tietokoneen_yksikot = uusi_lista


    def ohjaa_yksikoita(self):
        kohderuutu = self.paata_kohdealue()
        # käydään liikkumis loop kahdesti blokkauksen välttämiseksi, auttaa joissain tilanteissa
        self.__lajittele_listat("liikkuminen")
        for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
            if not yksikko.liikkuminen_kaytetty:
                yksikko.liike(kohderuutu)
                QtTest.QTest.qWait(self.__pelinohjain.viive)
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
            # ratsuväki voi liikkua hyökkäyksen jälkeen
            if yksikko.__class__.__name__ == "Ratsuvaki" and not yksikko.liikkuminen_kaytetty:
                yksikko.liike(kohderuutu)
                QtTest.QTest.qWait(self.__pelinohjain.viive)
                # joissain tapauksissa hyökkäys voi jäädä käyttämättä
                if not yksikko.hyokkays_kaytetty:
                    yksikko.hyokkays_toiminto()
                    QtTest.QTest.qWait(self.__pelinohjain.viive)
