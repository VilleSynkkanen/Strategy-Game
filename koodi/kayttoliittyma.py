from PyQt5 import QtWidgets, QtCore, QtGui, Qt

class Kayttoliittyma(QtWidgets.QMainWindow):
    '''
    The class GUI handles the drawing of the board and buttons
    '''
    def __init__(self, pelinohjain):
        super().__init__()
        self.scene_size = 880       #kentän koko pikseleinä
        self.pelinohjain = pelinohjain
        self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
        main_layout = QtWidgets.QHBoxLayout()  # Horizontal main layout
        self.centralWidget().setLayout(main_layout)

        # set window
        self.setGeometry(0, 0, self.scene_size + 420, self.scene_size)
        self.setWindowTitle('Strategiapeli')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()

        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        main_layout.addWidget(self.view)
        # main_layout.addStretch()

        button_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(button_layout)

        # buttons
        button1 = QtWidgets.QPushButton("HYÖKKÄÄ")
        button1.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button2 = QtWidgets.QPushButton("KYKY 1")
        button2.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button3 = QtWidgets.QPushButton("KYKY 2")
        button3.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button4 = QtWidgets.QPushButton("PERU VALINTA")
        button4.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button5 = QtWidgets.QPushButton("YKSIKÖN TIEDOT")
        button5.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button6 = QtWidgets.QPushButton("EDELLINEN YKSIKKÖ")
        button6.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button7 = QtWidgets.QPushButton("SEURAAVA YKSIKKÖ")
        button7.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button8 = QtWidgets.QPushButton("PÄÄTÄ VUORO")
        button8.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button9 = QtWidgets.QPushButton("TALLENNA PELI")
        button9.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        button1.setStyleSheet("font: 10pt Arial")
        button2.setStyleSheet("font: 10pt Arial")
        button3.setStyleSheet("font: 10pt Arial")
        button4.setStyleSheet("font: 10pt Arial")
        button5.setStyleSheet("font: 10pt Arial")
        button6.setStyleSheet("font: 10pt Arial")
        button7.setStyleSheet("font: 10pt Arial")
        button8.setStyleSheet("font: 10pt Arial")
        button9.setStyleSheet("font: 10pt Arial")

        # connect button to function
        button1.clicked.connect(self.test1)

        # add button widgets
        button_layout.addWidget(button1, 0, 0, 1, 2)
        button_layout.addWidget(button2, 1, 0)
        button_layout.addWidget(button3, 1, 1)
        button_layout.addWidget(button4, 2, 0)
        button_layout.addWidget(button5, 2, 1)
        button_layout.addWidget(button6, 3, 0)
        button_layout.addWidget(button7, 3, 1)
        button_layout.addWidget(button8, 4, 0)
        button_layout.addWidget(button9, 4, 1)

        # unit info
        health = QtWidgets.QLabel("ELÄMÄ: 100/100")
        energy = QtWidgets.QLabel("ENERGIA: 5/5")
        button_layout.addWidget(health, 5, 0, 1, 1)
        button_layout.addWidget(energy, 5, 1, 1, 1)
        health.setStyleSheet("font: 10pt Arial")
        energy.setStyleSheet("font: 10pt Arial")
        health.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        energy.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # game log test
        label = QtWidgets.QLabel("PELILOKI:\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"                                      
                                 "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n", self)
        button_layout.addWidget(label,6, 0, 6, 2, alignment=QtCore.Qt.AlignTop)
        label.setStyleSheet("font: 10pt Arial")

        ohjeteksti = QtWidgets.QLabel("OHJETEKSTI\n"
                                      "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                      "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                      "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                      "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                      "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
                                      "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n", self)
        button_layout.addWidget(ohjeteksti, 11, 0, 1, 0, alignment=QtCore.Qt.AlignTop)
        ohjeteksti.setStyleSheet("font: 10pt Arial")

    def set_scene_rect(self, x, y):
        # rectin skaalauskertoimet
        if x > y:
            y /= x
            x = 1
        else:
            x /= y
            y = 1
        self.scene.setSceneRect(0, 0, self.scene_size * x, self.scene_size * y)
        #self.setGeometry(0, 0, self.scene_size * x + 420, self.scene_size * y + 20)

        # keskelle liikuttaminen
        res_x = 1920
        res_y = 1080
        self.move((res_x / 2) - (self.frameSize().width() / 2),
                  (res_y / 2) - (self.frameSize().height() / 2))


    def test1(self):
        print("test button 1")