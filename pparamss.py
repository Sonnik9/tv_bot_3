from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

class BASIC_PARAMETRS():
    def __init__(self):        
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!'        
        # self.market = 'spot'
        self.market = 'futures'
        self.test_flag = True
        # self.test_flag = False
        self.DIVERCIFICATION_NUMDER = 15
        self.DEPO = 20

    def init_api_key(self):
        self.tg_api_token = os.getenv("TG_API_TOKEN", "")
        if not self.test_flag:
            self.api_key  = os.getenv("BINANCE_API_PUBLIC_KEY_REAL", "")
            self.api_secret = os.getenv("BINANCE_API_PRIVATE_KEY_REAL", "")
        else:
            self.api_key  = os.getenv("BINANCE_API_PUBLIC_KEY_FUTURES_TEST", "")
            self.api_secret = os.getenv("BINANCE_API_PRIVATE_KEY_FUTURES_TEST", "")    

        self.header = {
            'X-MBX-APIKEY': self.api_key
        }     

class URL_TEMPLATES(BASIC_PARAMETRS):
    def __init__(self) -> None:
        super().__init__()        
        self.URL_PATTERN_DICT= {}              

    def init_urls(self):  
        if not self.test_flag:      
            if self.market == 'spot':  
                print('spot') 
                self.URL_PATTERN_DICT['current_ptice_url'] = "https://api.binance.com/api/v3/ticker/price"            
                self.URL_PATTERN_DICT['all_tikers_url'] = "https://api.binance.com/api/v3/ticker/24hr"
                self.URL_PATTERN_DICT['create_order_url'] = 'https://api.binance.com/api/v3/order' 
                self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://api.binance.com/api/v3/exchangeInfo'
                self.URL_PATTERN_DICT['balance_url'] = 'https://api.binance.com/api/v3/account'
                self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://api.binance.com/api/v3/openOrders'
                self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://api.binance.com/api/v3/allOpenOrders'
                self.URL_PATTERN_DICT['positions_url'] = 'https://api.binance.com/api/v3/account'                
                self.URL_PATTERN_DICT["klines_url"] = 'https://api.binance.com/api/v3/klines'

        else:
            print('futures test')
            self.URL_PATTERN_DICT['current_ptice_url'] = "https://fapi.binance.com/fapi/v1/ticker/price"
            self.URL_PATTERN_DICT['all_tikers_url'] = "https://testnet.binancefuture.com/fapi/v1/ticker/24hr"
            self.URL_PATTERN_DICT['create_order_url'] = 'https://testnet.binancefuture.com/fapi/v1/order'
            self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://testnet.binancefuture.com/fapi/v1/exchangeInfo'
            self.URL_PATTERN_DICT['balance_url'] = 'https://testnet.binancefuture.com/fapi/v2/balance'
            self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://testnet.binancefuture.com/fapi/v1/openOrders'
            self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://testnet.binancefuture.com/fapi/v1/allOpenOrders'
            self.URL_PATTERN_DICT['positions_url'] = 'https://testnet.binancefuture.com/fapi/v2/positionRisk'
            self.URL_PATTERN_DICT["set_leverage_url"] = 'https://testnet.binancefuture.com/fapi/v1/leverage'
            self.URL_PATTERN_DICT["klines_url"] = 'https://testnet.binancefuture.com/fapi/v1/klines'

        
class TIME_TEMPLATES(URL_TEMPLATES):   
    def __init__(self) -> None:
        super().__init__()
        self.break_time = {}
        self.break_time["from"] = 3
        self.break_time["to"] = 4
        self.KLINE_TIME, self.TIME_FRAME = 1, 'h'
        self.INTERVAL = str(self.KLINE_TIME) + self.TIME_FRAME

class INDICATORD_PARAMS(TIME_TEMPLATES):
    def __init__(self) -> None:
        super().__init__()
        self.b_bband_q, self.s_bband_q = 1, 1
        self.b_rsi_lev, self.s_rsi_lev = 33, 67
        self.b_rsi_diver_lev = 50 
        self.rsi_period = 14   
        self.b_macd_q, self.s_macd_q = 1, 1
        self.b_stoch_q, self.s_stoch_q = 23, 77

class FILTER_SET(INDICATORD_PARAMS):
    def __init__(self) -> None:
        super().__init__()
        self.SLICE_VOLUME_PAIRS = 150 # volums
        self.SLICE_VOLATILITY = 120 # volatility
        self.MIN_FILTER_PRICE = 0.01 # min price
        self.MAX_FILTER_PRICE = 3000000 # max price
        # self.problem_pairs = ['SOLUSDT', 'ZECUSDT', 'MKRUSDT', 'COMPUSDT', 'ORDIUSDT']
        self.problem_pairs = ['DOGEUSDT'] # problem coins list

class INIT_PARAMS(FILTER_SET):
    def __init__(self) -> None:
        super().__init__()
        self.init_itits()

    def init_itits(self):
        print('helloo')
        self.init_api_key()       
        self.init_urls()



# python -m pparamss
