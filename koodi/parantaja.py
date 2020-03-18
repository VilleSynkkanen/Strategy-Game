from yksikko import  Yksikko

class Parantaja(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()

    def __str__(self):
        return "-Passiivinen kyky: inspiroi läheisiä\n" \
               " yksiköitä (parantaa hyökkäystä ja puolustusta)\n" \
               "-Kyky 1(alueparannus): parantaa alueella \n" \
               " yksiköitä tietyn määrän X vuoron ajan (heal over time)\n" \
               "-Kyky 2(kirous): kiroaa yhden vihollisyksikön.\n" \
               " Vihollisen puolustus ja hyökkäys ovat\n" \
               " heikompia X vuoron ajan. Vihollinen taintuu\n" \
               " yhden vuoron ajaksi, kun kirous loppuu."
