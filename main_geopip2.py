import tkinter as tk
import os
from threading import Thread
import logging
from logging.handlers import RotatingFileHandler
from tkinter.messagebox import showinfo
import pandas as pd
from string import Template
from time import time
import webbrowser
from lib.bottle import route, run, template  # Bottle  , ServerAdapter


bottle_serwer = Thread(target=run, kwargs=dict(host='localhost',
                                               port=8422, debug=True))
bottle_serwer.daemon = True
bottle_serwer.start()


class Baza:
    def __init__(self):
        import psycopg2
        self.connection = psycopg2.connect(host="localhost", port=2001,
                                           database="navi",
                                           user="Connector")
        self.connection.set_client_encoding('win1250')

    def zamknij_polaczenie(self):
        self.connection.close()


def o_programie():
    showinfo("O programie", "(c) Przemysław Przywarty  2018")


root = tk.Tk()
CONTEXT = {}
CONTEXT = {'LOGIN': os.getlogin(), 'COMPUTER': os.getenv("COMPUTERNAME"),
           'SCREENSIZE': {'X': 800,  # ctypes.windll.user32.GetSystemMetrics(0)
                          'Y': 600, },
           'CURRENT_DIR': os.path.dirname(os.path.realpath(__file__)),
           }
CONTEXT['LOG_FILE'] = CONTEXT['CURRENT_DIR']+'\log\main.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = RotatingFileHandler(CONTEXT['LOG_FILE'], mode='a',
                         maxBytes=3000000, backupCount=3)
fh.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
logger.addHandler(fh)

# tu sie konczy "szablon"
root.title("Wyszukaj zaklad")
# root.geometry(str
#              (CONTEXT['SCREENSIZE']['X'])+"x" +
#              str(str(CONTEXT['SCREENSIZE']['Y'])+"+0+0"))

mm_menu = tk.Menu(root)
mi_help = tk.Menu(mm_menu)
mi_help.add_command(label="O programie", command=o_programie)
root.config(menu=mm_menu)

tk.Label(root, text="Podaj PKD do wyszukania:").pack()
opisy_pol_formularza = ["PKD", ]  # , "miejscowość", "ulica", "numer"]
pola_formularza = {}
for opis in opisy_pol_formularza:
    tk.Label(root, text=opis).pack()
    pola_formularza[opis] = tk.Entry(root)
    pola_formularza[opis].pack()


def wyszukaj_zaklady():
    zapytanie = """select PL.regon as plregon, pkd, PAL.nazwa_skr,
            PAL.nazwa_pe, PAL.typ_adresu, PAL.ident_ter,
            PAL.miejscow,PAL.ulica, PAL.nr_posesji, PAL.nr_lokalu
        from dba.pracodawca_pkd_local PL  left join
             dba.pracodawca_adres_local PAL on PL.regon=PAL.regon
        where pkd like '%"""+pola_formularza["PKD"].get()+"""%' and

         PL.data_zmiany>'2018-04-01'"""

    df = pd.read_sql(zapytanie, navi_local.connection)
    return df


@route('/hello')
def hello():
    dict = {'DATAFRAME': wyszukaj_zaklady()}
    return template('data\DATAFRAME.tpl', dict)


tk.Button(root, text="Szukaj", command=hello).pack()

navi_local = Baza()

pola_formularza["PKD"].insert(0, "4321Z")

"""
    with open(os.path.join(CONTEXT['CURRENT_DIR'], 'data', 'DATAFRAME.tpl'),
              'r') as f:
        tpl = Template(f.read())
        rfile = 'raport_' + str(time()) + '.html'
        with open(os.path.join(CONTEXT['CURRENT_DIR'], 'tmp', rfile),
                  'w') as fw:
            fw.write(tpl.substitute(DATAFRAME=df.to_html()))
            #webbrowser.open(os.path.join(CONTEXT['CURRENT_DIR'], 'tmp', rfile))
            webbrowser.open('http://localhost:8422/hello')
"""


root.mainloop()
