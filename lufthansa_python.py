# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 21:46:56 2022
@author: PP

Nie wiem jeszcze, jak zadanie wykonac w Javie, z checia sie naucze.
W pythonie w wersji "minimum" mogloby to byc cos takiego.
Oczywiscie dalej w trybie pilnym do zrobienia try..excepty przy kazdej obsludze plikow,
input od uzytkownika wynikowej nazwy pliku (lub dodanie obslugi parametrow z linii polecen)
i opakowanie wszystkiego w jakas klase.

Doceniam jednoczesnie znaczenie testowanie (niedawno zrobilem certyfikat ISTQB) jednak 
w tym prostym wypadku chyba najbardziej testowane bylyby funkcje wewnetrzne jezyka.

"""
import urllib.request
import json


#KONFIGURACJA
url="https://newsapi.org/v2/top-headlines?country=pl&category=business&apiKey=96e23f3db1794f78b3df28dcc0bb85dc"
tmp_json_plik='news_json.json'
wynikowy_plik="artykuly.csv"
delim=":"


#WCZYTANIE Z API I ZAPISANIE DO PLIKU JSON
dane_json=""
with urllib.request.urlopen(url) as resp:
   dane_json = resp.read().decode('utf-8')
   with open(tmp_json_plik, "w",encoding="utf-8") as f:
       f.write(str(dane_json))
       f.close()


#ODCZYT Z JSON I ZAPIS W PORZĄDANYM FORMACIE
with open('news_json.json') as json_file:
    data = json.load(json_file)    
    f = open(wynikowy_plik, "w",encoding="utf-8")
    for article in data['articles']:
        f.write(str(article['title'])+delim+str(article['description'])+delim+str(article['author']))
    f.close()

