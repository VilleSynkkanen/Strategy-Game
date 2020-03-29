from PyQt5 import QtWidgets, QtGui, QtCore, Qt


class Elamapalkki(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, koko, ylaosan_koko, kayttoliittyma, yksikko):
        super(Elamapalkki, self).__init__()
        self.__koko = koko
        self.__ylaosan_koko = ylaosan_koko
        self.__kayttoliittyma = kayttoliittyma
        self.__vari = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        self.__vaikutus_vari = QtGui.QBrush(QtGui.QColor(115, 0, 115))
        self.__yksikko = yksikko

        # piirrä palkki
        self.paivita_koko()

        brush = QtGui.QBrush(self.__vari)
        self.setBrush(brush)

    def paivita_sijainti(self):
        self.setPos(self.__yksikko.ruutu.koordinaatit.x * self.__koko, self.__yksikko.ruutu.koordinaatit.y * self.__koko)

    def paivita_koko(self):
        a = self.__koko
        r = self.__koko / 4

        elama = self.__yksikko.ominaisuudet.nyk_elama / self.__yksikko.ominaisuudet.max_elama

        elamapalkki = QtGui.QPolygonF()
        elamapalkki.append(QtCore.QPointF(0, self.__ylaosan_koko * a))
        elamapalkki.append(QtCore.QPointF(a * elama, self.__ylaosan_koko * a))
        elamapalkki.append(QtCore.QPointF(a * elama, a))
        elamapalkki.append(QtCore.QPointF(0, a))

        self.setPolygon(elamapalkki)
        self.setTransformOriginPoint(self.__koko / 2, self.__koko / 2)
        self.paivita_sijainti()
        self.__kayttoliittyma.scene.addItem(self)

    def poista(self):
        elamapalkki = QtGui.QPolygonF()
        self.setPolygon(elamapalkki)
        self.setTransformOriginPoint(self.__koko / 2, self.__koko / 2)

    # palkin väri muuttuu ja palkki saa tooltipin, kun yksiköllä on jokin tilavaikutus
    def paivita_tilavaikutukset(self):
        if len(self.__yksikko.ominaisuudet.tilavaikutukset) != 0:
            brush = QtGui.QBrush(self.__vaikutus_vari)
            self.setBrush(brush)
            # yhteisten tilavaikutusten haku
            hyokkays, puolustus, liikkuminen, verenvuoto, taintuminen = \
                self.__yksikko.ominaisuudet.tilavaikutukset_yhteensa()
            if taintuminen is True:
                taintuminen = "kyllä"
            else:
                taintuminen = "ei"
            self.__aseta_tooltip("Tilavaikutukset:\nHyökkäys: {}\nPuolustus: {}\nLiikkuminen: {}\nVerenvuoto: {}\n"
                                 "Taintunut: {}".format(hyokkays, puolustus, liikkuminen, verenvuoto, taintuminen))
        else:
            brush = QtGui.QBrush(self.__vari)
            self.setBrush(brush)
            self.__aseta_tooltip("")

    def __aseta_tooltip(self, teksti):
        QtWidgets.QToolTip.setFont(Qt.QFont('SansSerif', 10))
        self.setToolTip(teksti)
