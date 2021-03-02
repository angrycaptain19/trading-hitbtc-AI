import matplotlib
import requests,json
import numpy as np
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


EMA_periode                  = "H1"
volume_filter                = 5
ema1                         = 21
ema2                         = 50
Coin_count                   = 30
jomle                        = 100                    # 650 data count  =  jomle+kalame
kalame                       = 1                     # 38 war bestes Ergebniss bei BTC

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
def ema_berechner (all_close, data_count, ema1, ema2, volume):
    #3-Day VWMA = (C1*V1 + C2*V2 + C3*V3) / (V1+ V2+ V3)
        ema_satz = [all_close[0]]
        ema_drittel = [all_close[0]]
        SF = 2/ (ema2+1)
        SF2 = 2/ ((ema1)+1)
        #start vvma
        all_close_summe = 0
        all_volume = 0
        VWMA = [all_close[0]]
        #end vwma
        for x in np.arange(data_count):
            ema_satz.append(   all_close[x]*SF+(1 - SF) * ema_satz[x-1]   )
            ema_drittel.append(   all_close[x]*SF2+(1 - SF2) * ema_drittel[x-1]    )
            #start vvma
            all_close_summe += (all_close[x]*volume[x])
            all_volume += (volume[x])
            VWMA.append(all_close_summe/all_volume)
            #end vwma
        return ema_satz, ema_drittel, VWMA 


def volumen_ema_berechner(all_close, volume):
    all_close_summe = 0
    all_volume = 0
    for x in np.arange(len(all_close)):
        all_close_summe += (all_close[x]*volume[x])
        all_volume += (volume[x])
    return all_close_summe/all_volume
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
        volume_avrage_btc /= reale_zahl
        close_avrage /= reale_zahl
        ema_satz, ema_drittel, VWMA  = ema_berechner (close, reale_zahl, ema1, ema2, volume)
        ema_satz = np.array(ema_satz, dtype=float)
        ema_drittel = np.array(ema_drittel, dtype=float)
        VWMA = np.array(VWMA, dtype=float)
        target_diferenz = []
        target_prozenz = []
        target_polar = []
        for i in np.arange(kalame, len(close)):
            target_prozenz.append(get_prozent(close[i-1], close[i], 0) - 100)
            target_diferenz.append(close[i] - close[i-1])
        target_diferenz = np.array(target_diferenz, dtype=float)
        target_prozenz = np.array(target_prozenz, dtype=float)
        target_polar = np.array(target_polar, dtype=float)

        return close, max, min, volume, volumeQuote, Tag, volume_avrage_btc, close_avrage, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar, VWMA
def diagramm(Coin_symbol, tozih, all_close, ema_satz, ema_drittel, volume, VWMA):
        VWMA_last  = volumen_ema_berechner(all_close, volume)
        plt.plot(all_close, color = 'red', label = 'close')
        plt.plot(ema_satz,  color = 'blue', label = Coin_symbol +' EMA '+str(50))
        plt.plot(ema_drittel,  color = 'green', label = Coin_symbol +' EMA '+str(21))
        plt.plot(VWMA,  color = 'black', label = Coin_symbol +' ' +str(VWMA_last))

        #plt.plot(volume,  color = 'black', label = Coin_symbol +'Vol ')

        plt.legend()
        #strFile = 'x2_png/'+Coin_symbol+' EMA.png'
        strFile = 'x2_png/'+Coin_symbol+' EMA.png'

        if os.path.isfile(strFile):
           os.remove(strFile)
        plt.savefig(strFile)
        plt.clf()

ergebnis = ["BTCUSD", "XRPBTC", "LTCBTC", "XMRBTC", "EOSBTC", "TRXBTC", "VETBTC", "OMGBTC", "ETCBTC", "ZILBTC", "ZECBTC", "ICXBTC", "IOTABTC"]
for Coin_symbol in ergebnis:
    close, max, min, volume, volumeQuote, Tag, volume_avrage_btc, close_avrage, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar, VWMA = hitbtc_query_mit_ema(Coin_symbol, EMA_periode, jomle + kalame, ema1, ema2, kalame)
    diagramm(Coin_symbol, "tozih", close, ema_satz, ema_drittel, volume, VWMA)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(range(100))






