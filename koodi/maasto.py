class Maasto:

    def __init__(self, tyyppi, liikkuminen, hinta, hyokkays, puolustus, vari, lapinakyvyys):
        self._tyyppi = tyyppi
        self._liikkuminen = liikkuminen
        self._liikkumisen_hinta = hinta
        self._hyokkayskerroin = hyokkays
        self._puolustuskerroin = puolustus
        self._vari = vari
        self._lapinakyvyys = lapinakyvyys

    @property
    def tyyppi(self):
        return self._tyyppi

    @property
    def liikkuminen(self):
        return self._liikkuminen

    @property
    def liikkumisen_hinta(self):
        return self._liikkumisen_hinta

    @property
    def hyokkayskerroin(self):
        return self._hyokkayskerroin

    @property
    def puolustuskerroin(self):
        return self._puolustuskerroin

    @property
    def vari(self):
        return self._vari

    @property
    def lapinakyvyys(self):
        return self._lapinakyvyys

    def __str__(self):
        # määrittelee läpinäkyvyyden ja liikkumisen
        liikkuminen = "kyllä"
        lapinakyvyys = "kyllä"
        if self._liikkuminen == False:
            liikkuminen = "ei"
        if self._lapinakyvyys == False:
            lapinakyvyys = "ei"

        return "Tyyppi: {}\nLiikkuminen: {} \nLiikkumisen hinta: {}\nHyökkäyskerroin: {}\n" \
               "Puolustuskerroin: {}\nLäpinäkyvyys: {}".format(self._tyyppi, liikkuminen, str(self._liikkumisen_hinta),
                                                               str(self._hyokkayskerroin), str(self._puolustuskerroin),
                                                               lapinakyvyys)
