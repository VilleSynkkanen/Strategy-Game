from PyQt5 import QtWidgets, QtGui, QtCore

class Elamapalkki(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, koko, ylaosan_koko, kayttoliittyma, yksikko):
        super(Elamapalkki, self).__init__()
        self._koko = koko
        self._ylaosan_koko = ylaosan_koko
        self._kayttoliittyma = kayttoliittyma
        self._vari = QtGui.QBrush(QtGui.QColor(230, 0, 0))
        self._yksikko = yksikko

        # piirrä palkki
        self.paivita_koko()

        brush = QtGui.QBrush(self._vari)
        self.setBrush(brush)

    def paivita_sijainti(self):
        self.setPos(self._yksikko.ruutu.koordinaatit.x * self._koko, self._yksikko.ruutu.koordinaatit.y * self._koko)

    def paivita_koko(self):
        a = self._koko
        r = self._koko / 4

        elama = self._yksikko.ominaisuudet.nyk_elama / self._yksikko.ominaisuudet.max_elama

        elamapalkki = QtGui.QPolygonF()
        elamapalkki.append(QtCore.QPointF(0, self._ylaosan_koko * a))
        elamapalkki.append(QtCore.QPointF(a * elama, self._ylaosan_koko * a))
        elamapalkki.append(QtCore.QPointF(a * elama, a))
        elamapalkki.append(QtCore.QPointF(0, a))

        self.setPolygon(elamapalkki)
        self.setTransformOriginPoint(self._koko / 2, self._koko / 2)
        self.paivita_sijainti()
        self._kayttoliittyma.scene.addItem(self)

    def poista(self):
        elamapalkki = QtGui.QPolygonF()
        self.setPolygon(elamapalkki)
        self.setTransformOriginPoint(self._koko / 2, self._koko / 2)
