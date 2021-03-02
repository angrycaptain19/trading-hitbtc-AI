from aa1_daten_query import aa1_daten_query_class
import numpy as np
from aa1_Diagramm import aa1_Diagramm_class
from aa1_daten_hilfe import aa1_daten_hilfe_class
EMA_periode                  = "D1"
jomle                        = 650                    # 650 data count  =  jomle+kalame
kalame                       = 38                     # 38 war bestes Ergebniss bei BTC
test_prozenz                 = 0.03                      # 0.2 = 20%
crash_filter                 = 2                        # %
Coin_symbol                  = "BTCUSD" # BTCUSD, ETHBTC, BCHBTC, XMRBTC, ADABTC, DASHBTC, BTGBTC
epochen                      = 100
tozih                        = "teste2"
ema1                         = 21
ema2                         = 12
save_AI_1                    = 1
erfolg_prozent               = 6
model_etiket                 = str("erfolg_prozent("+str(erfolg_prozent)+")")
volume_filter                = 5                     #BTC
Coin_count                   = 5

#Daten abrufen
#satz_wurfel = np.vstack([satz_wurfel, satz_wurfel])
ergebnis = ["BTCUSD", "ETHBTC", "XMRBTC", "ADABTC", "DASHBTC", "BTGBTC"]
ergebnis = ["QTUMBTC", "ONTBTC", "NEOBTC"]
ergebnis = ["BTCUSD"]
#ergebnis = ["XLMBTC", "ZECBTC", "LTCBTC", "NEOBTC", "DGTXBTC", "DOGEBTC","BTCUSD", "ETHBTC", "XMRBTC", "ADABTC", "DASHBTC", "BTGBTC"]
#ergebnis = aa1_daten_query_class.curency_list_hitbtc(EMA_periode, jomle, kalame, "hitbtc", volume_filter, ema1, ema2, Coin_count)
satz_wurfel_G = []
target_prozent_polar_G = []
for count, Coin_symbol in enumerate(ergebnis):
    #close, max, min, volume, volumeQuote, Tag, volume_avrage_btc, close_avrage, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar = aa1_daten_query_class.hitbtc_query_mit_ema(Coin_symbol, EMA_periode, jomle + kalame, ema1, ema2, kalame)
    #close, max, min, volume, volumeQuote, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar = aa1_daten_query_class.hitbtc_query_mit_ema_simulation(Coin_symbol, EMA_periode, jomle + kalame, ema1, ema2, kalame)
    close, max, min, volume, volumeQuote, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar, ema_volumen = aa1_daten_query_class.hitbtc_query_mit_ema_volumen_gewicht(Coin_symbol, EMA_periode, jomle + kalame, ema1, ema2, kalame)
    #normalisiren
    close, max, min, volume, volumeQuote, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar, cs_close, cs_max, cs_min, cs_volume, cs_volumeQuote, cs_ema_satz, cs_ema_drittel, cs_target_diferenz, cs_target_prozenz, cs_target_polar = aa1_daten_hilfe_class.normalisiren(close, max, min, volume, volumeQuote, ema_satz, ema_drittel, target_diferenz, target_prozenz, target_polar, Coin_symbol)
    satz_wurfel, target_prozent_polar, target_normal0 = aa1_daten_query_class.erfolg_fundament(close, volume, ema_satz, ema_drittel, kalame, erfolg_prozent)
    if count == 0:
        satz_wurfel_G = satz_wurfel
        target_prozent_polar_G = target_prozent_polar
    else:
        satz_wurfel_G = np.vstack([satz_wurfel_G, satz_wurfel])
        #target_prozent_polar_G = np.vstack([target_prozent_polar_G, target_prozent_polar])
        target_prozent_polar_G= np.append(target_prozent_polar_G, target_prozent_polar)
        target_prozent_polar_G = target_prozent_polar_G.ravel()
satz_wurfel = satz_wurfel_G
target_prozent_polar = target_prozent_polar_G

#AI
from aa1_AI import aa1_AI_class
target = target_prozent_polar # target, target_diferenz, target_prozenz, target_polar
close_scala = cs_target_polar #  cs_close, cs_target_diferenz, cs_target_prozenz, cs_target_polar
results_test, y_test, history = aa1_AI_class.AI_action(satz_wurfel, target, test_prozenz, epochen, model_etiket, save_AI_1)#------------------(  A I  )--------------------
#results_test, y_test = aa1_daten_hilfe_class.fit_trasport_zurueck(results_test, y_test, close_scala)
#Diagramm
fehler, ohne_reaktion = aa1_daten_hilfe_class.fehler_rechner(results_test, y_test)
#fehler, ohne_reaktion = aa1_daten_hilfe_class.fehler_rechner_polar(results_test, y_test)
#fehler, ohne_reaktion = aa1_daten_hilfe_class.fehler_prozent_polar(results_test, y_test)
aa1_Diagramm_class.diagramm(results_test, y_test, Coin_symbol, history, epochen, fehler, jomle, kalame, ohne_reaktion, tozih, close, ema_satz, ema_drittel)

ende=8




#aa1_Diagramm_class.diagramm_test(target_wert, ema_satz, ema_drittel, "",1)
#satz_wurfel2, target2, target_diferenz3, target_prozenz3, target_polar3, ema_satz2, ema_drittel2  =  aa1_daten_hilfe_class.W_U_E_R_F_E_L(close, volume, 0, 0, 0, 0, 0, 0, 0, 0, 0, jomle, kalame, crash_filter, ema1, ema2, 1)
#close, max, min, volume, volumeQuote, Tag, volume_avrage, close_avrage  =  aa1_daten_hilfe_class.hitbtc_query(Coin_symbol, EMA_periode, jomle + kalame)
#satz_wurfel, target, target_diferenz, target_prozenz, ema_satz, ema_drittel  =  aa1_daten_hilfe_class.W_U_E_R_F_E_L(close, wert1, wert2, wert3, wert4, wert5, wert6, wert7, wert8, wert9, wert10, jomle, kalame, crash_filter, ema1, ema2, 1)
#close, wert1, wert2, wert3, wert4, wert5, wert6, wert7, wert8, wert9, wert10  =  aa1_daten_hilfe_class.test_daten(jomle, kalame, 3)
#satz_wurfel, target, close_scala  =  aa1_daten_hilfe_class.fit_trasport_hin(satz_wurfel, target_prozenz, jomle, kalame)
