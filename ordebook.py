import requests,json
import time
import datetime
from datetime import timedelta
from tinydb import TinyDB, Query
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage
import matplotlib.pyplot as plt
import os
# multivariate lstm example
from numpy import array
from numpy import loadtxt
from numpy import hstack
import numpy as np # linear algebra
from sklearn.preprocessing import MinMaxScaler
from decimal import *
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from keras import optimizers
from keras import regularizers
def diagram(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model train vs validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()
def lasagna_x(output_dim,X_train,optimizer,activation,dorpout,loss):
    model = Sequential()
    #model.add(LSTM(units=output_dim, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(LSTM(units=output_dim, return_sequences=True, input_shape=(1,1)))
    #model.add(LSTM(units=output_dim, return_sequences=True, input_shape=(1)))
    if dorpout!=0:
        model.add(Dropout(0.2))
    model.add(Dense(units=32,activation=activation))
    model.add(LSTM(units=output_dim, return_sequences=False))
    if dorpout!=0:
        model.add(Dropout(0.2))
    model.add(Dense(units=1,activation=activation))
    model.compile(optimizer='rmsprop',loss=loss, metrics=['accuracy'])
    return model
def get_prozent(mutter,kind,int0_str1):
    prozent = 0 
    if mutter !=0:
        prozent = kind/mutter * 100
        #prozent = round(prozent, 2)
    if(int0_str1==1):
        prozent = str(prozent)+"%"
        if len(prozent)==4:
            prozent="0"+prozent
    return prozent

def get_prozent_array(mutter):
    first=0
    returnyy=[]
    for count, i_set in enumerate(mutter):
        if count==0:
            first = i_set
        returnyy.append(get_prozent(first,i_set,0))
    return returnyy

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
def daten_repair_1(sc,daten):
    daten =[float(numeric_string) for numeric_string in daten]
    daten = array(daten)
    daten = daten.reshape((len(daten),1))
    daten = sc.fit_transform(daten)
    return daten
def parameter_alt(ask_count, ask_price, bid_count, bid_price,result,bX, by):
    sc = MinMaxScaler(feature_range = (0, 1))
    ask_count   = daten_repair_1(sc,ask_count)
    ask_price   = daten_repair_1(sc,ask_price)
    bid_count   = daten_repair_1(sc,bid_count)
    bid_price   = daten_repair_1(sc,bid_price)
    #result   = daten_repair_1(sc,result)
    #result      = daten_repair_1(sc,result)
    ask_count   = ask_count[range(0, len(ask_count))]
    ask_price      = ask_price[range(0, len(ask_price))]
    bid_count    = bid_count[range(0 , len(bid_count))]
    bid_price    = bid_price[range(0 , len(bid_price))]
    #result    = result[range(0 , len(result))]
    dataset = hstack(( ask_count, ask_price, bid_count, ask_price, ask_price))#min max btv
    X, y = split_sequences(dataset, 1)
    n_features = X.shape[2]
    boss_futur = X[range(0, len(X))] #boss_futur bX
    model_etiket = "saved_models/oorderbook_BTCUSD_1.h5"
    exists = os.path.isfile(model_etiket)
    if exists:
        model_x6 = load_model(model_etiket)
        history_1 = model_x6.fit(result, result, validation_split=0.33, epochs=1, batch_size=1, verbose=1)
    else:
        model_x6 = lasagna_x(50, 0, 'adam', 'linear', 0, 'mse')
        history_1 = model_x6.fit(result, result, validation_split=0.33, epochs=10, batch_size=1, verbose=1)
    #diagram(history_1)
    model_x6.save(model_etiket)
    model_futur  = model_x6.predict(boss_futur)#array([[[1.11250591e-04, 1.00000000e+00, 3.60092328e-06, 
    model_18     = model_x6.predict(bX)        #array([[[2.36703385e-05, 1.00000000e+00, 4.72121052e-05, 1.00000000e+00]],

    model_18 = sc.inverse_transform(model_18)#array([[10786.009],
    plt.plot(model_18, color = 'red', label =  'Price')
    plt.plot(by, color = 'black', label =  'Price')
    model_futur = sc.inverse_transform(model_futur)
    plt.plot(model_futur, color = 'green', label =  'Price')
    plt.legend()
    plt.show()
    return n_features, X, y 
def parameter_u(ask_count, ask_price, bid_count, bid_price,result):
    sc = MinMaxScaler(feature_range = (0, 1))
    ask_count   = daten_repair_1(sc,ask_count)
    ask_price   = daten_repair_1(sc,ask_price)
    bid_count   = daten_repair_1(sc,bid_count)
    bid_price   = daten_repair_1(sc,bid_price)
    #result   = daten_repair_1(sc,result)
    ask_count = ask_count[range(len(ask_count))]
    ask_price = ask_price[range(len(ask_price))]
    bid_count = bid_count[range(len(bid_count))]
    bid_price = bid_price[range(len(bid_price))]
    #result    = result[range(0 , len(result))]
    dataset = hstack(( ask_count, ask_price, bid_count, ask_price,  ask_price))#min max btv
    X, y = split_sequences(dataset, 1)
    n_features = X.shape[2]
    return X, result
def daten_repair_1(sc,daten):
    daten =[float(numeric_string) for numeric_string in daten]
    daten = array(daten)
    daten = daten.reshape((len(daten), 1))
    daten = sc.fit_transform(daten)
    return daten
def time_macher(btc_result,symbol):
    db_coins = TinyDB('datenbank/coins_M1.json')
    db_coins2 = TinyDB('datenbank/coins_M1_mit_time.json')
    User = Query
    bii=0
    for btc_c, doc in enumerate(btc_result, start=1):
        tm = doc['timestamp']
        close = doc['close']
        jahr = tm.split("-")[0]
        mont = tm.split("-")[1]
        tag = tm.split("T")[0].split("-")[2]
        hour = tm.split("T")[1].split(":")[0]
        min = tm.split("T")[1].split(":")[1]
        sec = tm.split("T")[1].split(":")[2].split(".")[0]
        last_time = datetime.datetime(int(jahr), int(mont), int(tag), int(hour), int(min), int(sec))#2019, 8, 3, 17, 23
        last_time =  last_time+ timedelta(hours=4)
        last_time =  last_time+ timedelta(seconds=1800)
        count = db_coins.search(where('symbol') == symbol)
        for row_idx in count:
            set_time = row_idx['time']#'20:15:04.223782'
            set_time_str = row_idx['time']#'20:15:04.223782'
            hour2 = set_time.split(":")[0]
            min2 = set_time.split(":")[1]
            sec2 = set_time.split(":")[2].split(".")[0]
            set_time = datetime.datetime(int(jahr), int(mont), int(tag),int(hour2), int(min2), int(sec2))
            if set_time > datetime.datetime.now():
                set_time = datetime.datetime(int(jahr), int(mont), int(tag)-1,int(hour2), int(min2), int(sec2))#2019, 8, 3, 17, 22, 28
            if last_time + timedelta(seconds=80) >= set_time and last_time + timedelta(seconds=40) <= set_time :
                bii+=1
                n=row_idx
                ask_count = row_idx['ask_count']
                ask_price = row_idx['ask_price']
                bid_count = row_idx['bid_count']
                bid_price = row_idx['bid_price']
                time3     = row_idx['time']
                db_coins2.insert({'symbol': symbol ,'ask_count': ask_count,'ask_price': ask_price,'bid_count': bid_count,'bid_price': bid_price,'time': time3,'leer3': close})
                db_coins.remove(where('time') == set_time_str)
                break
            n=2
        print("btc_c" + str(btc_c)+" innen "+str(bii))#451 569

    return last_time
def row_macker(data,data2,data3,data4):
    ar_mm=[]
    data  = data.split(',')#['0.00205', '0.00026', '0.00001', '0.00026', '0.00002', '
    data2 = data2.split(',')#['11295.00', '11294.15', '11291.56', '11291.03', '11290.0
    data3 = data3.split(',')#['0.00214', '0.00001', '0.00213', '0.00021', '0.00214', '0.00261', '0.00
    data4 = data4.split(',')#['10360.30', '10361.00', '10361.20', '10362.00', '10362.10', '10362.70', '10363.1
    count = 0
    shish=0
    for row_data in data:
        if row_data!="":
            yek  = Decimal(row_data)
            do   = Decimal(data2[count])
            yekdo = yek*do
            se   = Decimal(data3[count])
            char = Decimal(data4[count])
            sechar = se*char
            panj = yekdo - sechar
            shish+=panj
            count+=1
    return shish
def query_orderbook(symbol):
    db_coins = TinyDB('datenbank/orderbook.json')
    sets = db_coins.search(where('symbol') == symbol)
    count=0
    dade_vorgestern=[]
    dade_gestern=[]
    javab_gestern=[]
    javab_heute=[]
    training_20_ta =0
    for row_idx in sets:
        training_20_ta        +=1
        if count>1:
            result_pasfarda = row_idx['bid_price'].split(',')#'10781.71'
            ng=len(result_pasfarda)-2
            result_pasfarda_0 = result_pasfarda[ng]
            javab_heute.append(Decimal(result_pasfarda_0))
        
        if count>2:#tv
            #bX, by = parameter_u(row_macker(ask_count_farda),row_macker(ask_price_farda),row_macker(bid_count_farda),row_macker(bid_price_farda),result_pasfarda_ar)
            #bX, by = parameter_u(row_macker(ask_count_farda),row_macker(ask_price_farda),row_macker(bid_count_farda),row_macker(bid_price_farda),result_pasfarda_0)
            #n_features, X, y = parameter(row_macker(ask_count),row_macker(ask_price),row_macker(bid_count),row_macker(bid_price),result_ar,bX, by)
            javab_gestern.append(Decimal(result_0))
            dade_gestern.append(row_macker(row_idx['ask_count'],row_idx['ask_price'],row_idx['bid_count'],row_idx['bid_price']))
            if training_20_ta>7:#EXIT
                training_20_ta = 0#                 5                3             3              4  
                n_features, X, y = parameter(dade_vorgestern, javab_gestern, dade_gestern, javab_heute)
                dade_vorgestern=[]
                dade_gestern=[]
                javab_gestern=[]
                javab_heute=[]
                count                =0
        if count>0:
            result = row_idx['bid_price'].split(',')#'10781.71'
            ng=len(result)-2
            result_0 = result[ng]
        count+=1
        print(str(count)+"/"+str(len(sets)))
        dade_vorgestern.append(row_macker(row_idx['ask_count'],row_idx['ask_price'],row_idx['bid_count'],row_idx['bid_price']))
def parameter(dade_vorgestern, javab_gestern, dade_gestern, javab_heute):
    defi = len(dade_vorgestern) - len(dade_gestern)
    dade_vorgestern     = dade_vorgestern[defi: len(dade_vorgestern)]
    defi = len(javab_gestern) - len(dade_gestern)
    javab_gestern       = javab_gestern[defi:  len(javab_gestern)]
    defi = len(javab_heute) - len(dade_gestern)
    javab_heute         = javab_heute[defi:  len(javab_heute)]

    ergebnis_heute = javab_heute
    sc = MinMaxScaler(feature_range = (0, 1))
    dade_vorgestern   = daten_repair_1(sc,dade_vorgestern)#array([[0.24125787],
    javab_gestern   = daten_repair_1(sc,javab_gestern)
    dade_gestern   = daten_repair_1(sc,dade_gestern)
    javab_heute   = daten_repair_1(sc,javab_heute)
    #result   = daten_repair_1(sc,result)
    #result      = daten_repair_1(sc,result)
    dade_vorgestern = dade_vorgestern[range(len(dade_vorgestern))]
    javab_gestern = javab_gestern[range(len(javab_gestern))]
    dade_gestern = dade_gestern[range(len(dade_gestern))]
    javab_heute = javab_heute[range(len(javab_heute))]
    #result    = result[range(0 , len(result))]
    dataset = hstack(( dade_vorgestern, javab_gestern))#min max btv
    dataset2 = hstack(( dade_gestern, javab_heute))#min max btv
    X______, y____ = split_sequences(dataset, 1)
    X2_____, y2___ = split_sequences(dataset2, 1)
    n_features = X______.shape[2]
    #boss_vorgestern = X______[range(0, len(X______))] #boss_futur bX
    boss_vorgestern = X______
    #boss_gestern = X2_____[range(0, len(X2_____))] #boss_futur bX
    boss_gestern = X2_____
    model_etiket = "saved_models/oorderbook_BTCUSD_3.h5"
    exists = os.path.isfile(model_etiket)
    if exists:
        model_x6 = load_model(model_etiket)
        history_1 = model_x6.fit(X______, y____, validation_split=0.33, epochs=50, batch_size=12, verbose=1)
    else:
        model_x6 = lasagna_x(50, 0, 'adam', 'linear', 0, 'mse')
        history_1 = model_x6.fit(X______, y____, validation_split=0.33, epochs=100, batch_size=12, verbose=1)
    #diagram(history_1)
    model_x6.save(model_etiket)
    model_vorgestern  = model_x6.predict(boss_vorgestern)
    model_gestern    = model_x6.predict(boss_gestern)

    model_gestern    = sc.inverse_transform(model_gestern)#array([[10786.009],
    model_vorgestern = sc.inverse_transform(model_vorgestern)
    #y____                = sc.inverse_transform(y____)
    #y2___                = sc.inverse_transform(y2___)
    plt.plot(get_prozent_array(model_vorgestern), color = 'yellow', label =  'model_vorgestern')
    plt.plot(get_prozent_array(model_gestern),    color = 'red',   label =  'model_gestern')
    plt.plot(get_prozent_array(ergebnis_heute),            color = 'black', label =  'ergebnis_heute')
    plt.legend()
    #plt.show()
    return n_features, X______, y____ 
def insert_ordebook(booking_all,My_traid_symbol):
    time_this = booking_all["timestamp"]
    konto_ask = booking_all["ask"]#verkauf
    konto_ask.reverse()
    ask_count =""
    ask_price =""
    for konto in konto_ask:
        ask_count += str(konto['size'])+","
        ask_price += str(konto['price'])+","
    konto_bid = booking_all["bid"]#kauf
    konto_bid.reverse()
    bid_count =""
    bid_price =""
    for konto in konto_bid:
        bid_count += str(konto['size'])+","
        bid_price += str(konto['price'])+","

    db_coins = TinyDB('datenbank/orderbook.json')
    User = Query
    set_count = db_coins.count(where('symbol') == My_traid_symbol)
    #db_coins.insert({'symbol': My_traid_symbol ,'ask_count': ask_count,'ask_price': ask_price,'bid_count': bid_count,'bid_price': bid_price,'time': str(datetime.datetime.now().time()),'leer3': str(0)})
    db_coins.insert({'symbol': My_traid_symbol ,'ask_count': ask_count,'ask_price': ask_price,'bid_count': bid_count,'bid_price': bid_price,'time': time_this,'leer3': str(0)})
EMA_periode ="M5"
satz = 500
count=0
while True:#cheshme
    count+=1
    #btc_result = requests.get("https://api.hitbtc.com/api/2/public/candles/BTCUSD?limit="+str(1000)+"&period="+EMA_periode).json() #'timestamp': '2019-08-03T11:26:00.000Z',
    #last_time = time_macher(btc_result,"BTCUSD")
    btc_orderbook = requests.get("https://api.hitbtc.com/api/2/public/orderbook/BTCUSD?limit="+str(satz)+"").json()
    insert_ordebook(btc_orderbook,"BTCUSD")
    query_orderbook("BTCUSD")
    print(count)
    time.sleep(60)



