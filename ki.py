import requests,json
import time
import datetime
import matplotlib.pyplot as plt
import os
# multivariate lstm example
from numpy import array
from numpy import loadtxt
from numpy import hstack
import numpy as np # linear algebra
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from decimal import *
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from keras import optimizers
from keras import regularizers
from tinydb import TinyDB, Query
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage
#from datetime import datetime, timedelta
def get_prozent(mutter,kind,int0_str1):
    prozent = 0 
    if mutter !=0:
        prozent = kind/mutter * 100
        prozent = round(prozent, 2)
    if(int0_str1==1):
        prozent = str(prozent)+"%"
        if len(prozent)==4:
            prozent="0"+prozent
    return prozent
def lasagna_x(output_dim,X_train,optimizer,activation,dorpout,loss):
    model = Sequential()
    model.add(LSTM(units=output_dim, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    if dorpout!=0:
        model.add(Dropout(0.2))
    model.add(Dense(units=32,activation=activation))
    model.add(LSTM(units=output_dim, return_sequences=False))
    if dorpout!=0:
        model.add(Dropout(0.2))
    model.add(Dense(units=1,activation=activation))
    model.compile(optimizer='rmsprop',loss=loss, metrics=['accuracy'])
    return model
def split_sequences(sequences, n_steps):
	X, y = list(), list()
	for i in range(len(sequences)):
		# find the end of this pattern
		end_ix = i + n_steps
		# check if we are beyond the dataset
		if end_ix > len(sequences):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1, -1]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)
def hist_price_dl_hitbtc_book(antwort,asking, bidding):
    btc = []
    btc_v = []
    counter=0
    for konto in asking:
        if counter >=2 and konto != "":#verursacht versetzung wegen ergebnis row
            btc.append(Decimal(konto))
            btc_v.append(Decimal(bidding[counter]))
        counter+=1
    close  = []
    volume = []
    min = []
    max = []
    out_seq = []
    counter=0
    summe=0
    osci = 0
    count_innen=0
    for konto in antwort:
        counter+=1
        if counter >=2 and counter <= len(antwort)-1 :#akahri tush nn�miad wa az dowwomi shuru mishe
            close.append(konto['close'])
            summe+=Decimal(konto['close'])
            count_innen+=1
            osci = (summe/count_innen)-Decimal(konto['close'])
            volume.append(konto['volume'])
            min.append(osci)
            max.append(0)
        if counter >=3:#az sewwomi shuru mishe
            out_seq.append(konto['close'])
    return btc,btc_v, volume, close, min, max, out_seq 
def hist_price_dl_hitbtc(antwort,btc_result):
    close  = []
    close_b  = []
    volume = []
    volume_b = []
    min = []
    min_b = []
    out_seq = []
    counter=0
    summe=0
    summe_b=0
    osci = 0
    osci_b = 0
    count_innen=0
    count_b=0
    for konto in antwort:
        counter+=1
        if counter >=2 and counter <= len(antwort)-1 :#akahri tush nn�miad wa az dowwomi shuru mishe
            close.append(konto['close'])
            summe+=Decimal(konto['close'])
            count_innen+=1
            osci = (summe/count_innen)-Decimal(konto['close'])
            volume.append(konto['volume'])
            min.append(osci)
        if counter >=3:#az sewwomi shuru mishe
            close_b.append(konto['close'])
            volume_b.append(konto['volume'])
            count_b+=1
            summe_b+=Decimal(konto['close'])
            osci_b = (summe_b/count_b)-Decimal(konto['close'])
            min_b.append(osci_b)
            out_seq.append(konto['close'])
   #return btc,btc_v, volume, close, min, max, out_seq 
    return volume, close, min, out_seq, close_b, volume_b, min_b
def hist_price_dl_hitbtc_alt(antwort,btc_result):
    btc = []
    btc_v = []
    counter=0
    summe=0
    osci = 0
    count_innen=0
    max = []
    for konto in btc_result:
        counter+=1
        if counter <= len(btc_result)-1 and counter >=2:#verursacht versetzung wegen ergebnis row
            result = get_prozent(kurs_vortag,Decimal(konto['close']),0) - 100
            result = result * 10
            btc.append(result)
            btc_v.append(konto['close'])
            count_innen+=1
            summe+=Decimal(konto['close'])
            osci = (summe/count_innen)-Decimal(konto['close'])
            #btc_v.append(konto['volume'])
            #btc_v.append(0)
            max.append(osci)
        kurs_vortag = Decimal(konto['close'])

    close  = []
    volume = []
    min = []
    out_seq = []
    counter=0
    kurs_vortag = 0
    summe=0
    osci = 0
    count_innen=0
    for konto in antwort:
        counter+=1
        if counter >=2 and counter <= len(antwort)-1 :#akahri tush nn�miad wa az dowwomi shuru mishe
            close.append(konto['close'])
            summe+=Decimal(konto['close'])
            count_innen+=1
            osci = (summe/count_innen)-Decimal(konto['close'])
            volume.append(konto['volume'])
            min.append(osci)
            #result_close = get_prozent(kurs_basis,Decimal(konto['close']),0) - 100
            #result_close = result_close * 10
            #close.append(0)
        if counter >=3:#az sewwomi shuru mishe
            out_seq.append(konto['close'])
        kurs_vortag = Decimal(konto['close'])
    
    return btc,btc_v, volume, close, min, max, out_seq 
def daten_repair_1(sc,daten):                                     #['778', '779', '703.8', '737.92', '701.41', '703.2
    daten =[float(numeric_string) for numeric_string in daten]    #[778.0, 779.0, 703.8, 737.92, 701.41, 703.28, 702.82, 
    daten = array(daten)                                          #array([778.  , 779.  , 703.8 , 737.92, 701.41, 703.28, 702.82, 702.58
    daten = daten.reshape((len(daten), 1))                        #array([[778.  ],
                                                                  #[779.  ],
                                                                  #[703.8 ],
                                                                  #[737.92],
                                                                  #[701.41],
    daten = sc.fit_transform(daten)
    return daten

def parameter(sc, volume, close, min,out_seq, close_b, volume_b, min_b, steps, mit_ergebniss_1, sequence):
    volume  = daten_repair_1(sc,volume)
    min     = daten_repair_1(sc,min)
    close   = daten_repair_1(sc,close)
    out_seq = daten_repair_1(sc,out_seq)
    close_b = daten_repair_1(sc,close_b)
    volume_b = daten_repair_1(sc,volume_b)
    min_b = daten_repair_1(sc,min_b)
    ergebniss =[]
    volume   = volume[range(0, len(volume)-steps)]
    min      = min[range(0, len(min)-steps)]
    close    = close[range(0 , len(close) -steps)]
    close_b  = close[range(0 , len(close_b) -steps)]
    volume_b = close[range(0 , len(volume_b) -steps)]
    min_b    = close[range(0 , len(min_b) -steps)]
    out_seq_beide = out_seq
    out_seq   = out_seq_beide[range(0   , len(out_seq_beide)-steps)]##########
    ergebniss = out_seq_beide[range(len(out_seq_beide)-steps, len(out_seq_beide)   )]
    if mit_ergebniss_1 == 1:
        dataset = hstack(( volume, close, min, out_seq))#min max btv
    else:
        dataset = hstack(( volume_b, close_b, min_b, out_seq))#min max btv
    X, y = split_sequences(dataset, sequence)
    n_features = X.shape[2]
    boss_test = X[range(len(X)-steps-steps, len(X)-steps)]
    test3 = X[range(len(X)-steps-steps+1, len(X)-steps+1)]
    test4 = X[range(len(X)-steps-steps+2, len(X)-steps+2)]
    test5 = X[range(len(X)-steps-steps+3, len(X)-steps+3)]
    boss_futur = X[range(len(X)-steps, len(X))]
    return steps, n_features , X , y , boss_test, boss_futur, ergebniss, test3, test4, test5
def korrektur(ergebniss,model_16,time_conect):
    diferenz = model_16[0]-ergebniss[time_conect]
    #diferenz = [0]
    deferenz_einzeln = 0
    count=0
    korected = []
    ki_close = 0
    for number in range(0,time_conect):
        korected.append(ergebniss[number])

    for konto in model_16:
        korected.append(model_16[count]-diferenz)
        val = ergebniss[count] - korected[count] #1:array([0.00208504]) 2:array([0.00208504])
        if val < 0:
            val = val*-1
        deferenz_einzeln += val
        ki_close = korected[count]
        count+=1
    deferenz_einzeln = deferenz_einzeln/count
    return korected, ki_close, deferenz_einzeln, count
class Start():
    def diagram(Coin_symbol,ergebniss,ergebniss1,ergebniss2,ergebniss3,ergebniss4,endung):
        if ergebniss1==0:
            ergebniss1 = ergebniss
        if ergebniss2==0:
            ergebniss2 = ergebniss

        if ergebniss3==0:
            ergebniss3 = ergebniss
        if ergebniss4==0:
            ergebniss4 = ergebniss
        plt.plot(ergebniss,  color = 'black', label = Coin_symbol +'Price')
        plt.plot(ergebniss1, color = 'red', label = Coin_symbol +'Price')
        plt.plot(ergebniss2, color = 'blue', label = Coin_symbol +'Price')
        plt.plot(ergebniss3, color = 'yellow', label = Coin_symbol +'Price')
        plt.plot(ergebniss4, color = 'green', label = Coin_symbol +'Price')
        plt.title(Coin_symbol)#
        plt.xlabel('Time')
        plt.ylabel(Coin_symbol +'Price')
        plt.legend()
        strFile = 'png/'+Coin_symbol+endung
        if os.path.isfile(strFile):
           os.remove(strFile)
        plt.savefig(strFile)
        plt.clf()
    def insert_ordebook(booking_all,My_traid_symbol):

        konto_ask = booking_all["ask"]#verkauf
        konto_ask.reverse()
        asking_ar = []
        ask_str =""
        for konto in konto_ask:
            asking_ar.append(Decimal(konto['size'])*Decimal(konto['price']))
            prov = Decimal(konto['size'])*Decimal(konto['price'])
            ask_str+=str(prov)+","
        konto_bid = booking_all["bid"]#kauf
        konto_bid.reverse()
        bidding_ar = []
        bid_str =""
        for konto in konto_ask:
            bidding_ar.append(Decimal(konto['size'])*Decimal(konto['price']))
            prov = Decimal(konto['size'])*Decimal(konto['price'])
            bid_str+=str(prov)+","
        db_coins = TinyDB('datenbank/coins.json')
        User = Query
        set_count = db_coins.count(where('symbol') == My_traid_symbol)
        db_coins.insert({'symbol': My_traid_symbol ,'asking_ar': ask_str,'bidding_ar': bid_str,'time': str(datetime.datetime.now().time()),'leer3': str(0)})
    def ord_book_bid_ask(booking_all,My_traid_symbol):

        konto_ask = booking_all["ask"]#verkauf
        konto_ask.reverse()
        asking_ar = []
        ask_str =""
        for konto in konto_ask:
            asking_ar.append(Decimal(konto['size'])*Decimal(konto['price']))
            prov = Decimal(konto['size'])*Decimal(konto['price'])
            ask_str+=str(prov)+","
        konto_bid = booking_all["bid"]#kauf
        konto_bid.reverse()
        bidding_ar = []
        bid_str =""
        for konto in konto_ask:
            bidding_ar.append(Decimal(konto['size'])*Decimal(konto['price']))
            prov = Decimal(konto['size'])*Decimal(konto['price'])
            bid_str+=str(prov)+","
        db_coins = TinyDB('datenbank/coins.json')
        User = Query
        set_count = db_coins.count(where('symbol') == My_traid_symbol)
        if set_count == 0:
            db_coins.insert({'symbol': My_traid_symbol ,'asking_ar': ask_str,'bidding_ar': bid_str,'leer2': str(0),'leer3': str(0)})
        if set_count == 1:
            db_set = db_coins.search(where('symbol') == My_traid_symbol)
            asking_ar_db = db_set[0]['asking_ar']  #[{'ki_erwartung': '0', 'leer1': '0', 'leer2': '0', 'leer3': '0', 'symbol': 'EOSBTC'}]
            bidding_ar_db = db_set[0]['bidding_ar']  #[{'ki_erwartung': '0', 'leer1': '0', 'leer2': '0', 'leer3': '0', 'symbol': 'EOSBTC'}]
            db_coins.update({'asking_ar': ask_str,'bidding_ar': bid_str}, where('symbol') == My_traid_symbol)
        asking_ar_db = asking_ar_db.split(',')
        bidding_ar_db = bidding_ar_db.split(',')
        asking_ar_db2 = []
        bidding_ar_db2 = []
        counter=0
        for konto in asking_ar_db:
            if counter >=2 and konto != "":#verursacht versetzung wegen ergebnis row
                asking_ar_db2.append(Decimal(konto))
                bidding_ar_db2.append(Decimal(bidding_ar_db[counter]))
            counter+=1
        return asking_ar_db2, bidding_ar_db2
    def load_train(Coin_symbol,steps,btc_result,epoche,time_takt,sequence):
        satz = 600
        antwort = requests.get("https://api.hitbtc.com/api/2/public/candles/"+str(Coin_symbol)+"?limit="+str(satz)+"&period="+time_takt).json()
        result_H1 = []
        for konto in antwort:
            result_H1.append(Decimal(konto['close']))
        btc_result = requests.get("https://api.hitbtc.com/api/2/public/candles/BTCUSD?limit="+str(satz)+"&period="+time_takt).json()
        btc_orderbook = requests.get("https://api.hitbtc.com/api/2/public/orderbook/BTCUSD?limit="+str(satz)+"").json()
        #asking, bidding = Start.ord_book_bid_ask(btc_orderbook,Coin_symbol)
        #Start.insert_ordebook(btc_orderbook,Coin_symbol)
        model_etiket = "saved_models/"+Coin_symbol+"_steps_"+str(10)+"sequence_"+str(sequence)+".h5"
        # define input sequence
        sc = MinMaxScaler(feature_range = (0, 1))
        volume1, close1, min1, out_seq, close_b, volume_b, min_b = hist_price_dl_hitbtc(antwort,btc_result)
        #btc1,btc_v1, volume1, close1, min1, max1, out_seq = hist_price_dl_hitbtc_book(antwort,asking, bidding)
        n_steps, n_features, X1 , y1, boss_test, boss_futur, ergebniss, test3, test4, test5  = parameter(sc, volume1, close1, min1, out_seq, close_b, volume_b, min_b, steps, 1, sequence)
        exists = os.path.isfile(model_etiket)
        if exists:
            model_x6 = load_model(model_etiket)
            history_1 = model_x6.fit(X1, y1, validation_split=0.33, epochs=1, batch_size=10, verbose=1)
            #diagram(history)
        else:
            model_x6 = lasagna_x(50,boss_test,'adam','linear',0,'mse')
            history_1 = model_x6.fit(X1, y1, validation_split=0.33, epochs=epoche, batch_size=10, verbose=1)
        n_steps, n_features, X1 , y1, boss_test, boss_futur, ergebniss, test3, test4, test5  = parameter(sc, volume1, close1, min1, out_seq, close_b, volume_b, min_b, steps, 0, sequence)
        model_16     = model_x6.predict(boss_test)
        #model_17     = model_x6.predict(test2)
        model_18     = model_x6.predict(test3)
        model_19     = model_x6.predict(test4)
        model_20     = model_x6.predict(test5)
        model_futur  = model_x6.predict(boss_futur)

        model_16 = sc.inverse_transform(model_16)
        #model_17 = sc.inverse_transform(model_17)
        model_18 = sc.inverse_transform(model_18)
        model_19 = sc.inverse_transform(model_19)
        model_20 = sc.inverse_transform(model_20)
        model_futur = sc.inverse_transform(model_futur)
        model_x6.save(model_etiket)
        ergebniss = sc.inverse_transform(ergebniss)
        #              8           6
        korected, ki_close, deferenz_einzeln, count = korrektur(ergebniss,model_16,0)
        #model_17, a, n   ,n                    = korrektur(ergebniss,model_17,1)
        model_18, a, n   ,n                    = korrektur(ergebniss,model_18,1)
        model_19, a, n     ,n                  = korrektur(ergebniss,model_19,2)
        model_20, a, n    ,n                = korrektur(ergebniss,model_futur,3)
        model_futur, a, n ,n                    = korrektur(ergebniss,model_futur,4)

        plt.plot(korected, color = 'yellow', label = Coin_symbol +'Price')
        #plt.plot(model_17, color = 'orange', label = Coin_symbol +'Price')
        plt.plot(model_18, color = 'red', label = Coin_symbol +'Price')
        plt.plot(model_19, color = 'blue', label = Coin_symbol +'Price')
        plt.plot(model_20, color = 'gray', label = Coin_symbol +'Price')
        plt.plot(model_futur, color = 'green', label = Coin_symbol +'Price')
        plt.plot(ergebniss, color = 'black', label = Coin_symbol +'Price')
        plt.title(Coin_symbol)#
        plt.xlabel('Time')
        plt.ylabel(Coin_symbol +'Price')
        plt.legend()
        #plt.show()
        strFile = 'png/'+Coin_symbol+'sys.png'
        if os.path.isfile(strFile):
           os.remove(strFile)
        plt.savefig(strFile)
        plt.clf()

        diferenz = model_futur[0]-ergebniss[count-1]
        korected_futur = []
        count=0
        for konto in model_futur:
            korected_futur.append(model_futur[count]-diferenz)
            count+=1
        #Start.diagram(Coin_symbol,korected,ergebniss,0,0,0,'sys.png')
        return diferenz[0], deferenz_einzeln[0] , ki_close[0], model_18, model_19, model_20, korected_futur, result_H1

#ki_reult = Start.load_train("ADABTC","",1 ,"",100 ,1,"H1",72)
















"""
#diferenz = 0
        count=0
        durch_a=0
        durch_b=0
        for konto in model_16:
            durch_a +=model_16[count]
            durch_b +=ergebniss[count]
            #deferenz_einzeln+= model_16[count] - ergebniss[count]
            count+=1
        durch_a = durch_a/count
        durch_b = durch_b/count
        diferenz = durch_a-durch_b
"""