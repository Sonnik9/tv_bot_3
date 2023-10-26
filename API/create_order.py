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
        # print(item["symbol"])
        params["type"] = market_type
        params["quantity"] = item['qnt']
        # print(item['qnt'])
      
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



    
create_orders_obj = CREATE_BINANCE_ORDER()


# make_order = None 
# item = {}
# symbol = 'BTCUSDT'
# item["symbol"] = 'BTCUSDT'
# item["qnt"] = 0.001
# item["atr"] = 475
# is_closing = 1
# type_market = 'MARKET'
# item["defender"] = 1
# target_price = None
# open_market_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)

# symbol = 'BTCUSDT'
# item["symbol"] = 'BTCUSDT'
# item["qnt"] = 0.001
# item["atr"] = 475
# is_closing = -1
# type_market = 'STOP_MARKET'
# item["defender"] = 1
# target_price = 30000
# open_market_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)

# symbol = 'BTCUSDT'
# item["symbol"] = 'BTCUSDT'
# item["qnt"] = 0.001
# item["atr"] = 475
# is_closing = -1
# type_market = 'TAKE_PROFIT_MARKET'
# item["defender"] = 1
# target_price = 40000
# open_market_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)

# print(open_market_order)

# symbol = 'ETHUSDT'
# item["symbol"] = 'ETHUSDT'
# item["qnt"] = 0.003
# item["atr"] = 475
# is_closing = 1
# type_market = 'LIMIT'
# item["defender"] = 1
# target_price = 1800
# open_market_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)

# print(open_market_order)

# symbol_list_to_cancel_orders = ['BTCUSDT']
# cancel_all_orders_answer = create_orders_obj.cancel_all_orders_for_position(symbol_list_to_cancel_orders)


# python -m API.create_order

        
        # if market_type == 'MARKET' or market_type == 'LIMIT' or market_type == 'TAKE_PROFIT_MARKET':
   


