# -*- coding: utf-8 -*- 
import psycopg2
import sqlite3
import pandas as pd
conn = psycopg2.connect(host="localhost",port=2001,database="navi", user="Connector")#tak, wiem, paskudne rozwiazanie
conn.set_client_encoding('win1250')
cur = conn.cursor()
cur.execute("select * from dba.pracodawca_adres_local where  typ_adresu=1 limit 1")#regon='41018881600000' or regon='30103531000000' or regon='25110561200000'     and "
data=cur.fetchall()
conn.close()
from geokoder import znajdz_adres, pl_znaki_sqlite
from geometria import opisz_punkt_adresowy, OBSZARY_SEKCJI_DO_SPRAWDZENIA, XY_from_WKTpoint
precyzja_wyszukiwania = {'miejscowosc': True, 'ulica': True, 'numer':True   , }
#print(len(data))
result={}
ostateczny_result=[]
#from . import geokoder
#from . import geometria
for item in data:
    #print(item)
    #print("\n")
    #print(item[8],item[10],item[11])  # to jest z naavi miejscowosc ulica numer
    #print("\n")

    znalezione_punkty_adresowe = znajdz_adres(item[8], item[10], item[11], {'miejscowosc': True, 'ulica': True,
                                                                    'numer': True, },
                                                       '.././PRG_PunktAdresowy.sqlite')
    if len(znalezione_punkty_adresowe) == 1:
        result = opisz_punkt_adresowy(znalezione_punkty_adresowe[0][1],
                                                OBSZARY_SEKCJI_DO_SPRAWDZENIA,
                                                '../.././WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')
    elif len(znalezione_punkty_adresowe) > 1:
        result[
            'ktorasekcja'] = "Znaleziono więcej niż jeden adres, uzupełnij o który Ci chodzi lub wybierz z powyższej listy."
        ostateczny_result.append([item[8], item[10], item[11], result['ktorasekcja']])
    else:
        result[
            'ktorasekcja'] = "Nie odnaleziono takiego adresu... próbuję luźnego wyszukiwania...nie odnaleziono lub odnaleziono więcej niż jeden wynik"
        ostateczny_result.append([item[8], item[10], item[11], result['ktorasekcja']])
        znalezione_punkty_adresowe = znajdz_adres(item[8], item[10], item[11],
                                                           {'miejscowosc': False, 'ulica': False, 'numer': False, },
                                                           '.././PRG_PunktAdresowy.sqlite')
        if len(znalezione_punkty_adresowe) == 1:
            result = opisz_punkt_adresowy(znalezione_punkty_adresowe[0][1],
                                                    OBSZARY_SEKCJI_DO_SPRAWDZENIA,
                                                    '../.././WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')
            ostateczny_result.append([item[8], item[10], item[11], result['ktorasekcja']])


    zgeokodowane=znajdz_adres(item[8],item[10],item[11],precyzja_wyszukiwania,'.././PRG_PunktAdresowy.sqlite')
    #print("\n")
    if len(zgeokodowane) == 1:
        result = opisz_punkt_adresowy(zgeokodowane[0][1], OBSZARY_SEKCJI_DO_SPRAWDZENIA,
                                                '../.././WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')
        ostateczny_result.append([item[8], item[10], item[11], result['ktorasekcja'], XY_from_WKTpoint(zgeokodowane[0][1])['X'], XY_from_WKTpoint(zgeokodowane[0][1])['Y']] )
    elif len(zgeokodowane) > 1:
        result[
            'ktorasekcja'] = "Znaleziono więcej niż jeden adres."
        ostateczny_result.append([item[8], item[10], item[11], result['ktorasekcja']])
    else:
        result['ktorasekcja'] = "Nie odnaleziono takiego adresu"
        ostateczny_result.append([item[8], item[10], item[11], result['ktorasekcja']])

###for i in ostateczny_result:
###    print(i,"\n\n")
import csv
with open("wynik.csv","w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for i in ostateczny_result:
        print(i)
        writer.writerow(i)