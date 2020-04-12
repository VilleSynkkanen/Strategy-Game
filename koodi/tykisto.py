from yksikko import Yksikko
from time import sleep
from ajastin import Ajastin

class Tykisto(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet, kyvyt):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()

        # kyky 1 tiedot
        self.__kyky1_hinta = int(kyvyt["kyky1_hinta"])
        self.__kyky1_kantama = int(kyvyt["kyky1_kantama"])
        self.__kyky1_hyokkayskerroin = kyvyt["kyky1_hyokkayskerroin"]
        self.__kyky1_liikkuminen = int(kyvyt["kyky1_liikkuminen"])
        self.__kyky1_kesto = int(kyvyt["kyky1_kesto"])

        # kyky 2 tiedot
        self.__kyky2_hinta = int(kyvyt["kyky2_hinta"])
        self.__kyky2_kantama = int(kyvyt["kyky2_kantama"])
        self.__kyky2_hyokkayskerroin = kyvyt["kyky2_hyokkayskerroin"]
        self.__kyky2_verenvuoto = int(kyvyt["kyky2_verenvuoto"])
        self.__kyky2_hyokkaysvahennys = int(kyvyt["kyky2_hyokkaysvahennys"])
        self.__kyky2_kesto = int(kyvyt["kyky2_kesto"])

        # kykyä 2 varten (muuttaa hyökkäystä ja kantamaa)
        self.__alkuperainen_hyok = self.ominaisuudet.hyokkays
        self.__alkuperainen_kant = self.ominaisuudet.kantama

    # propertyt

    @property
    def kyky1_hinta(self):
        return self.__kyky1_hinta

    @property
    def kyky1_kantama(self):
        return self.__kyky1_kantama

    @property
    def kyky1_hyokkayskerroin(self):
        return self.__kyky1_hyokkayskerroin

    @property
    def kyky2_hinta(self):
        return self.__kyky2_hinta

    @property
    def kyky2_kantama(self):
        return self.__kyky2_kantama

    @property
    def kyky2_hyokkayskerroin(self):
        return self.__kyky2_hyokkayskerroin

    @property
    def kyky2_verenvuoto(self):
        return self.__kyky2_verenvuoto

    @property
    def kyky2_hyokkaysvahennys(self):
        return self.__kyky2_hyokkaysvahennys

    @property
    def kyky2_kesto(self):
        return self.__kyky2_kesto

    @property
    def alkuperainen_hyok(self):
        return self.__alkuperainen_hyok

    @property
    def alkuperainen_kant(self):
        return self.__alkuperainen_kant

    # passiivinen tehty
    # kyky 1 toimii jotenkin (ei täydellisesti)
    # kyky 2 tehty (tilavaikutus ei testattu)

    # kohteet: ruutu ja sen naapurit
    def kyky1_lisaa_kohde(self, ruutu, tekoaly=False):
        # tarkista, onko ruutu kantamalla
        if ruutu in self.ruudut_kantamalla or tekoaly:
            for Ruutu in self.kayttoliittyma.pelinohjain.kartta.ruudut:
                if self.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, Ruutu) <= self.kyky1_kantama \
                        and Ruutu not in self.kyky1_kohteet:
                    self.kyky1_kohteet.append(Ruutu)
                    Ruutu.grafiikka.muuta_vari(Ruutu.grafiikka.valittu_kohteeksi_vari)
        # hyökkäys
        if not tekoaly:
            Ajastin.aloita_ajastin(self.visualisointi_viive, self.__kyky1_hyokkays)
        else:
            # print(self.kyky1_kohteet)
            # print("ko ", ruutu.koordinaatit.x, " ", ruutu.koordinaatit.x)
            self.__kyky1_hyokkays()

    # normaalit hyökkäyssäännöt pätevät
    # hyökkäyksen muuttaminen väliaikaisesti
    def __kyky1_hyokkays(self):
        alkuperainen = self.ominaisuudet.hyokkays
        self.ominaisuudet.hyokkays *= self.kyky1_hyokkayskerroin
        for ruutu in self.kyky1_kohteet:
            # tuhoaa ensin mahdolliset kiilat
            if ruutu.kiilat is not None:
                ruutu.kiilat.tuhoa()
            ruutu.grafiikka.palauta_vari()
            if ruutu.yksikko is not None:
                ruutu.yksikko.lisaa_tilavaikutus(self.__kyky1_kesto, 0, 0, self.__kyky1_liikkuminen, 0, False)
                ruutu.yksikko.hyokkays(self)
        self.ominaisuudet.hyokkays = alkuperainen
        self.peru_kyky1()
        self.kayta_energiaa(self.kyky1_hinta)
        self.hyokatty()
        teksti = self.__class__.__name__ + " käytti pommituksen"
        self.kayttoliittyma.lisaa_pelilokiin(teksti)

    # kantamaa vähennetään ja hyökkäystä lisätään väliaikaisesti
    # ei pysty ampumaan kohteiden yli
    def kyky2(self, tekoaly=False):
        self.__alkuperainen_hyok = self.ominaisuudet.hyokkays
        self.__alkuperainen_kant = self.ominaisuudet.kantama
        self.ominaisuudet.hyokkays *= self.kyky2_hyokkayskerroin
        self.ominaisuudet.kantama = self.kyky2_kantama
        if not tekoaly:
            self.kyky2_valitsee_kohteita = True
            self.laske_kantaman_sisalla_olevat_ruudut()
            self.nayta_kantaman_sisalla_olevat_ruudut()
            self.laske_hyokkayksen_kohteet(True)
            self.nayta_hyokkayksen_kohteet()

    def kayta_kyky2(self, kohde):
        kohde.hyokkays(self)
        if kohde is not None:
            kohde.lisaa_tilavaikutus(self.kyky2_kesto, -self.kyky2_hyokkaysvahennys, 0, 0, self.kyky2_verenvuoto, False)
        self.peru_kyky2()
        self.kayta_energiaa(self.kyky2_hinta)
        self.hyokatty()
        teksti = self.__class__.__name__ + " käytti kanisterilaukauksen"
        self.kayttoliittyma.lisaa_pelilokiin(teksti)

    def peru_kyky2(self):
        super(Tykisto, self).peru_kyky2()
        self.ominaisuudet.hyokkays = self.__alkuperainen_hyok
        self.ominaisuudet.kantama = self.__alkuperainen_kant

    def kyky1_voi_kayttaa(self):
        if self.ominaisuudet.nyk_energia >= self.__kyky1_hinta:
            return True
        return False

    def kyky2_voi_kayttaa(self):
        if self.ominaisuudet.nyk_energia >= self.__kyky2_hinta:
            self.__alkuperainen_kant = self.ominaisuudet.kantama
            self.ominaisuudet.kantama = self.kyky2_kantama
            self.laske_hyokkayksen_kohteet(False)
            self.ominaisuudet.kantama = self.__alkuperainen_kant
            if len(self.hyokkayksen_kohteet) > 0:
                return True
        return False
        
    def kyky1_nappi_tiedot(self):
        return "Pommitus\n" + "Hinta: " + str(self.kyky1_hinta)

    def kyky2_nappi_tiedot(self):
        return "Kanisterilaukaus\n" + "Hinta: " + str(self.kyky2_hinta)

    def __str__(self):
        return "PASSIIVINEN KYKY:\n{}\n\nKYKY 1 (POMMITUS):\n{}\n\nKYKY 2 (KANISTERILAUKAUS):\n{}"\
            .format(self.passiivinen_kyky(), self.kyky1_tooltip_teksti(), self.kyky2_tooltip_teksti())

    def passiivinen_kyky(self):
        return "Pystyy ampumaan kaikkien maastojen yli.\nOttaa paljon vähemmän" \
               " vahinkoa tykistöltä"

    def kyky1_tooltip_teksti(self):
        return "Ampuu kohdealuetta \n" \
               "(valittu ruutu ja sen naapurit.\nHyökkää kaikkien alueella olevien yksiköiden kimppuun\n(" \
               + str(100*self.__kyky1_hyokkayskerroin) +"% normaalista hyökkäyksestä).\n" + \
               "Vähentää kohteiden liikkumista " + str(-self.__kyky1_liikkuminen) + " verran " + \
               str(self.__kyky1_kesto) + " vuoron\najaksi. "\
               + "Jos alueella on kiiloja, ne tuhoutuvat\n(ennen hyökkäystä)"

    def kyky2_tooltip_teksti(self):
        return "Hyökkäys, jonka kantama on " + str(self.__kyky2_kantama) + ".\n" \
               + str(int(100*(self.__kyky2_hyokkayskerroin - 1))) \
               + "% lisää hyökkäystä.\nAiheuttaa " + str(self.__kyky2_verenvuoto) + " verenvuotoa" \
               " ja vähentää hyökkäystä\n" + str(self.__kyky2_hyokkaysvahennys) + " verran " + str(self.__kyky2_kesto) \
               + " vuoron ajaksi."
