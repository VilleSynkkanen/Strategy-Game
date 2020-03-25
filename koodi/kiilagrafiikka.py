from PyQt5 import QtWidgets, QtGui, QtCore, Qt

class Kiilagrafiikka(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, ruutu):
        super(Kiilagrafiikka, self).__init__()
        self._koko = ruutu.kartta.ruudun_koko
        self._ruutu = ruutu
        self._kayttoliittyma = self._ruutu.kayttoliittyma
        self._vari = QtGui.QBrush(QtGui.QColor(140, 70, 20))

        polygoni = QtGui.QPolygonF()

        a = self._koko
        r = self._koko / 8

        polygoni.append(QtCore.QPointF(2*r, 0))
        polygoni.append(QtCore.QPointF(3*r, 2*r))
        polygoni.append(QtCore.QPointF(3*r, a))
        polygoni.append(QtCore.QPointF(5*r, a))
        polygoni.append(QtCore.QPointF(5*r, 2*r))
        polygoni.append(QtCore.QPointF(6*r, 0))
        polygoni.append(QtCore.QPointF(7*r, 2*r))
        polygoni.append(QtCore.QPointF(7*r, a))
        polygoni.append(QtCore.QPointF(r, a))
        polygoni.append(QtCore.QPointF(r, 2*r))

        self.setPolygon(polygoni)

        brush = QtGui.QBrush(self._vari)
        self.setBrush(brush)

        # origin piste keskelle
        self.setTransformOriginPoint(self._koko / 2, self._koko / 2)
        # aseta yksikön ja ruudun väliin
        self.setZValue(-1)
        self.setPos(self._ruutu.koordinaatit.x * self._koko, self._ruutu.koordinaatit.y * self._koko)
        self._kayttoliittyma.scene.addItem(self)

    def poista(self):
        polygoni = QtGui.QPolygonF()

        a = self._koko
        r = self._koko / 8

        polygoni.append(QtCore.QPointF(0, 0))
        polygoni.append(QtCore.QPointF(0, 0))
        polygoni.append(QtCore.QPointF(0, 0))

        self.setPolygon(polygoni)