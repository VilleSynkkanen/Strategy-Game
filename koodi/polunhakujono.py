from jonon_elementti import Jonon_elementti

# prioriteettijono polunhakua varten
class Polunhakujono:
    def __init__(self):
        self.jono = []

    # palauttaa, onko jono tyhjä
    def tyhja(self):
        return len(self.jono) == []

    # elementin lisääminen jonoon
    def lisaa(self, elementti, prioriteetti):
        jasen = Jonon_elementti(elementti, prioriteetti)
        self.jono.append(jasen)     # tuplessa ruutu ja prioriteetti

    # poistaa elementin, jolla on pienin prioriteetti
    def poista(self):
        min = 0     # pienimmän indeksi
        for i in range(len(self.jono)):
            if self.jono[i].prioriteetti < self.jono[min].prioriteetti:
                min = i
        elementti = self.jono[min].elementti
        del self.jono[min]
        return elementti

