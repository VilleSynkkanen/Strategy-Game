from PyQt5 import QtWidgets, QtGui, QtCore

class Yksikkografiikka(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, luokka, ruutu, kayttoliittyma, omistaja, yksikko):
        super(Yksikkografiikka, self).__init__()
        # yksikön tyyppi luetaan sen luokan nimestä
        tyyppi = luokka.__class__.__name__
        self.yksikko = yksikko
        self.koko = ruutu.kartta.ruudun_koko
        self.ruutu = ruutu
        self.kayttoliittyma = kayttoliittyma
        self.omistaja = omistaja

        # eri tilanteissa käytettävien värien määrittely
        self.tietokoneen_vari = QtGui.QBrush(QtGui.QColor(155, 0, 0))
        self.pelaajan_vari = QtGui.QBrush(QtGui.QColor(0, 0, 155))
        self.pelaaja_valittu_vari = QtGui.QBrush(QtGui.QColor(0, 0, 255))

        # brush
        if self.omistaja == "COM":
            self.muuta_varia(self.tietokoneen_vari)
        else:
            self.muuta_varia(self.pelaajan_vari)


        if tyyppi == "Jalkavaki":
            self.piirra_jalkavaki()
        elif tyyppi == "Ratsuvaki":
            self.piirra_ratsuvaki()
        elif tyyppi == "Jousimiehet":
            self.piirra_jousimiehet()
        elif tyyppi == "Tykisto":
            self.piirra_tykisto()
        elif tyyppi == "Parantaja":
            self.piirra_parantaja()

        # Set the origin of transformations to the center of the triangle.
        # This makes it easier to rotate this Item.
        self.setTransformOriginPoint(self.koko / 2, self.koko / 2)

        self.setPos(self.ruutu.koordinaatit.x * self.koko, self.ruutu.koordinaatit.y * self.koko)
        self.kayttoliittyma.scene.addItem(self)

    def piirra_jalkavaki(self):
        # Create a new QPolygon object
        polygoni = QtGui.QPolygonF()

        a = self.koko

        r = self.koko / 4

        # Add the corners of a triangle to the the polygon object
        polygoni.append(QtCore.QPointF(r, 0))
        polygoni.append(QtCore.QPointF(2 * r, r))
        polygoni.append(QtCore.QPointF(3 * r, 0))
        polygoni.append(QtCore.QPointF(a, r))
        polygoni.append(QtCore.QPointF(3 * r, 2 * r))
        polygoni.append(QtCore.QPointF(a, 3 * r))
        polygoni.append(QtCore.QPointF(3 * r, a))
        polygoni.append(QtCore.QPointF(2 * r, 3 * r))
        polygoni.append(QtCore.QPointF(r, a))
        polygoni.append(QtCore.QPointF(0, 3 * r))
        polygoni.append(QtCore.QPointF(r, 2 * r))
        polygoni.append(QtCore.QPointF(0, r))

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(polygoni)

    def piirra_ratsuvaki(self):
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        a = self.koko
        r = self.koko / 4

        # Add the corners of a triangle to the the polygon object
        triangle.append(QtCore.QPointF(0, 3 * r))
        triangle.append(QtCore.QPointF(3 * r, 0))
        triangle.append(QtCore.QPointF(a, r))
        triangle.append(QtCore.QPointF(r, a))

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle)

    def piirra_jousimiehet(self):
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        a = self.koko
        r = self.koko / 4

        # Add the corners of a triangle to the the polygon object
        triangle.append(QtCore.QPointF(2 * r, 0))
        triangle.append(QtCore.QPointF(a, 2 * r))
        triangle.append(QtCore.QPointF(3 * r, 2 * r))
        triangle.append(QtCore.QPointF(3 * r, a))
        triangle.append(QtCore.QPointF(r, a))
        triangle.append(QtCore.QPointF(r, 2 * r))
        triangle.append(QtCore.QPointF(0, 2 * r))


        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle)

    def piirra_tykisto(self):
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        a = self.koko
        r = self.koko / 4

        # Add the corners of a triangle to the the polygon object
        triangle.append(QtCore.QPointF(r, 0))
        triangle.append(QtCore.QPointF(3 * r, 0))
        triangle.append(QtCore.QPointF(3 * r, 2 * r))
        triangle.append(QtCore.QPointF(a, 3 * r))
        triangle.append(QtCore.QPointF(3 * r, a))
        triangle.append(QtCore.QPointF(r, a))
        triangle.append(QtCore.QPointF(0, 3 * r))
        triangle.append(QtCore.QPointF(r, 2 * r))

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle)

    def piirra_parantaja(self):
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        a = self.koko
        r = self.koko / 4

        # Add the corners of a triangle to the the polygon object
        triangle.append(QtCore.QPointF(0, 0))
        triangle.append(QtCore.QPointF(r, r))
        triangle.append(QtCore.QPointF(3 * r, r))
        triangle.append(QtCore.QPointF(a, 0))
        triangle.append(QtCore.QPointF(a, a))
        triangle.append(QtCore.QPointF(3 * r, 3 * r))
        triangle.append(QtCore.QPointF(r, 3 * r))
        triangle.append(QtCore.QPointF(0, a))

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle)

    def muuta_varia(self, vari):        # vari = QColor
        brush = QtGui.QBrush(vari)
        self.setBrush(brush)

    def palauta_vari(self):
        if self.omistaja == "COM":
            brush = QtGui.QBrush(self.tietokoneen_vari_vari)
        else:
            brush = QtGui.QBrush(self.pelaajan_vari)
        self.setBrush(brush)

    def paivita_sijainti(self, ruutu):
        self.ruutu = ruutu
        self.setPos(self.ruutu.koordinaatit.x * self.koko, self.ruutu.koordinaatit.y * self.koko)

    def mousePressEvent(self, *args, **kwargs):
        if self.yksikko.omistaja == "PLR":
            self.kayttoliittyma.valitse_yksikko(self.yksikko)

