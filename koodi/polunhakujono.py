from jonon_elementti import Jonon_elementti

# prioriteettijono polunhakua varten
class Polunhakujono:
    def __init__(self):
        self._jono = []

    # palauttaa, onko jono tyhjä
    def tyhja(self):
        return len(self._jono) == []

    # elementin lisääminen jonoon
    def lisaa(self, elementti, prioriteetti):
        jasen = Jonon_elementti(elementti, prioriteetti)
        self._jono.append(jasen)     # tuplessa ruutu ja prioriteetti

    # poistaa elementin, jolla on pienin prioriteetti
    def poista(self):
        min = 0     # pienimmän indeksi
        for i in range(len(self._jono)):
            if self._jono[i].prioriteetti < self._jono[min].prioriteetti:
                min = i
        elementti = self._jono[min].elementti
        del self._jono[min]
        return elementti
