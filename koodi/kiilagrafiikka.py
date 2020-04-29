from PyQt5 import QtWidgets, QtGui, QtCore


class Kiilagrafiikka(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, ruutu):
        super(Kiilagrafiikka, self).__init__()
        self.__koko = ruutu.grafiikka.koko
        self.__ruutu = ruutu
        self.__kayttoliittyma = self.__ruutu.kayttoliittyma
        self.__vari = QtGui.QBrush(QtGui.QColor(140, 70, 20))

        polygoni = QtGui.QPolygonF()

        a = self.__koko
        r = self.__koko / 8

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

        brush = QtGui.QBrush(self.__vari)
        self.setBrush(brush)

        # origin piste keskelle
        self.setTransformOriginPoint(self.__koko / 2, self.__koko / 2)

        # asettaa kiilan yksikön ja ruudun väliin
        self.setZValue(-1)
        self.setPos(self.__ruutu.koordinaatit.x * self.__koko, self.__ruutu.koordinaatit.y * self.__koko)
        self.__kayttoliittyma.scene.addItem(self)

    def poista(self):
        polygoni = QtGui.QPolygonF()

        a = self.__koko
        r = self.__koko / 8

        polygoni.append(QtCore.QPointF(0, 0))
        polygoni.append(QtCore.QPointF(0, 0))
        polygoni.append(QtCore.QPointF(0, 0))

        self.setPolygon(polygoni)
