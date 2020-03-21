from yksikko import  Yksikko

class Tykisto(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()

        self.kyky1_kohteiden_maara = 2
        self.kyky1_kantama = 1
        self.kyky1_hyokkayskerroin = 0.6

    # passiivinen tehty
    # kyky 1 toimii jotenkin (ei täydellisesti)

    # kohteet: kaksi ruutua + viereiset, täytyy olla vierekkäisiä
    def kyky1_lisaa_kohde(self, ruutu):
        # tarkista, onko ruutu aikaisemmin valittujen vieressä
        if ruutu in self.ruudut_kantamalla:
            if len(self.kyky1_kohteet) > 0:
                for Ruutu in self.kyky1_kohteet:
                    if ruutu in Ruutu.naapurit:
                        for _ruutu in self.kayttoliittyma.pelinohjain.kartta.ruudut:
                            if self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, _ruutu) \
                                    <= self.kyky1_kantama and _ruutu not in self.kyky1_kohteet:
                                self.kyky1_kohteet.append(_ruutu)
                                _ruutu.grafiikka.muuta_vari(_ruutu.grafiikka.valittu_kohteeksi_vari)
                        # hyökkää, kun tarpeeksi kohteita on valittu
                        self.kyky1_hyokkays()
            else:
                for Ruutu in self.kayttoliittyma.pelinohjain.kartta.ruudut:
                    if self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, Ruutu) <= self.kyky1_kantama and \
                            Ruutu not in self.kyky1_kohteet:
                        self.kyky1_kohteet.append(Ruutu)
                        Ruutu.grafiikka.muuta_vari(Ruutu.grafiikka.valittu_kohteeksi_vari)

    # normaalit hyökkäyssäännöt pätevät
    # hyökkäyksen muuttaminen väliaikaisesti
    def kyky1_hyokkays(self):
        alkuperainen = self.ominaisuudet.hyokkays
        self.ominaisuudet.hyokkays *= self.kyky1_hyokkayskerroin
        for ruutu in self.kyky1_kohteet:
            ruutu.grafiikka.palauta_vari()
            # lisää maaston vahingoittaminen
            if ruutu.yksikko is not None:
                ruutu.yksikko.hyokkays(self)
        self.ominaisuudet.hyokkays = alkuperainen
        self.peru_kyky1()
        self.hyokatty()

    def kyky2(self):
        pass

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