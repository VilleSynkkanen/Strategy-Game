from yksikko import  Yksikko

class Ratsuvaki(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma):
        super().__init__(omistaja, ruutu, kayttoliittyma)
        self.luo_grafiikka()