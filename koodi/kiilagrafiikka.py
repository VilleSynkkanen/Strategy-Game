from PyQt5 import QtWidgets, QtGui, QtCore, Qt

class Kiilagrafiikka(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, ruutu):
        super(Kiilagrafiikka, self).__init__()
        self.koko = ruutu.kartta.ruudun_koko
        self.ruutu = ruutu
        self.kayttoliittyma = self.ruutu.kayttoliittyma
        self.vari = QtGui.QBrush(QtGui.QColor(140, 70, 20))

        polygoni = QtGui.QPolygonF()

        a = self.koko
        r = self.koko / 8

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

        brush = QtGui.QBrush(self.vari)
        self.setBrush(brush)

        # origin piste keskelle
        self.setTransformOriginPoint(self.koko / 2, self.koko / 2)
        # aseta yksikön ja ruudun väliin
        self.setZValue(-1)
        self.setPos(self.ruutu.koordinaatit.x * self.koko, self.ruutu.koordinaatit.y * self.koko)
        self.kayttoliittyma.scene.addItem(self)

    def poista(self):
        polygoni = QtGui.QPolygonF()

        a = self.koko
        r = self.koko / 8

        polygoni.append(QtCore.QPointF(0, 0))
        polygoni.append(QtCore.QPointF(0, 0))
        polygoni.append(QtCore.QPointF(0, 0))

        self.setPolygon(polygoni)