from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import load_model
from sklearn.model_selection import train_test_split
import numpy as np
import os

class aa1_AI_class():
    def fit_trasport_zurueck(target, close_scala):
        target = target.reshape((-1, 1))#listet daten verdikal
        target = close_scala.inverse_transform(target)
        target = target.ravel()#listet daten horizontal
        return target
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
    def AI_action(satz_wurfel, target, test_prozenz, epochen, model_etiket, save_AI_1):
        x_train, x_test, y_train, y_test  = train_test_split(satz_wurfel, target, test_size = test_prozenz, random_state=2)
        model_etiket = "saved_models/"+model_etiket+".h5"
        exists = os.path.isfile(model_etiket)
        if exists:
            regressor = load_model(model_etiket)
        else:
            regressor = aa1_AI_class.lasagna_x(x_train)
        history = regressor.fit(x_train, y_train, epochs = epochen, validation_data = (x_test, y_test))
        if save_AI_1 == 1:
            regressor.save(model_etiket)
        results_test  = regressor.predict(x_test)
        results_test = results_test.ravel()#listet daten horizontal
        results_test = np.array(results_test, dtype=float)
        y_test = np.array(y_test, dtype=float)

        #y_test = y_test.reshape(len(y_test), 1)
        #y_test = aa1_AI_class.fit_trasport_zurueck(y_test, close_scala)
        #results_test = aa1_AI_class.fit_trasport_zurueck(results_test, close_scala)
        return results_test, y_test, history



