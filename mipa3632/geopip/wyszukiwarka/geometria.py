# -*- coding: utf-8 -*-
import matplotlib.path as mplPath
import numpy as np

def diagnozuj(lista):
    print("RozpoczynamDiagnoze:\n")
    for i in lista:
        print("[",i,"]")
        #print("\n")
    print("Kończę diagnoze.\n")


def XY_from_WKTpoint(wkt_point):
    wspolrzedne={}
    wspolrzedne['X'],wspolrzedne['Y']=wkt_point.split("(")[1].split(")")[0].split(" ")
    return wspolrzedne
OBSZARY_SEKCJI_DO_SPRAWDZENIA=[u"NNK-A", u"NNK-C", u"PPP--A", u"Konin", u"Leszno", u"Ostrow",	u"Pila", u"NNK--B",  u"PPP-A", u"NLE--A",u"NLE-A", u"NNK-B"]
'''
NAZWY_OBSZAROW_SEKCJI_W_KOLEJNOSCI=[u"Poznań-NNK-A", u"Poznań-PPP-A", u"Poznań-NLE-A", u"Poznań-NNK-C", u"Poznań-NNK-B", u"Zbąszyń",	u"Opalenica",	u"Duszniki",	u"Wronki",
                                    u"Miedzichowo",	u"Międzychód",	u"Tarnowo Podgórne", u"Tarnowo Podgórne_",	u"Chrzypsko Wielkie",	u"Kuślin",	u"Sieraków",	u"Szamotuły",	u"Pniewy",	u"Kwilcz",	u"Kaźmierz",
                             u"Rokietnica",	u"Nowy Tomyśl",	u"Lwówek",	u"powiat słupecki",	u"powiat koniński",	u"powiat Konin",	u"powiat turecki",
                             u"powiat kolski",	u"powiat wolsztyński",	u"powiat leszczyński",	u"powiat rawicki",	u"powiat kościański",	u"powiat gostyński",
                             u"powiat Leszno",	u"Niechanowo",	u"Nekla",	u"Witkowo",	u"Pyzdry",	u"Września",	u"Swarzędz",	u"Miłosław",	u"Kostrzyn",
                             u"Trzemeszno",	u"Dominowo",	u"Środa Wielkopolska",	u"Czerwonak",	u"Czerwonak_",	u"Kołaczkowo",		u"Mosina",
                             u"Książ Wielkopolski",	u"Zaniemyśl",	u"Dolsk",	u"Kleszczewo",	u"Śrem",	u"Stęszew",	u"Brodnica",	u"Nowe Miasto nad Wartą",
                             u"Puszczykowo",	u"Krzykosy",	u"Kórnik",	u"Luboń",		u"Wielichowo",	u"Rakoniewice",	u"Granowo",	u"Buk",
                             u"Grodzisk Wielkopolski",	u"Dopiewo",	u"Komorniki",	u"Kamieniec",		u"Rogożno",	u"Oborniki",	u"Obrzycko",
                             u"Gniezno",	u"Kiszkowo",	u"Czerniejewo",	u"Obrzycko_",	u"Ryczywł",	u"Pobiedziska",	u"Łubowo",	u"Murowana Goślina",
                             u"Kłecko",	u"Gniezno_",	u"Mieleszyn",	u"Suchy Las",	u"Ostroróg",	u"powiat krotoszyński",
                             u"powiat pleszewski", u"powiat jarociński",	u"powiat Kalisz",	u"powiat kaliski",	u"powiat ostrzeszowski",	u"powiat ostrowski",	u"powiat kępiński",
                             u"powiat chodzieski",	u"powiat pilski",	u"powiat czarnkowsko-trzcianecki",	u"powiat złotowski",	u"powiat wągrowiecki",
]
'''

def sprawdz_czy_w_obszarze(punkt,obszar):
    poszukiwany_punkt= punkt#"POINT (16.8942 52.4092)"  ###punkt, ktory znajduje sie w 1a w poznaniu
    x,y=poszukiwany_punkt.split("(")[1].split(")")[0].split(" ")
    return obszar.contains_point((float(x), float(y)))

def pobierz_obszar(nazwa_obszaru, plik):
    #print nazwa_obszaru
    #print "\n"
    import json
    with open(plik) as f:
        data = json.load(f)
    for feature in data['features']:
        #diagnozuj(feature['properties']['nazwa'])
        #diagnozuj(nazwa_obszaru)
        #print(feature['properties']['nazwa'])
        if ((feature['properties']['nazwa'])==nazwa_obszaru ):##TODO: z jakiegos powodu wczytane dane nie rozpoznaje prawidlowo polskich liter
            return  feature['geometry']['coordinates'][0]
    #return "Ten return się nie powinien nigdy zwrócić...sprawdź nazwy obszarów w bazie" #data['features'][0]['geometry']['coordinates'][0]#!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!"Nie znaleziono obszaru o takiej nazwie" ##przerób to na django.errors TODO

def opisz_punkt_adresowy(punkt_adresowy,nazwy_obszarow_do_sprawdzenia, plik_z_geometriami):
    #print(punkt_adresowy)
    charakterystyka_punktu={}
    for nazwa_obszaru in nazwy_obszarow_do_sprawdzenia:  # NAZWY_OBSZAROW_SEKCJI_W_KOLEJNOSCI:
        array_do_sprawdzenia = pobierz_obszar(nazwa_obszaru,
                                                          plik_z_geometriami)  # 'WSZYSTKO.geojson')
        if sprawdz_czy_w_obszarze(punkt_adresowy, mplPath.Path(np.array(array_do_sprawdzenia))):
            charakterystyka_punktu['ktorasekcja'] = nazwa_obszaru
            charakterystyka_punktu['wspolrzedne'] = XY_from_WKTpoint(punkt_adresowy)
            charakterystyka_punktu['obszar_do_wyswietlenia']= [[array_do_sprawdzenia[i][1], array_do_sprawdzenia[i][0]] for i in
                                      range(len(array_do_sprawdzenia))]
            charakterystyka_punktu['punkt_WKT']=punkt_adresowy
            break
    return charakterystyka_punktu

def przygotuj_result():
    znalezione_punkty_adresowe = geokoder.znajdz_adres(miejscowosc, ulica, numer, precyzja_wyszukiwania,
                                                       'PRG_PunktAdresowy.sqlite')
    if len(znalezione_punkty_adresowe) == 1:
        result = geometria.opisz_punkt_adresowy(znalezione_punkty_adresowe[0][1],
                                                geometria.OBSZARY_SEKCJI_DO_SPRAWDZENIA,
                                                'WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')
    elif len(znalezione_punkty_adresowe) > 1:
        result[
            'ktorasekcja'] = "Znaleziono więcej niż jeden adres, uzupełnij o który Ci chodzi lub wybierz z powyższej listy."
    else:
        result[
            'ktorasekcja'] = "Nie odnaleziono takiego adresu... próbuję luźnego wyszukiwania...nie odnaleziono lub odnaleziono więcej niż jeden wynik"
        znalezione_punkty_adresowe = geokoder.znajdz_adres(miejscowosc, ulica, numer,
                                                           {'miejscowosc': False, 'ulica': False, 'numer': False, },
                                                           'PRG_PunktAdresowy.sqlite')
        if len(znalezione_punkty_adresowe) == 1:
            result = geometria.opisz_punkt_adresowy(znalezione_punkty_adresowe[0][1],
                                                    geometria.OBSZARY_SEKCJI_DO_SPRAWDZENIA,
                                                    'WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')