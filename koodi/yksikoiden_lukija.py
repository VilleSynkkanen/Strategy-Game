import os

from yksikon_ominaisuudet import Yksikon_ominaisuudet

class Yksikoiden_lukija:

    def __init__(self):
        self.__yksikot = {}  # sanakirja, johon lisätään yksiköt (avain = yksikön nimi)
        lue = None
        self.__lukeminen_onnistui = True
        self.__luettu_maara = 0
        yksikkotyypit = ["jalkavaki", "ratsuvaki", "jousimiehet", "tykisto", "parantaja"]
        try:
            tiedostot = os.scandir('yksikot/')

            # lukee jokaisesta tiedostosta yksikön tiedot
            # tietojen järjestyksellä ei ole väliä

            for tiedosto in tiedostot:
                lue = open(tiedosto, 'r')
                tyyppi = ""
                liikkumispisteet = 0
                max_elama = 0
                max_energia = 0
                hyokkays = 0
                puolustus = 0
                kantama = 0
                hinta = 0
                tyyppi_loydetty = False
                liikkumispisteet_loydetty = False
                max_elama_loydetty = False
                max_energia_loydetty = False
                hyokkays_loydetty = False
                puolustus_loydetty = False
                kantama_loydetty = False
                hinta_loydetty = False
                kyvyt_loydetty = False
                kyvyt = {}
                for rivi in lue:
                    rivi = rivi.lower()
                    #print(rivi)
                    rivi = rivi.rstrip()
                    rivi = rivi.split(':')
                    i = 0
                    while i < len(rivi):
                        rivi[i] = rivi[i].strip()
                        i += 1
                    if rivi[0] == "tyyppi":
                        tyyppi = rivi[1]
                        if tyyppi not in yksikkotyypit:
                            self.__lukeminen_onnistui = False
                            lue.close()
                            return
                        tyyppi_loydetty = True
                    elif rivi[0] == "liikkumispisteet":
                        liikkumispisteet = int(rivi[1])
                        if liikkumispisteet < 0:
                            self.__lukeminen_onnistui = False
                            lue.close()
                            return
                        liikkumispisteet_loydetty = True
                    elif rivi[0] == "maksimielama":
                        max_elama = int(rivi[1])
                        if max_elama <= 0:
                            self.__lukeminen_onnistui = False
                            lue.close()
                            return
                        max_elama_loydetty = True
                    elif rivi[0] == "maksimienergia":
                        max_energia = int(rivi[1])
                        if max_energia <= 0:
                            self.__lukeminen_onnistui = False
                            lue.close()
                            return
                        max_energia_loydetty = True
                    elif rivi[0] == "hyokkays":
                        hyokkays = int(rivi[1])
                        if hyokkays <= 0:
                            self.__lukeminen_onnistui = False
                            lue.close()
                            return
                        hyokkays_loydetty = True
                    elif rivi[0] == "puolustus":
                        puolustus = int(rivi[1])
                        if puolustus <= 0:
                            self.__lukeminen_onnistui = False
                            lue.close()
                            return
                        puolustus_loydetty = True
                    elif rivi[0] == "kantama":
                        kantama = int(rivi[1])
                        if kantama <= 0:
                            self.__lukeminen_onnistui = False
                            lue.close()
                            return
                        kantama_loydetty = True
                    elif rivi[0] == "pistehinta":
                        hinta = int(rivi[1])
                        if hinta <= 0:
                            self.__lukeminen_onnistui = False
                            lue.close()
                            return
                        hinta_loydetty = True
                    elif rivi[0] == "kyvyt":
                        # jokaisella tyypillä eri kykyihin liittyvät muuttujat, joten käytetään eri metodeita lukemiseen
                        # numerot tallennetaan sanakirjaan
                        kyvyt = self.__lue_kyvyt(lue)
                        kyvyt_loydetty = self.__kykyjen_tarkistus(tyyppi, kyvyt)
                        if kyvyt is False:
                            self.__lukeminen_onnistui = False
                            lue.close()
                            return
                    elif rivi[0] == "loppu":
                        break

                if not tyyppi_loydetty or not liikkumispisteet_loydetty or not hyokkays_loydetty or \
                        not puolustus_loydetty or not max_elama_loydetty or not max_energia_loydetty or \
                        not kantama_loydetty or not hinta_loydetty or not kyvyt_loydetty:
                    self.__lukeminen_onnistui = False
                    lue.close()
                    return

                # luo uuden yksikkö-instanssin, johon tiedot säilötään
                # luotu yksikkö lisätään sanakirjaan, josta se voiddan myöhemmin lukea
                # instanssi on tuple, jossa 1. jäsen on ominaisuudet-instanssi ja toinen kyvyt-sanakirja
                yksikko = (Yksikon_ominaisuudet(tyyppi, liikkumispisteet, max_elama, max_elama, max_energia, max_energia,
                                               hyokkays, puolustus, kantama, hinta, []), kyvyt)
                self.__yksikot[tyyppi.lower()] = yksikko
                self.__luettu_maara += 1
                lue.close()  # muista sulkea aina

            #print(self.__luettu_maara)
            if self.__luettu_maara < 5:
                self.__lukeminen_onnistui = False

        except IndexError:
            self.__lukeminen_onnistui = False
            if lue is not None and not lue.closed:
                lue.close()
            return
        except ValueError:
            self.__lukeminen_onnistui = False
            if lue is not None and not lue.closed:
                lue.close()
            return
        except OSError:
            self.__lukeminen_onnistui = False
            if lue is not None and not lue.closed:
                lue.close()
            return

    @property
    def yksikot(self):
        return self.__yksikot

    @property
    def lukeminen_onnistui(self):
        return self.__lukeminen_onnistui

    def __lue_kyvyt(self, tiedosto):
        try:
            kyvyt = {}
            rivi = tiedosto.readline()
            rivi = rivi.lower()
            rivi = rivi.rstrip()
            rivi = rivi.split(':')
            while rivi[0] != "loppu":
                kyvyt[rivi[0]] = float(rivi[1])
                rivi = tiedosto.readline()
                rivi = rivi.lower()
                rivi = rivi.rstrip()
                rivi = rivi.split(':')
            return kyvyt
        except ValueError:
            return False

    def __kykyjen_tarkistus(self, tyyppi, kyvyt):
        # palauttaa kyvyt, jos ne ovat validit, muuten palauttaa false
        try:
            if tyyppi == "jalkavaki":
                # tarkistus
                if kyvyt['kyky1_hinta'] <= 0:
                    return False
                if kyvyt['kyky1_kesto'] <= 0:
                    return False
                temp = kyvyt['kyky1_puolustus']
                temp = kyvyt['kyky1_liikkuminen']
                if kyvyt['kyky2_hinta'] <= 0:
                    return False
                if kyvyt['kyky2_kantama'] <= 0:
                    return False
                temp = kyvyt['kyky2_bonushyokkays']
                if kyvyt['kyky2_taintuminen_kesto'] <= 0:
                    return False
                return True
            elif tyyppi == "ratsuvaki":
                # tarkistus
                if kyvyt['kyky1_hinta'] <= 0:
                    return False
                if kyvyt['kyky1_kesto'] <= 0:
                    return False
                temp = kyvyt['kyky1_puolustusvahennys']
                temp = kyvyt['kyky1_hyokkaysbonus']
                if kyvyt['kyky2_hinta'] <= 0:
                    return False
                if kyvyt['kyky2_kantama'] <= 0:
                    return False
                temp = kyvyt['kyky2_puolustusvahennys']
                if kyvyt['kyky2_kesto'] <= 0:
                    return False
                return True
            elif tyyppi == "jousimiehet":
                # tarkistus
                if kyvyt['jalka_ratsu_vahinko_hyokkays'] <= 0:
                    return False
                if kyvyt['kyky2_hinta'] <= 0:
                    return False
                if kyvyt['kyky2_bonus'] <= 0:
                    return False
                if kyvyt['kyky2_bonus_ratsuvaki'] <= 0:
                    return False
                if kyvyt['kyky1_hinta'] <= 0:
                    return False
                if kyvyt['kyky1_kohteiden_maara'] <= 0:
                    return False
                if kyvyt['kyky1_hyokkayskerroin'] <= 0:
                    return False
                if kyvyt['kyky1_verenvuoto'] <= 0:
                    return False
                if kyvyt['kyky1_verenvuoto_kesto'] <= 0:
                    return False
                return True
            elif tyyppi == "tykisto":
                # tarkistus
                if kyvyt['kyky1_hinta'] <= 0:
                    return False
                if kyvyt['kyky1_kantama'] < 0:
                    return False
                if kyvyt['kyky1_hyokkayskerroin'] <= 0:
                    return False
                temp = kyvyt['kyky1_liikkuminen']
                if kyvyt['kyky1_kesto'] <= 0:
                    return False
                if kyvyt['kyky2_hinta'] <= 0:
                    return False
                if kyvyt['kyky2_kantama'] <= 0:
                    return False
                if kyvyt['kyky2_hyokkayskerroin'] <= 0:
                    return False
                if kyvyt['kyky2_verenvuoto'] <= 0:
                    return False
                temp = kyvyt['kyky2_hyokkaysvahennys']
                if kyvyt['kyky2_kesto'] <= 0:
                    return False
                return True
            elif tyyppi == "parantaja":
                # tarkistus
                if kyvyt['inspiraatio_kantama'] <= 0:
                    return False
                if kyvyt['inspiraatio_kerroin'] <= 0:
                    return False
                if kyvyt['kyky1_hinta'] <= 0:
                    return False
                if kyvyt['kyky1_kohteiden_maara'] <= 0:
                    return False
                if kyvyt['kyky1_kantama'] <= 0:
                    return False
                if kyvyt['kyky1_parannuskerroin'] <= 0:
                    return False
                if kyvyt['kyky2_hinta'] <= 0:
                    return False
                if kyvyt['kyky2_kesto'] <= 0:
                    return False
                temp = kyvyt['kyky2_hyokkaysvahennys']
                temp = kyvyt['kyky2_puolustusvahennys']
                if kyvyt['kyky2_taintumisaika'] <= 0:
                    return False
                return True
            else:
                return False
        except KeyError:
            return False
        except TypeError:
            return False
