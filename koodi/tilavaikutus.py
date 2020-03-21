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

    def vahenna_kestoa(self):
        self.kesto -= 1
