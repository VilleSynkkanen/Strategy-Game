from yksikko import Yksikko
from time import sleep

class Tykisto(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()

        # kyky 1 tiedot
        self.kyky1_hinta = 8
        self.kyky1_kohteiden_maara = 7
        self.kyky1_kantama = 1
        self.kyky1_hyokkayskerroin = 0.6

        # kyky 2 tiedot
        self.kyky2_hinta = 6
        self.kyky2_kantama = 3
        self.kyky2_hyokkayskerroin = 2
        self.kyky2_verenvuoto = 3
        self.kyky2_hyokkaysvahennys = 2
        self.kyky2_kesto = 2

        # kykyä 2 varten (muuttaa hyökkäystä ja kantamaa)
        self.alkuperainen_hyok = self.ominaisuudet.hyokkays
        self.alkuperainen_kant = self.ominaisuudet.kantama

    # passiivinen tehty
    # kyky 1 toimii jotenkin (ei täydellisesti)
    # kyky 2 tehty (tilavaikutus ei testattu)

    # kohteet: ruutu ja sen naapurit + muita ruutuja, yhteensä 7
    def kyky1_lisaa_kohde(self, ruutu):
        # tarkista, onko ruutu aikaisemmin valittujen vieressä
        if ruutu in self.ruudut_kantamalla:
            if len(self.kyky1_kohteet) > 0:
                for Ruutu in self.kyky1_kohteet:
                    if ruutu in Ruutu.naapurit and ruutu not in self.kyky1_kohteet:
                        self.kyky1_kohteet.append(ruutu)
                        ruutu.grafiikka.muuta_vari(ruutu.grafiikka.valittu_kohteeksi_vari)
            else:
                for Ruutu in self.kayttoliittyma.pelinohjain.kartta.ruudut:
                    if self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, Ruutu) <= self.kyky1_kantama and \
                            Ruutu not in self.kyky1_kohteet:
                        self.kyky1_kohteet.append(Ruutu)
                        Ruutu.grafiikka.muuta_vari(Ruutu.grafiikka.valittu_kohteeksi_vari)
        if len(self.kyky1_kohteet) >= self.kyky1_kohteiden_maara:
            # hyökkää, kun tarpeeksi kohteita on valittu
            self.kyky1_hyokkays()

    # normaalit hyökkäyssäännöt pätevät
    # hyökkäyksen muuttaminen väliaikaisesti
    def kyky1_hyokkays(self):
        alkuperainen = self.ominaisuudet.hyokkays
        self.ominaisuudet.hyokkays *= self.kyky1_hyokkayskerroin
        for ruutu in self.kyky1_kohteet:
            # tuhoaa ensin mahdolliset kiilat
            if ruutu.kiilat is not None:
                ruutu.kiilat.tuhoa()
            ruutu.grafiikka.palauta_vari()
            # lisää maaston vahingoittaminen
            if ruutu.yksikko is not None:
                ruutu.yksikko.hyokkays(self)
        self.ominaisuudet.hyokkays = alkuperainen
        self.peru_kyky1()
        self.kayta_energiaa(self.kyky1_hinta)
        self.hyokatty()

    # kantamaa vähennetään ja hyökkäystä lisätään väliaikaisesti
    # ei pysty ampumaan kohteiden yli
    def kyky2(self):
        self.alkuperainen_hyok = self.ominaisuudet.hyokkays
        self.alkuperainen_kant = self.ominaisuudet.kantama
        self.ominaisuudet.hyokkays *= self.kyky2_hyokkayskerroin
        self.ominaisuudet.kantama = self.kyky2_kantama
        self.kyky2_valitsee_kohteita = True
        self.laske_kantaman_sisalla_olevat_ruudut()
        self.nayta_kantaman_sisalla_olevat_ruudut()
        self.laske_hyokkayksen_kohteet(True)
        self.nayta_hyokkayksen_kohteet()

    def kayta_kyky2(self, kohde):
        kohde.hyokkays(self)
        kohde.lisaa_tilavaikutus(self.kyky2_kesto, -self.kyky2_hyokkaysvahennys, 0, 0, self.kyky2_verenvuoto, False)
        self.peru_kyky2()
        self.kayta_energiaa(self.kyky2_hinta)
        self.hyokatty()

    def peru_kyky2(self):
        super(Tykisto, self).peru_kyky2()
        self.ominaisuudet.hyokkays = self.alkuperainen_hyok
        self.ominaisuudet.kantama = self.alkuperainen_kant
        
    def __str__(self):
        return "-Passiivinen kyky: pystyy ampumaan \n" \
               " kaikkien maastojen yli\n" \
               "-Kyky 1 (pommitus): ampuu kohdealuetta \n" \
               " (monta ruutua). Alueella olevat\n" \
               " yksiköt ottavat vahinkoa (myös omat yksiköt).\n" \
               " Jos alueella on kiiloja, ne tuhoutuvat\n" \
               "-Kyky 2 (kanisterilaukaus): lyhyempi kantama.\n" \
               " Ampuu lähellä olevaa vihollista. Kohde ottaa\n" \
               " ylimääräistä vahinkoa. Aiheuttaa verenvuotoa\n" \
               " ja vähentää hyökkäystä X vuoron ajaksi."