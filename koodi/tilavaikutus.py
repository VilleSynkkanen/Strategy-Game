class Tilavaikutus:

    def __init__(self, yksikko, kesto, hyokkays, puolustus, liikkuminen, verenvuoto, taintuminen, loppuvaikutus=None):
        self.__yksikko = yksikko
        self.__kesto = kesto
        self.__hyokkaysbonus = hyokkays
        self.__puolustusbonus = puolustus
        self.__liikkumisbonus = liikkuminen
        self.__verenvuoto = verenvuoto
        self.__taintuminen = taintuminen

        # vaikutus, joka tulee voimaan, kun self.__kesto menee nollaan
        self.__loppuvaikutus = loppuvaikutus

        if self.__yksikko is not None:
            self.__yksikko.muuta_hyokkaysta(self.__hyokkaysbonus)
            self.__yksikko.muuta_puolustusta(self.__puolustusbonus)
            self.__yksikko.muuta_liikkumista(self.__liikkumisbonus)

            if self.__taintuminen:
                # jos taintui, poista kyky liikkua ja hyökätä
                # palautetaan vuoron alussa, jos taintuminen ei enää voimassa
                self.__yksikko.liikuttu()
                self.__yksikko.hyokatty()

    @property
    def kesto(self):
        return self.__kesto

    @property
    def hyokkaysbonus(self):
        return self.__hyokkaysbonus

    @property
    def puolustusbonus(self):
        return self.__puolustusbonus

    @property
    def liikkumisbonus(self):
        return self.__liikkumisbonus

    @property
    def verenvuoto(self):
        return self.__verenvuoto

    @property
    def taintuminen(self):
        return self.__taintuminen

    @property
    def loppuvaikutus(self):
        return self.__loppuvaikutus

    def vahenna_kestoa(self):
        self.__kesto -= 1
        print("vah")
