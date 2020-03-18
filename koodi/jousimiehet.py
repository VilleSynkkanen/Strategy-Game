from yksikko import  Yksikko

class Jousimiehet(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        # kerroin jalka- ja ratsuväkeä vastaan hyökkäyksessä
        self.jalka_ratsu_vahinko_hyokkays = 1.25

    # passiivinen tehty

    def __str__(self):
        return "-Passiivinen kyky: Tekee bonusvahinkoa\n" \
               " jalka- ja ratsuväkeen hyökkäyksessä\n" \
               "-Kyky 1 (nuolisade): Ampuu kohdealuetta\n" \
               " (itse valitut ruudut).\n" \
               " Tekee vahinkoa kaikkiin alueella oleviin\n" \
               " yksiköihin. Aiheuttaa verenvuotoa X vuoron ajan\n" \
               "-Kyky 2 (kiilat): Pystyttää kiilat ruutuun,\n" \
               " jossa on. Kiilat antavat pienen\n" \
               " puolustusbonuksen kaikkia yksiköitä vastaan\n" \
               " ja suuren bonuksen ratsuväkeä vastaan"