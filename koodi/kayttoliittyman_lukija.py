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
        try:
            lue = open(tiedosto, 'r')
            self.__x = 0
            self.__y = 0
            self.__koko = 0
            self.__viive = 0
            for rivi in lue:
                rivi = rivi.lower()
                rivi = rivi.rstrip()
                rivi = rivi.split(':')
                if rivi[0] == "nayton resoluutio":
                    tieto = rivi[1].split("*")
                    self.__x = int(tieto[0])
                    self.__y = int(tieto[1])
                elif rivi[0] == "ikkunan koko":
                    self.__koko = int(rivi[1])
                elif rivi[0] == "viive":
                    self.__viive = int(rivi[1])
                elif rivi[0] == "loppu":
                    lue.close()
                    break
        except IndexError:
            self.__lukeminen_onnistui = False
            return
        except ValueError:
            self.__lukeminen_onnistui = False
            return
        except OSError:
            self.__lukeminen_onnistui = False
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
