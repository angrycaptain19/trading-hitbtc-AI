import numpy as np
import requests,json
from decimal import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

class x2_keras_class():
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
    def ema (all_close, data_count):
        ema_satz = [all_close[0]]
        ema_drittel = [all_close[0]]
        SF = 2/ (45+1)
        SF2 = 2/ ((15)+1)
        for x in np.arange(data_count):
            ema_satz.append(   all_close[x]*SF+(1 - SF) * ema_satz[x-1]   )
            ema_drittel.append(   all_close[x]*SF2+(1 - SF2) * ema_drittel[x-1]     )
        
        

        plt.plot(all_close, color = 'red', label = 'close')
        plt.plot(ema_satz,  color = 'blue', label = Coin_symbol +'EMA '+str(45))
        plt.plot(ema_drittel,  color = 'green', label = Coin_symbol +'EMA '+str(15))
        plt.legend()
        #plt.show()

        return ema_satz, ema_drittel
    def stossdaempfer(all_close, crash_filter):
        all_close_filter  = []
        for i in np.arange(len(all_close)):
            if i == 0:
                all_close_filter.append(all_close[i])
            else:
                prozent = x2_keras_class.get_prozent(all_close_filter[i-1], all_close[i], 0) - 100
                diruz = all_close_filter[i-1]
                emrooz = all_close[i]
                n=1
                if prozent < crash_filter*-1:#dirooz az emrooz behtar boode
                    emrooz = all_close_filter[i-1]*(1-(crash_filter/100))
                elif prozent > crash_filter:#dirooz az emrooz badtar boode
                    emrooz = all_close_filter[i-1]*(1+(crash_filter/100))
                all_close_filter.append(emrooz)
        plt.plot(all_close, color = 'red', label = 'close')
        plt.plot(all_close_filter, color = 'black', label = 'filter')
        plt.legend()
        plt.show()


    def hitbtc_wurfel(Coin_symbol, EMA_periode, jomle, kalame):
        data_count = jomle+kalame
        data_btc = requests.get("https://api.hitbtc.com/api/2/public/candles/"+str(Coin_symbol)+"?limit="+str(data_count)+"&sort=DESC&period="+EMA_periode).json()
        data_btc.reverse()
        #from pandas.io.json import json_normalize
        #exit = json_normalize(data_btc)

        all_close = [data_btc[i]['close'] for i in np.arange(data_count)]
        all_close = np.array(all_close,dtype=float)
        x2_keras_class.stossdaempfer(all_close, 2.5)
        ema_satz, ema_drittel = x2_keras_class.ema (all_close, data_count)
        satz_wurfel  = []
        wort_zelle  = []
        horuf_zelle  = []
        for ema_count, i in enumerate(np.arange(jomle)):
            wort_zelle  = []
            for j in np.arange(kalame):
                horuf_zelle = [
                    data_btc[j + i]['close'],
                    data_btc[j + i]['max'],
                    data_btc[j + i]['min'],
                    data_btc[j + i]['volume'],
                    data_btc[j + i]['volumeQuote'],
                    ema_satz[ema_count],
                    ema_drittel[ema_count],
                ]

                wort_zelle.append(horuf_zelle)
                horuf_zelle=None
            satz_wurfel.append(wort_zelle)
            wort_zelle=None
        #test vergleich
        zeig = satz_wurfel[80]
        target_diferenz = np.array([all_close[i+kalame]-all_close[i+kalame-1]  for  i in range(jomle)],dtype=float)
        target_prozenz = np.array([x2_keras_class.get_prozent(all_close[i+kalame-1], all_close[i+kalame], 0)-100  for  i in range(jomle)],dtype=float)

        target = np.array([data_btc[i+kalame]['close']  for  i in range(jomle)])
        satz_wurfel = np.array(satz_wurfel)
        target = np.array([data_btc[i+kalame]['close']  for  i in range(jomle)])
        satz_wurfel = np.array(satz_wurfel)

        return satz_wurfel, target, target_diferenz, target_prozenz

    def fit_trasport_hin(wurfel, target, jomle, kalame):
        horuf = wurfel.shape[2]
        close_scala = MinMaxScaler(feature_range = (0, 1))
        wurfel = wurfel.reshape(jomle*kalame,horuf)
        wurfel = close_scala.fit_transform(wurfel)
        wurfel = wurfel.reshape(jomle,kalame,horuf)

        target = target.reshape((-1, 1))#listet daten verdikal
        target = close_scala.fit_transform(target)
        target = target.ravel()#listet daten horizontal
        return wurfel, target, close_scala
    def fit_trasport_zurueck(target, close_scala):
        target = target.reshape((-1, 1))#listet daten verdikal
        target = close_scala.inverse_transform(target)
        target = target.ravel()#listet daten horizontal
        return target
    def test_daten_wurfel(jomle, kalame):
        data_count = jomle+kalame
        data_btc = np.array([int(i) for i in np.arange(data_count)])
        satz_wurfel  = []
        wort_zelle  = []
        horuf_zelle  = []
        test_target_hilfe = 0
        target = []
        for i in np.arange(jomle):
            wort_zelle  = []
            for j in np.arange(kalame):
                # hier sollte noch eine schleife kommen mit count_of_values als range. aber ich war faul und habe 5 Sätze gesetzt.
                horuf_zelle = [data_btc[j+i] * 1]
                test_target_hilfe += int(data_btc[j+i]*1)

                horuf_zelle.append(data_btc[j+i]*2)
                test_target_hilfe += data_btc[j+i]*2

                horuf_zelle.append(data_btc[j+i]*3)
                test_target_hilfe += data_btc[j+i]*3

                horuf_zelle.append(data_btc[j+i]*4)
                test_target_hilfe += data_btc[j+i]*4

                horuf_zelle.append(data_btc[j+i]*5)
                test_target_hilfe += data_btc[j+i]*5
                wort_zelle.append(horuf_zelle)
                horuf_zelle=None
            target.append(test_target_hilfe)
            test_target_hilfe = 0

            satz_wurfel.append(wort_zelle)
            wort_zelle=None
        satz_wurfel = np.array(satz_wurfel)
        target = np.array(target)
        return satz_wurfel, target
    def hermannplatz(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen):
        if training_0 == 1:
            satz_wurfel, target, target_diferenz, target_prozenz = x2_keras_class.hitbtc_wurfel(Coin_symbol, EMA_periode, jomle, kalame)
        if training_0 == 0:
            satz_wurfel, target = x2_keras_class.test_daten_wurfel(jomle, kalame)
        satz_wurfel, target, close_scala = x2_keras_class.fit_trasport_hin(satz_wurfel, target, jomle, kalame)

        x_train, x_test, y_train, y_test  = train_test_split(satz_wurfel, target, test_size = test_prozenz, random_state=2)
        return x_train, x_test, y_train, y_test, close_scala

Coin_symbol = "BTCUSD"
EMA_periode ="D1"
jomle = 90
kalame = 15
test_prozenz = 0.02 # 0.2 = 20%
training_0 = 1
#count_of_values = 5 # ist die Anzahl von Werten(1:close 2:max 3:min........  der wurfel wird 2d gemcht
epochen = 1000
x_train, x_test, y_train, y_test, close_scala = x2_keras_class.hermannplatz(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen)
#y_test = np.array(y_test)

#data = requests.get("https://api.hitbtc.com/api/2/public/candles/BTCUSD?limit=600&period=D1").json()
#data2 = requests.get("https://api.hitbtc.com/api/2/public/candles/").json()
x = np.array([1,2,3,4,5,6])

