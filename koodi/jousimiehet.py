from yksikko import  Yksikko

class Jousimiehet(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        # kerroin jalka- ja ratsuväkeä vastaan hyökkäyksessä ja kiiloissa puolustaessa (myös muille yksiköille)
        self.jalka_ratsu_vahinko_hyokkays = 1.25

        self.kyky2_hinta = 5
        self.kyky2_bonus = 1.1
        self.kyky2_bonus_ratsuvaki = 1.5

        self.kyky1_hinta = 6
        self.kyky1_kohteiden_maara = 3
        self.kyky1_hyokkayskerroin = 0.9
        self.kyky1_verenvuoto = 3
        self.kyky1_verenvuoto_kesto = 3

    # passiivinen tehty
    # kyky 1 (osittain) tehty
    # kyky 2 tehty (ei testattu)

    def kyky1_lisaa_kohde(self, ruutu):
        # tarkista, onko ruutu aikaisemmin valittujen vieressä
        if ruutu in self.ruudut_kantamalla:
            if len(self.kyky1_kohteet) > 0:
                for Ruutu in self.kyky1_kohteet:
                    if ruutu in Ruutu.naapurit and ruutu not in self.kyky1_kohteet:
                        self.kyky1_kohteet.append(ruutu)
                        ruutu.grafiikka.muuta_vari(ruutu.grafiikka.valittu_kohteeksi_vari)
                        break
            else:
                self.kyky1_kohteet.append(ruutu)
                ruutu.grafiikka.muuta_vari(ruutu.grafiikka.valittu_kohteeksi_vari)
            if len(self.kyky1_kohteet) == self.kyky1_kohteiden_maara:
                # hyökkää, kun tarpeeksi kohteita on valittu
                self.kyky1_hyokkays()

    # jousimiesten hyökkäystä muutetaan hyökkäysten ajaksi
    # normaalit hyökkäyssäännöt pätevät
    def kyky1_hyokkays(self):
        alkuperainen = self.ominaisuudet.hyokkays
        self.ominaisuudet.hyokkays *= self.kyky1_hyokkayskerroin
        for ruutu in self.kyky1_kohteet:
            if ruutu.yksikko is not None and ruutu.yksikko.omistaja != self.omistaja:
                ruutu.yksikko.hyokkays(self)
                ruutu.yksikko.lisaa_tilavaikutus(self.kyky1_verenvuoto_kesto, 0, 0, 0, self.kyky1_verenvuoto, False)
        self.ominaisuudet.hyokkays = alkuperainen
        self.peru_kyky1()
        self.kayta_energiaa(self.kyky1_hinta)
        self.hyokatty()

    def kyky2(self):
        if self.ruutu.kiilat is None:
            self.ruutu.luo_kiilat(self.kyky2_bonus, self.kyky2_bonus_ratsuvaki)
            self.kayta_energiaa(self.kyky2_hinta)
            self.hyokatty()

    def __str__(self):
        return "-Passiivinen kyky: Tekee bonusvahinkoa\n" \
               " jalka- ja ratsuväkeen hyökkäyksessä\n" \
               "-Kyky 1 (nuolisade): Ampuu kohdealuetta\n" \
               " (3 itse valittua vierekkäistä ruutua).\n" \
               " Tekee vahinkoa alueella oleviin vihollisen\n" \
               " yksiköihin. Aiheuttaa verenvuotoa X vuoron ajan\n" \
               "-Kyky 2 (kiilat): Pystyttää kiilat ruutuun,\n" \
               " jossa on. Kiilat antavat pienen\n" \
               " puolustusbonuksen kaikkia yksiköitä vastaan\n" \
               " ja suuren bonuksen ratsuväkeä vastaan"