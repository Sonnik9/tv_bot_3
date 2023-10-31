from pparamss import my_params
from API.config import Configg
import pandas as pd

class GETT_API(Configg):

    def __init__(self) -> None:
        super().__init__()   
        self.method = 'GET'

    def get_all_tickers(self):

        all_tickers = None
        url = my_params.URL_PATTERN_DICT['all_tikers_url']       
        # print(url)
        all_tickers = self.HTTP_request(url, method=self.method, headers=self.header)

        return all_tickers
    
    def get_excangeInfo(self, symbol):

        exchangeInfo = None
        if symbol:            
            url = f"{my_params.URL_PATTERN_DICT['exchangeInfo_url']}?symbol={symbol}"
        else:
            url = my_params.URL_PATTERN_DICT['exchangeInfo_url']        
        exchangeInfo = self.HTTP_request(url, method=self.method, headers=self.header)

        return exchangeInfo
    
    def get_balance(self):

        current_balance = None        
        url = my_params.URL_PATTERN_DICT['balance_url']
        params = {}
        params = self.get_signature(params)
        current_balance = self.HTTP_request(url, method=self.method, headers=self.header, params=params)
        current_balance = float([x['balance'] for x in current_balance if x['asset'] == 'USDT'][0])

        return current_balance
    
    def get_position_price(self, symbol):

        positions = None        
        url = my_params.URL_PATTERN_DICT['positions_url']
        params = {}
        params = self.get_signature(params)
        positions = self.HTTP_request(url, method=self.method, headers=self.header, params=params)
        # print(positions)
        positions = float([x for x in positions if x['symbol'] == symbol][0]["entryPrice"])

        return positions
    
    def get_klines(self, symbol):

        klines = None
        url = my_params.URL_PATTERN_DICT["klines_url"]        
        params = {}
        params["symbol"] = symbol
        params["interval"] = my_params.INTERVAL
        params["limit"] = 16
        params = self.get_signature(params)
        klines = self.HTTP_request(url, method=self.method, headers=self.header, params=params)
        if klines:
            data = pd.DataFrame(klines).iloc[:, :6]
            data.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            data = data.set_index('Time')
            data.index = pd.to_datetime(data.index, unit='ms')
            data = data.astype(float)
        
        return data
    
# ////////////////////////////////////////////////////////////////////////////////////

    def get_all_orders(self):

        all_orders = None        
        params = {}               
        url = my_params.URL_PATTERN_DICT['get_all_orders_url']
        params = self.get_signature(params)
        all_orders = self.HTTP_request(url, method=self.method, headers=self.header, params=params)

        return all_orders
    
    def get_open_positions(self):

        all_positions = None        
        params = {}          
        symbol = None     
        url = my_params.URL_PATTERN_DICT['positions_url']
        if symbol:
            params["symbol"] = symbol
        params = self.get_signature(params)
        all_positions = self.HTTP_request(url, method=self.method, headers=self.header, params=params)
        all_positions = [x for x in all_positions if float(x["positionAmt"]) != 0]

        return all_positions 
# //////////////////////////////////////////////////////////////////////////////////

get_apii = GETT_API()
    
# python -m API.bin_data_get
