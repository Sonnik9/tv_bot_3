class Parameters:
    def __init__(self):
        self.URL_PATTERN_DICT= {}
        self.DIVERCIFICATION_NUMDER = 9
        self.KLINE_TIME, self.TIME_FRAME = 4, 'h'
        self.interval = str(self.KLINE_TIME) + self.TIME_FRAME
        self.MARKET = 'futures'
        # self.market = 'spot'
        if self.MARKET == 'spot':
            self.LEVERANGE = None            
        elif self.MARKET == 'futures':
            self.LEVERANGE = 1
        # self.test_flag = False # -- real
        self.TEST_FLAG = True # -- test
        self.DEPO = 25
         
        self.MAIN_STRATEGY_NUMBER = 1
        self.SL_STRATEGY_NUMBER = 2
        self.BUNCH_VARIANT = 1 
        
        self.SLICE_VOLUME_PAIRS = 100
        self.SLICE_CHANGINGPRICES_PAIRS = 80

        if not self.TEST_FLAG:
            if self.MARKET == 'spot':                
                self.URL_PATTERN_DICT['all_tikers_url'] = "https://api.binance.com/api/v3/ticker/24hr"
                self.URL_PATTERN_DICT['create_order_url'] = 'https://api.binance.com/api/v3/order' 
                self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://api.binance.com/api/v3/exchangeInfo'
                self.URL_PATTERN_DICT['balance_url'] = 'https://api.binance.com/api/v3/account'
                self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://api.binance.com/api/v3/openOrders'
                self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://api.binance.com/api/v3/allOpenOrders'

            else:
                self.URL_PATTERN_DICT['all_tikers_url'] = "https://fapi.binance.com/fapi/v1/ticker/24hr"
                self.URL_PATTERN_DICT['create_order_url'] = 'https://fapi.binance.com/fapi/v1/order' 
                self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
                self.URL_PATTERN_DICT['balance_url'] = 'https://fapi.binance.com/fapi/v1/balance'
                self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://fapi.binance.com/fapi/v1/openOrders'
                self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://fapi.binance.com/fapi/v1/allOpenOrders'
        else:
            if self.MARKET == 'spot':
                self.URL_PATTERN_DICT['all_tikers_url'] = "https://testnet.binance.com/v3/ticker/24hr"
                self.URL_PATTERN_DICT['create_order_url'] = 'https://testnet.binance.vision/api/v3/order' 
                self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://testnet.binance.vision/api/v3/exchangeInfo'
                self.URL_PATTERN_DICT['balance_url'] = 'https://testnet.binance.vision/api/v3/account'
                self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://testnet.binance.vision/api/v3/openOrders'
                self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://testnet.binance.vision/api/v3/allOpenOrders'

            else:
                self.URL_PATTERN_DICT['all_tikers_url'] = "https://testnet.binancefuture.com/fapi/v1/ticker/24hr"
                self.URL_PATTERN_DICT['create_order_url'] = 'https://testnet.binancefuture.com/fapi/v1/order'
                self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://testnet.binancefuture.com/fapi/v1/exchangeInfo'
                self.URL_PATTERN_DICT['balance_url'] = 'https://testnet.binancefuture.com/fapi/v2/balance'
                self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://testnet.binancefuture.com/fapi/v1/openOrders'
                self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://testnet.binancefuture.com/fapi/v1/allOpenOrders'
                self.URL_PATTERN_DICT['positions_url'] = 'https://testnet.binancefuture.com/fapi/v2/positionRisk'
                
my_params = Parameters()
