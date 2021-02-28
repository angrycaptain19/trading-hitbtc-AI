from x2_keras import x2_keras_class
EMA_periode ="D1"
jomle = 650 # data count  =  jomle+kalame
kalame = 16
test_prozenz = 0.2 # 0.2 = 20%
training_0 = 1
epochen = 100
crash_filter = 3 #%
#Coin_symbol ="btc_500epochs_"
#count_of_values = 5 # ist die Anzahl von Werten(1:close 2:max 3:min........  der wurfel wird 2d gemcht
Coin_symbol = "BTCUSD"
epochen = 50
tozih = "teste2"
results, y_test = x2_keras_class.my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen, tozih, crash_filter)
Coin_symbol = "BTCUSD"
epochen = 54
results, y_test = x2_keras_class.my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen)
Coin_symbol = "BTCUSD"
epochen = 104
results, y_test = x2_keras_class.my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen)
Coin_symbol = "BTCUSD"
epochen = 1004
results, y_test = x2_keras_class.my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen)




Coin_symbol = "ETHBTC"
results, y_test = x2_keras_class.my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen)
Coin_symbol = "BCHBTC"
results, y_test = x2_keras_class.my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen)
Coin_symbol = "LTCBTC"
results, y_test = x2_keras_class.my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen)
Coin_symbol = "IOTABTC"
results, y_test = x2_keras_class.my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen)
Coin_symbol = "XRPBTC"
results, y_test = x2_keras_class.my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen)
Coin_symbol = "QTUMBTC"
results, y_test = x2_keras_class.my_ki_strat(Coin_symbol, EMA_periode, jomle, kalame, test_prozenz, training_0, epochen)

print('end1')
print(results)
print(y_test)
#results = x2_keras_class.my_ki_strat(data)
#print('end1')
#print(results)
