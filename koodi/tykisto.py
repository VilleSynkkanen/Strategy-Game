from yksikko import  Yksikko

class Tykisto(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()

    def __str__(self):
        return "-Passiivinen kyky: pystyy ampumaan \n" \
               " kaikkien maastojen yli\n" \
               "-Kyky 1 (pommitus): ampuu kohdealuetta \n" \
               " (monta ruutua). Kohdealueen puolustusarvo\n" \
               " laskee pysyvästi (jos se on > 0) ja\n" \
               " liikkumisen hinta nousee. Alueella olevat\n" \
               " yksiköt ottavat vahinkoa (myös omat yksiköt)\n" \
               "-Kyky 2 (kanisterilaukaus): lyhyempi kantama.\n" \
               " Ampuu lähellä olevaa vihollista. Kohde ottaa\n" \
               " ylimääräistä vahinkoa. Aiheuttaa verenvuotoa\n" \
               " ja vähentää hyökkäystä X vuoron ajaksi."