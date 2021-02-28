import requests,json
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class aa1_daten_hilfe_class():
    def normalisiren_hilfe(wert, close_scala, Coin_symbol):
        wert = wert.reshape((-1, 1))#listet daten verdikal
        wert = close_scala.fit_transform(wert)
        wert = wert.ravel()#listet daten horizontal
        return wert
    def normalisiren(close, max, min, volume, volumeQuote, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar, Coin_symbol):
        cs_close = MinMaxScaler(feature_range = (0, 1))
        close = aa1_daten_hilfe_class.normalisiren_hilfe(close, cs_close, Coin_symbol)

        cs_max = MinMaxScaler(feature_range = (0, 1))
        max = aa1_daten_hilfe_class.normalisiren_hilfe(max, cs_max, Coin_symbol)

        cs_min = MinMaxScaler(feature_range = (0, 1))
        min = aa1_daten_hilfe_class.normalisiren_hilfe(min, cs_min, Coin_symbol)
        
        cs_volume = MinMaxScaler(feature_range = (0, 1))
        volume = aa1_daten_hilfe_class.normalisiren_hilfe(volume, cs_volume, Coin_symbol)

        cs_volumeQuote = MinMaxScaler(feature_range = (0, 1))
        volumeQuote = aa1_daten_hilfe_class.normalisiren_hilfe(volumeQuote, cs_volumeQuote, Coin_symbol)

        cs_ema_satz = MinMaxScaler(feature_range = (0, 1))
        ema_satz = aa1_daten_hilfe_class.normalisiren_hilfe(ema_satz, cs_ema_satz, Coin_symbol)

        cs_ema_drittel = MinMaxScaler(feature_range = (0, 1))
        ema_drittel = aa1_daten_hilfe_class.normalisiren_hilfe(ema_drittel, cs_ema_drittel, Coin_symbol)

        cs_target_diferenz = MinMaxScaler(feature_range = (0, 1))
        target_diferenz = aa1_daten_hilfe_class.normalisiren_hilfe(target_diferenz, cs_target_diferenz, Coin_symbol)

        cs_target_prozenz = MinMaxScaler(feature_range = (0, 1))
        target_prozenz = aa1_daten_hilfe_class.normalisiren_hilfe(target_prozenz, cs_target_prozenz, Coin_symbol)

        cs_target_polar = MinMaxScaler(feature_range = (0, 1))
        target_polar = aa1_daten_hilfe_class.normalisiren_hilfe(target_polar, cs_target_polar, Coin_symbol)

        return close, max, min, volume, volumeQuote, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar, cs_close, cs_max, cs_min, cs_volume, cs_volumeQuote, cs_ema_satz, cs_ema_drittel, cs_target_diferenz, cs_target_prozenz, cs_target_polar
    def fit_trasport_zurueck(results_test, y_test, close_scala):
        results_test = results_test.reshape((-1, 1))#listet daten verdikal
        results_test = close_scala.inverse_transform(results_test)
        results_test = results_test.ravel()#listet daten horizontal
        y_test = y_test.reshape((-1, 1))#listet daten verdikal
        y_test = close_scala.inverse_transform(y_test)
        y_test = y_test.ravel()#listet daten horizontal
        return results_test, y_test,
    def test_daten(jomle, kalame, wert_count):
        data_count = jomle+kalame
        wert1 = 0
        wert2 = 0
        wert3 = 0
        wert4 = 0
        wert5 = 0
        wert6 = 0
        wert7 = 0
        wert8 = 0
        wert9 = 0
        wert10 = 0

        if wert_count>1:
            wert1 = np.array([int(i+3) for i in np.arange(data_count)])
        if wert_count>2:
            wert2 = np.array([int(i+7) for i in np.arange(data_count)])
        if wert_count>3:
            wert3 = np.array([int(i+20) for i in np.arange(data_count)])
        if wert_count>4:
            wert4 = np.array([int(i+30) for i in np.arange(data_count)])
        if wert_count>5:
            wert5 = np.array([int(i+40) for i in np.arange(data_count)])
        if wert_count>6:
            wert6 = np.array([int(i+50) for i in np.arange(data_count)])
        if wert_count>7:
            wert7 = np.array([int(i+60) for i in np.arange(data_count)])
        if wert_count>8:
            wert8 = np.array([int(i+70) for i in np.arange(data_count)])
        if wert_count>9:
            wert9 = np.array([int(i+80) for i in np.arange(data_count)])
        if wert_count>10:
            wert10 = np.array([int(i+90) for i in np.arange(data_count)])
        wert1 = np.array(wert1,dtype=float)
        wert2 = np.array(wert2,dtype=float)
        wert3 = np.array(wert3,dtype=float)
        wert4 = np.array(wert4,dtype=float)
        wert5 = np.array(wert5,dtype=float)
        wert6 = np.array(wert6,dtype=float)
        wert7 = np.array(wert7,dtype=float)
        wert8 = np.array(wert8,dtype=float)
        wert9 = np.array(wert9,dtype=float)
        wert10 = np.array(wert10,dtype=float)

        target_wert = np.array([(wert1[i]*28/wert2[i])*(wert1[i]*28/wert2[i]) for i in np.arange(data_count)])
        return target_wert, wert1, wert2, wert3, wert4, wert5, wert6, wert7, wert8, wert9, wert10

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
    def get_polar(mutter,kind):
        polar = 0 
        if mutter >kind:
            polar = -1
        else:
            polar = 1
        return polar
    def ema (all_close, data_count, ema1, ema2):
        ema_satz = [all_close[0]]
        ema_drittel = [all_close[0]]
        SF = 2/ (ema2+1)
        SF2 = 2/ ((ema1)+1)
        for x in np.arange(data_count):
            ema_satz.append(   all_close[x]*SF+(1 - SF) * ema_satz[x-1]   )
            ema_drittel.append(   all_close[x]*SF2+(1 - SF2) * ema_drittel[x-1]     )
        return ema_satz, ema_drittel
    def fehler_rechner(results, y_test):
        counter = 0
        fehler = 0
        ohne_reaktion = 0 # zeigt den Fehler wenn man den t-1 angibt. also einfach nichts vorhersgat
        for wert in results:
            distanz = wert - y_test[counter] # wert -0.96844065 distanz=2.5315593481063865
            distanz_zu_zero = y_test[counter]
            counter += 1
            if distanz <= 0:
                distanz = distanz * -1
            fehler += distanz
            if distanz_zu_zero <= 0:
                distanz_zu_zero = distanz_zu_zero * -1
            ohne_reaktion += distanz_zu_zero  # distanz_zu_zero = 3.500000000000002
        return fehler/counter, ohne_reaktion/counter
    def fehler_prozent_polar(results, y_test):
        #result = array([ 0.01874222, -0.01470321,  0.07847983,  0.0341922 ,  0.44422168,        0.53358972,  0.05137402,  0.2266587 ,  0.04979908,  0.48476723, 0.09676301,  0.10620622,  0.01660462,  0.03720167,  0.0237819 ,       -0.00810272])
        #y_test = array([0.         , 0.         , 1.         , 0.         , 0.         , 0.               , 0.         , 0.         , 0.         , 0.         , 0.        , 0.         , 0.         , 1.         , 0.         ,        1.])
        #                     1           1            0            1             0               0               1            1              1          0           1             1            1            0            1             0
        counter = 0
        fehler = 0
        for wert in results:
            if wert >= 0.25:
                wert = 1
            else:
                wert = 0
            if wert != y_test[counter]:
                fehler += 1
            counter += 1
        return fehler, counter
    def fehler_rechner_polar(results, y_test):
        counter = 0
        fehler = 0
        for wert in results:
            if wert < 0 and y_test[counter] > 0:
                fehler += 1
            if wert > 0 and y_test[counter] < 0:
                fehler += 1
            counter += 1
        return fehler, counter
    def stossdaempfer(all_close, crash_filter):
        all_close_filter  = []
        for i in np.arange(len(all_close)):
            if i == 0:
                all_close_filter.append(all_close[i])
            else:
                prozent = aa1_daten_query_class.get_prozent(all_close_filter[i-1], all_close[i], 0) - 100
                if prozent < crash_filter*-1:#dirooz az emrooz behtar boode
                    emrooz = all_close_filter[i-1]*(1-(crash_filter/100))
                    all_close_filter.append(emrooz)
                elif prozent > crash_filter:#dirooz az emrooz badtar boode
                    emrooz = all_close_filter[i-1]*(1+(crash_filter/100))
                    all_close_filter.append(emrooz)
                else:
                    all_close_filter.append(all_close[i])
        return all_close_filter
    def hitbtc_query_mit_ema(Coin_symbol, EMA_periode, data_count, ema1, ema2, kalame):
        data_btc = requests.get("https://api.hitbtc.com/api/2/public/candles/"+str(Coin_symbol)+"?limit="+str(data_count)+"&sort=DESC&period="+EMA_periode).json()
        data_btc.reverse()
        reale_zahl = len(data_btc)
        close  = []
        max  = []
        min  = []
        volume  = []
        volumeQuote  = []
        Tag  = []
        #volume_avrage = 0
        volume_avrage_btc = 0
        close_avrage = 0
        for i in np.arange(reale_zahl):
            close.append(data_btc[i]['close'])
            max.append(data_btc[i]['max'])
            min.append(data_btc[i]['min'])
            volume.append(data_btc[i]['volume'])
            #volume_avrage += float(data_btc[i]['volume'])
            volume_avrage_btc += float( data_btc[i]['volume']) * float( data_btc[i]['close'] )
            close_avrage += float( data_btc[i]['close'] )
            volumeQuote.append(data_btc[i]['volumeQuote'])
            Tag.append(str(data_btc[i]['timestamp'].split("T")[0]))

        close = np.array(close,dtype=float)
        max = np.array(max,dtype=float)
        min = np.array(min,dtype=float)
        volume = np.array(volume,dtype=float)
        volumeQuote = np.array(volumeQuote,dtype=float)
        volume_avrage_btc = volume_avrage_btc/reale_zahl
        close_avrage = close_avrage/reale_zahl
        ema_satz, ema_drittel = aa1_daten_query_class.ema (close, reale_zahl, ema1, ema2)
        ema_satz = np.array(ema_satz, dtype=float)
        ema_drittel = np.array(ema_drittel, dtype=float)
        target_diferenz = []
        target_prozenz = []
        target_polar = []
        for i in np.arange(kalame, len(close)):
            target_prozenz.append(aa1_daten_query_class.get_prozent(close[i-1], close[i], 0) - 100)
            target_polar.append(aa1_daten_query_class.get_polar(close[i-1], close[i]))
            target_diferenz.append(close[i] - close[i-1])
        target_diferenz = np.array(target_diferenz, dtype=float)
        target_prozenz = np.array(target_prozenz, dtype=float)
        target_polar = np.array(target_polar, dtype=float)

        return close, max, min, volume, volumeQuote, Tag, volume_avrage_btc, close_avrage, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar
    def hitbtc_query(Coin_symbol, EMA_periode, data_count):
        data_btc = requests.get("https://api.hitbtc.com/api/2/public/candles/"+str(Coin_symbol)+"?limit="+str(data_count)+"&sort=DESC&period="+EMA_periode).json()
        data_btc.reverse()
        reale_zahl = len(data_btc)
        close  = []
        max  = []
        min  = []
        volume  = []
        volumeQuote  = []
        Tag  = []
        #volume_avrage = 0
        volume_avrage_btc = 0
        close_avrage = 0
        for i in np.arange(reale_zahl):
            close.append(data_btc[i]['close'])
            max.append(data_btc[i]['max'])
            min.append(data_btc[i]['min'])
            volume.append(data_btc[i]['volume'])
            #volume_avrage += float(data_btc[i]['volume'])
            volume_avrage_btc += float( data_btc[i]['volume']) * float( data_btc[i]['close'] )
            close_avrage += float( data_btc[i]['close'] )
            volumeQuote.append(data_btc[i]['volumeQuote'])
            Tag.append(str(data_btc[i]['timestamp'].split("T")[0]))

        close = np.array(close,dtype=float)
        max = np.array(max,dtype=float)
        min = np.array(min,dtype=float)
        volume = np.array(volume,dtype=float)
        volumeQuote = np.array(volumeQuote,dtype=float)
        volume_avrage_btc = volume_avrage_btc/reale_zahl
        close_avrage = close_avrage/reale_zahl
        return close, max, min, volume, volumeQuote, Tag, volume_avrage_btc, close_avrage
    def Hitbtc_curency_list():
        #currency_list = requests.get("https://api.hitbtc.com/api/2/public/currency").json()
        currency_list = requests.get("https://api.hitbtc.com/api/2/public/symbol").json()
        baseCurrency  = []
        id  = []
        for doc in currency_list:
            if str(doc['quoteCurrency']) == "BTC": 
                baseCurrency.append(doc['baseCurrency'])
                id.append(doc['id'])
        #{'crypto': True, 'delisted': False, 'fullName': 'DDF', 'id': 'DDF', 'payinConfirmations': 20, 'payinEnabled': False, 'payinPaymentId': False, 'payoutEnabled': True, 'payoutFee': '646.000000000000', 'payoutIsPaymentId': False, 'transferEnabled': True}
        return baseCurrency, id
    def W_U_E_R_F_E_L(target_wert, wert1, wert2, wert3, wert4, wert5, wert6, wert7, wert8, wert9, wert10, jomle, kalame, crash_filter, ema1, ema2, mit_close_1):
        data_count = jomle+kalame
        target_wert = np.array(target_wert,dtype=float)
        wert1       = np.array(wert1,      dtype=float)
        wert2       = np.array(wert2,      dtype=float)
        wert3       = np.array(wert3,      dtype=float)
        wert4       = np.array(wert4,      dtype=float)
        wert5       = np.array(wert5,      dtype=float)
        wert6       = np.array(wert6,      dtype=float)
        wert7       = np.array(wert7,      dtype=float)
        wert8       = np.array(wert8,      dtype=float)
        wert9       = np.array(wert9,      dtype=float)
        wert10      = np.array(wert10,     dtype=float)
        target_wert = aa1_daten_query_class.stossdaempfer(target_wert, crash_filter)
        ema_satz, ema_drittel = aa1_daten_query_class.ema (target_wert, data_count,ema1,ema2)

        satz_wurfel  = []
        wort_zelle  = []
        horuf_zelle  = []
        ema_count = 0

        for i in np.arange(jomle):
            wort_zelle  = []
            for j in np.arange(kalame):
                horuf_zelle  = []
                if mit_close_1==1:
                    horuf_zelle.append(target_wert[j+i])
                if wert1.any():
                    horuf_zelle.append(wert1[j+i])
                if wert2.any():
                    horuf_zelle.append(wert2[j+i])
                if wert3.any():
                    horuf_zelle.append(wert3[j+i])
                if wert4.any():
                    horuf_zelle.append(wert4[j+i])
                if wert5.any():
                    horuf_zelle.append(wert5[j+i])
                if wert6.any():
                    horuf_zelle.append(wert6[j+i])
                if wert7.any():
                    horuf_zelle.append(wert7[j+i])
                if wert8.any():
                    horuf_zelle.append(wert8[j+i])
                if wert9.any():
                    horuf_zelle.append(wert9[j+i])
                if wert10.any():
                    horuf_zelle.append(wert10[j+i])


                horuf_zelle.append(ema_satz[ema_count])
                horuf_zelle.append(ema_drittel[ema_count])
                
                wort_zelle.append(horuf_zelle)
                horuf_zelle=None
            ema_count += 1
            satz_wurfel.append(wort_zelle)
            wort_zelle=None
        #test vergleich
        target_diferenz = np.array([target_wert[i+kalame]-target_wert[i+kalame-1]  for  i in range(jomle)],dtype=float)
        target_prozenz  = np.array([aa1_daten_query_class.get_prozent(target_wert[i+kalame-1], target_wert[i+kalame], 0)-100  for  i in range(jomle)],dtype=float)
        target_polar    = np.array([aa1_daten_query_class.get_polar(target_wert[i+kalame-1], target_wert[i+kalame])  for  i in range(jomle)],dtype=float)
        target = np.array([target_wert[i+kalame]  for  i in range(jomle)])
        satz_wurfel = np.array(satz_wurfel)

        return satz_wurfel, target, target_diferenz, target_prozenz, target_polar, ema_satz, ema_drittel
    def fit_trasport_hin_multi_n(wert):
        dimensionen = []
        count_bood1 = 0
        last_bood   = 0
        for i in np.arange(len(wert.shape)):
            dimensionen.append(wert.shape[i])
            count_bood1 = count_bood1 * wert.shape[i]
            last_bood = wert.shape[i]
        close_scala = MinMaxScaler(feature_range = (0, 1))
        nabardeboon = wert.reshape(count_bood1, last_bood)


        #wurfel = close_scala.fit_transform(wurfel)
        #for dim in dimensionen:

        wurfel = nabardeboon.reshape(dimensionen)

        target = target.reshape((-1, 1))#listet daten verdikal
        target = close_scala.fit_transform(target)
        target = target.ravel()#listet daten horizontal
        return wurfel, target, close_scala
    def fit_trasport_hin(wurfel, target, jomle, kalame):
        horuf = wurfel.shape[2]
        close_scala = MinMaxScaler(feature_range = (0, 1))
        nabardeboon = wurfel.reshape(jomle*kalame, horuf)
        nabardeboon = close_scala.fit_transform(nabardeboon)
        wurfel_normal = nabardeboon.reshape(jomle, kalame, horuf)

        nabardeboon_zurueck = wurfel_normal.reshape(jomle*kalame, horuf)
        nabardeboon_normal_zurucke = close_scala.inverse_transform(nabardeboon_zurueck)
        wurfel_normal_zurucke = nabardeboon_normal_zurucke.reshape(jomle, kalame, horuf)
        target = target.reshape((-1, 1))#listet daten verdikal
        #target = close_scala.fit_transform(target)
        target = target.ravel()#listet daten horizontal
        return 



