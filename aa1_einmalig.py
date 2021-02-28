from tinydb import TinyDB, Query
from tinydb import TinyDB, where
import requests,json
import numpy as np
EMA_periode                  = "D1"
Coin_symbol                  = "BTCUSD"
jomle                        = 650                     # 650 data count  =  jomle+kalame
kalame                       = 38                       # 38 war bestes Ergebniss bei BTC
data_count  = jomle+ kalame
data_btc = requests.get("https://api.hitbtc.com/api/2/public/candles/"+str(Coin_symbol)+"?limit="+str(data_count)+"&sort=DESC&period="+EMA_periode).json()
timestamp  = []
db_kalender = TinyDB('aa1_Kalender.json')
db_layers = TinyDB('aa1_layers.json')
User = Query()
print(len(data_btc))
name = "bitcoin"
quelle = "hitbtc"
for i in np.arange(data_count):
    kauftime = data_btc[i]['timestamp']
    jahr = kauftime.split("-")[0]
    mont = kauftime.split("-")[1]
    tag = kauftime.split("T")[0].split("-")[2]
    ziel = kauftime.split("T")[0]
    Tag = str(ziel)
    hour = kauftime.split("T")[1].split(":")[0]
    min = kauftime.split("T")[1].split(":")[1]
    sec = kauftime.split("T")[1].split(":")[2].split(".")[0]
    close_value = data_btc[i]['close']
    close_value = float(close_value)
    volume_value = data_btc[i]['volume']
    volume_value = float(volume_value)
    db_kalender.insert({'aa_Tag': str(ziel)})
    #db_kalender.update({Coin_symbol+"-name": name, Coin_symbol+"-kuerzel": Coin_symbol, Coin_symbol+"-close": close_value, Coin_symbol+"-volume": volume_value, Coin_symbol+"-ema12": 0, Coin_symbol+"-ema21": 0}, where('aa_Tag') == Tag)
    #db_kalender.update({'ki_erwartung': str(1),'leer1': str(1),'leer2': str(1),'leer3': str(1)}, where('Tag') == ziel)
    #2020-04-24
set_count = db_layers.count(where('symbol') == Coin_symbol)
if set_count == 0:
    db_layers.insert({'symbol': Coin_symbol ,'quelle': quelle,'name': name})
print(len(db_kalender))

#docs = db_bilanz.search(User.symbol == symbol)
#for doc in docs:
kafie = 0
docs = db_kalender.search(User.aa_Tag == "2020-04-24")
print(docs[0])
#.insert({'dax': str(333)})
print("arschloch")
"""
atributen:
1:name
2:kürzel
3:quelle
4:close
5:volume
6:ema1
7:ema2
"""