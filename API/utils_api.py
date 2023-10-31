from pparamss import my_params
from API.get_api import get_apii
from API.post_api import post_apii

class UTILS_FOR_ORDERS():

    def __init__(self) -> None:
        pass

    def try_to_close_by_market_open_position_by_stake(self, main_stake):

        close_pos_by_market = None            
        is_closing = -1
        target_price = None
        market_type = 'MARKET'
        succes_closed_symbol_list = []
        dont_closed_symbol_list = []

        for item in main_stake:
            success_flag = False
            try:
                _, success_flag = post_apii.make_order(item, is_closing, target_price, market_type)
                
                if success_flag:
                    succes_closed_symbol_list.append(item["symbol"])
                else:
                    dont_closed_symbol_list.append(item["symbol"])
                    
            except Exception as ex:
                # print(ex)
                dont_closed_symbol_list.append(item["symbol"])
                continue

        return succes_closed_symbol_list, dont_closed_symbol_list
    
    def try_to_close_by_market_all_open_positions(self, main_stake):

        all_positions = None   
        succes_closed_symbol_list = []     
        dont_closed_symbol_list = []    
        is_closing = -1
        target_price = None
        market_type = 'MARKET'
        all_openPos_symbols = []

        try:
            all_positions = get_apii.get_open_positions()  
        except Exception as ex:
            print(ex)

        all_openPos_symbols = [x["symbol"] for x in all_positions]  
        # print(all_openPos_symbols)     

        for item in main_stake:
            success_flag = False 
            # print(item)
            if item["symbol"] in all_openPos_symbols:
                try:
                    _, success_flag = post_apii.make_order(item, is_closing, target_price, market_type)
                    if success_flag:
                        succes_closed_symbol_list.append(item["symbol"])
                    else:
                        dont_closed_symbol_list.append(item["symbol"])                
                except Exception as ex:
                    # print(ex)
                    dont_closed_symbol_list.append(item["symbol"])
                    # close_pos_by_market_answer_list.append(ex)
                    continue

        return succes_closed_symbol_list, dont_closed_symbol_list

# ///////////////////////////////////////////////////////////////////////////////////////
        
    def assets_filters(self):
        # print('bkhsdv')
        all_tickers = []
        top_pairs = []
        sorted_by_volume_data = []
        sorted_by_changing_price_data = []

        all_tickers = get_apii.get_all_tickers()
        # print(all_tickers)

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
    
# ///////////////////////////////////////////////////////////////////////////////////

utils_apii = UTILS_FOR_ORDERS() 

# # python -m API.orders_utils