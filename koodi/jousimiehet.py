from yksikko import Yksikko
from ajastin import Ajastin

class Jousimiehet(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()
        # kerroin jalka- ja ratsuväkeä vastaan hyökkäyksessä ja kiiloissa puolustaessa (myös muille yksiköille)
        self.__jalka_ratsu_vahinko_hyokkays = kyvyt["jalka_ratsu_vahinko_hyokkays"]

        self.__kyky2_hinta = int(kyvyt["kyky2_hinta"])
        self.__kyky2_bonus = kyvyt["kyky2_bonus"]
        self.__kyky2_bonus_ratsuvaki = kyvyt["kyky2_bonus_ratsuvaki"]

        self.__kyky1_hinta = int(kyvyt["kyky1_hinta"])
        self.__kyky1_kohteiden_maara = int(kyvyt["kyky1_kohteiden_maara"])
        self.__kyky1_hyokkayskerroin = kyvyt["kyky1_hyokkayskerroin"]
        self.__kyky1_verenvuoto = int(kyvyt["kyky1_verenvuoto"])
        self.__kyky1_verenvuoto_kesto = int(kyvyt["kyky1_verenvuoto_kesto"])

    # propertyt

    @property
    def jalka_ratsu_vahinko_hyokkays(self):
        return self.__jalka_ratsu_vahinko_hyokkays

    @property
    def kyky1_hinta(self):
        return self.__kyky1_hinta

    @property
    def kyky1_kohteiden_maara(self):
        return self.__kyky1_kohteiden_maara

    @property
    def kyky1_hyokkayskerroin(self):
        return self.__kyky1_hyokkayskerroin

    @property
    def kyky1_verenvuoto(self):
        return self.__kyky1_verenvuoto

    @property
    def kyky1_verenvuoto_kesto(self):
        return self.__kyky1_verenvuoto_kesto

    @property
    def kyky2_hinta(self):
        return self.__kyky2_hinta

    @property
    def kyky2_bonus(self):
        return self.__kyky2_bonus

    @property
    def kyky2_bonus_ratsuvaki(self):
        return self.__kyky2_bonus_ratsuvaki

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
                Ajastin.aloita_ajastin(self.visualisointi_viive, self.__kyky1_hyokkays)

    # jousimiesten hyökkäystä muutetaan hyökkäysten ajaksi
    # normaalit hyökkäyssäännöt pätevät
    def __kyky1_hyokkays(self):
        alkuperainen = self.ominaisuudet.hyokkays
        self.ominaisuudet.hyokkays *= self.kyky1_hyokkayskerroin
        for ruutu in self.kyky1_kohteet:
            if ruutu.yksikko is not None and ruutu.yksikko.omistaja != self.omistaja:
                ruutu.yksikko.hyokkays(self)
                if ruutu.yksikko is not None:
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

    def kyky1_voi_kayttaa(self):
        if self.ominaisuudet.nyk_energia >= self.__kyky1_hinta:
            return True
        return False

    def kyky2_voi_kayttaa(self):
        if self.ominaisuudet.nyk_energia >= self.__kyky2_hinta and self.ruutu.kiilat is None:
            return True
        return False

    def kyky1_nappi_tiedot(self):
        return "Nuolisade\n" + "Hinta: " + str(self.kyky1_hinta)

    def kyky2_nappi_tiedot(self):
        return "Kiilat\n" + "Hinta: " + str(self.kyky2_hinta)

    def __str__(self):
        return "PASSIIVINEN KYKY:\n{}\n\nKYKY 1 (NUOLISADE):\n{}\n\nKYKY 2 (KIILAT):\n{}"\
            .format(self.passiivinen_kyky(), self.kyky1_tooltip_teksti(), self.kyky2_tooltip_teksti())

    def passiivinen_kyky(self):
        return "Tekee " + str(int(100*(self.__jalka_ratsu_vahinko_hyokkays - 1))) + "% bonusvahinkoa jalka- " \
                                                                             "ja ratsuväkeen \nhyökkäyksessä"
    def kyky1_tooltip_teksti(self):
        return "Ampuu kohdealuetta (" + str(self.__kyky1_kohteiden_maara) + " itse valittua vierekkäistä\nruutua)." \
               "Hyökkää alueella olevien vihollisten kimppuun\n(" \
               + str(100*self.__kyky1_hyokkayskerroin) +"% normaalista hyökkäyksestä)\n" \
               "Aiheuttaa " + str(self.__kyky1_verenvuoto) + " verenvuotoa " + str(self.__kyky1_verenvuoto_kesto) \
               + " vuoron ajan"

    def kyky2_tooltip_teksti(self):
        return "Pystyttää kiilat ruutuun, " \
               "jossa on. Kiilat antavat " + str(int(100*(self.__kyky2_bonus - 1))) + "%\n" \
               "puolustusbonuksen kaikkia yksiköitä vastaan\n" \
               "ja " + str(int(100*(self.__kyky2_bonus_ratsuvaki - 1))) + "% bonuksen ratsuväkeä vastaan"
