from jonon_elementti import Jonon_elementti

# prioriteettijono polunhakua varten
class Polunhakujono:
    def __init__(self):
        self.__jono = []

    # palauttaa, onko jono tyhjä
    def tyhja(self):
        return len(self.__jono) == []

    # elementin lisääminen jonoon
    def lisaa(self, elementti, prioriteetti):
        jasen = Jonon_elementti(elementti, prioriteetti)
        self.__jono.append(jasen)     # tuplessa ruutu ja prioriteetti

    # poistaa elementin, jolla on pienin prioriteetti
    def poista(self):
        min = 0     # pienimmän indeksi
        for i in range(len(self.__jono)):
            if self.__jono[i].prioriteetti < self.__jono[min].prioriteetti:
                min = i
        elementti = self.__jono[min].elementti
        del self.__jono[min]
        return elementti
