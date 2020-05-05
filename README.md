# Strategiapeli Y2

## Tiedosto- ja kansiorakenne

  - Repository on jaettu kahteen pääkansioon: koodi ja dokumentaatio
  - Koodi-kansiosta löytyy projektin lähdekoodi ja pelin käyttämät tiedostot
  - Maastot-, yksiköt- ja muut-kansioista löytyy asetustiedostot, joita muokkaamalla peliä voi konfiguroida
  - Pelikentät löytyvät kartat-kansiosta
  - Tallennettu pelitilanne löytyy pelitilanne-kansiosta
  - Dokumentaatio-kansiosta löytyy alkuperäiset suunnitelmat suunnitelmat-kansiosta ja ohjelman dokumentaatio loppudokumentaatio-kansiosta
  - Polunhakualgoritmi perustuu osittain netistä löydettyyn koodiin (tarkempi selitys koodin kommenteissa)
  - Muuten koodi on itse kirjoitettua

## Asennusohje

  - Ohjelma tarvitsee toimiakseen PyQt5-kirjaston.
  - Käytetty Python-versio on 3.8, mutta hieman vanhempikin versio pitäisi toimia

## Käyttöohje

  - Ohjelma käynnistetään ajamalla main.py-tiedosto komentoriviltä tai IDE:stä käsin
  - Asetustiedostoista pystyy muokkaamaan kaksoispisteiden jälkeisiä kohtia (pitäisi olla intuitiivistä)
  - Karttojen muokkaus suoraan tiedostojen avulla on mahdollista, mutta suositeltavaa on käyttää kenttäeditoria
  - Tallennettua peliä pystyy myös muokkamaan halutessaan tiedoston kautta
  - Jos tallennustiedostoa muokkaa, se tulee sulkea kokonaan ennen ohjelman käynnistämistä
  - Asetustiedostojen muokkauksen jälkeen ohjelma tulee käynnistää uudestaan, jotta muutokset tulevat voimaan
