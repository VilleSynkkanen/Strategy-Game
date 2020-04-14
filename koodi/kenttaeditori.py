from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from kartta import Kartta
import sys


class Kenttaeditori(QtWidgets.QMainWindow):

    def __init__(self, paavalikko):
        super().__init__()
        self.__scene_size = 880       # kentän koko pikseleinä
        self.__paavalikko = paavalikko

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
        # main_layout.addStretch()

        self.__nappi_layout = QtWidgets.QGridLayout()
        self.__paa_layout.addLayout(self.__nappi_layout)

        # napit
        self.__uusi_kentta_nappi = QtWidgets.QPushButton("UUSI KENTTÄ")
        self.__uusi_kentta_nappi.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__muokkaa_vanhaa_nappi = QtWidgets.QPushButton("MUOKKAA KENTTÄÄ")
        self.__muokkaa_vanhaa_nappi.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__vaihda_nappien_sisalto = QtWidgets.QPushButton("YKSIKÖT/MAASTOT")
        self.__vaihda_nappien_sisalto.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__tasanko_nappi = QtWidgets.QPushButton("TASANKO")
        self.__tasanko_nappi.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__kukkula_nappi = QtWidgets.QPushButton("KUKKULA")
        self.__kukkula_nappi.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__pelto_nappi = QtWidgets.QPushButton("PELTO")
        self.__pelto_nappi.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__vuoristo_nappi = QtWidgets.QPushButton("VUORISTO")
        self.__vuoristo_nappi.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__silta_nappi = QtWidgets.QPushButton("SILTA")
        self.__silta_nappi.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__joki_nappi = QtWidgets.QPushButton("JOKI")
        self.__joki_nappi.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__vahvista_koko = QtWidgets.QPushButton("VAHVISTA KOKO")
        self.__vahvista_koko.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.__leveys = QtWidgets.QLineEdit()
        self.__leveys.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__korkeus = QtWidgets.QLineEdit()
        self.__korkeus.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.__napit = []
        self.__napit.append(self.__uusi_kentta_nappi)
        self.__napit.append(self.__muokkaa_vanhaa_nappi)
        self.__napit.append(self.__vaihda_nappien_sisalto)
        self.__napit.append(self.__tasanko_nappi)
        self.__napit.append(self.__kukkula_nappi)
        self.__napit.append(self.__pelto_nappi)
        self.__napit.append(self.__vuoristo_nappi)
        self.__napit.append(self.__silta_nappi)
        self.__napit.append(self.__joki_nappi)
        self.__napit.append(self.__vahvista_koko)

        self.__uusi_kentta_nappi.setStyleSheet("font: 10pt Arial")
        self.__muokkaa_vanhaa_nappi.setStyleSheet("font: 10pt Arial")
        self.__vaihda_nappien_sisalto.setStyleSheet("font: 10pt Arial")
        self.__tasanko_nappi.setStyleSheet("font: 10pt Arial")
        self.__kukkula_nappi.setStyleSheet("font: 10pt Arial")
        self.__pelto_nappi.setStyleSheet("font: 10pt Arial")
        self.__vuoristo_nappi.setStyleSheet("font: 10pt Arial")
        self.__silta_nappi.setStyleSheet("font: 10pt Arial")
        self.__joki_nappi.setStyleSheet("font: 10pt Arial")
        self.__vahvista_koko.setStyleSheet("font: 10pt Arial")
        self.__leveys.setStyleSheet("font: 10pt Arial")
        self.__korkeus.setStyleSheet("font: 10pt Arial")

        # nappi widgetit
        self.__nappi_layout.addWidget(self.__uusi_kentta_nappi, 0, 0)
        self.__nappi_layout.addWidget(self.__muokkaa_vanhaa_nappi, 0, 1)
        self.__nappi_layout.addWidget(self.__vaihda_nappien_sisalto, 1, 0)
        self.__nappi_layout.addWidget(self.__tasanko_nappi, 2, 0)
        self.__nappi_layout.addWidget(self.__kukkula_nappi, 2, 1)
        self.__nappi_layout.addWidget(self.__pelto_nappi, 3, 0)
        self.__nappi_layout.addWidget(self.__vuoristo_nappi, 3, 1)
        self.__nappi_layout.addWidget(self.__silta_nappi, 4, 0)
        self.__nappi_layout.addWidget(self.__joki_nappi, 4, 1)
        self.__nappi_layout.addWidget(self.__vahvista_koko, 5, 0)
        self.__nappi_layout.addWidget(self.__leveys, 6, 0)
        self.__nappi_layout.addWidget(self.__korkeus, 6, 1)

        self.__vahvista_koko.clicked.connect(self.__lue_koko)
        self.__tasanko_nappi.clicked.connect(self.valitse_tasanko)
        self.__pelto_nappi.clicked.connect(self.valitse_pelto)
        self.__vuoristo_nappi.clicked.connect(self.valitse_vuoristo)
        self.__kukkula_nappi.clicked.connect(self.valitse_kukkula)
        self.__silta_nappi.clicked.connect(self.valitse_silta)
        self.__joki_nappi.clicked.connect(self.valitse_joki)

        self.__koko_x = 0
        self.__koko_y = 0

        self.__kartta = None

        # maasto tai yksikkö
        self.__valittu_elementti = None

    @property
    def scene(self):
        return self.__scene

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
    def scene_size(self):
        return self.__scene_size

    @property
    def valittu_elementti(self):
        return self.__valittu_elementti

    @property
    def kartta(self):
        return self.__kartta

    def __aseta_scene_rect(self, x, y):
        # rectin skaalauskertoimet
        if x > y:
            y /= x
            x = 1
        else:
            x /= y
            y = 1
        self.__scene.setSceneRect(0, 0, self.__scene_size * x, self.__scene_size * y)
        #self.setGeometry(0, 0, self.scene_size * x + 420, self.scene_size * y + 20)

        # keskelle liikuttaminen
        res_x = 1920
        res_y = 1080
        self.move(int(res_x / 2) - int(self.frameSize().width() / 2),
                  int(res_y / 2) - int(self.frameSize().height() / 2))

    def __lue_koko(self):
        try:
            self.__koko_x = int(self.__leveys.text())
            self.__koko_y = int(self.__korkeus.text())
            print(self.__koko_x)
            print(self.__koko_y)
            self.__piirra_tyhja_kartta()
        except ValueError:
            print("invalid value")

    # piirtää tyhjän kartan, jonka mitat ovat koko_x ja koko_y
    def __piirra_tyhja_kartta(self):
        self.__tyhjenna_kartta()
        ruudut = [["tasanko" for i in range(self.__koko_y)] for j in range(self.__koko_x)]
        self.__kartta = Kartta(self.__koko_x, self.__koko_y, ruudut, self)

        for ruutu in self.__kartta.ruudut:
            ruutu.luo_maasto(True)
            ruutu.luo_grafiikka(self.__kartta.ruudun_koko, True)

        self.__aseta_scene_rect(self.__koko_x, self.__koko_y)

    def __tyhjenna_kartta(self):
        # implementoi kartan tyhjennys
        pass

    def valitse_tasanko(self):
        self.__valittu_elementti = "tasanko"
        print(self.__valittu_elementti)

    def valitse_kukkula(self):
        self.__valittu_elementti = "kukkula"
        print(self.__valittu_elementti)

    def valitse_pelto(self):
        self.__valittu_elementti = "pelto"
        print(self.__valittu_elementti)

    def valitse_vuoristo(self):
        self.__valittu_elementti = "vuoristo"
        print(self.__valittu_elementti)

    def valitse_joki(self):
        self.__valittu_elementti = "joki"
        print(self.__valittu_elementti)

    def valitse_silta(self):
        self.__valittu_elementti = "silta"
        print(self.__valittu_elementti)

    def muuta_nappien_toiminnot(self, tyyppi):
        pass

