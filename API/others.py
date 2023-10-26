from API.create_order import CREATE_BINANCE_ORDER
from pparamss import my_params


class OTHERS_FOR_ORDERS(CREATE_BINANCE_ORDER):

    def __init__(self) -> None:
        super().__init__()


    def try_to_close_by_market_all_open_positions(self, main_stake):
        all_positions = None        
        close_pos_by_market = None        
        close_pos_by_market_answer_list = []      
        is_closing = -1
        target_price = None
        type_market = 'MARKET'
        symbol = None
        all_symbols = []
        try:
            all_positions = self.get_open_positions(symbol)  
        except Exception as ex:
            print(ex)

        all_symbols = [x["symbol"] for x in all_positions]
        main_stakee = [x for x in main_stake if x["symbol"] in all_symbols]

        for item in main_stakee:
            try:
                close_pos_by_market = self.make_order(item, is_closing, type_market, target_price)
                close_pos_by_market_answer_list.append(close_pos_by_market)
            except Exception as ex:
                print(ex)
                close_pos_by_market_answer_list.append(ex)
                continue

        return close_pos_by_market_answer_list
    
    def cancel_all_open_orders(self):
        cancel_orders = None
        all_orders = None

        all_orders = self.get_all_orders()

        for item in all_orders:
            params = {}
            params["symbol"] = item["symbol"]
            params = self.get_signature(params)
            url = my_params.URL_PATTERN_DICT['cancel_all_orders_url']
            method = 'DELETE'
            cancel_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)
            print(cancel_orders)

        return 