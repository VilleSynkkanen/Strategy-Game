from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from elamapalkki import Elamapalkki

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
        self.ylaosan_koko = 0.75        # alas jää 1 - ylaosan_koko ruutua elämänpalkille

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

        # luo elämäpalkki
        self.elamapalkki = Elamapalkki(self.koko, self.ylaosan_koko, self.kayttoliittyma, self.yksikko)

        # luo tooltip
        self.aseta_tooltip(self.yksikko.__class__.__name__ +"\nElämä : " + str(self.yksikko.ominaisuudet.nyk_elama) +
                           "/" + str(self.yksikko.ominaisuudet.max_elama) + "\nEnergia: " + 
                           str(self.yksikko.ominaisuudet.nyk_energia) + "/" + str(self.yksikko.ominaisuudet.max_energia))

    def piirra_jalkavaki(self):
        # Create a new QPolygon object
        polygoni = QtGui.QPolygonF()

        a = self.koko

        r = self.koko / 4

        # Add the corners of a triangle to the the polygon object
        polygoni.append(QtCore.QPointF(r, 0))
        polygoni.append(QtCore.QPointF(2 * r, r * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 0))
        polygoni.append(QtCore.QPointF(a, r * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 2 * r * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(a, 3 * r * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, a * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(2 * r, 3 * r * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, a * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, 3 * r * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, 2 * r * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(0, r * self.ylaosan_koko))

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(polygoni)

    def piirra_ratsuvaki(self):
        # Create a new QPolygon object
        polygoni = QtGui.QPolygonF()

        a = self.koko
        r = self.koko / 4

        # Add the corners of a triangle to the the polygon object
        polygoni.append(QtCore.QPointF(0, 3 * r * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(3 * r, 0))
        polygoni.append(QtCore.QPointF(a, r * self.ylaosan_koko))
        polygoni.append(QtCore.QPointF(r, a * self.ylaosan_koko))

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(polygoni)

    def piirra_jousimiehet(self):
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        a = self.koko
        r = self.koko / 4

        # Add the corners of a triangle to the the polygon object
        triangle.append(QtCore.QPointF(2 * r, 0))
        triangle.append(QtCore.QPointF(a, 2 * r * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(3 * r, 2 * r * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(3 * r, a * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(r, a * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(r, 2 * r * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(0, 2 * r * self.ylaosan_koko))


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
        triangle.append(QtCore.QPointF(3 * r, 2 * r * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(a, 3 * r * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(3 * r, a * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(r, a * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(0, 3 * r * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(r, 2 * r * self.ylaosan_koko))

        # Set this newly created polygon as this Item's polygon.
        self.setPolygon(triangle)

    def piirra_parantaja(self):
        # Create a new QPolygon object
        triangle = QtGui.QPolygonF()

        a = self.koko
        r = self.koko / 4

        # Add the corners of a triangle to the the polygon object
        triangle.append(QtCore.QPointF(0, 0))
        triangle.append(QtCore.QPointF(r, r * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(3 * r, r * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(a, 0))
        triangle.append(QtCore.QPointF(a, a * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(3 * r, 3 * r * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(r, 3 * r * self.ylaosan_koko))
        triangle.append(QtCore.QPointF(0, a * self.ylaosan_koko))

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
        self.elamapalkki.paivita_sijainti()

    def aseta_tooltip(self, teksti):
        QtWidgets.QToolTip.setFont(Qt.QFont('SansSerif', 10))
        self.setToolTip(teksti)

    def mousePressEvent(self, *args, **kwargs):
        if self.yksikko.omistaja == "PLR":
            self.kayttoliittyma.valitse_yksikko(self.yksikko)

