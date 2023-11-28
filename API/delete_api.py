# import pandas as pd
from API.get_api import GETT_API

class DELETEE_API(GETT_API):

    def __init__(self) -> None:
        super().__init__()       

    def cancel_all_orders_for_position(self, symbol_list):
        cancel_orders_list = []  
        method = 'DELETE'    

        for item in symbol_list:
            cancel_order = None
            params = {}
            params["symbol"] = item
            params = self.get_signature(params)
            url = self.URL_PATTERN_DICT['cancel_all_orders_url']
            
            cancel_order = self.HTTP_request(url, method=method, headers=self.header, params=params)
            cancel_orders_list.append(cancel_order)
            
        return cancel_orders_list
    
    def cancel_all_open_orders(self):

        cancel_orders = None
        all_orders = None
        all_orders = self.get_all_orders()

        for item in all_orders:
            params = {}
            params["symbol"] = item["symbol"]
            params = self.get_signature(params)
            url = self.URL_PATTERN_DICT['cancel_all_orders_url']
            method = 'DELETE'
            cancel_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)
            # print(cancel_orders)

        return 
    
delete_apii = DELETEE_API()