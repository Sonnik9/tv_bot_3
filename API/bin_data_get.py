from API.config import Configg
from pparamss import my_params
import pandas as pd

class GET_BINANCE_DATA(Configg):

    def __init__(self) -> None:
        super().__init__()   

    def get_all_tickers(self):
        all_tickers = None
        url = my_params.URL_PATTERN_DICT['all_tikers_url']
        method = 'GET'
        all_tickers = self.HTTP_request(url, method=method, headers=self.header)
        return all_tickers
    
    def get_excangeInfo(self, symbol):
        exchangeInfo = None
        if symbol:            
            url = f"{my_params.URL_PATTERN_DICT['exchangeInfo_url']}?symbol={symbol}"
        else:
            url = my_params.URL_PATTERN_DICT['exchangeInfo_url']

        method = 'GET'
        exchangeInfo = self.HTTP_request(url, method=method, headers=self.header)
        return exchangeInfo
    
    def get_balance(self):
        current_balance = None
        method = 'GET'
        url = my_params.URL_PATTERN_DICT['balance_url']
        params = {}
        params = self.get_signature(params)
        current_balance = self.HTTP_request(url, method=method, headers=self.header, params=params)
        current_balance = float([x['balance'] for x in current_balance if x['asset'] == 'USDT'][0])
        return current_balance
    
    def get_position_price(self, symbol):
        positions = None
        method = 'GET'
        url = my_params.URL_PATTERN_DICT['positions_url']
        params = {}
        params = self.get_signature(params)
        positions = self.HTTP_request(url, method=method, headers=self.header, params=params)
        # print(positions)
        positions = float([x for x in positions if x['symbol'] == symbol][0]["entryPrice"])
        return positions

    def get_top_pairs(self):
        all_tickers = []
        top_pairs = []
        sorted_by_volume_data = []
        sorted_by_changing_price_data = []

        all_tickers = self.get_all_tickers()

        if all_tickers:            
            # print(len(all_tickers))
            # print(all_tickers[0]['lastPrice'])
            usdt_filtered = [ticker for ticker in all_tickers if ticker['symbol'].upper().endswith('USDT') and 'UP' not in ticker['symbol'].upper() and 'DOWN' not in ticker['symbol'].upper() and 'RUB' not in ticker['symbol'].upper() and 'EUR' not in ticker['symbol'].upper() and float(ticker['lastPrice']) >= my_params.FILTER_PRICE]
            
            sorted_by_volume_data = sorted(usdt_filtered, key=lambda x: float(x['quoteVolume']), reverse=True)

            sorted_by_volume_data = sorted_by_volume_data[:my_params.SLICE_VOLUME_PAIRS]

            sorted_by_changing_price_data = sorted(sorted_by_volume_data, key=lambda x: float(x['priceChangePercent']), reverse=True)
    
            sorted_by_changing_price_data = sorted_by_changing_price_data[:my_params.SLICE_CHANGINGPRICES_PAIRS]

            top_pairs = [coins['symbol'] for coins in sorted_by_changing_price_data]

        return top_pairs
    
    def get_klines(self, symbol):
        klines = None
        url = my_params.URL_PATTERN_DICT["klines_url"]
        method = 'GET'
        params = {}
        params["symbol"] = symbol
        params["interval"] = my_params.INTERVAL
        params["limit"] = 16
        params = self.get_signature(params)
        klines = self.HTTP_request(url, method=method, headers=self.header, params=params)
        if klines:
            data = pd.DataFrame(klines).iloc[:, :6]
            data.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            data = data.set_index('Time')
            data.index = pd.to_datetime(data.index, unit='ms')
            data = data.astype(float)
        
        return data

    
# python -m API.bin_data_get
   
bin_data = GET_BINANCE_DATA()

# klines = None 
# klines = bin_data.get_klines()
# print(klines)



# symbol = 'BTCUSDT'
# s = bin_data.get_position_price(symbol)
# print(s)

# all_tickers = None 
# # all_tickers = bin_data.get_excangeInfo()
# all_tickers = bin_data.get_balance()
# print(all_tickers)


# if "symbols" in all_tickers:
#     symbols = all_tickers["symbols"]
#     for symbol_data in symbols:
#         # Вы можете здесь обрабатывать информацию о символе
#         print("Информация о символе:", symbol_data)
# else:
#     print("Данные о символах ('symbols') отсутствуют в ответе.")


# print(all_tickers)
