from PyQt5 import QtWidgets, QtGui

class Yksikkografiikka(QtWidgets.QGraphicsPolygonItem):

    def __init__(self, luokka, yksikko, koko, ruutu):
        super(Yksikkografiikka, self).__init__()
        # yksikön tyyppi luetaan sen luokan nimestä
        tyyppi = luokka.__class__.__name__
        self.koko = koko
        self.ruutu = ruutu

        # brush
        brush = QtGui.QBrush(1)  # 1 for even fill
        self.setBrush(brush)

        if tyyppi == "Jalkavaki":
            self.piirra_jalkavaki()
        elif tyyppi == "Ratsuvaki":
            self.piirra_ratsuvaki()
        elif tyyppi == "Jousimiehet":
            self.piirra_jousimiehet()
        elif tyyppi == "Tykistö":
            self.piirra_tykisto()
        elif tyyppi == "Parantaja":
            self.piirra_parantaja()

    def piirra_jalkavaki(self):
        pass

    def piirra_ratsuvaki(self):
        pass

    def piirra_jousimiehet(self):
        pass

    def piirra_tykisto(self):
        pass

    def piirra_parantaja(self):
        pass

