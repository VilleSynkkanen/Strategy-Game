from yksikko import  Yksikko

class Jousimiehet(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        # kerroin jalka- ja ratsuväkeä vastaan hyökkäyksessä ja kiiloissa puolustaessa (myös muille yksiköille)
        self._jalka_ratsu_vahinko_hyokkays = 1.25

        self._kyky2_hinta = 5
        self._kyky2_bonus = 1.1
        self._kyky2_bonus_ratsuvaki = 1.5

        self._kyky1_hinta = 6
        self._kyky1_kohteiden_maara = 3
        self._kyky1_hyokkayskerroin = 0.9
        self._kyky1_verenvuoto = 3
        self._kyky1_verenvuoto_kesto = 3

    # propertyt

    @property
    def jalka_ratsu_vahinko_hyokkays(self):
        return self._jalka_ratsu_vahinko_hyokkays

    @property
    def kyky1_hinta(self):
        return self._kyky1_hinta

    @property
    def kyky1_kohteiden_maara(self):
        return self._kyky1_kohteiden_maara

    @property
    def kyky1_hyokkayskerroin(self):
        return self._kyky1_hyokkayskerroin

    @property
    def kyky1_verenvuoto(self):
        return self._kyky1_verenvuoto

    @property
    def kyky1_verenvuoto_kesto(self):
        return self._kyky1_verenvuoto_kesto

    @property
    def kyky2_hinta(self):
        return self._kyky2_hinta

    @property
    def kyky2_bonus(self):
        return self._kyky2_bonus

    @property
    def kyky2_bonus_ratsuvaki(self):
        return self._kyky2_bonus_ratsuvaki

    # passiivinen tehty
    # kyky 1 (osittain) tehty
    # kyky 2 tehty (ei testattu)

    def kyky1_lisaa_kohde(self, ruutu):
        # tarkista, onko ruutu aikaisemmin valittujen vieressä
        if ruutu in self._ruudut_kantamalla:
            if len(self._kyky1_kohteet) > 0:
                for Ruutu in self._kyky1_kohteet:
                    if ruutu in Ruutu.naapurit and ruutu not in self._kyky1_kohteet:
                        self._kyky1_kohteet.append(ruutu)
                        ruutu.grafiikka.muuta_vari(ruutu.grafiikka.valittu_kohteeksi_vari)
                        break
            else:
                self._kyky1_kohteet.append(ruutu)
                ruutu.grafiikka.muuta_vari(ruutu.grafiikka.valittu_kohteeksi_vari)
            if len(self._kyky1_kohteet) == self._kyky1_kohteiden_maara:
                # hyökkää, kun tarpeeksi kohteita on valittu
                self.kyky1_hyokkays()

    # jousimiesten hyökkäystä muutetaan hyökkäysten ajaksi
    # normaalit hyökkäyssäännöt pätevät
    def kyky1_hyokkays(self):
        alkuperainen = self._ominaisuudet.hyokkays
        self._ominaisuudet.hyokkays *= self._kyky1_hyokkayskerroin
        for ruutu in self._kyky1_kohteet:
            if ruutu.yksikko is not None and ruutu.yksikko.omistaja != self._omistaja:
                ruutu.yksikko.hyokkays(self)
                ruutu.yksikko.lisaa_tilavaikutus(self._kyky1_verenvuoto_kesto, 0, 0, 0, self._kyky1_verenvuoto, False)
        self._ominaisuudet.hyokkays = alkuperainen
        self.peru_kyky1()
        self.kayta_energiaa(self._kyky1_hinta)
        self.hyokatty()

    def kyky2(self):
        if self._ruutu.kiilat is None:
            self._ruutu.luo_kiilat(self._kyky2_bonus, self._kyky2_bonus_ratsuvaki)
            self.kayta_energiaa(self._kyky2_hinta)
            self.hyokatty()

    def kyky1_nappi_tiedot(self):
        return "Nuolisade\n" + "Hinta: " + str(self._kyky1_hinta)

    def kyky2_nappi_tiedot(self):
        return "Kiilat\n" + "Hinta: " + str(self._kyky2_hinta)

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