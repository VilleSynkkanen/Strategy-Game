import os


class Kayttoliittyman_lukija:

    def __init__(self):
        tiedostot = os.scandir('muut/')
        tiedosto = None
        self.__lukeminen_onnistui = True
        for tied in tiedostot:
            if tied.name == "kayttoliittyma.txt":
                tiedosto = tied
        if tiedosto is None:
            self.__lukeminen_onnistui = False
            return
        lue = None
        try:
            koko_loydetty = False
            x_y_loydetty = False
            viive_loydetty = False
            lue = open(tiedosto, 'r')
            self.__x = 0
            self.__y = 0
            self.__koko = 0
            self.__viive = 0
            for rivi in lue:
                rivi = rivi.lower()
                rivi = rivi.rstrip()
                rivi = rivi.split(':')
                i = 0
                while i < len(rivi):
                    rivi[i] = rivi[i].strip()
                    i += 1
                if rivi[0] == "nayton resoluutio":
                    tieto = rivi[1].split("*")
                    self.__x = int(tieto[0])
                    self.__y = int(tieto[1])
                    if self.__x <= 0 or self.__y <= 0:
                        self.__ei_validi(lue)
                        return
                    x_y_loydetty = True
                elif rivi[0] == "ikkunan koko":
                    self.__koko = int(rivi[1])
                    if self.__koko <= 0:
                        self.__ei_validi(lue)
                        return
                    koko_loydetty = True
                elif rivi[0] == "viive":
                    self.__viive = int(rivi[1])
                    if self.__viive < 0:
                        self.__ei_validi(lue)
                        return
                    viive_loydetty = True
                elif rivi[0] == "loppu":
                    lue.close()
                    if not x_y_loydetty or not koko_loydetty or not viive_loydetty:
                        self.__lukeminen_onnistui = False
                    break
        except IndexError:
            self.__ei_validi(lue)
            return
        except ValueError:
            self.__ei_validi(lue)
            return
        except OSError:
            self.__ei_validi(lue)
            return

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def koko(self):
        return self.__koko

    @property
    def viive(self):
        return self.__viive

    @property
    def lukeminen_onnistui(self):
        return self.__lukeminen_onnistui

    def __ei_validi(self, tiedosto):
        self.__lukeminen_onnistui = False
        if tiedosto is not None and not tiedosto.closed:
            tiedosto.close()
