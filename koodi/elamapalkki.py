from PyQt5 import QtWidgets, QtGui, QtCore

class Elamapalkki(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, koko, ylaosan_koko, kayttoliittyma, yksikko):
        super(Elamapalkki, self).__init__()
        self.koko = koko
        self.ylaosan_koko = ylaosan_koko
        self.kayttoliittyma = kayttoliittyma
        self.vari = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        self.yksikko = yksikko

        # piirrä palkki
        self.paivita_koko()

        brush = QtGui.QBrush(self.vari)
        self.setBrush(brush)

    def paivita_sijainti(self):
        self.setPos(self.yksikko.ruutu.koordinaatit.x * self.koko, self.yksikko.ruutu.koordinaatit.y * self.koko)

    def paivita_koko(self):
        a = self.koko
        r = self.koko / 4

        elama = self.yksikko.ominaisuudet.nyk_elama / self.yksikko.ominaisuudet.max_elama

        elamapalkki = QtGui.QPolygonF()
        elamapalkki.append(QtCore.QPointF(0, self.ylaosan_koko * a))
        elamapalkki.append(QtCore.QPointF(a * elama, self.ylaosan_koko * a))
        elamapalkki.append(QtCore.QPointF(a * elama, a))
        elamapalkki.append(QtCore.QPointF(0, a))

        self.setPolygon(elamapalkki)
        self.setTransformOriginPoint(self.koko / 2, self.koko / 2)
        self.paivita_sijainti()
        self.kayttoliittyma.scene.addItem(self)