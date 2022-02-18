# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice
from .forms import SzukajAdres, SzukajWNavi
import os         ## nie wyrzucać stąd bo "precyzja" przy formularzach się psuje
import sqlite3    ## nie wyrzucać stąd bo "precyzja" przy formularzach się psuje
import numpy as np
from . import geometria
from . import geokoder

import logging
loggerGEO = logging.getLogger('geologger')

def wyszukaj(request, miejscowosc=u"Poznań",ulica=u"Marcin",numer=u"46/50"):
    #new_url="http://"
    znalezione_punkty_adresowe=[]
    result = {}
    result['wspolrzedne'] = geometria.XY_from_WKTpoint("POINT (16.9239333283202 52.4068497452665)")  ## marcin46, po to żeby się szablony nie buntowały update:
    result['obszar_do_wyswietlenia'] = []
    result['ktorasekcja'] = "nieokreślone"  # po to żeby się szablony nie buntowały
    if request.method == 'POST':
        form = SzukajAdres(request.POST)
        miejscowosc, ulica, numer = form.data['miejscowosc'], form.data['ulica'], form.data['numer']
        precyzja_wyszukiwania = {'miejscowosc': "0", 'ulica': "0", 'numer':"0", }
        #if form.data['precyzjamiejscowosc']=="1":
        precyzja_wyszukiwania['miejscowosc']=form.data['precyzjamiejscowosc']
        precyzja_wyszukiwania['ulica'] = form.data['precyzjaulica']
        precyzja_wyszukiwania['numer'] = form.data['precyzjanumer']
        znalezione_punkty_adresowe=geokoder.znajdz_adres(miejscowosc,ulica,numer,precyzja_wyszukiwania,'PRG_PunktAdresowy.sqlite')
        if len(znalezione_punkty_adresowe)==1:
            result=geometria.opisz_punkt_adresowy(znalezione_punkty_adresowe[0][1],geometria.OBSZARY_SEKCJI_DO_SPRAWDZENIA,'WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')
        elif len(znalezione_punkty_adresowe)>1:
            loggerGEO.info("Wiecej niż jeden adres:" + "|" + miejscowosc + "|" + ulica + "|" + numer)
            result['ktorasekcja'] = "Znaleziono więcej niż jeden adres, uzupełnij o który Ci chodzi lub wybierz z powyższej listy."
        else:
            loggerGEO.error("Nie znaleziono:"+"|"+miejscowosc+"|"+ulica+"|"+numer)
            result['ktorasekcja']="Nie znalazłem (dosłownie)... próbuję (zawiera)...nie odnaleziono lub odnaleziono więcej niż jeden wynik. Wybierz z listy lub uzupełnij pola."
            znalezione_punkty_adresowe = geokoder.znajdz_adres(miejscowosc, ulica, numer, {'miejscowosc': "0", 'ulica': "2", 'numer': "0", },
                                                               'PRG_PunktAdresowy.sqlite')
            if len(znalezione_punkty_adresowe) == 1:
                result = geometria.opisz_punkt_adresowy(znalezione_punkty_adresowe[0][1],
                                                        geometria.OBSZARY_SEKCJI_DO_SPRAWDZENIA,
                                                        'WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')

    else: ## method=="GET" lub np. z linka
        precyzja_wyszukiwania = {'miejscowosc': "0", 'ulica': "2", 'numer': "0", } ##czyli dopoki nie wybrales precyzyjnie to zwykly GET chce z %%
        if miejscowosc!=u"Poznań" or ulica!=u"Marcin" or numer!=u"46/50":#czyli klikałeś w linka lub masz coś w url
            precyzja_wyszukiwania = {'miejscowosc': "1", 'ulica': "2", 'numer': "1", }  ##no ale jak kliknales w linka to badzmy prezyzyjni, niestety z palca tez musisz byc precyzyjny

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
                    'ktorasekcja'] = "Nie znalazłem (dosłownie)... próbuję (zawiera)...nie odnaleziono lub odnaleziono więcej niż jeden wynik. Wybierz z listy lub uzupełnij pola."
                znalezione_punkty_adresowe = geokoder.znajdz_adres(miejscowosc, ulica, numer,
                                                                   {'miejscowosc': "0", 'ulica': "2",
                                                                    'numer': "0", },
                                                                   'PRG_PunktAdresowy.sqlite')
                if len(znalezione_punkty_adresowe) == 1:
                    result = geometria.opisz_punkt_adresowy(znalezione_punkty_adresowe[0][1],
                                                            geometria.OBSZARY_SEKCJI_DO_SPRAWDZENIA,
                                                            'WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')
                else: #czyli nie znalazles w PRG, sprawdz w nominatim
                    from geopy.geocoders import geonames
                    from geopy.geocoders import Nominatim
                    geolocator = Nominatim()



                    location = geolocator.geocode(miejscowosc + " " + ulica + " " + numer)
                    if location:
                        result = geometria.opisz_punkt_adresowy("POINT ("+str(location.longitude)+" "+str(location.latitude)+")",
                                                                 geometria.OBSZARY_SEKCJI_DO_SPRAWDZENIA,
                                                                'WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')
                        form = SzukajAdres()
                        #print(result)
                        #result['ktorasekcja'] = "nieokreślone"
                        #result['wspolrzedne'] = geometria.XY_from_WKTpoint("POINT ("+str(location.latitude)+" "+str(location.longitude)+")")
                        #result['obszar_do_wyswietlenia']= []
                        return render(request, 'wyszukiwarka/wyniki.html', {'form': form,
                                                                            'wyniki': znalezione_punkty_adresowe,
                                                                            'nominatim_alert':True,
                                                                            'ktorasekcja': result['ktorasekcja'],
                                                                            'wspolrzedne': result['wspolrzedne'],
                                                                            'obszar_do_wyswietlenia': result[
                                                                                'obszar_do_wyswietlenia']})




        form = SzukajAdres()

        #print result
    return render(request, 'wyszukiwarka/wyniki.html', {'form': form,
                                                        'wyniki':znalezione_punkty_adresowe,
                                                        'ktorasekcja':result['ktorasekcja'],
                                                        'wspolrzedne':result['wspolrzedne'],
                                                        'obszar_do_wyswietlenia': result['obszar_do_wyswietlenia'] })

def wyszukajWNavi(request,nazwapracodawcy):
    result = {}
    znalezione_punkty_adresowe = []
    result = {}
    znalezione_firmy=[]
    result['wspolrzedne'] = geometria.XY_from_WKTpoint(
        "POINT (16.9239333283202 52.4068497452665)")  ## marcin46, po to żeby się szablony nie buntowały update:
    result['obszar_do_wyswietlenia'] = []
    result['ktorasekcja'] = "nieokreślone"  # po to żeby się szablony nie buntowały
    if request.method == 'POST':
        form_navi=SzukajWNavi(request.POST)
        nazwapracodawcy = form_navi.data['nazwapracodawcy'].upper()
        print(nazwapracodawcy)
        import psycopg2
        conn = psycopg2.connect(host="localhost", port=2001, database="navi",
                                user="Connector")  # tak, wiem, paskudne rozwiazanie
        ###zrob z tego funkcje: wyszukaj w navi nazwapracodawcy
        zapytanie="select * from dba.pracodawca_adres_local where nazwa_PE like '%"+nazwapracodawcy+"%' and ident_ter like '30%'"
        print(zapytanie)
        conn.set_client_encoding('win1250')
        cur = conn.cursor()
        cur.execute(
            zapytanie)  # regon='41018881600000' or regon='30103531000000' or regon='25110561200000'     and "
        data = cur.fetchall()
        conn.close()
        ###
        znalezione_firmy=data



        znalezione_punkty_adresowe = geokoder.znajdz_adres(data[0][8], data[0][10], data[0][11], {'miejscowosc': True, 'ulica': True,
                                                                        'numer': True},'PRG_PunktAdresowy.sqlite')
        if len(znalezione_punkty_adresowe) == 1:
            result = geometria.opisz_punkt_adresowy(znalezione_punkty_adresowe[0][1],
                                                    geometria.OBSZARY_SEKCJI_DO_SPRAWDZENIA,
                                                    'WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')
        elif len(znalezione_punkty_adresowe) > 1:
            #loggerGEO.info("Wiecej niż jeden adres:" + "|" + miejscowosc + "|" + ulica + "|" + numer)
            result[
                'ktorasekcja'] = "Znaleziono więcej niż jeden adres, uzupełnij o który Ci chodzi lub wybierz z powyższej listy."
        else:
            #loggerGEO.error("Nie znaleziono:" + "|" + miejscowosc + "|" + ulica + "|" + numer)
            result[
                'ktorasekcja'] = "Nie znalazłem (dosłownie)... próbuję (zawiera)...nie odnaleziono lub odnaleziono więcej niż jeden wynik. Wybierz z listy lub uzupełnij pola."
            znalezione_punkty_adresowe = geokoder.znajdz_adres(data[0][8], data[0][10], data[0][11],
                                                               {'miejscowosc': "0", 'ulica': "2", 'numer': "0", },
                                                               'PRG_PunktAdresowy.sqlite')
            if len(znalezione_punkty_adresowe) == 1:
                result = geometria.opisz_punkt_adresowy(znalezione_punkty_adresowe[0][1],
                                                        geometria.OBSZARY_SEKCJI_DO_SPRAWDZENIA,
                                                        'WSZYSTKO_bez_podzialu_powiatow_BEZ_poznanskich.geojson')

        return render(request, 'wyszukiwarka/wynikiZNavi.html', { 'form_navi': form_navi,
                                                             'wyniki': znalezione_punkty_adresowe,
                                                            'znalezione_firmy':znalezione_firmy,
                                                            'ktorasekcja': result['ktorasekcja'],
                                                            'wspolrzedne': result['wspolrzedne'],
                                                            'obszar_do_wyswietlenia': result['obszar_do_wyswietlenia']})

    else:##GET lub z linka
        form_navi = SzukajWNavi()
        return render(request, 'wyszukiwarka/wynikiZNavi.html', { 'form_navi': form_navi,
                                                             'wyniki': znalezione_punkty_adresowe,
                                                            'znalezione_firmy': znalezione_firmy,
                                                            'ktorasekcja': result['ktorasekcja'],
                                                            'wspolrzedne': result['wspolrzedne'],
                                                            'obszar_do_wyswietlenia': result['obszar_do_wyswietlenia']})