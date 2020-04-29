from PyQt5 import QtWidgets
from kartta import Kartta
from pelinohjain import Pelinohjain


class Pelaa_valikko(QtWidgets.QMainWindow):

    def __init__(self, paavalikko):
        super(Pelaa_valikko, self).__init__()
        self.__scene_size = paavalikko.scene_size  # kentän koko pikseleinä
        self.__paavalikko = paavalikko
        self.__viive = 1400

        self.setCentralWidget(QtWidgets.QWidget())  # QMainWindown must have a centralWidget to be able to add layouts
        self.__paa_layout = QtWidgets.QHBoxLayout()  # Horizontal main layout
        self.centralWidget().setLayout(self.__paa_layout)

        # set window
        self.setGeometry(0, 0, self.__scene_size + 420, self.__scene_size + 20)
        self.setWindowTitle('Strategiapeli')
        self.show()

        # Add a scene for drawing 2d objects
        self.__scene = QtWidgets.QGraphicsScene()

        # Add a view for showing the scene
        self.__nakyma = QtWidgets.QGraphicsView(self.__scene, self)
        self.__nakyma.adjustSize()
        self.__nakyma.show()
        self.__paa_layout.addWidget(self.__nakyma)

        self.__nappi_layout = QtWidgets.QGridLayout()
        self.__paa_layout.addLayout(self.__nappi_layout)

        # widgetit
        self.__seuraava_kentta_nappi = QtWidgets.QPushButton("SEURAAVA KENTTÄ")
        self.__seuraava_kentta_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__edellinen_kentta_nappi = QtWidgets.QPushButton("EDELLINEN KENTTÄ")
        self.__edellinen_kentta_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__valitse_kentta = QtWidgets.QPushButton("VALITSE KENTTÄ")
        self.__valitse_kentta.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.__poistu_nappi = QtWidgets.QPushButton("POISTU VALIKOSTA")
        self.__poistu_nappi.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.__seuraava_kentta_nappi.setStyleSheet("font: 10pt Arial")
        self.__edellinen_kentta_nappi.setStyleSheet("font: 10pt Arial")
        self.__poistu_nappi.setStyleSheet("font: 10pt Arial")
        self.__valitse_kentta.setStyleSheet("font: 10pt Arial")

        self.__nappi_layout.addWidget(self.__seuraava_kentta_nappi, 0, 1)
        self.__nappi_layout.addWidget(self.__edellinen_kentta_nappi, 0, 0)
        self.__nappi_layout.addWidget(self.__valitse_kentta, 1, 0)
        self.__nappi_layout.addWidget(self.__poistu_nappi, 1, 1)

        self.__seuraava_kentta_nappi.clicked.connect(self.__seuraava)
        self.__edellinen_kentta_nappi.clicked.connect(self.__edellinen)
        self.__valitse_kentta.clicked.connect(self.__valitse)
        self.__poistu_nappi.clicked.connect(self.__poistu)

        self.__pelinohjain = None
        self.__kartta = None
        self.__valittu_elementti = None
        self.__koko_x = 0
        self.__koko_y = 0
        self.__kartta_index = 0
        self.__kartat = list(self.__paavalikko.kartan_lukija.kartat.keys())
        self.__piirra_kartta(self.__kartat[self.__kartta_index])
        self.__valitse_kentta.setText("VALITSE\n" + self.__kartat[self.__kartta_index])

    @property
    def paavalikko(self):
        return self.__paavalikko

    @property
    def koko_x(self):
        return self.__koko_x

    @property
    def koko_y(self):
        return self.__koko_y

    @property
    def kartat(self):
        return self.__kartat

    @property
    def scene_size(self):
        return self.__scene_size

    @property
    def scene(self):
        return self.__scene

    @property
    def kartta(self):
        return self.__kartta

    @property
    def valittu_elementti(self):
        return self.__valittu_elementti

    def __aseta_scene_rect(self, x, y):
        # rectin skaalauskertoimet
        if x > y:
            y /= x
            x = 1
        else:
            x /= y
            y = 1
        self.__scene.setSceneRect(0, 0, self.__scene_size * x, self.__scene_size * y)
        # self.setGeometry(0, 0, self.scene_size * x + 420, self.scene_size * y + 20)

        # keskelle liikuttaminen
        res_x = self.paavalikko.kayttoliittyman_lukija.x
        res_y = self.paavalikko.kayttoliittyman_lukija.y
        self.move(int(res_x / 2) - int(self.frameSize().width() / 2),
                  int(res_y / 2) - int(self.frameSize().height() / 2))

    def poista_pelinohjain(self):
        self.__pelinohjain = None


    def __piirra_kartta(self, nimi):
        x, y, ruudut, yksikot = self.__paavalikko.kartan_lukija.kartat[nimi]
        koko = (x, y)
        self.__koko_x = koko[0]
        self.__koko_y = koko[1]
        # print(ruudut)
        self.__kartta = Kartta(koko[0], koko[1], ruudut, self)

        self.__aseta_scene_rect(koko[0], koko[1])

        # tehdään vasta koko kartan luomisen jälkeen, kun kaikki ruudut ovat paikallaan
        for ruutu in self.__kartta.ruudut:
            ruutu.luo_maasto()
            ruutu.luo_grafiikka()
            ruutu.etsi_kartta()

        self.__kartta.lisaa_yksikot(yksikot, self.__paavalikko.yksikoiden_lukija.yksikot)

    def __seuraava(self):
        self.kartta.tyhjenna()
        self.__kartta_index += 1
        if self.__kartta_index == len(self.__kartat):
            self.__kartta_index = 0
        self.__piirra_kartta(self.__kartat[self.__kartta_index])
        self.__valitse_kentta.setText("VALITSE\n" + self.__kartat[self.__kartta_index])

    def __edellinen(self):
        self.kartta.tyhjenna()
        self.__kartta_index -= 1
        if self.__kartta_index == -1:
            self.__kartta_index = len(self.__kartat) - 1
        self.__piirra_kartta(self.__kartat[self.__kartta_index])
        self.__valitse_kentta.setText("VALITSE\n" + self.__kartat[self.__kartta_index])

    def __valitse(self):
        self.__pelinohjain = Pelinohjain(self.__kartat[self.__kartta_index], self.__paavalikko)
        self.hide()

    def __poistu(self):
        self.paavalikko.show()
        self.hide()
