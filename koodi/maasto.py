class Maasto:

    def __init__(self, tyyppi, liikkuminen, hinta, hyokkays, puolustus, vari, lapinakyvyys):
        self.__tyyppi = tyyppi
        self.__liikkuminen = liikkuminen
        self.__liikkumisen_hinta = hinta
        self.__hyokkayskerroin = hyokkays
        self.__puolustuskerroin = puolustus
        self.__vari = vari
        self.__lapinakyvyys = lapinakyvyys

    @property
    def tyyppi(self):
        return self.__tyyppi

    @property
    def liikkuminen(self):
        return self.__liikkuminen

    @property
    def liikkumisen_hinta(self):
        return self.__liikkumisen_hinta

    @property
    def hyokkayskerroin(self):
        return self.__hyokkayskerroin

    @property
    def puolustuskerroin(self):
        return self.__puolustuskerroin

    @property
    def vari(self):
        return self.__vari

    @property
    def lapinakyvyys(self):
        return self.__lapinakyvyys

    def __str__(self):
        # määrittelee läpinäkyvyyden ja liikkumisen
        liikkuminen = "kyllä"
        lapinakyvyys = "kyllä"
        if self.__liikkuminen is False:
            liikkuminen = "ei"
        if self.__lapinakyvyys is False:
            lapinakyvyys = "ei"

        return "Tyyppi: {}\nLiikkuminen: {} \nLiikkumisen hinta: {}\nHyökkäyskerroin: {}\n" \
               "Puolustuskerroin: {}\nLäpinäkyvyys: {}".format(self.__tyyppi, liikkuminen, str(self.__liikkumisen_hinta),
                                                               str(self.__hyokkayskerroin), str(self.__puolustuskerroin),
                                                               lapinakyvyys)
