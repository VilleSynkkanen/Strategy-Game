from yksikko import  Yksikko

class Jalkavaki(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        # pelkkä numero (ei prosentti/kerroin)
        # ottaa ensin vahinkoa, sitten paranee
        self.parannus_hyokkayksessa = 2

    # passiivinen tehty

    def __str__(self):
        return "-Passiivinen kyky: vahingon aiheuttaminen\n " \
               " hyökkäyksessä parantaa hieman\n" \
               "-Kyky 1 (kilpiseinä): Parantaa puolustusta\n" \
               " X vuoron ajaksi, vähentää liikkumispisteitä\n" \
               "-Kyky 2 (rynnäkkö): Valitsee kohteen enintään\n" \
               " Y ruudun päässä. Liikkuu kohteen viereen\n" \
               " ja hyökkää sen kimppuun. Tekee bonusvahinkoa\n" \
               " ja tainnuttaa yksikön 1 vuoron ajaksi"