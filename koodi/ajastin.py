from PyQt5 import QtCore
from functools import partial


class Ajastin:

    @staticmethod
    def aloita_ajastin(aika, metodi):
        ajastin = QtCore.QTimer()
        ajastin.timeout.connect(partial(Ajastin.__ajastin_pysaytys, ajastin, metodi))
        ajastin.start(aika)

    @staticmethod
    def __ajastin_pysaytys(ajastin, metodi):
        ajastin.stop()
        ajastin.deleteLater()
        metodi()
