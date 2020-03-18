from yksikko import  Yksikko

class Ratsuvaki(Yksikko):

    def __init__(self, omistaja, ruutu, kayttoliittyma, ominaisuudet):
        super().__init__(omistaja, ruutu, kayttoliittyma, ominaisuudet)
        self.luo_grafiikka()

    # passiivinen tehty

    def __str__(self):
        return "-Passiivinen kyky: voi liikkua myös\n" \
               " kyvyn käyttämisen/hyökkäyksen jälkeen\n" \
               "-Kyky 1(tiedustelu): Merkitsee kohteen.\n" \
               " Kohteen puolustus kärsii X vuoron ajan.\n" \
               "-Kyky 2(kolmiokiila): Menee kiilaan X vuoron\n" \
               " ajaksi. Kiilassa ollessaan puolustus vähenee\n" \
               " hiukan, mutta vahinko kasvaa merkittävästi"