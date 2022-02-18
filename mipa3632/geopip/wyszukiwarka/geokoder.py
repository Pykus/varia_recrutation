# -*- coding: utf-8 -*-
import os
import sqlite3
from geopy.geocoders import geonames
pl_znaki_sqlite = {'ś':'_', 'ż':'_', 'ą':'_','ź':'_','ł':'_','ó':'_','ń':'_','ć':'_','ę':'_','.':'_','Ś':'_','Ł':'_','Ź':'_'}
def zmienLiteryWgSlownika(string, slownik):
    for i, j in slownik.items():
        string = string.replace(i, j)
    return string


def precyzjawyszukiwania(poszukiwane,czy_precyzja):
    wynik=""
    if poszukiwane is None:
        return wynik
    if (czy_precyzja=="1"):
        wynik += ""
    else:
        wynik += '%'
    wynik += poszukiwane
    if (czy_precyzja=="1"):
        wynik += "\'"
    else:
        wynik += '%\''
    return  wynik


def znajdz_adres(miejscowosc, ulica,numer, precyzja_wyszukiwania, baza_adresowa):
    #directory=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print "[test]Bede szukał:", miejscowosc,ulica,numer
    con = sqlite3.connect(baza_adresowa)#PRG_PunktAdresowy.sqlite  ')
    #print "[test]poloczono z baza adresowa"
    cur = con.cursor()
    poszukiwane={}
    poszukiwane['miejscowosc']=zmienLiteryWgSlownika(miejscowosc.lower(),pl_znaki_sqlite)
    #if ulica=="":
    #    poszukiwane['ulica']=None  ##jak to ustawisz to przestaje dzialać   [pozn, 46/]
    #else:
    poszukiwane['ulica']=zmienLiteryWgSlownika(ulica.lower(),pl_znaki_sqlite)
    poszukiwane['nrporzadkowy']=zmienLiteryWgSlownika(numer.lower(),pl_znaki_sqlite)
    zapytanie='select * from prg_punktadresowy where miejscowosc like \''+precyzjawyszukiwania(poszukiwane['miejscowosc'], precyzja_wyszukiwania['miejscowosc'])
    #else:
    if ulica=="":
        #print("ulicajest pusta")
        pass
    else:
        if precyzja_wyszukiwania['ulica']=="2": #czyli chce kombinowac
            poszukiwane['ulica']=poszukiwane['ulica'].split()[-1]
        zapytanie+=' and ulica like \''+precyzjawyszukiwania(poszukiwane['ulica'], precyzja_wyszukiwania['ulica'])
    zapytanie += ' and numerporzadkowy like \'' + precyzjawyszukiwania(poszukiwane['nrporzadkowy'],precyzja_wyszukiwania['numer'])
    #zapytanie+=' COLLATE NOCASE'
    print(zapytanie,"<<to sie za chwile wykona")
    cur.execute(zapytanie)
    #print("[test]zapytanie wykonane[endtest]")
    data=cur.fetchall()

    '''
    jesli data=0 to znaczy ze pewnie dowcipy z ulica sa
    '''


    con.close()
    return data

