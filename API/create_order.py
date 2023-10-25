from API.config import Configg
from pparamss import my_params
import time
from API.bin_data_get import bin_data

import logging
import os
import inspect

logging.basicConfig(filename='API/orders_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

# except Exception as ex:
#     logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

class CREATE_BINANCE_ORDER(Configg):

    def __init__(self) -> None:
        super().__init__()

    def set_leverage(self, symbol):

        params = {}
        url = my_params.URL_PATTERN_DICT["set_leverage_url"]            
        method = 'POST'
        params['symbol'] = symbol
        params['leverage'] = my_params.LEVERAGE
        params = self.get_signature(params)
        response = self.HTTP_request(url, method=method, headers=self.header, params=params)
        
        return response 
    
    def make_order(self, item, is_closing, target_price, market_type):

        response = None
        success_flag = False
        url = my_params.URL_PATTERN_DICT['create_order_url']
        params = {}
        method = 'POST'
        params["symbol"] = item["symbol"] 
        params["type"] = market_type
        params["quantity"] = item['qnt']
        # print(item["qnt"])
     
        if market_type == 'LIMIT':            
            params["price"] = target_price
            params["timeinForce"] = 'GTC' 
            
        if market_type == 'STOP_MARKET' or market_type == 'TAKE_PROFIT_MARKET':
            params['stopPrice'] = target_price
            params['closePosition'] = True 
  
        if item["defender"] == 1*is_closing:
            side = 'BUY'
        elif item["defender"] == -1*is_closing:
            side = "SELL" 
        params["side"] = side 

        params = self.get_signature(params)
        response = self.HTTP_request(url, method=method, headers=self.header, params=params)
        if response and 'status' in response and response['status'] == 'NEW':
            success_flag = True

        return response, success_flag
    
# ////////////////////////////////////////////////////////////////////////////////////

    def get_all_orders(self):
        all_orders = None
        
        params = {}
        method = 'GET'       
        url = my_params.URL_PATTERN_DICT['get_all_orders_url']
        params = self.get_signature(params)
        all_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)

        return all_orders
    
    def cancel_order_by_id(self, symbol, last_sl_order_id):

        cancel_order = None
        all_orders = None
        success_flag = False

        all_orders = self.get_all_orders()

        for item in all_orders:
            if item["symbol"] == symbol:
                params = {}
                params["symbol"] = item["symbol"]
                params["orderId"] = last_sl_order_id
                params = self.get_signature(params)
                url = my_params.URL_PATTERN_DICT['create_order_url']
                method = 'DELETE'
                cancel_order = self.HTTP_request(url, method=method, headers=self.header, params=params)                
                break

        if cancel_order and 'status' in cancel_order and cancel_order['status'] == 'CANCELED':
            success_flag = True 
            
        return cancel_order, success_flag
    
    def get_open_positions(self):
        all_positions = None        
        params = {}
        method = 'GET'  
        symbol = None     
        url = my_params.URL_PATTERN_DICT['positions_url']
        if symbol:
            params["symbol"] = symbol
        params = self.get_signature(params)
        all_positions = self.HTTP_request(url, method=method, headers=self.header, params=params)

        all_positions = [x for x in all_positions if float(x["positionAmt"]) != 0]

        return all_positions
    
    def try_to_close_by_market_open_position_by_item(self, main_stake):   
        close_pos_by_market = None            
        is_closing = -1
        target_price = None
        type_market = 'MARKET'
        good_news = []
        bad_news = []

        for item in main_stake:
            try:
                close_pos_by_market = self.make_order(item, is_closing, type_market, target_price)
                
                if close_pos_by_market and 'status' in close_pos_by_market and close_pos_by_market['status'] == 'NEW':
                    good_news.append(item["symbol"])
                else:
                    bad_news.append(item["symbol"])
                    
            except Exception as ex:
                print(ex)
                bad_news.append(item["symbol"])
                continue

        return good_news, bad_news
    
    def try_to_close_by_market_all_open_positions(self, main_stake):
        all_positions = None        
        close_pos_by_market = None        
        close_pos_by_market_answer_list = []      
        is_closing = -1
        target_price = None
        type_market = 'MARKET'
        symbol = None
        all_symbols = []
        try:
            all_positions = self.get_open_positions(symbol)  
        except Exception as ex:
            print(ex)

        all_symbols = [x["symbol"] for x in all_positions]
        main_stakee = [x for x in main_stake if x["symbol"] in all_symbols]

        for item in main_stakee:
            try:
                close_pos_by_market = self.make_order(item, is_closing, type_market, target_price)
                close_pos_by_market_answer_list.append(close_pos_by_market)
            except Exception as ex:
                print(ex)
                close_pos_by_market_answer_list.append(ex)
                continue

        return close_pos_by_market_answer_list
       
    def cancel_all_open_orders(self):
        cancel_orders = None
        all_orders = None

        all_orders = self.get_all_orders()

        for item in all_orders:
            params = {}
            params["symbol"] = item["symbol"]
            params = self.get_signature(params)
            url = my_params.URL_PATTERN_DICT['cancel_all_orders_url']
            method = 'DELETE'
            cancel_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)
            print(cancel_orders)

        return 
        
    def cancel_all_orders_for_position(self, symbol_list):
        cancel_orders_list = []      

        for item in symbol_list:
            cancel_order = None
            params = {}
            params["symbol"] = item
            params = self.get_signature(params)
            url = my_params.URL_PATTERN_DICT['cancel_all_orders_url']
            method = 'DELETE'
            cancel_order = self.HTTP_request(url, method=method, headers=self.header, params=params)
            cancel_orders_list.append(cancel_order)
            # print(cancel_orders)

        return cancel_orders_list


    def close_position_confidencer(self, main_stake):

        main_stake_var = main_stake.copy()
        open_pos = None
        cancel_all_orders_answer = None
        open_pos_symbol_list = []
        try_to_close_by_market_list = []

        open_pos = self.get_open_positions()   
        open_pos_symbol_list = [x["symbol"] for x in open_pos]

        for i, item in enumerate(main_stake):
            if item["done_level"] == 6:
                if item["symbol"] in open_pos_symbol_list:
                    try_to_close_by_market_list.append(item)
                else:
                    main_stake_var[i]["close_position"] = True
        try: 
            good_news_symbol_list, bad_news_symbol_list = [], []   
            good_news_symbol_list, bad_news_symbol_list = self.try_to_close_by_market_open_position_by_item(try_to_close_by_market_list)
            if good_news_symbol_list:           
                for i, item in enumerate(main_stake):
                    if item["done_level"] == 6:
                        if item["symbol"] in good_news_symbol_list:
                            main_stake_var[i]["close_position"] = True           
            
            symbol_list_to_cancel_orders = [x["symbol"] for x in main_stake_var if x["close_position"]]
            cancel_all_orders_answer = self.cancel_all_orders_for_position(symbol_list_to_cancel_orders)
        except Exception as ex:
            print(ex)

        return main_stake_var, bad_news_symbol_list, cancel_all_orders_answer 
    
create_orders_obj = CREATE_BINANCE_ORDER()

# make_order = None 
# item = {}
# symbol = 'BTCUSDT'
# item["symbol"] = 'BTCUSDT'
# item["qnt"] = 0.001
# item["atr"] = 475
# is_closing = 1
# type_market = 'LIMIT'
# item["defender"] = 1
# target_price = 30000 
# open_market_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)

# print(open_market_order)

# python -m API.create_order

        
        # if market_type == 'MARKET' or market_type == 'LIMIT' or market_type == 'TAKE_PROFIT_MARKET':
   


