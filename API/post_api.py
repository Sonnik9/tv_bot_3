from pparamss import my_params
from API.config import Configg

class POSTT_API(Configg):

    def __init__(self) -> None:
        super().__init__()
        self.method = 'POST'

    def set_leverage(self, symbol):

        params = {}
        url = my_params.URL_PATTERN_DICT["set_leverage_url"]
        params['symbol'] = symbol
        params['leverage'] = my_params.LEVERAGE
        params = self.get_signature(params)
        response = self.HTTP_request(url, method=self.method, headers=self.header, params=params)
        
        return response 
    
    def make_order(self, item, is_closing, target_price, market_type):

        response = None
        success_flag = False
        url = my_params.URL_PATTERN_DICT['create_order_url']
        params = {}        
        params["symbol"] = item["symbol"]        
        params["type"] = market_type
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
        response = self.HTTP_request(url, method=self.method, headers=self.header, params=params)
        if response and 'status' in response and response['status'] == 'NEW':
            success_flag = True

        return response, success_flag
    
post_apii = POSTT_API()

