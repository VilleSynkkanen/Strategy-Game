class Kartan_lukija:

    def __init__(self):
        self.ruudut = []
        self.yksikot = []
        self.lue_kartta()
        self.kartta_x = 20
        self.kartta_y = 16

        '''
        tallentaa lukemansa tiedot kaksiulotteiseen listaan (ruuduista), jossa
        jokainen jäsen on maaston tyyppi
        
        toinen lista yksiköistä 
        '''

    def lue_kartta(self):
        return self.ruudut  #placeholder, palauttaa tyhjän listan

    def koko_x(self):
        return self.kartta_x

    def koko_y(self):
        return self.kartta_y