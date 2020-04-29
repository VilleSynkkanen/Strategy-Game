from polunhakujono import Polunhakujono


class Polunhaku:

    '''
    polunhaku on toteutettu A*-algoritmilla
    hae_polkua ja rakenna_polku -metodit perustuvat seuraavalta sivustolta löytyvään koodiin:
    https://www.redblobgames.com/pathfinding/a-star/implementation.html
    koodiin on tehty jonkin verran muutoksia ja lisäyksiä
    '''

    def hae_polkua(self, alku, loppu, blokkaus=True):
        jono = Polunhakujono()
        jono.lisaa(alku, 0)
        tulopaikat = {}
        hinta_tahan_mennessa = {}
        tulopaikat[alku] = None
        hinta_tahan_mennessa[alku] = 0
        epaonnistumiset = 0
        nyk_tulopaikat = len(tulopaikat)

        while not jono.tyhja():
            nykyinen = jono.poista()
            if nykyinen == loppu:
                break
            elif nyk_tulopaikat == len(tulopaikat):
                epaonnistumiset += 1
            nyk_tulopaikat = len(tulopaikat)
            if epaonnistumiset > 50:
                # jos tulopaikkojen kasvatus epäonnistuu tarpeeksi, todetaan, että ruutuun ei pääse
                # tehdään näin, jotta looppi ei jäisi jumiin
                return False, False

            # nykyinen = ruutu
            if nykyinen is not None:
                # laskenta, jos blokkaus otetaan huomioon
                if blokkaus:
                    for seuraava in nykyinen.vapaat_naapurit():
                        uusi_hinta = hinta_tahan_mennessa[nykyinen] + seuraava.maasto.liikkumisen_hinta
                        if seuraava not in hinta_tahan_mennessa or uusi_hinta < hinta_tahan_mennessa[seuraava]:
                            hinta_tahan_mennessa[seuraava] = uusi_hinta
                            prioriteetti = uusi_hinta + self.heuristiikka(loppu, seuraava)
                            jono.lisaa(seuraava, prioriteetti)
                            tulopaikat[seuraava] = nykyinen
                else:
                    # laskenta huomioimatta blokkausta
                    for seuraava in nykyinen.naapurit:
                        if seuraava.maasto.liikkuminen:
                            uusi_hinta = hinta_tahan_mennessa[nykyinen] + seuraava.maasto.liikkumisen_hinta
                            if seuraava not in hinta_tahan_mennessa or uusi_hinta < hinta_tahan_mennessa[seuraava]:
                                hinta_tahan_mennessa[seuraava] = uusi_hinta
                                prioriteetti = uusi_hinta + self.heuristiikka(loppu, seuraava)
                                jono.lisaa(seuraava, prioriteetti)
                                tulopaikat[seuraava] = nykyinen

        return tulopaikat, hinta_tahan_mennessa

    # rakentaa tiedoistaan polkulistan ja palauttaa sen
    def rakenna_polku(self, tulopaikat, alku, maali):
        nykyinen = maali
        polku = []
        while nykyinen != alku:
            polku.append(nykyinen)
            nykyinen = tulopaikat[nykyinen]
        polku.append(alku)
        polku.reverse()
        return polku

    # laskee ruutuun liikkumisen hinnan
    def laske_hinta(self, hinta_tahan_mennessa, maali):
        for elementti in hinta_tahan_mennessa:
            if elementti == maali:
                hinta = hinta_tahan_mennessa[elementti]
                return hinta

    # heuristiikan laskeminen, voi liikkua vain neljään suuntaan
    def heuristiikka(self, paikka, kohde):
        x = abs(paikka.koordinaatit.x - kohde.koordinaatit.x)
        y = abs(paikka.koordinaatit.y - kohde.koordinaatit.y)
        return x + y
