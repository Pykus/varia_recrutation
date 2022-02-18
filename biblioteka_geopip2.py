import sqlite3
import tkinter as tk
from tkinter.messagebox import showinfo, askokcancel
import os
# import ctypes #bylo potrzebne do fullscreena
import logging
CONTEXT = {}
CONTEXT = {'LOGIN': os.getlogin(), 'COMPUTER': os.getenv("COMPUTERNAME"),
           'SCREENSIZE': {'X': 800,  # ctypes.windll.user32.GetSystemMetrics(0),  #te w nawiasach daja fullscreen
                          'Y': 600},  # ctypes.windll.user32.GetSystemMetrics(1)},
           'CURRENT_DIR': os.path.dirname(os.path.realpath(__file__)),
           }
CONTEXT['LOG_FILE'] = CONTEXT['CURRENT_DIR']+'\log\main.log'
#logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',datefmt='%d/%m/%Y %I:%S')


from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = RotatingFileHandler(CONTEXT['LOG_FILE'], mode='a', maxBytes=3000000, backupCount=3)
fh.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
logger.addHandler(fh)
os.environ['PATH'] = CONTEXT['CURRENT_DIR'] + \
    '\lib\mod_spatialite-4.3.0a-win-x86;' + os.environ['PATH']

PLIKI_BAZ = {'punkty': os.path.join(CONTEXT['CURRENT_DIR'], 'data', 'punktyadresowe.db'),
             'ulice': os.path.join(CONTEXT['CURRENT_DIR'], 'data', 'ulice.db'),
             'sekcje': os.path.join(CONTEXT['CURRENT_DIR'], 'data', 'sekcje.db'),
             'sadyrejonowe': os.path.join(CONTEXT['CURRENT_DIR'], 'data', 'sadyrejonowe.db'),
             }


def o_programie():
    showinfo("O programie", "(c) Przemysław Przywarty  2018")


class Baza:
    def __init__(self, baza="", type="spatialite"):
        if type == "spatialite":
            self.database = baza
        elif type == "navi_local":
            pass
        else:
            print("Błąd, umiem sie tylko podlaczac do spatialite")

    def wykonaj_sql(self, sql, type="spatialite"):  # params):
        if type == "spatialite":
            self.cur.execute(sql)
            self.conn.commit()
            return self.cur
        elif type == "navi_local":
            self.cur.execute(sql)
            self.conn.commit()
            return self.cur
        else:
            print("Błąd, umiem sie tylko podlaczac do spatialite")

    def otworz_polaczenie(self, type="spatialite"):
        if type == "spatialite":
            self.conn = sqlite3.connect(self.database)
            self.conn.enable_load_extension(True)
            self.conn.execute('SELECT load_extension("mod_spatialite")')
            self.cur = self.conn.cursor()
        elif type == "navi_local":
            import psycopg2
            self.conn = psycopg2.connect(host="localhost", port=2001, database="navi",
                                         user="Connector")  # tak, wiem, paskudne rozwiazanie
            self.conn.set_client_encoding('win1250')
            self.cur = self.conn.cursor()
        else:
            print("Błąd, nie umiem sie się otworzyc z polaczeniem...")

    def zamknij_polaczenie(self):
        self.conn.close()


class Adres:
    def __init__(self):
        self.znalezione_adresy = []
        self.dane_o_adresie = {}
        self.bazy = {'punkty': Baza(PLIKI_BAZ['punkty']),
                     'miejscowosci': '',
                     'ulice': Baza(PLIKI_BAZ['ulice']),
                     'sekcje': Baza(PLIKI_BAZ['sekcje']),
                     'sadyrejonowe': Baza(PLIKI_BAZ['sadyrejonowe']),
                     }
        self.wybrany_adres = []

    def szukaj_adres(self, e_miejscowosc, e_ulica, e_numerporzadkowy, wyniki_listBox):
        # if e_numerporzadkowy.get()=="":
        #     logging.info('rozpoczeto wyszukiwanie ulicy')
        #     wyniki_listBox.delete(0, tk.END)
        #     self.szukane['nazwaglownaczesc']
        #     print("numer pusty")
        #     pass#wyszukaj w bazy ulice
        # else:

        wyniki_listBox.delete(0, tk.END)
        # !!! uwaga nie tykaj kolejnosci ponizszego self.szukane !! duzo sie dalej odnosze po indeksie, jesli juz to dodawaj na koncu
        # TOREDO: tego nie moge ruszyc, bo w wynik_z_listy_selected mi sie sypie
        self.szukane = ['miejscowosc', 'ulica', 'numerporzadkowy', 'id',
                        'kodpocztowy', 'asText(GEOMETRY)', 'X(Geometry)', 'Y(Geometry)']
        self.bazy['punkty'].otworz_polaczenie()
        self.znalezione_adresy = self.bazy['punkty'].wykonaj_sql(sql='''select ''' + ','.join(
            self.szukane) + ''' from punktyadresowe where miejscowosc like "%''' + e_miejscowosc.get()
            + '''''''%" and ulica like "%''' + e_ulica.get()
            + '''''''%" and numerporzadkowy like "%''' + e_numerporzadkowy.get() + '''''''%" order by miejscowosc,ulica,numerporzadkowy''').fetchall()  # to mi zastepuje return

        logger.info('Szukałem:' + ",".join([_.get() for _ in [e_miejscowosc, e_ulica,
                                                              e_numerporzadkowy]])+":("+str(len(self.znalezione_adresy))+")wyników")
        self.bazy['punkty'].zamknij_polaczenie()

        # [(x[1]+","+x[2]+","+x[3])  for x in [(i[0], i[2], i[3], i[4]) for i in baza.znalezione_adresy]]:
        for wynik in self.znalezione_adresy:
            wyniki_listBox.insert(tk.END, (",".join([str(_) for _ in wynik[:3]])).replace(',', (
                ' ' * 8)) + "    [id adresu:#" + str(wynik[3]) + "]")
        # wyniki_listBox.insert(END,",".join([[str(_) for _ in wynik[:3]] for wynik in db_punkty.znalezione_adresy]))#.replace(',', (' '*8))+"    [id adresu:#"+str(wynik[3])+"]")
        # [(wyniki_listBox.insert(END,adres) for adres in znalezione_adresy]
        # wyniki_listBox.select_set(0)  # This only sets focus on the first item.
        #   wyniki_listBox.event_generate("<<ListboxSelect>>")
        #print("Return z szukaj_adres")
        # print(self.znalezione_adresy)
        return  # nic nie zwracam, ponieważ ta funkcja jest przewidziana jako lambda; zwrot nastepuje do zmiennej znalezione_adresy

    def wynik_z_listy_selected(self, lbx_lista, lista, wynikowa_frame):
        logger.info('wybrano adres z listy')
        self.wybrany_adres = lista[lbx_lista.curselection()[0]]
        # print(self.wybrany_adres[5])# 5- to 'POINT(x,y)'
        # TOREDO: tu narazie nie moge dodac bo mi flooduje text
        self.szukane = ['nazwa', 'kolor', 'kierownik', 'asGeoJSON(GEOMETRY)']

        self.bazy['sekcje'].otworz_polaczenie()
        self.dane_o_adresie['sekcja'] = self.bazy['sekcje'].wykonaj_sql(
            "select "+','.join(self.szukane)+" from sekcje where within(GeomFromText('"+self.wybrany_adres[5]+"'), sekcje.GEOMETRY);").fetchall()
        self.bazy['sekcje'].zamknij_polaczenie()

        print(self.dane_o_adresie)  # TOREDO: narazie po prostu wyprintuj wszystko co zebrałeś o adresie
        _ = tk.Text(wynikowa_frame, width=40, height=4)
        _.grid(row=0, column=0, sticky="WE")
        _.insert(tk.CURRENT, "Teren sekcji:")
        _.insert(tk.END, str([_[0] for _ in self.dane_o_adresie['sekcja']]))

    # Przemek: dziala nawet fajnie, ale niestety pyinstaller nie ogarnia, TOREDO: zrob z tego zwykly szblon z html - mapka z leafletem nie jest trudna ani duza
    def pokaz_na_mapie(self, wariant="targeo"):
        import webbrowser
        if wariant == "targeo":
            webbrowser.open("https://mapa.targeo.pl/trasa,,Poznań%20Św%20marcin%2046,," +
                            '%20'.join(self.wybrany_adres[0:3]))
        elif wariant == "leaflet":
            # print(CONTEXT['CURRENT_DIR'])
            from time import time
            from string import Template
            with open(os.path.join(CONTEXT['CURRENT_DIR'], 'data', 'templates', 'leaflet_simple_template.tpl'), 'r') as f:
                tpl = Template(f.read())
            mapfile = 'leaflet_'+str(time())+'.html'
            with open(os.path.join(CONTEXT['CURRENT_DIR'], 'tmp', mapfile), 'w') as f:
                result_map = tpl.substitute(test="", X=self.wybrany_adres[6], Y=self.wybrany_adres[7], adres=" ".join(self.wybrany_adres[0:3]),
                                            geoJSON_sekcja=self.dane_o_adresie['sekcja'][0][3],
                                            nazwa_sekcji=self.dane_o_adresie['sekcja'][0][0],
                                            kolor_sekcji=self.dane_o_adresie['sekcja'][0][1]
                                            )
                f.write(result_map)
            webbrowser.open(os.path.join(CONTEXT['CURRENT_DIR'], 'tmp', mapfile))
            #print("mapka leafletowa")

    def raport_o_adresie(self):
        import webbrowser
        from time import time
        from string import Template

        self.bazy['sadyrejonowe'].otworz_polaczenie()
        self.dane_o_adresie['sad_rejonowy'] = self.bazy['sadyrejonowe'].wykonaj_sql(
            "select nazwajednostki from sadyrejonowe where within(GeomFromText('" + self.wybrany_adres[
                5] + "'), sadyrejonowe.GEOMETRY);").fetchall()
        self.bazy['sadyrejonowe'].zamknij_polaczenie()

        self.bazy['ulice'].otworz_polaczenie()
        self.dane_o_adresie['ulica'] = self.bazy['ulice'].wykonaj_sql(
            "select nazwaglownaczesc, GLength(ulice.GEOMETRY,0) as dlugosc, distance(MakePoint(" + str(
                self.wybrany_adres[6]) + "," + str(self.wybrany_adres[7]) +
            ",4326),MakePoint(16.923933, 52.40685, 4326),0) as odleglosc_od_siedziby,   " +
            "distance(ulice.GEOMETRY,MakePoint(" + str(self.wybrany_adres[6]) + "," + str(
                self.wybrany_adres[7]) + ",4326),0) as odleglosc_od_ulicy   "
                                         "from ulice where distance(ulice.GEOMETRY,MakePoint(" + str(
                self.wybrany_adres[6]) + "," + str(
                self.wybrany_adres[7]) + ",4326),0)<50").fetchall()  # !!nie dawaj tu ogc i wazny od bo popsujesz
        # "'), Buffer(ulice.GEOMETRY,'0.0000005')) and waznyod is NULL order by ogc_fid desc limit 1;").fetchall()
        self.bazy['ulice'].zamknij_polaczenie()

        with open(os.path.join(CONTEXT['CURRENT_DIR'], 'data', 'templates', 'raport_o_adresie.tpl'), 'r') as f:
            tpl = Template(f.read())
        raportfile = 'raport_' + str(time()) + '.html'
        with open(os.path.join(CONTEXT['CURRENT_DIR'], 'tmp', raportfile), 'w') as f:
            result_map = tpl.substitute(nazwa_sekcji=self.dane_o_adresie['sekcja'][0][0], sad_rejonowy=self.dane_o_adresie['sad_rejonowy'][0][0],
                                        pobliskie_ulice=self.dane_o_adresie['ulica'], adres=" ".join(self.wybrany_adres[0:3]))
            f.write(result_map)
        webbrowser.open(os.path.join(CONTEXT['CURRENT_DIR'], 'tmp', raportfile))


class Navigator:
    def __init__(self):
        self.bazy = {'navi_local_Connector': Baza(type="navi_local"), }
        self.znalezione_zaklady = []

    def szukaj_zaklad(self, miejscowosc, ulica, numerporzadkowy, wyniki_listBox):
        wyniki_listBox.delete(0, tk.END)
        self.bazy['navi_local_Connector'].otworz_polaczenie(type="navi_local")
        self.znalezione_zaklady = self.bazy['navi_local_Connector'].wykonaj_sql(sql="""select regon,nazwa_pe,miejscow, ulica,nr_posesji from dba.pracodawca_adres_local PAL  where miejscow like upper('%"""+miejscowosc +
                                                                                    """%') and ulica like upper('%"""+ulica+"""%') and nr_posesji like '"""+numerporzadkowy +
                                                                                    """' order by miejscow,ulica,nr_posesji,nazwa_pe""").fetchall()
        self.bazy['navi_local_Connector'].zamknij_polaczenie()
        logger.info("Zakłady pod adresem:" +
                    ",".join([miejscowosc, ulica, numerporzadkowy])+":("+str(len(self.znalezione_zaklady))+")")
        # [(x[1]+","+x[2]+","+x[3])  for x in [(i[0], i[2], i[3], i[4]) for i in baza.znalezione_adresy]]:
        for wynik in self.znalezione_zaklady:
            wyniki_listBox.insert(
                tk.END, ((",".join([str(_) for _ in wynik])).replace(',', (' ' * 8))))

    def wynik_z_listy_selected(self, lbx_lista, lista, wynikowa_frame):
        pass
        # tu zrob jakis guziczek typu "znajdz kontrole zakladu"

    def pokaz_zaklady_pod_adresem(self):
        pass
        # select * from dba.pracodawca_adres_local PAL  where miejscow like upper('%ń%') and ulica like upper('%arcin%') and nr_posesji like '%46%'


def bottle_test():
    import webbrowser

    #bottle.run(host='localhost', port=8080, debug=True)
    webbrowser.open("http://localhost:8080/helo")


'''jakby sie folium wciagał,to pewnie użyłbym tego
        logging.warning('ktos chcial pokazac na mapie')
        import folium
        import webbrowser
        x,y, adres= self.wybrany_adres[7],self.wybrany_adres[6], self.wybrany_adres[:3]
        mapa = folium.Map(location=[x, y],
                           tiles="Stamen Toner",
                           zoom_start=13)
        folium.Marker([x, y], popup=','.join(adres)).add_to(mapa)
        mapa.save('_tmp_mapa.html')
        webbrowser.open('_tmp_mapa.html')

        #print([i for i in self.dane_o_adresie['sekcja']])##TOREDO zamiast tego printa wrzuc jakos w prawy panel
        #r=0
        ##########################self.pokaz_na_mapie() #Przemek: pyinstaller nie wciaga ... jak przerobisz folium na leaflet i text to pomysl
        # for k,v in self.dane_o_adresie.items():
        #     tk.Text(wynikowa_frame, text="Jest to teren sekcji: " + ','.join(v), anchor=tk.W, justify=tk.CENTER,
        #              wraplength=700).grid(row=r, column=1, sticky="WE")
        #       print(k)
        #       #print("k:"+','.join(k)+"|v:"+','.join(v))
        #       print("\n\n")
        #       # if k=="sekcja":
        #
              # if k == "sad_rejonowy":
              #     tk.Label(wynikowa_frame, text="Teren sądu rejonowego: " +','.join(v), anchor=tk.W, justify=tk.CENTER,wraplength=700).grid(row=r+1, column=1, sticky="WE")

                  # pola_formularza[opis] = tk.Entry(f_lewa)
        #     pola_formularza[opis].grid(row=r, column=1, sticky="WE")
        #     r = r + 1
        # self

        ktorasekcja= select * sekcje where sekcje.geometria intersects wybrany_adres(geometria)
        prawytekst.insert(jest to teren sekcji ktorasekcja
        '''
# https://mapa.targeo.pl/trasa,,Poznañ%20Św%20marcin%2046,,Poznań%20Marcelińska%2090

'''
    lista.get(ACTIVE).split(",")
    #['Poznań', 'Święty Marcin','46/50']
    db_punkty.znalezione_adresy miejscowosc
    '''
'''
inne rozne
w compat.py:
    encoding = kwargs.pop('encoding', None) #przemek zamiast None wpisalem errors=ignore
#tmp= ",".join(tmp)
    #[(150708, 'Czmoń', 'Świerkowa', '46'),
    ## (408974, 'Poznań', 'Bohaterów II Wojny Światowej', '46'),
    ## (415529, 'Poznań', 'Świebodzińska', '46'),
    ## (418280, 'Poznań', 'Święty Marcin', '46/50')]
    #[(418280, '(4:Polska,wielkopolskie,Poznań,Poznań)', 'Poznań', 'Święty Marcin', '46/50', '61-807', 'istniejacy', None, None, None, '2017-10-04T12:49:07.570+02:00', b"\x00\x01\xe6\x10\xa7\x134J@\xfe")]
    #w[0],w[2],w[3],w[4]
    #wynik_tkStringVar.set()#str([w[1] for w in baza.znalezione_adresy]))#str([(w[0],w[2],w[3],w[4]) for w in baza.znalezione_adresy]))

###  root.attributes("-fullscreen", True) ##robi fullscreeena, ale tylko alt+f4 moze zamknac, chyba ze jakis event podepniesz
#print(evt.widget.get(ACTIVE))
#print(evt.widget.get(ACTIVE).split(","))
lista_wynikow_tkStringVar= tk.StringVar()
lista_wynikow_tkStringVar.set("poczatek...")
lista_wynikow_label=tk.Label(root, textvariable=lista_wynikow_tkStringVar, anchor=tk.W, justify=tk.LEFT)
'''


def test_pokaz_zmienna(var, label):  # testowe, pokazane na tutorialu z licznikiem na labalu
    def update():
        global x, v
        label.config(text=str(var.get()))
        label.after(1000, update)
    update()
