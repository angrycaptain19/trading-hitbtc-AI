import requests,json
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from aa1_daten_hilfe import aa1_daten_hilfe_class


class aa1_daten_query_class():
    def erfolg_fundament(close, volume, ema1, ema2, fundament_lenght, erfolg_prozent):
        array_ganz  = []
        array_jomle = []
        target = []
        target_normal = []
        erfolg_serie = 0
        erfolg_anfang_merker = 0 #damit nicht zu spät anfängt die Sträne zu merken
        for i in np.arange(fundament_lenght, len(close)):
            diferenz_zu_t_davor = aa1_daten_hilfe_class.get_prozent(close[i-1], close[i], 0) - 100
            if diferenz_zu_t_davor >= 0:#age plus Tag hastesh
                erfolg_serie += diferenz_zu_t_davor
                erfolg_anfang_merker += 1
            else:                       #age negativ Tag hastesh
                erfolg_serie = 0
                erfolg_anfang_merker = 0
            if erfolg_serie >= erfolg_prozent:
                #target.append(close[i])
                if erfolg_anfang_merker >1:
                    target.append(0)
                    target[len(target) - erfolg_anfang_merker] = 1 #aktuelle wird auf null gesetzt und es wird rückwirkend 1 gesetzt damit anfang von positiv Trend gemekt wird
                else:#[1, 0, 0, 1, 0]
                    target.append(1)

            else:
                target.append(0)

            array_kalame = []
            erfolg_close  = []
            erfolg_volume  = []
            erfolg_ema1  = []
            erfolg_ema2  = []
            target_normal.append(close[i])

            for j in range(i-fundament_lenght, i):# az this ta hafta ghablish
                erfolg_close.append(close[j])
                erfolg_volume.append(volume[j])
                erfolg_ema1.append(ema1[j])
                erfolg_ema2.append(ema2[j])
            array_kalame.append(erfolg_close)
            array_kalame.append(erfolg_volume)
            array_kalame.append(erfolg_ema1)
            array_kalame.append(erfolg_ema2)
            #break
            array_jomle.append(array_kalame)
            #array_ganz.append(array_jomle)
        array_jomle = np.array(array_jomle, dtype=float)
        target = np.array(target, dtype=float)
        target_normal = np.array(target_normal, dtype=float)
        return array_jomle, target, target_normal
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
        ema_satz, ema_drittel = aa1_daten_hilfe_class.ema (close, reale_zahl, ema1, ema2)
        ema_satz = np.array(ema_satz, dtype=float)
        ema_drittel = np.array(ema_drittel, dtype=float)
        target_diferenz = []
        target_prozenz = []
        target_polar = []
        for i in np.arange(kalame, len(close)):
            target_prozenz.append(aa1_daten_hilfe_class.get_prozent(close[i-1], close[i], 0) - 100)
            target_polar.append(aa1_daten_hilfe_class.get_polar(close[i-1], close[i]))
            target_diferenz.append(close[i] - close[i-1])
        target_diferenz = np.array(target_diferenz, dtype=float)
        target_prozenz = np.array(target_prozenz, dtype=float)
        target_polar = np.array(target_polar, dtype=float)

        return close, max, min, volume, volumeQuote, Tag, volume_avrage_btc, close_avrage, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar
    def hitbtc_query_mit_ema_simulation(Coin_symbol, EMA_periode, data_count, ema1, ema2, kalame):
        close  = []
        max  = []
        min  = []
        volume  = []
        volumeQuote  = []
        Tag  = []
        volume_avrage_btc = 0
        simulation_close = 0
        simulation_max = 0
        simulation_min = 0
        simulation_volume = 0
        simulation_volumeQuote= 0
        for i in np.arange(data_count):
            plus = 1
            if(i>=100):
                plus = -11
            if(i>=200):
                plus = 41
            if(i>=300):
                plus = -81
            if(i>=400):
                plus = 61
            if(i>=500):
                plus = -31
            if(i>=550):
                plus = 181
            simulation_close += plus 
            close.append(simulation_close)
            simulation_max  += plus
            max.append(simulation_max)
            simulation_min += plus
            min.append(simulation_min)
            simulation_volume += plus
            volume.append(simulation_volume)
            simulation_volumeQuote += plus
            volumeQuote.append(simulation_volumeQuote )

        close = np.array(close,dtype=float)
        max = np.array(max,dtype=float)
        min = np.array(min,dtype=float)
        volume = np.array(volume,dtype=float)
        volumeQuote = np.array(volumeQuote,dtype=float)
        ema_satz, ema_drittel = aa1_daten_hilfe_class.ema (close, data_count, ema1, ema2)
        ema_satz = np.array(ema_satz, dtype=float)
        ema_drittel = np.array(ema_drittel, dtype=float)
        target_diferenz = []
        target_prozenz = []
        target_polar = []
        for i in np.arange(kalame, len(close)):
            target_prozenz.append(aa1_daten_hilfe_class.get_prozent(close[i-1], close[i], 0) - 100)
            target_polar.append(aa1_daten_hilfe_class.get_polar(close[i-1], close[i]))
            target_diferenz.append(close[i] - close[i-1])
        target_diferenz = np.array(target_diferenz, dtype=float)
        target_prozenz = np.array(target_prozenz, dtype=float)
        target_polar = np.array(target_polar, dtype=float)

        return close, max, min, volume, volumeQuote, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar
    def hitbtc_query_mit_ema_volumen_gewicht(Coin_symbol, EMA_periode, data_count, ema1, ema2, kalame):
        close  = []
        max  = []
        min  = []
        volume  = []
        volumeQuote  = []
        Tag  = []
        volume_avrage_btc = 0
        simulation_close = 0
        simulation_max = 0
        simulation_min = 0
        simulation_volume = 0
        simulation_volumeQuote= 0
        for i in np.arange(data_count):
            plus = 1
            if(i>=100):
                plus = -11
            if(i>=200):
                plus = 41
            if(i>=300):
                plus = -81
            if(i>=400):
                plus = 61
            if(i>=500):
                plus = -31
            if(i>=550):
                plus = 181
            simulation_close += plus 
            close.append(simulation_close)
            simulation_max  += plus
            max.append(simulation_max)
            simulation_min += plus
            min.append(simulation_min)
            simulation_volume += plus
            volume.append(simulation_volume)
            simulation_volumeQuote += plus
            volumeQuote.append(simulation_volumeQuote )

        close = np.array(close,dtype=float)
        max = np.array(max,dtype=float)
        min = np.array(min,dtype=float)
        volume = np.array(volume,dtype=float)
        volumeQuote = np.array(volumeQuote,dtype=float)
        ema_satz, ema_drittel = aa1_daten_hilfe_class.ema (close, data_count, ema1, ema2)
        ema_satz = np.array(ema_satz, dtype=float)
        ema_drittel = np.array(ema_drittel, dtype=float)
        target_diferenz = []
        target_prozenz = []
        target_polar = []
        for i in np.arange(kalame, len(close)):
            target_prozenz.append(aa1_daten_hilfe_class.get_prozent(close[i-1], close[i], 0) - 100)
            target_polar.append(aa1_daten_hilfe_class.get_polar(close[i-1], close[i]))
            target_diferenz.append(close[i] - close[i-1])
        target_diferenz = np.array(target_diferenz, dtype=float)
        target_prozenz = np.array(target_prozenz, dtype=float)
        target_polar = np.array(target_polar, dtype=float)

        return close, max, min, volume, volumeQuote, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar, ema_volumen

    def curency_list_hitbtc(EMA_periode, jomle, kalame, quelle, volume_filter, ema1, ema2, count):
        fullName_array, kurzel_array = aa1_daten_hilfe_class.Hitbtc_curency_list()
        ergebnis = []
        i = 0
        for Coin_symbol in kurzel_array:
            close, max, min, volume, volumeQuote, Tag, volume_avrage_btc, close_avrage, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar = aa1_daten_query_class.hitbtc_query_mit_ema(Coin_symbol, EMA_periode, jomle + kalame, ema1, ema2, kalame)
            innerhalt = len(close)
            if volume_avrage_btc > volume_filter:
                ergebnis.append(Coin_symbol)
                print(Coin_symbol)
                i += 1
            else:
                print("No: "+Coin_symbol)
            if i > count:
                break
            #ema_result1 = tendenz_ticker(ema_satz)
            #ema_result2 = tendenz_ticker(ema_drittel)
            #if volume_avrage > volume_filter and ema_result1 >= ema1_serie and ema_result2 >= ema2_serie:
                #print(Coin_symbol+ " V("+str(volume_avrage)+")  EMA1("+str(ema_result1)+") EMA2("+str(ema_result2)+")-------------------------------------------------")
                #win32api.MessageBox(0,Coin_symbol+ " V("+str(volume_avrage)+")  EMA1("+str(ema_result1)+") EMA2("+str(ema_result2)+")", 'Insert Fehler')
                #ergebnis += Coin_symbol+ " V("+str(volume_avrage)+")  EMA1("+str(ema_result1)+") EMA2("+str(ema_result2)+")------------"
            #else:
                #print(str(ema_result1) + " " + str(ema_result2) +" "+ Coin_symbol+ "  V"+str(volume_avrage))
        return ergebnis




