from PyQt5 import QtCore


class Ajastin:

    def __init__(self):
        self.metodi = None
        self.timer = None

    def aloita_ajastin(self, aika, metodi):
        self.metodi = metodi
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.ajastin_pysaytys)
        self.timer.start(aika)

    def ajastin_pysaytys(self):
        self.timer.stop()
        self.timer.deleteLater()
        self.metodi()