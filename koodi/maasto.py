class Maasto:

    def __init__(self, tyyppi, liikkuminen, hinta, hyokkays, puolustus, vari, lapinakyvyys):
        self.tyyppi = tyyppi
        self.liikkuminen = liikkuminen
        self.liikkumisen_hinta = hinta
        self.hyokkayskerroin = hyokkays
        self.puolustuskerroin = puolustus
        self.vari = vari
        self.lapinakyvyys = lapinakyvyys

    def __str__(self):
        # määrittelee läpinäkyvyyden ja liikkumisen
        liikkuminen = "kyllä"
        lapinakyvyys = "kyllä"
        if self.liikkuminen == False:
            liikkuminen = "ei"
        if self.lapinakyvyys == False:
            lapinakyvyys = "ei"

        return "Tyyppi: {}\nLiikkuminen: {} \nLiikkumisen hinta: {}\nHyökkäyskerroin: {}\n" \
               "Puolustuskerroin: {}\nLäpinäkyvyys: {}".format(self.tyyppi, liikkuminen, str(self.liikkumisen_hinta),
                                                               str(self.hyokkayskerroin), str(self.puolustuskerroin),
                                                               lapinakyvyys)

    def ota_vahinkoa(self, puolustus, liikkuminen):
        pass    #implement