class Parameters:
    def __init__(self):
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!'
        fibonacci_levels = [0, 0.236, 0.382, 0.50, 0.618, 1, 1.618, 2.618, 4.236]
        self.URL_PATTERN_DICT= {}
        self.DIVERCIFICATION_NUMDER = 5
        self.KLINE_TIME, self.TIME_FRAME = 4, 'h'
        self.INTERVAL = str(self.KLINE_TIME) + self.TIME_FRAME
        self.MARKET = 'futures'
        # self.market = 'spot'
        # self.test_flag = False # -- real
        self.TEST_FLAG = True # -- test
        self.DEPO = 25
        self.LEVERAGE = 1
        self.SLIPPAGE_COEFFICIENT = 0.005  # Коэффициент погрешности 0.5%         
        self.MAIN_STRATEGY_NUMBER = 1
        self.BUNCH_VARIANT = 1
        # self.SL_STRATEGY_NUMBER = 2

        self.SL_TABULA_NUMBER = 3
        self.SL_TABULA_LIST = [
            self.SOLI_DEO_GLORIA,            
            [[fibonacci_levels[4], fibonacci_levels[6]], [[fibonacci_levels[1] * 0.5,fibonacci_levels[1]], [fibonacci_levels[2] * 0.5, fibonacci_levels[2]], [fibonacci_levels[3] * 0.5, fibonacci_levels[3]], [fibonacci_levels[4] * 0.5, fibonacci_levels[4]], [fibonacci_levels[5] * 0.5, fibonacci_levels[5]]]],
            [[0.9, 1.2], [[0.2, 0.4], [0.3, 0.6], [0.45, 0.9], [0.55, 1.11]]],
            [[2.36, 1.618], [[0.45, 0.7], [0.9, 1.2]]]
        ]
        
        self.SLICE_VOLUME_PAIRS = 10
        self.SLICE_CHANGINGPRICES_PAIRS = 10
        self.FILTER_PRICE = 0.1

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
                self.URL_PATTERN_DICT["set_leverage_url"] = 'https://testnet.binancefuture.com/fapi/v1/leverage'
                self.URL_PATTERN_DICT["klines_url"] = 'https://testnet.binancefuture.com/fapi/v1/klines'
                
my_params = Parameters()

# print[my_params.sl_tabula_list]
# print[my_params.SL_TABULA_LIST[my_params.SL_TABULA_NUMBER][1][0][1]]




# itemm = tabula.pop[0]
# print(my_params.STATIC_SL)
# print(my_params.STATIC_TP)
# python -m pparamss
