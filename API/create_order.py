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
        
        if market_type == 'MARKET' or market_type == 'LIMIT':
            params["quantity"] = item['qnt']
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
# type_market = 'MARKET'
# item["defender"] = 1
# target_price = None 
# # open_market_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)

# # print(open_market_order)
# type_market = 'TRAILING_STOP_MARKET'
# is_closing = -1
# item["qnt"] = 0.001
# target_price = None
# item["enter_deFacto_price"] = 31276
# open_trailing_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)
# print(open_trailing_order)



# open_pos = create_orders_obj.get_open_positions(symbol)
# print(open_pos)

# answer_list = create_orders_obj.try_to_close_by_market_all_open_positions()
# print(answer_list)



# {'symbol': 'BTCUSDT', 'positionAmt': '0.001', 'entryPrice': '28050.0', 'breakEvenPrice': '28061.22', 'markPrice': '28355.00586813', 'unRealizedProfit': '0.30500586', 'liquidationPrice': '0', 'leverage': '1', 'maxNotionalValue': '5.0E8', 'marginType': 'cross', 'isolatedMargin': '0.00000000', 'isAutoAddMargin': 'false', 'positionSide': 'BOTH', 'notional': '28.35500586', 'isolatedWallet': '0', 'updateTime': 1697469250488, 'isolated': False, 'adlQuantile': 1}



# all_orders = None 
# make_order = None 
# item = {}
# symbol = 'BTCUSDT'
# item["symbol"] = 'BTCUSDT'
# item["qnt"] = 0.001
# is_closing = 1
# type_market = 'MARKET'
# item["defender"] = 1
# target_price = None

# make_order = create_orders_obj.make_order(item, is_closing, type_market, target_price)
# print(make_order)
# url = None
# symbol_info = bin_data.get_excangeInfo(item["symbol"])

# symbol_data = None
# if symbol_info:
#     symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)

# print(symbol_data)

# position_price = None

# position_price = bin_data.get_position_price(symbol)

# print(position_price)




# is_closing = -1
# target_price = make_order["price"] * 500 * 0.9
# type_market = 'LIMIT'
# make_order = create_orders_obj.make_order(item, is_closing, type_market, target_price)
# print(make_order)

# is_closing = -1
# target_price = make_order["price"] * 500 * 1.2
# type_market = 'LIMIT'
# make_order = create_orders_obj.make_order(item, is_closing, type_market, target_price)
# print(make_order)

# target_price = 26500
# item["defender"] = 1
# make_order = create_orders_obj.make_order(item, is_closing, type_market, target_price)
# print(make_order)

# time.sleep(5)

# all_orders = create_orders_obj.get_all_orders()
# print(all_orders)

# item["last_sl_order_id"] = '3486091588'
# cancel_orders = None 
# cancel_orders = create_orders_obj.cancel_order_by_id(item["symbol"], item["last_sl_order_id"])
# print(cancel_orders)


# resp = None
# resp = create_orders_obj.close_all_position()
# print(resp)

# python -m API.create_order

# {'orderId': 3486091588, 'symbol': 'BTCUSDT', 'status': 'CANCELED', 'clientOrderId': '6TNC4fs0Xzmp1Dth3o7lLh', 'price': '30500.00', 'avgPrice': '0.00', 'origQty': '0.001', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'LIMIT', 'reduceOnly': False, 'closePosition': False, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'LIMIT', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'NONE', 'goodTillDate': 0, 'updateTime': 1697468019394}


        # ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET']
        # print(item)