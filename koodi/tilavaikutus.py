class Tilavaikutus:

    def __init__(self, yksikko, kesto, hyokkays, puolustus, liikkuminen, verenvuoto, taintuminen):
        self._yksikko = yksikko
        self._kesto = kesto
        self._hyokkaysbonus = hyokkays
        self._puolustusbonus = puolustus
        self._liikkumisbonus = liikkuminen
        self._verenvuoto = verenvuoto
        self._taintuminen = taintuminen

        self._yksikko.muuta_hyokkaysta(self._hyokkaysbonus)
        self._yksikko.muuta_puolustusta(self._puolustusbonus)
        self._yksikko.muuta_liikkumista(self._liikkumisbonus)

        if self._taintuminen:
            # jos taintui, poista kyky liikkua ja hyökätä
            # palautetaan vuoron alussa, jos taintuminen ei enää voimassa
            self._yksikko.liikuttu()
            self._yksikko.hyokatty()

    @property
    def kesto(self):
        return self._kesto

    @property
    def hyokkaysbonus(self):
        return self._hyokkaysbonus

    @property
    def puolustusbonus(self):
        return self._puolustusbonus

    @property
    def liikkumisbonus(self):
        return self._liikkumisbonus

    @property
    def verenvuoto(self):
        return self._verenvuoto

    @property
    def taintuminen(self):
        return self._taintuminen

    def vahenna_kestoa(self):
        self._kesto -= 1
        print("vah")
