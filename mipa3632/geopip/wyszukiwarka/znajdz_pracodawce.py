import psycopg2
conn = psycopg2.connect(host="localhost",port=2001,database="navi", user="Connector")#tak, wiem, paskudne rozwiazanie
conn.set_client_encoding('win1250')
cur = conn.cursor()
#nazwa_PE like '%SKLEP \"BIEDRONKA%' and ident_ter like '30%'
cur.execute("select * from dba.pracodawca_adres_local where ident_ter like '30%' limit 1")# and typ_adresu=1")#regon='41018881600000' or regon='30103531000000' or regon='25110561200000'     and "
data=cur.fetchall()
conn.close()


from geokoder import znajdz_adres, pl_znaki_sqlite

ostateczny_result=[]
for item in data:
    print(item,"\n")
    znalezione_punkty_adresowe = znajdz_adres(item[8], item[10], item[11], {'miejscowosc': "0", 'ulica': "2", 'numer': "1", },
                                                       '.././PRG_PunktAdresowy.sqlite')
    if len(znalezione_punkty_adresowe) == 1:
        ostateczny_result.append([item,znalezione_punkty_adresowe[0][1]])
    else:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim()
        location = geolocator.geocode(item[8]+" "+item[10]+" "+item[11])
        ostateczny_result.append([item,"Nie odnaleziono jednoznacznego punktu."])

for x in ostateczny_result:
    print("\n")
    print(x)