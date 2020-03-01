class Maasto:

    def __init__(self, tyyppi, liikkuminen, hinta, hyokkays, puolustus, vari, lapinakyvyys):
        self.tyyppi = tyyppi
        self.liikkuminen = liikkuminen
        self.liikkumisen_hinta = hinta
        self.hyokkayskerroin = hyokkays
        self.puolustuskerroin = puolustus
        self.vari = vari
        self.lapinakyvyys = lapinakyvyys

    def ota_vahinkoa(self, puolustus, liikkuminen):
        pass    #implement