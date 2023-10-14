from API.config import Configg
from pparamss import my_params
import time

class CREATE_BINANCE_ORDER(Configg):

    def __init__(self) -> None:
        super().__init__()

    def make_order(self, item, is_closing):
        # ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET']
        response = None
        url = my_params.URL_PATTERN_DICT['create_order_url']
        params = {}
        method = 'POST'
        params["symbol"] = item["symbol"] 
        params["type"] = 'MARKET'
        if is_closing == -1:
            qnt = item['qnt_exit']  
        else: 
            qnt = item['qnt']  
        params["quantity"] = qnt
        if item["defender"] == 1*is_closing:
            side = 'BUY'
        elif item["defender"] == -1*is_closing:
            side = "SELL" 
        params["side"] = side 

        params = self.get_signature(params)
        response = self.HTTP_request(url, method=method, headers=self.header, params=params)
        
        return response 
       
    def cancel_all_orders(self):

        all_orders = None
        cancel_orders = None
        params = {}
        method = 'GET'       
        url = my_params.URL_PATTERN_DICT['get_all_orders_url']
        params = self.get_signature(params)
        all_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)

        for item in all_orders:
            params = {}
            params["symbol"] = item["symbol"]
            params = self.get_signature(params)
            url = my_params.URL_PATTERN_DICT['cancel_all_orders_url']
            method = 'DELETE'
            cancel_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)
            print(cancel_orders)

        return 
        
create_orders_obj = CREATE_BINANCE_ORDER()

# resp = None
# resp = create_orders_obj.close_all_position()
# print(resp)

# python -m API.create_order
