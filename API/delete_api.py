from API.import_a import *

class DELETEE_API(Configg):

    def __init__(self) -> None:
        super().__init__()
        self.method = 'DELETE'

    def cancel_order_by_id(self, symbol, last_sl_order_id):

        cancel_order = None
        all_orders = None
        success_flag = False
        all_orders = get_apii.get_all_orders()

        for item in all_orders:
            if item["symbol"] == symbol:
                params = {}
                params["symbol"] = item["symbol"]
                params["orderId"] = last_sl_order_id
                params = self.get_signature(params)
                url = my_params.URL_PATTERN_DICT['create_order_url']                
                cancel_order = self.HTTP_request(url, method=self.method, headers=self.header, params=params)                
                break

        if cancel_order and 'status' in cancel_order and cancel_order['status'] == 'CANCELED':
            success_flag = True 
            
        return cancel_order, success_flag

    def cancel_all_orders_for_position(self, symbol_list):
        cancel_orders_list = []      

        for item in symbol_list:
            cancel_order = None
            params = {}
            params["symbol"] = item
            params = self.get_signature(params)
            url = my_params.URL_PATTERN_DICT['cancel_all_orders_url']
            
            cancel_order = self.HTTP_request(url, method=self.method, headers=self.header, params=params)
            cancel_orders_list.append(cancel_order)
            
        return cancel_orders_list
    
    def cancel_all_open_orders(self):

        cancel_orders = None
        all_orders = None
        all_orders = get_apii.get_all_orders()

        for item in all_orders:
            params = {}
            params["symbol"] = item["symbol"]
            params = self.get_signature(params)
            url = my_params.URL_PATTERN_DICT['cancel_all_orders_url']
            method = 'DELETE'
            cancel_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)
            # print(cancel_orders)

        return 
    
delete_apii = DELETEE_API()