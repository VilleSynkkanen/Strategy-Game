

class Tekoalyn_ohjain:

    def __init__(self, pelinohjain):
        self.__pelinohjain = pelinohjain

    # alustava säätö: aggressiivinen, lähestyy kohdealuetta
    # yksikön oma tekoäly hoitaa tarkemmat päätökset
    # pieni pistebonus kohdealuetta kohdi liikkumisessa
    # priorisoi alueen valinnassa tärkeitä yksiköitä

    def paata_kohdealue(self):
        x = 0
        y = 0
        maara = 0
        for yksikko in self.__pelinohjain.kartta.pelaajan_yksikot:
            kerroin = 0
            if yksikko.__class__.__name__ == "Tykisto" or yksikko.__class__.__name__ == "Parantaja":
                kerroin = 1.5

            x += kerroin * yksikko.ruutu.koordinaatit.x
            y += kerroin * yksikko.ruutu.koordinaatit.y
            maara += kerroin
        if maara > 0:
            x /= maara
            y /= maara
            x = int(x)
            y = int(y)

            #print(x)
            #print(y)

            return self.__pelinohjain.kartta.ruudut_koordinaateilla[x][y]
        # muuta myöhemmin
        return self.__pelinohjain.kartta.pelaajan_yksikot[0].ruutu

    def ohjaa_yksikoita(self):
        kohderuutu = self.paata_kohdealue()
        #print(kohderuutu)
        for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
            if yksikko.__class__.__name__ == "Jalkavaki":   # aluksi vain jalkaväki toteutettu
                yksikko.liike(kohderuutu)                   # lisää vaatimukset myöhemmin
        for yksikko in self.__pelinohjain.kartta.tietokoneen_yksikot:
            if yksikko.__class__.__name__ == "Jalkavaki":   # aluksi vain jalkaväki toteutettu
                yksikko.hyokkays_toiminto()
