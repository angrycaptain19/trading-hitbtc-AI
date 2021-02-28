import os
import numpy as np
import matplotlib.pyplot as plt


class aa1_Diagramm_class():
    def diagramm(results_test, y_test, Coin_symbol, history, epochen, fehler, jomle, kalame, ohne_reaktion, tozih, all_close, ema_satz, ema_drittel):
        plt.scatter(range(len(y_test)),results_test,c='r',label='results_test')  #array([[33.150745]], dtype=float32)
        plt.scatter(range(len(y_test)),y_test,c='g',label='y_test')        #array([['6627.10']], dtype='<U7')
        plt.title(Coin_symbol +" e:"+str(epochen)+" f "+str(fehler) )
        plt.legend()
        file_name =str(round(ohne_reaktion-fehler, 4))+' '+ Coin_symbol+' '+str(epochen)+' t('+tozih+')('+str(jomle)+ 'x'+str(kalame)+')f'+str(round(fehler, 4))+'-'+str(round(ohne_reaktion, 4))
        strFile = 'x2_png/'+file_name+' scatter.png'
        if os.path.isfile(strFile):
           os.remove(strFile)
        plt.savefig(strFile)
        plt.clf()
        #if history.any():
            #print(333333333333333333)
        #all_loss=history.history['loss'][25:]
        all_loss=history.history['loss']
        plt.plot(all_loss, label='all_loss')
        plt.title(Coin_symbol +" e:"+str(epochen)+" f "+str(fehler) )
        plt.legend()
        strFile = 'x2_png/'+file_name+' loss.png'
        if os.path.isfile(strFile):
            os.remove(strFile)
        plt.savefig(strFile)
        plt.clf()

        #all_accuracy=history.history['accuracy']
        #all_val_accuracy=history.history['val_accuracy']
        plt.plot(history.history['acc'], label='acc')
        plt.plot(history.history['val_acc'], label='val_acc')  
        plt.legend()
        plt.title(Coin_symbol +" e:"+str(epochen)+" f "+str(fehler) )
        strFile = 'x2_png/'+file_name+' accuracy.png'
        if os.path.isfile(strFile):
            os.remove(strFile)
        plt.savefig(strFile)
        plt.clf()

        plt.plot(results_test, color = 'red', label = 'results_test')
        plt.plot(y_test, color = 'black', label = 'y_test')
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
    
        
        
        
    def diagramm_test(wert1, wert2, wert3, file_name, show_1_save_0):
        plt.plot(wert1, color = 'red', label = 'wert1')
        plt.plot(wert2, color = 'black', label = 'wert2')
        plt.plot(wert3, color = 'green', label = 'wert3')
        #plt.title(Coin_symbol +" e:"+str(epochen)+" f "+str(fehler) )
        plt.legend()
        if show_1_save_0 == 0:
            strFile = 'Test_diagram/'+file_name+' plot.png'
            if os.path.isfile(strFile):
               os.remove(strFile)
            plt.savefig(strFile)
            plt.clf()
        else:
            plt.show()

