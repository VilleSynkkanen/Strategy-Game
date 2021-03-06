from math import sqrt


class Tekoaly:
    '''
    Tekoälyn yleinen toimintaperiaate:
    -jos on kohteita kantamalla, valitsee niistä yhden, jonka viereen liikkuu pisteytyksen perusteella
        -heikompien/tiettyjen yksikkötyyppejen priorisaatio
        -ei mieluiten mene huonoon maastoon
    -vaihtoehtoisesti liikkuu hyvään maastoon, jos ei heikkoja vihollisia tarjolla

    ts. pisteytykseen vaikuttaa:
    -mahdollisen vihollisen puolustus, elämä, tyyppi, ruudun maasto
    -maasto
    -läheiset omat yksiköt
    -pääsy lähemmäs vihollista

    apukeino:
    -"ylempi voima", joka päättää, mitä kohti liikutaan
        -ruutu, jota kohti liikutaan
        -yksiköiden päätöksenteko hoitaa yksityiskohdat

    -ensin katsotaan, halutaanko liikkua johonkin
    -mahdollisen liikkumisen jälkeen katsotaan, halutaanko käyttää kykyjä tai hyökätä

    Kohteen/kyvyn valintaan vaikuttaa:
    -kohteiden tyyppi (priorisaatiokertoimet)
    -odotettujen vahinkojen suhde (suurempi parempi)
    -onko mahdollista käyttää kyky: jokaisella kyvyllä oma pisteytys
    '''


    @staticmethod
    def liike(yksikko, kohderuutu, palauta=False):
        # sanakirja, johon lisätään ruudut, avaimena pisteytys
        # jokaiselle ruudulle kutsutaan pistytysmetodi
        vaihtoehdot = {}
        yksikko.laske_mahdolliset_ruudut()
        # lisätään yksikön oma ruutu, koska muuten ei tule lisättyä
        yksikko.mahdolliset_ruudut.append(yksikko.ruutu)
        for ruutu in yksikko.mahdolliset_ruudut:
            vaihtoehdot[ruutu] = yksikko.pisteyta_ruutu(ruutu, kohderuutu)

        # etsi korkein pistemäärä
        paras = yksikko.ruutu
        for ruutu in vaihtoehdot:
            if vaihtoehdot[ruutu] > vaihtoehdot[paras]:
                paras = ruutu
        if palauta:
            return paras, vaihtoehdot[paras]
        # liiku ruutuun
        if paras != yksikko.ruutu:
            yksikko.liiku_ruutuun(paras)

    @staticmethod
    def hyokkays_toiminto(yksikko, ei_kykyja=False, pisteet=False):
        # pisteyttää jokaisen hyökkäyksen kohteen (ja kyvyn) ja palauttaa parhaan kohteen (ja mahdollisesti pisteet)
        vaihtoehdot = {}
        yksikko.laske_hyokkayksen_kohteet(False)
        for vihollinen in yksikko.hyokkayksen_kohteet:
            hyok_vahinko, puol_vahinko, flanking = yksikko.laske_vahinko(yksikko, vihollinen, True)
            suhde = (puol_vahinko + 0.001) / (hyok_vahinko + 0.001)
            # priorisoitavat tyypit
            if vihollinen.__class__.__name__ == "Tykisto":
                suhde *= yksikko.tykisto_prio
            elif vihollinen.__class__.__name__ == "Parantaja":
                suhde *= yksikko.parantaja_prio
            elif vihollinen.__class__.__name__ == "Jousimiehet":
                suhde *= yksikko.jousimies_prio
            elif vihollinen.__class__.__name__ == "Ratsuvaki":
                suhde *= yksikko.ratsuvaki_prio
            elif vihollinen.__class__.__name__ == "Jalkavaki":
                suhde *= yksikko.jalkavaki_prio
            elamakerroin = 1 / sqrt(vihollinen.ominaisuudet.nyk_elama / vihollinen.ominaisuudet.max_elama)
            if elamakerroin > yksikko.max_elamakerroin:
                elamakerroin = yksikko.max_elamakerroin
            suhde *= elamakerroin
            vaihtoehdot[vihollinen] = suhde

        if not ei_kykyja:
            kyky1_pisteet = 0
            kyky2_pisteet = 0
            # katsotaan voidaanko kykyjä käyttää, jos voidaan, pisteytetään ne
            if yksikko.ominaisuudet.nyk_energia >= yksikko.kyky1_hinta:
                kyky1_pisteet = yksikko.pisteyta_kyky1()
                vaihtoehdot["KYKY1"] = kyky1_pisteet
            if yksikko.ominaisuudet.nyk_energia >= yksikko.kyky2_hinta:
                kyky2_pisteet = yksikko.pisteyta_kyky2()
                vaihtoehdot["KYKY2"] = kyky2_pisteet

        korkeimmat_pisteet = 0
        paras_kohde = None
        for vaihtoehto in vaihtoehdot:
            # puolustajan vahingon täytyy olla suurempi tai yhtä suuri kuin hyökkääjän, jotta hyökkäys tapahtuisi
            if vaihtoehdot[vaihtoehto] is not None:
                if vaihtoehdot[vaihtoehto] > korkeimmat_pisteet and vaihtoehdot[vaihtoehto] >= 1:
                    korkeimmat_pisteet = vaihtoehdot[vaihtoehto]
                    paras_kohde = vaihtoehto    # voi olla yksikkö tai merkkijono
        if pisteet:
            return paras_kohde, korkeimmat_pisteet
        return paras_kohde

    # joitain kykyjä varten tulee pisteyttää pelkkä kohde
    @staticmethod
    def pisteyta_pelkka_kohde(yksikko, vihollinen):
        hyok_vahinko, puol_vahinko, flanking = yksikko.laske_vahinko(yksikko, vihollinen, True)
        suhde = (puol_vahinko + 0.001) / (hyok_vahinko + 0.001)
        # priorisoitavat tyypit
        if vihollinen.__class__.__name__ == "Tykisto":
            suhde *= yksikko.tykisto_prio
        elif vihollinen.__class__.__name__ == "Parantaja":
            suhde *= yksikko.parantaja_prio
        elif vihollinen.__class__.__name__ == "Jousimiehet":
            suhde *= yksikko.jousimies_prio
        elif vihollinen.__class__.__name__ == "Ratsuvaki":
            suhde *= yksikko.ratsuvaki_prio
        elif vihollinen.__class__.__name__ == "Jalkavaki":
            suhde *= yksikko.jalkavaki_prio
        elamakerroin = 1 / sqrt(vihollinen.ominaisuudet.nyk_elama / vihollinen.ominaisuudet.max_elama)
        if elamakerroin > yksikko.max_elamakerroin:
            elamakerroin = yksikko.max_elamakerroin
        suhde *= elamakerroin
        return suhde

    @staticmethod
    def pisteyta_kantamalla_olevat_viholliset(ruutu, yksikko):
        # aluksi 10 pistettä, muokataan kertoimien avulla
        pisteet = 10
        # lasketaan mahdolliset kohteet ja käydään ne läpi for-loopilla
        viholliset = yksikko.kantamalla_olevat_viholliset(ruutu)
        suurin_kerroin = 1
        for vihollinen in viholliset:
            kerroin = 1
            # priorisoitavat tyypit
            if vihollinen.__class__.__name__ == "Tykisto":
                kerroin *= yksikko.tykisto_prio
            elif vihollinen.__class__.__name__ == "Parantaja":
                kerroin *= yksikko.parantaja_prio
            elif vihollinen.__class__.__name__ == "Jousimiehet":
                kerroin *= yksikko.jousimies_prio
            elif vihollinen.__class__.__name__ == "Ratsuvaki":
                kerroin *= yksikko.ratsuvaki_prio
            elif vihollinen.__class__.__name__ == "Jalkavaki":
                kerroin *= yksikko.jalkavaki_prio

            # elämän vaikutus
            elamakerroin = 1 / sqrt(vihollinen.ominaisuudet.nyk_elama / vihollinen.ominaisuudet.max_elama)
            if elamakerroin > yksikko.max_elamakerroin:
                elamakerroin = yksikko.max_elamakerroin
            kerroin *= elamakerroin

            # puolustuksen vaikutus
            puolustuskerroin = 1 * (yksikko.ominaisuudet.hyokkays / vihollinen.ominaisuudet.puolustus)
            if puolustuskerroin > yksikko.max_puolustuskerroin:
                puolustuskerroin = yksikko.max_puolustuskerroin
            elif puolustuskerroin < yksikko.min_puolustuskerroin:
                puolustuskerroin = yksikko.min_puolustuskerroin
            kerroin *= puolustuskerroin

            # ruudun maasto
            maastokerroin = 1
            maastokerroin *= 1 / sqrt(vihollinen.ruutu.maasto.hyokkayskerroin)
            maastokerroin *= 1 / sqrt(vihollinen.ruutu.maasto.puolustuskerroin)
            if maastokerroin > yksikko.max_maastokerroin:
                maastokerroin = yksikko.max_maastokerroin
            elif maastokerroin < yksikko.min_maastokerroin:
                maastokerroin = yksikko.min_maastokerroin
            kerroin *= maastokerroin

            # flankkays, tarkistetaan vieressäolo
            if vihollinen.vieressa_monta_vihollista(True) and yksikko.ruutu in ruutu.naapurit:
                kerroin *= yksikko.flanking_kerroin

            # kiilat
            if vihollinen.ruutu.kiilat is not None:
                if yksikko.__class__.__name__ == "Ratsuvaki":
                    kerroin *= 1 / vihollinen.ruutu.kiilat.puolustusbonus_ratsuvaki
                else:
                    kerroin *= 1 / vihollinen.ruutu.kiilat.puolustusbonus

            # suurimman kertoimen määrittely
            if kerroin > suurin_kerroin:
                suurin_kerroin = kerroin
        pisteet *= suurin_kerroin
        return pisteet

    @staticmethod
    def pisteyta_liikuttava_maasto(yksikko, ruutu):
        maastokerroin = 1
        # jos kerroin huonompi kuin 1, vähennetään, jos parempi, niin lisätään
        maastokerroin += yksikko.oma_maastokerroin_hyokkays * (ruutu.maasto.hyokkayskerroin - 1)
        maastokerroin += yksikko.oma_maastokerroin_puolustus * (ruutu.maasto.puolustuskerroin - 1)
        # kiilat
        if ruutu.kiilat is not None:
            maastokerroin *= ruutu.kiilat.puolustusbonus
        return maastokerroin

    @staticmethod
    def pisteyta_kohteen_lahestyminen(yksikko, ruutu, kohderuutu):
        # lasketaan, lähestytäänkö kohderuutua liikuttaessa ruutuun
        # lasketaan hinta ilman blokkausta (ikään kuin oletetaan, että tilanne muuttuu)
        kerroin = 1
        polku, hinnat = yksikko.kayttoliittyma.pelinohjain.polunhaku.hae_polkua(ruutu, kohderuutu, False)
        if hinnat is not False:
            etaisyys = yksikko.kayttoliittyma.pelinohjain.polunhaku.laske_hinta(hinnat, kohderuutu)
            if etaisyys <= yksikko.max_etaisyys_kohteesta:
                kerroin = yksikko.kulmakerroin * etaisyys + yksikko.max_lahestymisbonus
        return kerroin

    @staticmethod
    def pisteyta_oman_yksikon_laheisyys(yksikko, ruutu):
        # jos omia yksiköitä on tarpeeksi monta tarpeeksi lähellä ruutuam siitä saa lisäpisteitä
        etaisyyskerroin = 1
        yksikot = 0
        for oma in yksikko.kayttoliittyma.pelinohjain.kartta.tietokoneen_yksikot:
            etaisyys = yksikko.kayttoliittyma.pelinohjain.polunhaku.heuristiikka(ruutu, oma.ruutu)
            if 0 < etaisyys < yksikko.oma_max_kantama and oma is not yksikko:
                yksikot += 1
        if yksikot >= yksikko.laheisyys_bonus_yksikot:
            etaisyyskerroin = yksikko.oma_lahestymisbonus
        return etaisyyskerroin

    @staticmethod
    def pisteyta_vihollisten_valttely(yksikko, ruutu):
        # jotkut yksiköt pyrkivät pysymään mahdollisimman kaukana vihollisesta (mutta kuitenkin kantamalla)
        # kerrointa vähennetään, jos kohderuutu on lähempänä vihollista kuin yksikön maksimikantama
        kerroin = 1
        for vihollinen in yksikko.kayttoliittyma.pelinohjain.kartta.pelaajan_yksikot:
            polku, hinnat = yksikko.kayttoliittyma.pelinohjain.polunhaku.hae_polkua(ruutu, vihollinen.ruutu, False)
            if hinnat is not False:
                etaisyys = yksikko.kayttoliittyma.pelinohjain.polunhaku.laske_hinta(hinnat, vihollinen.ruutu)
                if etaisyys < yksikko.ominaisuudet.kantama:
                    uusi_kerroin = (etaisyys / yksikko.ominaisuudet.kantama)**yksikko.etaisyys_vihollisista_eksp
                    if uusi_kerroin < kerroin:
                        kerroin = uusi_kerroin
        return kerroin
