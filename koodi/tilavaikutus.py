class Tilavaikutus:

    def __init__(self, yksikko, kesto, hyokkays, puolustus, liikkuminen, verenvuoto, taintuminen):
        self.yksikko = yksikko
        self.kesto = kesto
        self.hyokkaysbonus = hyokkays
        self.puolustusbonus = puolustus
        self.liikkumisbonus = liikkuminen
        self.verenvuoto = verenvuoto
        self.taintuminen = taintuminen

        self.yksikko.muuta_hyokkaysta(self.hyokkaysbonus)
        self.yksikko.muuta_puolustusta(self.puolustusbonus)
        self.yksikko.muuta_liikkumista(self.liikkumisbonus)

        if self.taintuminen:
            # jos taintui, poista kyky liikkua ja hyökätä
            # palautetaan vuoron alussa, jos taintuminen ei enää voimassa
            self.yksikko.liikuttu()
            self.yksikko.hyokatty()

    def vahenna_kestoa(self):
        self.kesto -= 1
        print("vah")
