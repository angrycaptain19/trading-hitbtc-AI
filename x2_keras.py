from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import load_model
from decimal import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import os
import requests,json
import numpy as np
import matplotlib.pyplot as plt


class x2_keras_class():
    def fit_trasport_hin(wurfel, target, jomle, kalame):
        horuf = wurfel.shape[2]
        close_scala = MinMaxScaler(feature_range = (0, 1))
        wurfel = wurfel.reshape(jomle*kalame, horuf)
        wurfel = close_scala.fit_transform(wurfel)
        wurfel = wurfel.reshape(jomle, kalame, horuf)

        target = target.reshape((-1, 1))#listet daten verdikal
        target = close_scala.fit_transform(target)
        target = target.ravel()#listet daten horizontal
        return wurfel, target, close_scala
    def fit_trasport_zurueck(target, close_scala):
        target = target.reshape((-1, 1))#listet daten verdikal
        target = close_scala.inverse_transform(target)
        target = target.ravel()#listet daten horizontal
        return target
    def diagramm(results_test, y_test, Coin_symbol, history, epochen, fehler, jomle, kalame, ohne_reaktion, tozih, all_close, ema_satz, ema_drittel):
        plt.scatter(range(len(y_test)),results_test,c='r')  #array([[33.150745]], dtype=float32)
        plt.scatter(range(len(y_test)),y_test,c='g')        #array([['6627.10']], dtype='<U7')
        plt.title(Coin_symbol +" e:"+str(epochen)+" f "+str(fehler) )
        plt.legend()
        file_name =str(round(ohne_reaktion-fehler, 4))+' '+ Coin_symbol+' '+str(epochen)+' t('+tozih+')('+str(jomle)+ 'x'+str(kalame)+')f'+str(round(fehler, 4))+'-'+str(round(ohne_reaktion, 4))
        strFile = 'x2_png/'+file_name+' scatter.png'
        if os.path.isfile(strFile):
           os.remove(strFile)
        plt.savefig(strFile)
        plt.clf()

        all_loss=history.history['loss'][25:]
        plt.plot(all_loss)
        plt.title(Coin_symbol +" e:"+str(epochen)+" f "+str(fehler) )
        strFile = 'x2_png/'+file_name+' loss.png'
        if os.path.isfile(strFile):
           os.remove(strFile)
        plt.savefig(strFile)
        plt.clf()

        plt.plot(results_test, color = 'red', label = 'y_test')
        plt.plot(y_test, color = 'black', label = 'results')
        plt.title(Coin_symbol +" e:"+str(epochen)+" f "+str(fehler) )
        plt.legend()
        strFile = 'x2_png/'+file_name+' plot.png'
        if os.path.isfile(strFile):
           os.remove(strFile)
        plt.savefig(strFile)
        plt.clf()
        plt.plot(all_close, color = 'red', label = 'close')
        plt.plot(ema_satz,  color = 'blue', label = Coin_symbol +'EMA '+str(45))
        plt.plot(ema_drittel,  color = 'green', label = Coin_symbol +'EMA '+str(15))
        plt.legend()
        #strFile = 'x2_png/'+Coin_symbol+' EMA.png'
        strFile = 'x2_png/'+file_name+' EMA.png'

        if os.path.isfile(strFile):
           os.remove(strFile)
        plt.savefig(strFile)
        plt.clf()
    def lasagna_x(x_train):
        regressor = Sequential()                                                     #jomle    #kalame    ,    horuf
        regressor.add(LSTM(units = 50, return_sequences = True, batch_input_shape = (None,   x_train.shape[1], x_train.shape[2])))
        regressor.add(Dropout(0.2))
        regressor.add(LSTM(units = 50, return_sequences = True))
        regressor.add(Dropout(0.2))
        regressor.add(LSTM(units = 50, return_sequences = True))
        regressor.add(Dropout(0.2))
        regressor.add(LSTM(units = 50))
        regressor.add(Dropout(0.2))
        regressor.add(Dense(units = 1))
        regressor.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])
        return regressor
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
                horuf_zelle  = [] 
                horuf_zelle.append(data_btc[j+i]*1)
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
    def ema (all_close, data_count, Coin_symbol):
        ema_satz = [all_close[0]]
        ema_drittel = [all_close[0]]
        SF = 2/ (45+1)
        SF2 = 2/ ((15)+1)
        for x in np.arange(data_count):
            ema_satz.append(   all_close[x]*SF+(1 - SF) * ema_satz[x-1]   )
            ema_drittel.append(   all_close[x]*SF2+(1 - SF2) * ema_drittel[x-1]     )
        return ema_satz, ema_drittel
    def fehler_rechner(results, y_test):
        counter = 0
        fehler = 0
        ohne_reaktion = 0 # zeigt den Fehler wenn man den t-1 angibt. also einfach nichts vorhersgat
        for wert in results:
            distanz = wert - y_test[counter]
            distanz_zu_zero = y_test[counter]
            counter += 1
            if distanz <= 0:
                distanz = distanz * -1
            fehler += distanz
            if distanz_zu_zero <= 0:
                distanz_zu_zero = distanz_zu_zero * -1
            ohne_reaktion += distanz_zu_zero
        return fehler/counter, ohne_reaktion/counter
    def stossdaempfer(all_close, crash_filter):
        all_close_filter  = []
        for i in np.arange(len(all_close)):
            if i == 0:
                all_close_filter.append(all_close[i])
            else:
                prozent = x2_keras_class.get_prozent(all_close_filter[i-1], all_close[i], 0) - 100
                if prozent < crash_filter*-1:#dirooz az emrooz behtar boode
                    emrooz = all_close_filter[i-1]*(1-(crash_filter/100))
                    all_close_filter.append(emrooz)
                elif prozent > crash_filter:#dirooz az emrooz badtar boode
                    emrooz = all_close_filter[i-1]*(1+(crash_filter/100))
                    all_close_filter.append(emrooz)
                else:
                    all_close_filter.append(all_close[i])
        return all_close_filter
    def hitbtc_wurfel(Coin_symbol, EMA_periode, jomle, kalame, crash_filter):
        data_count = jomle+kalame
        data_btc = requests.get("https://api.hitbtc.com/api/2/public/candles/"+str(Coin_symbol)+"?limit="+str(data_count)+"&sort=DESC&period="+EMA_periode).json()
        data_btc.reverse()
        
        all_close  = []
        for i in np.arange(data_count):
            all_close.append(data_btc[i]['close'])
        all_close = np.array(all_close,dtype=float)
        all_close = x2_keras_class.stossdaempfer(all_close, crash_filter)
        ema_satz, ema_drittel = x2_keras_class.ema (all_close, data_count, Coin_symbol)
        satz_wurfel  = []
        wort_zelle  = []
        horuf_zelle  = []
        ema_count = 0

        for i in np.arange(jomle):
            wort_zelle  = []
            for j in np.arange(kalame):
                horuf_zelle  = []
                #horuf_zelle.append(data_btc[j+i]['close'])
                horuf_zelle.append(all_close[j+i])
                #horuf_zelle.append(data_btc[j+i]['max'])
                #horuf_zelle.append(data_btc[j+i]['min'])
                horuf_zelle.append(data_btc[j+i]['volume'])
                #horuf_zelle.append(data_btc[j+i]['volumeQuote'])
                horuf_zelle.append(ema_satz[ema_count])
                horuf_zelle.append(ema_drittel[ema_count])
                wort_zelle.append(horuf_zelle)
                horuf_zelle=None
            ema_count += 1
            satz_wurfel.append(wort_zelle)
            wort_zelle=None
        #test vergleich
        target_diferenz = np.array([all_close[i+kalame]-all_close[i+kalame-1]  for  i in range(jomle)],dtype=float)
        target_prozenz = np.array([x2_keras_class.get_prozent(all_close[i+kalame-1], all_close[i+kalame], 0)-100  for  i in range(jomle)],dtype=float)
        
        target = np.array([data_btc[i+kalame]['close']  for  i in range(jomle)])
        satz_wurfel = np.array(satz_wurfel)
        target = np.array([data_btc[i+kalame]['close']  for  i in range(jomle)])
        satz_wurfel = np.array(satz_wurfel)

        return satz_wurfel, target, target_diferenz, target_prozenz, all_close, ema_satz, ema_drittel
    def hermannplatz(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, crash_filter):
        if training_0 == 1:
            satz_wurfel, target, target_diferenz, target_prozenz, all_close, ema_satz, ema_drittel = x2_keras_class.hitbtc_wurfel(Coin_symbol, EMA_periode, jomle, kalame, crash_filter)
        if training_0 == 0:
            satz_wurfel, target = x2_keras_class.test_daten_wurfel(jomle, kalame)
        satz_wurfel, target, close_scala = x2_keras_class.fit_trasport_hin(satz_wurfel, target_prozenz, jomle, kalame)

        x_train, x_test, y_train, y_test  = train_test_split(satz_wurfel, target, test_size = test_prozenz, random_state=2)
        return x_train, x_test, y_train, y_test, close_scala, all_close, ema_satz, ema_drittel
    def my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen, tozih, crash_filter):
        x_train, x_test, y_train, y_test, close_scala, all_close, ema_satz, ema_drittel = x2_keras_class.hermannplatz(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, crash_filter)
        #daten = sc.fit_transform(x)
        model_etiket = "saved_models/kalame_"+str(kalame)+"_EMA_periode_"+str(EMA_periode)+"training_0"+str(training_0)+".h5"
        exists = os.path.isfile(model_etiket)
        if exists:
            regressor = load_model(model_etiket)
            #epochen = epochen/10
            history = regressor.fit(x_train, y_train, epochs = epochen, validation_data = (x_test, y_test))
        else:
            regressor = x2_keras_class.lasagna_x(x_train)
            history = regressor.fit(x_train, y_train, epochs = epochen, validation_data = (x_test, y_test))
        regressor.save(model_etiket)

        results_test  = regressor.predict(x_test)#array([[0.08052856],[0.05391689]], dtype=float32)
        results_test = x2_keras_class.fit_trasport_zurueck(results_test, close_scala)

        y_test = np.array(y_test, dtype=float)
        y_test = y_test.reshape(len(y_test), 1)
        y_test = x2_keras_class.fit_trasport_zurueck(y_test, close_scala)
        fehler, ohne_reaktion = x2_keras_class.fehler_rechner(results_test, y_test)
        x2_keras_class.diagramm(results_test, y_test, Coin_symbol, history, epochen, fehler, jomle, kalame, ohne_reaktion, tozih, all_close, ema_satz, ema_drittel)
        
        return results_test, y_test



