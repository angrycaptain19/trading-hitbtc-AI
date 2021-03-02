#import uuid
import time
import requests
from decimal import *
import json
#import xlrd
#import xlwt
import os
import datetime
#from datetime import datetime, now
from numpy import array

from os.path import abspath
#import sys
from ki import Start

#import numpy as np
#import pandas as pd
#import requests,json,numpy as np,pandas as pd

#import tensorflow as tf
#from keras.models import Sequential
#from keras.layers import LSTM, Dense, Activation


sedf_ema_best = 0
sedf_ema_last= 0
sedf_ema_long= 0
class Client(object):
    def __init__(self, url, public_key, secret):
        self.url = url + "/api/2"
        self.session = requests.session()
        self.session.auth = (public_key, secret)
        """Get Candle."""
    def restart(self,konto,sender):
        if len(str(konto)) <= 100:
            print("connecting error   "+sender)
            print(konto)
            print("in 10 secunden.......................................")
            time.sleep(10)
            flut()
        return
    def get_trading_balance(self,symbol_code,all_balance):
        konto_balance = 0
        konto = all_balance
        for konto in konto:
            if konto['currency'] == symbol_code:
                konto_balance = Decimal(konto['available'])
                konto_balance += Decimal(konto['reserved'])
                break
        return konto_balance
    def get_trading_balance_all(self):
        konto = ""
        try:
            konto =self.session.get("%s/trading/balance" % self.url).json()
            Client.restart(self,konto,"get_trading_balance_all")
        except:
            Client.restart(self,konto,"get_trading_balance_all")
        return konto
    def get_last_price(self, symbol_code):
        konto = ""
        try:
            konto = self.session.get("%s/public/ticker/%s" % (self.url, symbol_code)).json()
            Client.restart(self,konto,"get_last_price")
        except:
            Client.restart(self,konto,"get_last_price")
        return konto
    def get_symbol(self, symbol_code):
        konto = self.session.get("%s/public/symbol/%s" % (self.url, symbol_code)).json()
        Client.restart(self,konto,"get_symbol")
        return konto
    def get_orderbook(self, symbol_code):
        konto = ""
        try:
            konto = self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()
        except:
            Client.restart(self,konto,"get_orderbook")
        return konto
    def get_orderbook_best_preis(self, symbol_code,ask_or_bid,volum_filter,difrenz):
        konto = ""
        try:
            konto = self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()
        except:
            Client.restart(self,konto,"get_orderbook_best_preis")
        konto = konto[ask_or_bid]
        konto_balance = 0
        for konto in konto:
            if Decimal(konto['size']) >= Decimal(volum_filter):
                konto_balance = str(konto['price'])
                break
        my_zahl=0
        if ask_or_bid=="bid":
            my_zahl = Decimal(konto_balance)+Decimal(difrenz)
        if ask_or_bid=="ask":
            my_zahl = Decimal(konto_balance)-Decimal(difrenz)
        return str(my_zahl)
    def get_address(self, currency_code):#nashode
        konto = ""
        try:
            konto = self.session.get("%s/account/crypto/address/%s" % (self.url, currency_code)).json()
        except:
            Client.restart(self,konto,"get_address")
        return konto
    def get_order_info(self):
        #data = {'wait': wait} if wait is not None else {}
        #return self.session.get("%s/order/%s" % (self.url, client_order_id), params=data).json()
        konto_balance = ""
        konto = ""
        try:
            konto = self.session.get("%s/order" % self.url).json()
        except:
            Client.restart(self,konto,"get_order_info")
        for konto in konto:
                konto_balance = str(konto) +"<br><br>"+str(konto_balance)
        return konto_balance
    def cancel_order(self, client_order_id):
        konto = ""
        try:
            konto = self.session.delete("%s/order/%s" % (self.url, client_order_id)).json()
        except:
            Client.restart(self,konto,"cancel_order")
        return konto
    def cancel_order_info_by_symbol(self, symbol_code):
        #data = {'wait': wait} if wait is not None else {}
        #return self.session.get("%s/order/%s" % (self.url, client_order_id), params=data).json()
        konto_balance = ""
        konto = "hjjjzguzgzukjhghjgjhgkjhgkjhgkjgkzgughlhjlhlhlhjgjghkjhgkhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj"
        try:
            konto = self.session.get("%s/order" % self.url).json()
        except:
            Client.restart(self,konto,"cancel_order_info_by_symbol")
        for konto in konto:
            if konto['symbol'] == symbol_code:
                cancel_id = str(konto['clientOrderId'])
                self.session.delete("%s/order/%s" % (self.url, cancel_id))
                konto_balance = cancel_id +"<br><br>"+cancel_id
        return konto_balance
    def transfer(self, currency_code, amount, to_exchange):
        return self.session.post("%s/account/transfer" % self.url, data={
                'currency': currency_code, 'amount': amount,
                'type': 'bankToExchange' if to_exchange else 'exchangeToBank'
            }).json()
    def withdraw(self, currency_code, amount, address, network_fee=None):
        data = {'currency': currency_code, 'amount': amount, 'address': address}
        if network_fee is not None:
            data['networkfee'] = network_fee
        return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()
    def get_transaction(self, transaction_id):
        return self.session.get("%s/account/transactions/%s" % (self.url, transaction_id)).json()
    def update_trade_history(self,db,User,db_archive,count):
        konto_balance = ""
        konto = ""
        try:
            konto = self.session.get("%s/history/trades" % self.url+"?limit="+str(count)).json()
            Client.restart(self,konto,"update_trade_history")
        except:
            Client.restart(self,konto,"update_trade_history")
        for konto in konto:
            #if int(konto['id']) > 566334860:
            SQL.update_db(db,User,db_archive,str(konto['timestamp']),str(konto['symbol']),str(konto['id']),str(konto['orderId']),str(konto['side']),str(konto['quantity']),str(konto['price']),str(Decimal(konto['quantity'])*Decimal(konto['price'])),str(konto['fee']),"0","0")
                            #(Date                   ,symbol              ,Trade_id        ,order_id             ,side              ,quanty                ,price              ,volume                                                 ,fee              ,rabate,total)
                #SQL.insert_db(konto['timestamp'],strkonto['symbol'],konto['id'],konto['orderId'],konto['side'],konto['quantity'],konto['price'],round(Decimal(konto['quantity'])*Decimal(konto['price']),9),konto['fee'],"0","0")
        return ""
    def falsches_ende_beim_archiv(self,db,User,My_traid_symbol,count):
        konto_balance = ""
        konto = ""
        try:
            konto = self.session.get("%s/history/trades" % self.url+"?limit="+str(count)).json()
        except:
            Client.restart(self,konto,"falsches_ende_beim_archiv")
        for konto in konto:
            if konto['symbol'] == My_traid_symbol:
                SQL.falsches_ende_beim_archiv2(db,User,str(konto['timestamp']),str(konto['symbol']),str(konto['id']),str(konto['orderId']),str(konto['side']),str(konto['quantity']),str(konto['price']),str(Decimal(konto['quantity'])*Decimal(konto['price'])),str(konto['fee']),"0","0")
                            #(Date                   ,symbol              ,Trade_id        ,order_id             ,side              ,quanty                ,price              ,volume                                                 ,fee              ,rabate,total)
                #SQL.insert_db(konto['timestamp'],strkonto['symbol'],konto['id'],konto['orderId'],konto['side'],konto['quantity'],konto['price'],round(Decimal(konto['quantity'])*Decimal(konto['price']),9),konto['fee'],"0","0")
        return ""
    def new_order(self, client_order_id, symbol_code, side, quantity, order_art, price=None):
        data = {'symbol': symbol_code, 'side': side,'type': order_art, 'quantity': quantity}
        if price is not None:
            data['price'] = price
        konto = ""
        try:
            konto = self.session.put("%s/order/%s" % (self.url,client_order_id), data=data).json()
        except:
            Client.restart(self,konto,"new_order")
        return konto
    def get_ema(self,symbol_code,time,days):#mehwar
        global sedf_ema_best
        sedf_ema_best        =  0
        global sedf_ema_last
        sedf_ema_last        =  999999
        konto_balance = 0
        konto = ""
        try:
            kontos = self.session.get("%s/public/candles/%s" % (self.url, symbol_code)+"?limit="+str(days)+"&period="+time).json()
            Client.restart(self,kontos,"get_ema")
        except:
            Client.restart(self,kontos,"get_ema")
        preis_summe=0
        durchschnit=0
        count=0
        best   =        0
        last   =        0
        best2  =        0
        last2  =        999999
        gestern  =        0
        for konto in kontos:
            best  += Decimal(konto['max'])
            best2 = max(best2, Decimal(konto['max']))
            last  += Decimal(konto['min'])
            last2 = min(last2, Decimal(konto['min']))
            preis_summe   += Decimal(konto['close'])
            gestern           = Decimal(konto['close'])
            count+=1
                    #if count> (Decimal(days)/Decimal(1.5)):
                        #break
        result         =  ((preis_summe/count)+gestern)/2
        sedf_ema_best  =  ((best/count)+best2)/2
        sedf_ema_last  =  ((last/count)+last2)/2
        return result
    def order_book_gewicht(self,symbol_code):#tarazo
        konto = ""
        try:
            konto = self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()
            Client.restart(self,konto,"order_book_gewicht")
        except:
            Client.restart(self,konto,"order_book_gewicht")
        letze_buy = konto['bid']
        letze_sell = konto['ask']
        volum_buy  = 0
        volum_sell = 0
        count=0
        for konto in letze_buy:
            volum_buy += Decimal(konto['size'])
            count +=count
            if count == 20:
                break
        count=0
        for konto in letze_sell:
            count +=count
            volum_sell += Decimal(konto['size'])
            if count == 20:
                break

        return calc.get_prozent(volum_buy,volum_sell,0)
    def get_client_volume(self,symbol_code,side,bestand_anzahl_hitbtc,anzahl):
        global letzter_Kauf
        global Nachkauf_stufe
        erste_kauf_merker=0
        global letze_traid_info
        letze_traid_info =""
        kauf_preis = 0
        abschluss = 0
        vorher_kauf=0
        nachkauf_var1=0
        if bestand_anzahl_hitbtc >0:
            try:
                docs = self.session.get("%s/history/trades?symbol=%s" % (self.url, symbol_code)+"&limit="+str(anzahl)).json()
                Client.restart(self,docs,"get_client_volume")
            except:
                Client.restart(self,konto,"get_client_volume")
            my_volume = 0
            my_quanty = 0
            count = 0
            Nachkauf_stufe = 0
            for doc in docs:
                count +=1
                if doc['side'] == "buy": 
                    if erste_kauf_merker == 0:
                        letzter_Kauf = Decimal(doc['price'])
                        letze_traid_info = doc
                        erste_kauf_merker=1
                    if vorher_kauf !=0:
                        nachkauf_var1 = calc.get_prozent(Decimal(doc['price']),vorher_kauf,0)
                        if nachkauf_var1 < 97:
                            Nachkauf_stufe+=1
                    vorher_kauf = Decimal(doc['price'])

                    my_quanty += Decimal(doc['quantity'])
                    my_volume += Decimal(doc['quantity'])*Decimal(doc['price'])
                if my_quanty >= bestand_anzahl_hitbtc:
                    overflow_qunaty = my_quanty - bestand_anzahl_hitbtc
                    my_quanty -= overflow_qunaty
                    my_volume -= overflow_qunaty * Decimal(doc['price'])
                    abschluss = 1
                    break
                #tm= doc['timestamp']
                #jahr = tm.split("-")[0]
                #mont = tm.split("-")[1]
                #tag = tm.split("T")[0].split("-")[2]
                #hour = tm.split("T")[1].split(":")[0]
                #min = tm.split("T")[1].split(":")[1]
                #sec = tm.split("T")[1].split(":")[2].split(".")[0]
                #last_time = datetime.datetime(int(jahr), int(mont), int(tag), int(hour), int(min), int(sec))
            if my_quanty>0:
                kauf_preis = my_volume/my_quanty
                    #break
            if abschluss ==0:
                client.get_client_volume(symbol_code,side,bestand_anzahl_hitbtc,anzahl+100)
        return kauf_preis
class Handel(object):#dalal
    def normal_sell(sell,symbol_code,volum_filter,soll_count,preis_differenz,durchschnit_preis,risikoClasse,order_art):
        """verkaufsignal 00stk  2% ist null"""
        if sell=="1":
            soll_count2 = soll_count*-1
            mein_order_preis = client.get_orderbook_best_preis(symbol_code,"ask",volum_filter,preis_differenz)#bid ist Kauf  ask ist Verkauf
            #mein_order_preis = pflicht_summe+(pflicht_summe*Decimal(0.7))
            if risikoClasse == 1:
                client.new_order(time.time(),symbol_code,"sell",(soll_count2),order_art,durchschnit_preis)
                print_string= "SELL("+str(round(soll_count*durchschnit_preis*7600,2))+")€" 
            if risikoClasse == 2:
                client.new_order(time.time(),symbol_code,"sell",(soll_count2),order_art,mein_order_preis)
                print_string= "SELL("+str(round(soll_count*durchschnit_preis*7600,2))+")€" 
        if sell!="1":
            print_string= "S("+str(round(soll_count*durchschnit_preis*7600,2))+")€ BLOCKED"
        return print_string
    def normal_buy(buy,sell,symbol_code,volum_filter,soll_count,preis_differenz,durchschnit_preis,risikoClasse,order_art):
        """kaufsignal   1000stk -2% ist 1000"""
        if buy=="1":
            if risikoClasse == 1:
                client.new_order(time.time(),symbol_code,"buy",soll_count,order_art,durchschnit_preis)
                print_string= "BUY("+str(round(soll_count*durchschnit_preis*7600,2))+")€" 
            if risikoClasse == 2:
                mein_order_preis = client.get_orderbook_best_preis(symbol_code,"bid",volum_filter,preis_differenz)#bid ist Kauf  ask ist Verkauf
                client.new_order(time.time(),symbol_code,"buy",soll_count,order_art,mein_order_preis)
                print_string= "BUY("+str(round(soll_count*durchschnit_preis*7600,2))+")€" 
        else:
            print_string= "BUY("+str(round(soll_count*durchschnit_preis*7600,2))+")€"
        return print_string
    def jackport(symbol_code,soll_count,durchschnit_preis):
            client.new_order(time.time(),symbol_code,"sell",soll_count,"limit",str(durchschnit_preis))

sbkw_kauf_volumen    = 0
sbkw_verkauf_volumen = 0
sbkw_fee             = 0
sbkw_first_id        = 0
sbkw_last_id        = 0
class SQL(object):
    def insert_from_excel_in_bilanz_db(path):
        db_bilanz = TinyDB('bilanz.json')
        User = Query()

        sbkw_kauf_volumen    = 0
        sbkw_verkauf_volumen = 0
        sbkw_fee             = 0
        sbkw_first_id        = 999999999999999990
        sbkw_last_id        = 0
        """start excel"""
        xl_workbook = xlrd.open_workbook(path)
        sheet_names = xl_workbook.sheet_names()
        print('Sheet Names', sheet_names)
        xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
        print ('Sheet name: %s' % xl_sheet.name)
        row = xl_sheet.row(0)  # 1st row
        my_row_int = xl_sheet.nrows
        from xlrd.sheet import ctype_text   
        print('(Column #) type:value')
        for idx, cell_obj in enumerate(row):
            cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
            print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))
        num_cols = xl_sheet.ncols   # Number of columns
        for row_idx in range(1, my_row_int):    # Iterate through rows 3239
            print ('-'*40)
            print ('Row: %s' % row_idx) 
            Date     = xl_sheet.cell(row_idx, 0)
            py_date = datetime.datetime(*xlrd.xldate_as_tuple(Date.value,xl_workbook.datemode))
            py_date = str(py_date.year)+"-"+str(py_date.month)+"-"+str(py_date.day)+"T00:00:00.0Z"
            #"Date": "2019-05-29T08:29:52.569Z",
            symbol   = str(xl_sheet.cell(row_idx, 1).value)
            Trade_id = Decimal(xl_sheet.cell(row_idx, 2).value)
            side     = str(xl_sheet.cell(row_idx, 4).value)
            volume   = xl_sheet.cell(row_idx, 7).value
            if side == "buy":
                sbkw_kauf_volumen = Decimal(round(Decimal(volume), 9))
            if side == "sell":
                sbkw_verkauf_volumen = Decimal(round(Decimal(volume), 9))
            if sbkw_first_id > Trade_id:
                sbkw_first_id = Trade_id # grooste trade id wird ermittelt
            if sbkw_last_id < Trade_id:
                sbkw_last_id = Trade_id # grooste trade id wird ermittelt
            fee      = xl_sheet.cell(row_idx, 8).value
            sbkw_fee = Decimal(round(Decimal(fee), 9))
            print(symbol + " --- "+str(volume))
            count = db_bilanz.count(where('symbol') == symbol)
            if count == 0:
                db_bilanz.insert({'symbol': symbol ,'last_rade_id': str(sbkw_last_id)+str(volume),'Buy_BTC': str(sbkw_kauf_volumen),'Sell_BTC': str(sbkw_verkauf_volumen),'Fee': str(sbkw_fee)})
            if count == 1:
                docs = db_bilanz.search(User.symbol == symbol)
                for doc in docs:

                    #count_intern = db_bilanz.count(User.groups.all(['last_rade_id',str(sbkw_last_id)+str(volume)]) == str(sbkw_last_id)+str(volume))
                    #docs = db_bilanz.search(User.doc['last_rade_id # '+str(sbkw_last_id)] == [date_605+" # "+str(sbkw_last_id)])
                    new_buy = Decimal(doc['Buy_BTC']) + sbkw_kauf_volumen
                    new_sell = Decimal(doc["Sell_BTC"]) + sbkw_verkauf_volumen 
                    new_fee = Decimal(doc["Fee"]) + sbkw_fee
                #db_bilanz.update({'last_rade_id': str(sbkw_last_id)+str(volume)}, where(doc['symbol']) == symbol)
                #db_bilanz.update({'Buy_BTC': str(new_buy)}, where(doc['symbol']) == symbol)
                #db_bilanz.update({'Sell_BTC': str(new_sell)}, where(doc['symbol']) == symbol)
                #db_bilanz.update({'Fee': str(new_fee)}, where(doc['symbol']) == symbol)
                #docs = db_bilanz.all()
                db_bilanz.update({'last_rade_id': str(sbkw_last_id)+str(volume),'Buy_BTC': str(new_buy),'Sell_BTC': str(new_sell),'Fee': str(new_fee)}, where('symbol') == symbol)
            """ende excel"""
            
        return ""
    def get_sql_alle_laden_global_sbkw(symbol_code):
        db_bilanz = TinyDB('bilanz.json')
        User = Query()
        global sbkw_kauf_volumen
        sbkw_kauf_volumen    = 0
        global sbkw_verkauf_volumen
        sbkw_verkauf_volumen = 0
        global sbkw_fee
        sbkw_fee             = 0
        global sbkw_first_id
        sbkw_first_id        = 0
        global sbkw_last_id
        sbkw_last_id        = 0
        docs = db_bilanz.search(User.symbol == symbol_code)
        for doc in docs:
            sbkw_kauf_volumen = Decimal(doc['Buy_BTC'])
            sbkw_verkauf_volumen = Decimal(doc['Sell_BTC'])
            sbkw_last_id = Decimal(doc['last_rade_id']) # grooste trade id wird ermittelt
            sbkw_fee = Decimal(doc['Fee'])
            print(symbol_code)
        return ""
    def get_sql_price(db,User,symbol_code,side):
        docs = db.search(User.symbol == symbol_code)
        return sum(Decimal(doc['price']) for doc in docs if doc['side'] == side)
    def unic_archiv(User):
        db_archive = TinyDB('archive.json')
        db_archive.all()
        docs_ar = db_archive.all()
        for doc_ar in docs_ar:
            symbol = doc_ar['symbol']
            vol_ar = 0
            letze_id=""
            docs_ar_2 = db_archive.search(User.symbol == symbol)
            for doc_ar_2 in docs_ar_2:
                vol_ar += Decimal(doc_ar_2['volume'])
                letze_id = doc_ar_2['Trade_id']
            db_archive.remove(User.symbol == symbol)
            db_archive.insert({'Date': str(datetime.datetime.now()),'Trade_id': letze_id,'symbol': symbol,'volume': str(vol_ar), 'fee': "0"})
    def new_id(db,User):
        docs = db.all()
        for doc in docs:
            Trade_id =  doc['Trade_id']
            volume =  doc['volume']
            db.update({'Trade_id': Trade_id+volume}, where('Trade_id') == Trade_id)
            print("update............."+volume+"..................db trade.json "+ Trade_id)
    def update_db(db,User,db_archive,Date,symbol,Trade_id,order_id,side,quanty,price,volume,fee,rabate,total):
        docs_archive = db_archive.search(User.symbol == symbol)
        letze_id_hier=0#abgeschlossen coin sollen nicht mehr aktueliziert werden
        for doc_archiv in docs_archive:
            if letze_id_hier<Decimal(doc_archiv['Trade_id']):
                letze_id_hier = Decimal(doc_archiv['Trade_id']) # in ke dare miad tu archiv exist

        if letze_id_hier < Decimal(Trade_id):#waghti inset kon ke az archiv bala ta bood
            #docs = db.search(User.Trade_id == Trade_id+round(volume,5))
            count = db.count(where('Trade_id') == Trade_id+str(round(Decimal(volume),5)))
            if count == 0:
                db.insert({'Date': Date,'symbol': symbol,'Trade_id': Trade_id+str(round(Decimal(volume),5)),'order_id': order_id,'side': side,'quanty': quanty,'price': price, 'volume': volume, 'fee': fee, 'rabate': rabate, 'total': total})
                print("insert............."+symbol+"..................db trade.json "+ Trade_id)
    def insert_from_excel_to_db(db,User,path):
        """ Open and read an Excel file """
        # Open the workbook
        xl_workbook = xlrd.open_workbook(path)
        # List sheet names, and pull a sheet by name
        sheet_names = xl_workbook.sheet_names()
        print('Sheet Names', sheet_names)
        xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
        # Or grab the first sheet by index 
        #  (sheets are zero-indexed)
        xl_sheet = xl_workbook.sheet_by_index(0)
        print ('Sheet name: %s' % xl_sheet.name)
        # Pull the first row by index
        #  (rows/columns are also zero-indexed)
        row = xl_sheet.row(0)  # 1st row
        my_row_int = xl_sheet.nrows
        # Print 1st row values and types
        from xlrd.sheet import ctype_text   
        print('(Column #) type:value')
        for idx, cell_obj in enumerate(row):
            cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
            print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))
            # Print all values, iterating through rows and columns
        num_cols = xl_sheet.ncols   # Number of columns
        # Print row number
        for row_idx in range(1, my_row_int):    # Iterate through rows 3239
            print ('-'*40)
            print ('Row: %s' % row_idx) 
            Date     = xl_sheet.cell(row_idx, 0)
            py_date = datetime.datetime(*xlrd.xldate_as_tuple(Date.value,xl_workbook.datemode))
            py_date = str(py_date.year)+"-"+str(py_date.month)+"-"+str(py_date.day)+"T00:00:00.0Z"
            #"Date": "2019-05-29T08:29:52.569Z",
            symbol   = str(xl_sheet.cell(row_idx, 1).value)
            Trade_id = str(xl_sheet.cell(row_idx, 2).value)
            order_id = str(xl_sheet.cell(row_idx, 3).value)
            side     = str(xl_sheet.cell(row_idx, 4).value)
            quanty   = xl_sheet.cell(row_idx, 5).value
            quanty   = str(quanty)
            price    = xl_sheet.cell(row_idx, 6).value
            price    = str(round(Decimal(price), 9))
            volume   = xl_sheet.cell(row_idx, 7).value
            volume   = str(round(Decimal(volume), 9))
            fee      = xl_sheet.cell(row_idx, 8).value
            fee      = str(round(Decimal(fee), 9))
            rabate   = xl_sheet.cell(row_idx, 9).value
            rabate   = str(round(Decimal(rabate), 9))
            total    = xl_sheet.cell(row_idx, 10).value
            total    = str(round(Decimal(total), 9))
            new_id = Trade_id+str(round(Decimal(volume), 5))
            #SQL.update_db(db,User,db_archive,py_date,symbol,Trade_id,order_id,side,quanty,price,volume,fee,rabate,total)
            db.insert({'Date': py_date,'symbol': symbol,'Trade_id': new_id,'order_id': order_id,'side': side,'quanty': quanty,'price': price, 'volume': volume, 'fee': fee, 'rabate': rabate, 'total': total})
            print("insert............."+symbol+"..................db trade.json "+ Trade_id)
                        #(Date   ,symbol,Trade_id,order_id,side,quanty,price,volume,fee,rabate,total):
           # time.sleep(0.41)
        print("ende convert")
    def falsches_ende_beim_archiv2(db,User,Date,symbol,Trade_id,order_id,side,quanty,price,volume,fee,rabate,total):
        docs = db.search(User.Trade_id == Trade_id)
        for doc in docs:
            db.insert({'Date': Date,'symbol': symbol,'Trade_id': Trade_id,'order_id': order_id,'side': side,'quanty': quanty,'price': price, 'volume': volume, 'fee': fee, 'rabate': rabate, 'total': total})
            print("insert............."+symbol+"..................db trade.json "+ Trade_id)
king_global=""
queen_global=""
turm_global=""
class calc(object):
    def IQ_kers(durchschnit_preis, deferenz_einzeln, ki_close ,model_18,model_19,model_20,korected_futur,toleranz,kaufblock,bestand_anzahl_hitbtc):
        global varkaufen_ab
        global gozaresh
        last_0 = 0
        last_1 = 0
        last_2 = 0
        last_3 = 0
        last_4 = 0
        glaubhaftigkeit = 0
        glaubhaftigkeit = calc.get_prozent(durchschnit_preis,Decimal(ki_close),0) - 100
        if glaubhaftigkeit > toleranz*-1 and glaubhaftigkeit < toleranz:
            glaubhaftigkeit = 1
            for i in range(len(korected_futur)):
                last_0 = korected_futur[i]
            #last_1 = model_17[len(model_17)-1]
            last_2 = model_18[len(model_18)-1]
            last_3 = model_19[len(model_19)-1]
            last_4 = model_20[len(model_20)-1]
            last_0 = Decimal(str(last_0[0]))
            #last_1 = Decimal(str(last_1[0]))
            last_2 = Decimal(str(last_2[0]))
            last_3 = Decimal(str(last_3[0]))
            last_4 = Decimal(str(last_4[0]))
        else:
            glaubhaftigkeit = 0
        turbo=1
        ha = varkaufen_ab * durchschnit_preis
        if last_0 > varkaufen_ab * durchschnit_preis:
            #if last_1>1 * durchschnit_preis:
                #turbo+=1
            if last_2>1 * durchschnit_preis:
                turbo+=1
            if last_3>1 * durchschnit_preis:
                turbo+=1
            if last_4>1 * durchschnit_preis:
                turbo+=1
            jetzige_preis_erwartung = 0
            kaufblock = kaufblock * turbo
            gozaresh += "soll kaufen turbo("+str(turbo)+")"
            jetzige_preis_erwartung  = last_0
            erwartung_prozent = calc.get_prozent(durchschnit_preis , jetzige_preis_erwartung,0) - 100
            soll_new = calc.get_alborz(erwartung_prozent,     0,     2,    0,     kaufblock )
            soll_new = soll_new - bestand_anzahl_hitbtc
            if soll_new < 0:
                soll_new = 0 
                gozaresh += "aber wir haben schon."
        else:
            gozaresh += "KI("+str(last_0)+") aber zu schwach."
        return  last_0 , glaubhaftigkeit, turbo

    def get_alborz(variab,imput_sefr,imput_sad,out_sefr,out_sad):
        input_defizit   = 0 - Decimal(imput_sefr)
        output_defizit  = 0 - Decimal(out_sefr)
        new_variable    = input_defizit + Decimal(variab)
        new_imput_sad   = input_defizit + Decimal(imput_sad)
        imput_verh      = 1/new_imput_sad
        new_output_sad  = output_defizit + Decimal(out_sad)
        output_verh     = 1/new_output_sad
        return new_variable/output_verh*imput_verh
    def time_compars():
        global letze_traid_info 
        if letze_traid_info!="":
            kauftime = letze_traid_info['timestamp']
            kauf_volume = Decimal(letze_traid_info['price'])*Decimal(letze_traid_info['quantity'])
            #tm= doc['timestamp']
            jahr = kauftime.split("-")[0]
            mont = kauftime.split("-")[1]
            tag = kauftime.split("T")[0].split("-")[2]
            hour = kauftime.split("T")[1].split(":")[0]
            min = kauftime.split("T")[1].split(":")[1]
            sec = kauftime.split("T")[1].split(":")[2].split(".")[0]
            start_time   = int(hour)*60           + int(min)
            current_time = datetime.now().hour*60 + datetime.now().minute
            vergangen = current_time - start_time
            vergangen =  vergangen - 270
            return vergangen
                #soll_new = bestand_anzahl_hitbtc * -1
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
    def eins_hoch_rechner(myint):
        prozent = 1
        for _ in range(int(myint)):
            prozent *= 10
        return prozent
    def stk_balace(durchschnit_preis, prozent, bestand_anzahl_hitbtc, stichprobe_kauf):
        x = (durchschnit_preis + (durchschnit_preis * prozent)/100)
        gesamt_wert = (bestand_anzahl_hitbtc * stichprobe_kauf)
        antwort = 0
        count=0
        for _ in range(1000):
            count+=1
            gesamt_wert += durchschnit_preis
            antwort = gesamt_wert/(bestand_anzahl_hitbtc + count)
            if antwort <= x:
                break
        return count
    def soll_new_rechner(My_traid_symbol,durchschnit_preis,vorrunde,anteil_prozent,stk_round,kaufblock,bestand_anzahl_hitbtc):#ski
        global EMA_periode
        soll_new  = 0
        geht_runter = 0
        turbo=1
        diferenz, deferenz_einzeln, ki_close, model_18, model_19, model_20, korected_futur, result_H1 = Start.load_train(My_traid_symbol,100 ,"",1 ,EMA_periode,1)
        erwatung_price, glaubhaft, turbo = calc.IQ_kers(durchschnit_preis, deferenz_einzeln, ki_close ,model_18,model_19,model_20,korected_futur,Decimal(0.75),kaufblock,bestand_anzahl_hitbtc)
        if durchschnit_preis > erwatung_price and erwatung_price!=0:
            geht_runter = 1
        volum_filter = kaufblock/5
        volum_filter = round(volum_filter,stk_round)
        #return soll_new , result_H1 ,korected_futur , volum_filter, glaubhaft, geht_runter,turbo
        return soll_new , result_H1 ,korected_futur , volum_filter, glaubhaft, geht_runter,turbo
    def nachkauf_func(bestand_anzahl_hitbtc,kaufblock,stichprobe_kauf,durchschnit_preis,turbo):
        global Nachkauf_stufe
        global nachkauf_ab
        global gozaresh
        global nachkauf_ziel
        soll_new        =0
        nachkauf_ab_new = ((nachkauf_ab*100)+Nachkauf_stufe)/100
        if durchschnit_preis * nachkauf_ab_new <  stichprobe_kauf and turbo >3:
            soll_new = calc.stk_balace(durchschnit_preis, nachkauf_ab_new, bestand_anzahl_hitbtc, stichprobe_kauf)
            gozaresh += "Nachkauf("+str(soll_new*durchschnit_preis*10000)+") "
        else:
            gozaresh += "Nachkaufgrenze nicht erreicht "
        return soll_new

    def sell_comando(sell,buy,My_traid_symbol,volum_filter,soll_new,preis_differenz,durchschnit_preis,risikoClasse):
        global html_m
        print_html=""
        global M5_control
        order_art  = "limit"
        if soll_new < 0 and sell in ["1", "sell"]: #SELL dalal
            M5_control += 1
            html_m += druck.td_decimal(1)#td15
            html_m += druck.td_str( Handel.normal_sell(sell,My_traid_symbol,volum_filter,soll_new,preis_differenz,durchschnit_preis,risikoClasse,order_art))#buy,sell
        elif soll_new > 0 : # BUY
        #elif EMA > durchschnit_preis: #+ (durchschnit_preis*Decimal(0.005)):
            M5_control += 1
            html_m += druck.td_decimal(1)#td15
            html_m += druck.td_str(Handel.normal_buy(buy,sell,My_traid_symbol,volum_filter,soll_new,preis_differenz,durchschnit_preis,risikoClasse,order_art))#buy,sell
        else:
            M5_control += 0
            html_m += druck.td_decimal(0)#td15
            html_m += druck.td_str( "")
            html_m        += "<script>for (var i=0; i<document.getElementsByClassName('"+My_traid_symbol+"').length; i++) {document.getElementsByClassName('"+My_traid_symbol+"')[i].className = 'Neutral';}</script>"
    def verdacht_sell(My_traid_symbol, bestand_anzahl_hitbtc, stichprobe_kauf, sell, soll_new):
        global varkaufen_ab
        soll_foroosh_normal = 0
        if(soll_new < 0):
            soll_foroosh_normal = soll_new*-1
        verdacht_menge = bestand_anzahl_hitbtc - soll_foroosh_normal
        verdacht_preis = stichprobe_kauf*varkaufen_ab
        verdacht_menge = bestand_anzahl_hitbtc
        Handel.jackport(My_traid_symbol,verdacht_menge,verdacht_preis)#buy,sell

        
bil_Kauf_BTC   =  0
bil_verkauf_BTC   =  0
bil_fee   =  0
#db_bilanz = TinyDB('bilanz.json')
bilanz_html=""
class druck(object):
    def print_beginn_and_titel_td(html_name,tit_tds):
        with open(html_name+'.html', 'w') as file2:
            file2.write("")
        global bilanz_html
        bilanz_html += druck.td_titel(tit_tds)
        druck.page_maker("bilanz",bilanz_html)
        bilanz_html =""
        return ""
    def td_decimal(my_st):
        color="948ACE"
        if my_st<0:
            color="D05557"
        if my_st == 0:
            color="008000"
        return "<td style='padding:0px;' bgcolor= #"+color+">"+str(my_st)+"</td>"
    def html_header():
        result  ="<style>html, body  {font-family: 'Comic Sans MS', cursive, sans-serif; }</style>"
        result  +="<body onload=myFunction();  style='padding:0px;' bgcolor= #c3c5e4>"
        result +="<script>function myFunction() { document.body.scrollTop = 2000; }function myFunction2() {\
                   for (var i=0; i<document.getElementsByClassName('Neutral').length; i++) {\
                        document.getElementsByClassName('Neutral')[i].style.display='none';\
                    }}\
                   </script></body><button onclick='myFunction2()'>Hide Neutral</button>"
        return result
    def td_str(my_st):
        color="44A1A8"
        return "<td style='padding:0px;' bgcolor= #"+color+">"+str(my_st)+"</td>"
    def td_alborz(my_st,imput0,imput100,wert):
        color2  ="#44A1A8"
        my_width   = calc.get_alborz(wert,imput0,imput100,0,100)
        if my_width < 0:
            color2  ="#d15ed1"
            my_width    = my_width*-1
        my_width   = my_width
        return (
            "<td style='padding:0px;' ><div style='padding:0px; width: 100; background: lavender;'><div style='padding:0px; width: "
            + str(my_width)
            + "; background: "
            + color2
            + ";'>"
            + str(my_st)
            + "</div></div></td>"
        )
    def td_jay(my_st,voll,wert):
        color2  ="#44A1A8"
        if wert < 0:
            color2  ="red"
            voll    = voll*-1
        my_width   = calc.get_prozent(voll,wert,0)
        my_width   = my_width
        return (
            "<td style='padding:0px;' ><div style='padding:0px; width: 100; background: lavender;'><div style='padding:0px; width: "
            + str(my_width)
            + "; background: "
            + color2
            + ";'>"
            + str(my_st)
            + "</div></div></td>"
        )
    def td_jay_best(my_st,voll,wert):
        color2  ="#44A1A8"
        my_width   = calc.get_prozent(voll,wert,0)
        my_width   = my_width
        return (
            "<td style='padding:0px;' ><div style='padding:0px; width: 100; background: lavender;'><div style='padding:0px; width: "
            + str(my_width)
            + "; background: "
            + color2
            + ";'>"
            + str(my_st)
            + "</div></div></td>"
        )
    def td_titel(my_st):
        
        #result +="<script>function hide_zero() {document.getElementsByClassName('Neutral').style.visibility = 'hidden';alert();}</script></body><button onclick='hide_zero()'>Hide Neutral</button>"
        color="AAA"
        result ="<table  style='font-size:60%; border=0><tr>"
        for i in my_st.split(','):
            my_st_td = i
            result +="<td style='padding:0px;' bgcolor= #"+color+">"+str(my_st_td)+"</td>"
        result +="</tr>"
        return result
    def page_maker(page_name,innerHtml):#chap
        global create_html
        if create_html== 1:
            with open(page_name+'.html', 'r') as file:
                filetxt =file.read()
            time.sleep(1.5)
            with open(page_name+'.html', 'w') as file2:
                file2.write(filetxt + innerHtml)
        return ""
    def kino(html_m, My_traid_symbol, Coin_symbol, count_coints, gesamt_summe, vorrunde, durchschnit_preis, stichprobe_kauf,preis_round,model_futur,Preis,bestand_anzahl_hitbtc,result_H1,glaubhaft):
        global letzter_Kauf
        global varkaufen_ab
        global gozaresh
        if bestand_anzahl_hitbtc==0:
            letzter_Kauf = Decimal(Preis['bid'])*Decimal(0.98)
        global Nachkauf_stufe
        html_m        += "<tr class='"+My_traid_symbol+"'>"
        html_m += druck.td_str(str(count_coints)+" "+Coin_symbol)#td1 
        result_H1=array(result_H1)
        ff   = len(result_H1)
        result_H1 = result_H1[range(ff-25,ff)]
        Start.diagram(My_traid_symbol ,  result_H1,0,0,0,0,"24h.png"  )#create and save diagram 24h
        html_m += druck.td_str("<img src=png/"+My_traid_symbol+"24h.png style=width:120px;>")#td1 
        html_m += druck.td_str("<img src=png/"+My_traid_symbol+"sys.png style=width:120px;>")#td1 
        Start.diagram(My_traid_symbol ,  model_futur,0,0,0,0,"Ftr.png"  )#create and save diagram 24h
        html_m += druck.td_str("<img src=png/"+My_traid_symbol+"Ftr.png style=width:120px;>")#td1 
        
        #html_m += druck.td_str(str(diferenz))#td1 
        #html_m += druck.td_str(str(deferenz_einzeln))
        
        html_m += druck.td_decimal(Nachkauf_stufe)#Anteile
        html_m += druck.td_alborz(round(gesamt_summe*10000,2),      0,    Decimal(vorrunde)/8,  gesamt_summe)#Summe€
        gewinn = calc.get_prozent(stichprobe_kauf,durchschnit_preis,0)
        if gewinn!=0:
            html_m += druck.td_alborz(round(gewinn,2),     100,        102,         gewinn)#Gewinn
        else:
            html_m += druck.td_decimal(0)
        antwort = requests.get("https://api.hitbtc.com/api/2/public/candles/"+str(My_traid_symbol)+"?limit="+str(10)+"&period=H4").json()
        h4_ar=[]
        stichprobe_kauf_ar = []
        for konto in antwort:
            h4_ar.append(Decimal(konto['close']))
            if stichprobe_kauf!=0:
                stichprobe_kauf_ar.append(stichprobe_kauf)
            else:
                stichprobe_kauf_ar.append(Decimal(konto['close']))

        Start.diagram(My_traid_symbol , h4_ar,stichprobe_kauf_ar,0,0,0,"40h.png"  )#create and save diagram 24h
        html_m += druck.td_str("<img src=png/"+My_traid_symbol+"40h.png style=width:120px;>")#td1 
        if glaubhaft == 1:
            sh = model_futur[len(model_futur)-1]
            sh = sh[0]
            sh = Decimal(sh)
            gewinn_futur = calc.get_prozent(durchschnit_preis,sh,1)
            html_m += druck.td_str(gewinn_futur)#Anteile
        else:
            html_m += druck.td_decimal(0)#Anteile

        #html_m += druck.td_alborz(round(calc.get_prozent(EMA,durchschnit_preis,0),2)-100,    0,    0.5,    (calc.get_prozent(EMA,durchschnit_preis,0)-100))#Ema/Preis 
        #html_m += druck.td_decimal(coin_anteile)#Anteile
        html_m += druck.td_str(gozaresh)#KHARID 
        html_m += druck.td_str(datetime.datetime.now().time())#KHARID 
        return html_m
    def print_report(stk_round,count_coints,Coin_symbol,gesamt_summe):
        print(str(count_coints))
        print(Coin_symbol)
        print(str(round(gesamt_summe*7600,2)))

class traid(object):
    def traid2(risikoClasse,method,vorrunde,EMA_stk,My_traid_symbol,Coin_symbol,anteil_prozent,sell,buy,stk_round,preis_round):
        global all_balance
        global count_coints
        global gozaresh
        gozaresh        =""
        count_coints +=1
        gozaresh=""
        preis_differenz = 1/Decimal(calc.eins_hoch_rechner(preis_round)) 
        client.cancel_order_info_by_symbol(My_traid_symbol)          #/order
        bestand_anzahl_hitbtc = client.get_trading_balance(Coin_symbol,all_balance)
        Preis = client.get_last_price(My_traid_symbol)#/ticker/
        durchschnit_preis = (Decimal(Preis['ask'])+Decimal(Preis['bid']))/2
        bestand_anzahl_hitbtc = round(bestand_anzahl_hitbtc,stk_round)
        gesamt_summe = durchschnit_preis * bestand_anzahl_hitbtc
        stichprobe_kauf    = client.get_client_volume(My_traid_symbol,"buy",bestand_anzahl_hitbtc,20)#/trades
        #soll_new
        kaufblock = ((vorrunde*Decimal(anteil_prozent))/100)/durchschnit_preis
        menge_test = durchschnit_preis * kaufblock *10000
        soll_new , result_H1, model_futur, volum_filter, glaubhaft, geht_runter, turbo = calc.soll_new_rechner(My_traid_symbol,durchschnit_preis,vorrunde,anteil_prozent,stk_round,kaufblock,bestand_anzahl_hitbtc)#ski
        if bestand_anzahl_hitbtc > 0 and geht_runter !=1:#nach kauf
            soll_new = calc.nachkauf_func(bestand_anzahl_hitbtc, kaufblock, stichprobe_kauf, durchschnit_preis, turbo)
        #prints
        druck.print_report(stk_round,count_coints,Coin_symbol,gesamt_summe)
        #kino
        global html_m
        html_m += druck.kino(html_m, My_traid_symbol, Coin_symbol, count_coints, gesamt_summe, vorrunde, durchschnit_preis, stichprobe_kauf,preis_round,model_futur,Preis,bestand_anzahl_hitbtc,result_H1,glaubhaft)
                           #(html_m,My_traid_symbol,Coin_symbol,count_coints,ki_close      ,gesamt_summe,vorrunde,empr,varkaufen_ab,EMA,durchschnit_preis,stichprobe_kauf,preis_round,buy,model_futur,Preis,bestand_anzahl_hitbtc,result_H1)

        #sell_comando
        calc.sell_comando(sell,buy,My_traid_symbol,volum_filter,soll_new,preis_differenz,durchschnit_preis,risikoClasse)
        #Verdachte Plazierung
        if bestand_anzahl_hitbtc>0:
            calc.verdacht_sell(My_traid_symbol,bestand_anzahl_hitbtc,stichprobe_kauf,sell,soll_new)
        html_m        += "</tr>"
        druck.page_maker("index",html_m)
        html_m        = ""
        return gesamt_summe

ser_wird = ""
M5_control = 0
all_balance = 0
all_price   = 0
#db = TinyDB('trade.json')
#User = Query()
#db_archive = TinyDB('archive.json')
#f_path = abspath("trades.xlsx")#import ecxel datei 1/2
#SQL.insert_from_excel_to_db(db,User,f_path)#import ecxel datei 2/2
euro = 7000
html_m=""
public_key = "9STf5pZbMCnxOy+FUcHCj7xOwOGR95Gu"
secret = "JldVqSH+7xGVu1kKgU9h6tdBcjY6V7W5"
client = Client("https://api.hitbtc.com", public_key, secret)
sell_pwer_over  = 0
tendenz_indagine1=0
tendenz_indagine2=0
tendenz_indagine3=0
tendenz_indagine4=0
tendenz_indagine5=0
tendenz_indagine6=0
tendenz_indagine7=0
tendenz_indagine8=0
tendenz_indagine9=0
tendenz_indagine10=0
tendenz_indagine11=0
tendenz_indagine12=0
buy_ohm_over  = 0
sell_ohm_down  = 0
buy_pwer_down  = 0
prozent_all = 0
count_coints = 0
create_html = 1
week_tendenz_alle = 0
days_last = 0
letzter_Kauf = 0
nachkauf_ab = 0
varkaufen_ab = 0
Nachkauf_stufe = 0
kurs_merker = ""
gozaresh = ""
letze_traid_info =""
result_H1=[]
EMA_periode ="H1"
nachkauf_ziel =0

#SQL.new_id(db,User)
def flut():
    file =open('index.html', 'w')
    file.write("")
    file.close()
    ht_count=0
    global sell_pwer_over
    global buy_ohm_over
    global sell_ohm_down
    global buy_pwer_down
    global create_html
    global nachkauf_ab
    global varkaufen_ab
    global EMA_periode
    global nachkauf_ziel
    EMA_stk       = 0 #nicht ändern
    anteile_prz    = 0 #nicht ändern
    EMA_periode ="M5"
    EMA_stk_panel = 12 #anzahl von berechnung durchschnitt
    vorrunde = 0
    anteile_prz_panel = Decimal(1)
    sell_pwer_over  = 2  #wiederstand bei verlust weniger verkauf und bei gewinn weniger kauf
    buy_ohm_over  = 2  #wiederstand bei verlust weniger verkauf und bei gewinn weniger kauf pilott
    sell_ohm_down  = 2  #wiederstand bei verlust weniger verkauf und bei gewinn weniger kauf
    buy_pwer_down  = 2  #wiederstand bei verlust weniger verkauf und bei gewinn weniger kauf
    buy=  "0"  #panel
    sell = "0"
    method = 3 #ebe und flut immer(1) ebe und flut ab EMA(2) kaufen unter bande verkaufen über bande(3)
    risikoClassel   = 2 #sell und buy method 
    EMAClasse = 1 # durchschnit(1)  2Kaufprobe(2)  vor bestimmte zeit(3) 
    EMAAnteil = Decimal(1) # nur EMA(1)  halbhalb(0.5) drittel(0.33)
    sensibility = Decimal(2)  #sollstk bei 1% (1) sollstk bei 2% (2) sollstk bei 3% (3) usw...  beste war 3
    timer_secund = 300
    nachkauf_ab = Decimal(1.02)
    varkaufen_ab = Decimal(1.01)
    nachkauf_ziel = Decimal(1) 
    create_html = 1
    
    """BILANZ 1/3"""
    #druck.print_beginn_and_titel_td("bilanz","COIN , Date , letze_id , kaufVolum , Verkaufvolum , Kauf BTC , Verkauf btc, fee btc , fee €, Gewinn Netto , Netto% ,leer,leer,leer")#bilanz 1/3
    #SQL.insert_from_excel_in_bilanz_db("trades.xlsx")
    global html_m
    html_m += druck.html_header()
    while True:#cheshme
        ht_count+=1
        if ht_count ==5:
            ht_count=0
            file =open('index.html', 'w')
            file.write("")
            file.close()
        if anteile_prz == 0:#erste Runde
            anteile_prz = anteile_prz_panel
        if EMA_stk == 0:#erste Runde
            EMA_stk = EMA_stk_panel
        #                         td1    td2    td3      td4        td5      td6       td7         td8         td9         td10       td11      td12    td13    td14     
        html_m += druck.td_titel(",COIN........., 24h , TEST KI , FUTUR ,  S , Summe€  ,  Gewinn , 40 H  , glaubhaft  , Report , brocker")#titel
        druck.page_maker("index",html_m)#kalle
        html_m        =""
        #client.update_trade_history(db,User,db_archive,70)
        #SQL.unic_archiv(User)
        global all_balance
        all_balance = client.get_trading_balance_all()
        global all_price
        all_price = client.get_trading_balance("BTC",all_balance)
        #history = client.get_history()

        if vorrunde ==0:
            vorrunde = Decimal(0.2)
                  #traid.traid2(risikoClassel,method,vorrunde,EMA_stk,My_traid_symbol,Coin_symbol,anteil_%      ,sell,buy,stk_round,preis_round,preis_differenz)
        
        
        all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BTCUSD"       ,"BTC"      ,anteile_prz   ,sell,buy      ,4        ,6    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ETHBTC"       ,"ETH"      ,anteile_prz   ,sell,buy      ,4        ,6    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BSVBTC"       ,"BSV"      ,anteile_prz   ,sell,buy      ,3        ,6    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"LTCBTC"       ,"LTC"      ,anteile_prz   ,sell,buy      ,3        ,7    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"NEOBTC"       ,"NEO"      ,anteile_prz   ,sell,buy      ,2        ,7    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"IOTABTC"      ,"IOTA"     ,anteile_prz   ,sell,buy      ,1        ,9    )

        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ETCBTC"       ,"ETC"      ,anteile_prz   ,sell,buy      ,2        ,7    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"XRPBTC"       ,"XRP"      ,anteile_prz   ,sell,buy      ,1        ,9    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ZRXBTC"       ,"ZRX"      ,anteile_prz   ,sell,buy      ,1        ,9    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"QTUMBTC"      ,"QTUM"     ,anteile_prz   ,sell,buy      ,2        ,8    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BCHBTC"       ,"BCH"      ,anteile_prz   ,sell,buy      ,4        ,6    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"XMRBTC"       ,"XMR"      ,anteile_prz   ,sell,buy      ,3        ,6    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ADABTC"       ,"ADA"      ,anteile_prz   ,sell,buy      ,0        ,9    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"DASHBTC"      ,"DASH"     ,anteile_prz   ,sell,buy      ,3        ,6    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"XLMBTC"       ,"XLM"      ,anteile_prz   ,sell,buy      ,1        ,9    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ZECBTC"       ,"ZEC"      ,anteile_prz   ,sell,buy      ,3        ,6    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"DOGEBTC"      ,"DOGE"     ,anteile_prz   ,sell,buy      ,0        ,11   )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"EOSBTC"       ,"EOS"      ,anteile_prz   ,sell,buy      ,2        ,8    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ONTBTC"       ,"ONT"      ,anteile_prz   ,sell,buy      ,3        ,8    )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"TRXBTC"       ,"TRX"      ,anteile_prz   ,sell,buy      ,0        ,10   )
        #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BTGBTC"       ,"BTG"      ,anteile_prz   ,sell,buy      ,3        ,7    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"STRATBTC"     ,"STRAT"    ,anteile_prz   ,sell,buy      ,1        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"KBCBTC"       ,"KBC"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"DGTXBTC"      ,"DGTX"     ,anteile_prz   ,sell,buy      ,0        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"XEMBTC"       ,"XEM"      ,anteile_prz   ,sell,buy      ,0        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"C20BTC"       ,"C20"      ,anteile_prz   ,"sell",buy    ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"GNOBTC"       ,"GNO"      ,anteile_prz   ,sell,buy      ,3        ,7    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"OMGBTC"       ,"OMG"      ,anteile_prz   ,sell,buy      ,2        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BERRYBTC"     ,"BERRY"    ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ZILBTC"       ,"ZIL"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"MAIDBTC"      ,"MAID"     ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"WAXBTC"       ,"WAX"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"KMDBTC"       ,"KMD"      ,anteile_prz   ,sell,buy      ,1        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"NOAHBTC"      ,"NOAH"     ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"AEBTC"        ,"AE"       ,anteile_prz   ,sell,buy      ,1        ,8   )
       #BATall_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BTSBTC"       ,"BTS"      ,anteile_prz   ,sell,buy      ,0        ,7    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BTTBTC"       ,"BTT"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"LSKBTC"       ,"LSK"      ,anteile_prz   ,sell,buy      ,2        ,7    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"REPBTC"       ,"REP"      ,anteile_prz   ,sell,buy      ,3        ,7    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"SCBTC"        ,"SC"       ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"VETBTC"       ,"VET"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"WAVESBTC"     ,"WAVES"    ,anteile_prz   ,sell,buy      ,2        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"XDNBTC"       ,"XDN"      ,anteile_prz   ,sell,buy      ,0        ,11   )
        
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"PREBTC"       ,"PRE"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ICXBTC"       ,"ICX"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"DGBBTC"       ,"DGB"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"XVGBTC"       ,"XVG"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"NXTBTC"       ,"NXT"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"VRABTC"       ,"VRA"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"TNTBTC"       ,"TNT"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BTMBTC"       ,"BTM"      ,anteile_prz   ,sell,buy      ,0        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"WIKIBTC"      ,"WIKI"     ,anteile_prz   ,sell,buy      ,1        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ETPBTC"       ,"ETP"      ,anteile_prz   ,sell,buy      ,1        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"CROBTC"       ,"CRO"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"STEEMBTC"     ,"STEEM"    ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BMCBTC"       ,"BMC"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"XTZBTC"       ,"XTZ"      ,anteile_prz   ,sell,buy      ,1        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BNTBTC"       ,"BNT"      ,anteile_prz   ,sell,buy      ,1        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"DCTBTC"       ,"DCT"      ,anteile_prz   ,sell,buy      ,0        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ARDRBTC"      ,"ARDR"     ,anteile_prz   ,sell,buy      ,0        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"SMARTBTC"     ,"SMART"    ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"NANOBTC"      ,"NANO"     ,anteile_prz   ,sell,buy      ,2        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"GNTBTC"       ,"GNT"      ,anteile_prz   ,sell,buy      ,0        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BATBTC"       ,"BAT"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"IPLBTC"       ,"IPL"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"EDOBTC"       ,"EDO"      ,anteile_prz   ,sell,buy      ,1        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ETNBTC"       ,"ETN"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BCNBTC"       ,"BCN"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"IOSTBTC"      ,"IOST"     ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"NEBLBTC"      ,"NEBL"     ,anteile_prz   ,sell,buy      ,2        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"NEXOBTC"      ,"NEXO"     ,anteile_prz   ,sell,buy      ,0        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"PPCBTC"       ,"PPC"      ,anteile_prz   ,sell,buy      ,1        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"MCOBTC"       ,"MCO"      ,anteile_prz   ,sell,buy      ,2        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ABYSSBTC"     ,"ABYSS"    ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"HVNBTC"       ,"HVN"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"XZCBTC"       ,"XZC"      ,anteile_prz   ,sell,buy      ,2        ,7    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ORMEUSBTC"    ,"ORMEUS"   ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"EDGBTC"       ,"EDG"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ZENBTC"       ,"ZEN"      ,anteile_prz   ,sell,buy      ,2        ,7    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"CRPTBTC"      ,"CRPT"     ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"GRINBTC"      ,"GRIN"     ,anteile_prz   ,sell,buy      ,2        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ENJBTC"       ,"ENJ"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BCDBTC"       ,"BCD"      ,anteile_prz   ,sell,buy      ,1        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"NIMBTC"       ,"NIM"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BNBBTC"       ,"BNB"      ,anteile_prz   ,sell,buy      ,2        ,7    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"ZRCBTC"       ,"ZRC"      ,anteile_prz   ,sell,buy      ,2        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BMHBTC"       ,"BMH"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"PMABTC"       ,"PMA"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"SWMBTC"       ,"SWM"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"YCCBTC"       ,"YCC"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BNKBTC"       ,"BNK"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"PPTBTC"       ,"PPT"      ,anteile_prz   ,sell,buy      ,2        ,8    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"PASSBTC"      ,"PASS"     ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"EMCBTC"       ,"EMC"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"STXBTC"       ,"STX"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"EVXBTC"       ,"EVX"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BANCABTC"     ,"BANCA"    ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BCHBTC"       ,"BCH"      ,anteile_prz   ,sell,buy      ,4        ,6    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"SPDBTC"       ,"SPD"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"MITHBTC"      ,"MITH"     ,anteile_prz   ,sell,buy      ,0        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"XCONBTC"      ,"XCON"     ,anteile_prz   ,sell,buy      ,0        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"CHSBBTC"      ,"CHSB"     ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"MRKBTC"       ,"MRK"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"MRSBTC"       ,"MRS"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"MKRBTC"       ,"MKR"      ,anteile_prz   ,"sell",buy    ,4        ,5    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"BCIBTC"       ,"BCI"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"VOCOBTC"      ,"VOCO"     ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"PAYBTC"       ,"PAY"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"DCNBTC"       ,"DCN"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"NCTBTC"       ,"NCT"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"NCTBTC"       ,"NCT"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"SRNBTC"       ,"SRN"      ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"JBCBTC"       ,"JBC"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"STORJBTC"     ,"STORJ"    ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"MANABTC"      ,"MANA"     ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"CPTBTC"       ,"CPT"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"RLCBTC"       ,"RLC"      ,anteile_prz   ,sell,buy      ,1        ,9    )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"PROCBTC"      ,"PROC"     ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"LENDBTC"      ,"LEND"     ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"TELBTC"       ,"TEL"      ,anteile_prz   ,sell,buy      ,0        ,11   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"MESSEBTC"     ,"MESSE"    ,anteile_prz   ,sell,buy      ,0        ,10   )
       #all_price+=traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"NPLCBTC"      ,"NPLC"     ,anteile_prz   ,sell,buy      ,0        ,11   )
                  #traid.traid2(risikoClassel,method,vorrunde,EMA_stk,"XEMBTC"       ,"XEM"      ,anteile_prz   ,sell,buy      ,0        ,9    )#payan
        kaufkraft = str(round(Decimal(client.get_trading_balance("BTC",all_balance))*7600,2))+"€"
        #print("------------------  BTC: "+str(all_price)+"("+calc.get_prozent(vorrunde,all_price,1)+")% -----------------Kraft: "+kaufkraft+"--------")
        vorrunde = all_price
        
        html_m        = ""
        global prozent_all
        global count_coints
        gesamte_prozente       = prozent_all/Decimal(count_coints)
        zusatzt                = (anteile_prz_panel *gesamte_prozente )/100#d
        zusatzt                = anteile_prz_panel - zusatzt#e
        zusatzt                = zusatzt * 10
        anteile_prz           = anteile_prz_panel
        zusatzt               = zusatzt
        anteile_prz           = anteile_prz + zusatzt
        prozent_all = 0
        global M5_control
        if method == 3:
            drchschnitt = M5_control/count_coints
            if drchschnitt < Decimal(0.04):
                EMA_stk = EMA_stk_panel
                EMA_stk = round(EMA_stk_panel*0.65)
            elif drchschnitt < Decimal(0.116):
                EMA_stk = EMA_stk_panel
                EMA_stk = round(EMA_stk_panel*0.85)
            if EMA_stk<7:
                EMA_stk = 7 
        global week_tendenz_alle
        week_tendenz_alle = week_tendenz_alle/count_coints
        M5_control = 0
        count_coints = 0

        html_m +=         "</table><H1><ENDE></H1>"#
        html_m +=         druck.td_titel(",Kraft  , BTC  , Änderung%  , Prozent alle , anteile Original , anteile , zusatzt , EMA_stk ,week_tendenz_alle")
        html_m +=         druck.td_str(kaufkraft)
        html_m +=         druck.td_str(str(round(all_price,5)))#BTC
        html_m +=         druck.td_str(str(calc.get_prozent(vorrunde,all_price,1)))#Änderung%
        html_m +=         druck.td_str(str(round(gesamte_prozente,2)))#Prozent alle
        html_m +=         druck.td_str(str(round(anteile_prz_panel,2)))#anteile Original
        html_m +=         druck.td_str(str(round(anteile_prz,2)))#anteile
        html_m +=         druck.td_str(str(round(zusatzt,3)))
        html_m +=         druck.td_str(str(EMA_stk))
        html_m +=         druck.td_str(str(round(week_tendenz_alle,2)))
        week_tendenz_alle = 0
        html_m += "</table><H1><ENDE></H1>"#payan flut
        druck.page_maker("index",html_m)

        html_m        =""
        time.sleep(timer_secund)
        
flut()

#history = client.get_address()
#Preis = client.get_last_price('IOTA') fehler
#symbol = client.get_symbol('IOTAbtc')#{'id': 'IOTABTC', 'baseCurrency': 'IOTA', 'quoteCurrency': 'BTC', 'quantityIncrement': '0.1', 'tickSize': '0.000000001', 'takeLiquidityRate': '0.002', 'provideLiquidityRate': '0.001', 'feeCurrency': 'BTC'}
#orderbook = client.get_orderbook('IOTABTC')

#adress = client.get_address('IOTABTC') fehler
#order_info = client.get_order_info()
#candle = client.get_candlel('IOTABTC',"M15")








