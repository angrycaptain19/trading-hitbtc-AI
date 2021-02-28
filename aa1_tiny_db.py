from tinydb import TinyDB, Query
from tinydb import TinyDB, where
import numpy as np
import win32api
from aa1_daten_query import aa1_daten_query_class
from aa1_daten_hilfe import aa1_daten_hilfe_class

#win32api.MessageBox(0, 'hello', 'title', 0x00001000) 
#2019-08-08  bis  2020-04-29
def bericht(db_kalender, db_layers):
    win32api.MessageBox(0,"db_kalender(" + str(len(db_kalender))+ ")  db_layers("+ str(len(db_layers))+")", '!')

def add_table(Coin_symbol, Tag, table_name, kuerzel, quelle, close_array, volume_array, volume_avrage, close_avrage):
    if len(close_array)==len(volume_array):
        db_kalender = TinyDB('aa_Tabellen/'+table_name+'.json')
        db_administartor= TinyDB('aa_Tabellen/administartor.json')
        set_count = db_administartor.count(where('symbol') == Coin_symbol)
        if set_count == 0:
            db_administartor.insert({'symbol': Coin_symbol ,'volume_avrage': volume_avrage, 'close_avrage': close_avrage})
        db_kalender.purge()
        for i in np.arange(len(close_array)):
            db_kalender.insert({"aa_Tag": Tag[i], "kuerzel": Coin_symbol, "fullName": Coin_symbol, "close": close_array[i], "volume": volume_array[i]})
    else:
        win32api.MessageBox(0,"fehler g69j. array len sind ungleich" + str(len(close_array))+ " "+ str(len(volume_array)), 'Insert Fehler')
    if len(close_array)==len(db_kalender):
        #win32api.MessageBox(0,"Table Neueintrag erfolgreich", '!')
        print(str(len(close_array))+" "+Coin_symbol+" Table Neueintrag erfolgreich "+ str(len(db_administartor)) )
    else:
        win32api.MessageBox(0,Coin_symbol+ " close_array(" + str(len(close_array))+ ")  table_sets("+ str(len(db_kalender))+") passen nicht", '!')
def tendenz_ticker(wert):
    wert_result1 = 0
    counter     = 0
    for i in np.arange(1,len(wert)):
        if wert[i]>wert[i-1]:
            wert_result1 += 1
        else:
            wert_result1 = 0
    return wert_result1

def delete_layer_familly(Coin_symbol, Tag, name, kuerzel, quelle, close_array, volume_array):
    if len(close_array) != len(db_kalender):
        win32api.MessageBox(0,"wahrnung! xnei8 ungleiche daten gesendet(" + str(len(close_array))+ ") Tabelle ("+ str(len(db_kalender))+")", 'Wahrnung!')
    if len(close_array)==len(volume_array):
        docs = db_kalender.all()
        #for i in np.arange(len(close_array)):
        for doc in docs:
            #db_kalender.remove(User.symbol == symbol)

            db_kalender.update({Coin_symbol+"-name": name, Coin_symbol+"-kuerzel": Coin_symbol, Coin_symbol+"-close": close_array[i], Coin_symbol+"-volume": volume_array[i]}, where('aa_Tag') == Tag[i])
        #set_count = db_layers.count(where('symbol') == Coin_symbol)
        #if set_count == 0:
            #db_layers.insert({'symbol': Coin_symbol ,'quelle': quelle,'name': name})
    else:
        win32api.MessageBox(0,"fehler g69j. array len sind ungleich" + str(len(close_array))+ " "+ str(len(volume_array))+ " "+str(len(ema1_array))+ " "+ str(len(ema2_array)), 'Insert Fehler')
    print("Eintag erfolgreich")
def insert_massen(kuerzel_array, fullName_array, EMA_periode, jomle, kalame, quelle, volume_filter):
    for Coin_symbol in kuerzel_array:
        close, max, min, volume, volumeQuote, Tag, volume_avrage, close_avrage = aa1_daten_query_class.hitbtc_query(Coin_symbol, EMA_periode, jomle + kalame)
        if volume_avrage > volume_filter:
            add_table(Coin_symbol, Tag, Coin_symbol, Coin_symbol, quelle, close, volume, volume_avrage, close_avrage)
        else:
            print(Coin_symbol+ " V("+str(volume_avrage)+")  ausgeschlossen")
def dedektiv(EMA_periode, jomle, kalame, quelle, volume_filter, ema1, ema2, ema1_serie, ema2_serie):
    fullName_array, kurzel_array = aa1_daten_hilfe_class.Hitbtc_curency_list()
    ergebnis = ""
    for Coin_symbol in kuerzel_array:
        close, max, min, volume, volumeQuote, Tag, volume_avrage, close_avrage, ema_satz, ema_drittel = aa1_daten_query_class.hitbtc_query_mit_ema(Coin_symbol, EMA_periode, jomle + kalame, ema1, ema2)
        ema_result1 = tendenz_ticker(ema_satz)
        ema_result2 = tendenz_ticker(ema_drittel)
        if volume_avrage > volume_filter and ema_result1 >= ema1_serie and ema_result2 >= ema2_serie:
            #print(Coin_symbol+ " V("+str(volume_avrage)+")  EMA1("+str(ema_result1)+") EMA2("+str(ema_result2)+")-------------------------------------------------")
            #win32api.MessageBox(0,Coin_symbol+ " V("+str(volume_avrage)+")  EMA1("+str(ema_result1)+") EMA2("+str(ema_result2)+")", 'Insert Fehler')
            ergebnis += Coin_symbol+ " V("+str(volume_avrage)+")  EMA1("+str(ema_result1)+") EMA2("+str(ema_result2)+")------------"
        else:
            print(str(ema_result1) + " " + str(ema_result2) +" "+ Coin_symbol+ "  V"+str(volume_avrage))
    return ergebnis

EMA_periode                  = "D1"
Coin_symbol                  = "ETHBTC,BTCUSD"
jomle                        = 32                     # 650 data count  =  jomle+kalame
kalame                       = 38 
volume_filter                = 5                     #BTC
ema1                         = 5
ema2                         = 40
ema1_serie                    = 4
ema2_serie                    = 0
#db_kalender = TinyDB('aa_Tabellen/aa1_Kalender.json')
#db_layers = TinyDB('aa1_layers.json')
#bericht(db_kalender)
#kurzel_array = ['MDABTC']
ergebnis = dedektiv(EMA_periode, jomle, kalame, "hitbtc", volume_filter, ema1, ema2, ema1_serie, ema2_serie)
print(ergebnis)