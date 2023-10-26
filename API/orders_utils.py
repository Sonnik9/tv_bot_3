from API.create_order import CREATE_BINANCE_ORDER
from pparamss import my_params

class UTILS_FOR_ORDERS(CREATE_BINANCE_ORDER):

    def __init__(self) -> None:
        super().__init__()

    def cancel_order_by_id(self, symbol, last_sl_order_id):

        cancel_order = None
        all_orders = None
        success_flag = False

        all_orders = self.get_all_orders()

        for item in all_orders:
            if item["symbol"] == symbol:
                params = {}
                params["symbol"] = item["symbol"]
                params["orderId"] = last_sl_order_id
                params = self.get_signature(params)
                url = my_params.URL_PATTERN_DICT['create_order_url']
                method = 'DELETE'
                cancel_order = self.HTTP_request(url, method=method, headers=self.header, params=params)                
                break

        if cancel_order and 'status' in cancel_order and cancel_order['status'] == 'CANCELED':
            success_flag = True 
            
        return cancel_order, success_flag

# ////////////////////////////////////////////////////////////////////////////////////

    def get_all_orders(self):
        all_orders = None
        
        params = {}
        method = 'GET'       
        url = my_params.URL_PATTERN_DICT['get_all_orders_url']
        params = self.get_signature(params)
        all_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)

        return all_orders
    
    def get_open_positions(self):
        all_positions = None        
        params = {}
        method = 'GET'  
        symbol = None     
        url = my_params.URL_PATTERN_DICT['positions_url']
        if symbol:
            params["symbol"] = symbol
        params = self.get_signature(params)
        all_positions = self.HTTP_request(url, method=method, headers=self.header, params=params)

        all_positions = [x for x in all_positions if float(x["positionAmt"]) != 0]

        return all_positions 
# //////////////////////////////////////////////////////////////////////////////////
        
    def try_to_close_by_market_open_position_by_stake(self, main_stake):   
        close_pos_by_market = None            
        is_closing = -1
        target_price = None
        market_type = 'MARKET'
        good_news = []
        bad_news = []

        for item in main_stake:
            try:
                close_pos_by_market, success_flag = self.make_order(item, is_closing, target_price, market_type)
                # print(close_pos_by_market)
                
                if close_pos_by_market and 'status' in close_pos_by_market and close_pos_by_market['status'] == 'NEW':
                    good_news.append(item["symbol"])
                else:
                    bad_news.append(item["symbol"])
                    
            except Exception as ex:
                print(ex)
                bad_news.append(item["symbol"])
                continue

        return good_news, bad_news
    
    def cancel_all_orders_for_position(self, symbol_list):
        cancel_orders_list = []      

        for item in symbol_list:
            cancel_order = None
            params = {}
            params["symbol"] = item
            params = self.get_signature(params)
            url = my_params.URL_PATTERN_DICT['cancel_all_orders_url']
            method = 'DELETE'
            cancel_order = self.HTTP_request(url, method=method, headers=self.header, params=params)
            cancel_orders_list.append(cancel_order)
            # print(cancel_orders)

        return cancel_orders_list

    def close_position_confidencer(self, main_stake):

        main_stake_var = main_stake.copy()
        open_pos = None
        cancel_all_orders_answer = None
        open_pos_symbol_list = []
        try_to_closing_by_market_list = []        
        problem_to_closing_by_market_list = []

# ///////////////////////////////////////////////////////////////////////////////////////////////////

        cancel_all_orders_for_position_candidate_symbol_list = [x["symbol"] for x in main_stake_var if x["done_level"] == 6]
        _ = self.cancel_all_orders_for_position(cancel_all_orders_for_position_candidate_symbol_list)

# //////////////////////////////////////////////////////////////////////////////////////////////////

        open_pos = self.get_open_positions()   
        open_pos_symbol_list = [x["symbol"] for x in open_pos]

        for i, item in enumerate(main_stake):
            if item["done_level"] == 6:
                if item["symbol"] in open_pos_symbol_list:
                    try_to_closing_by_market_list.append(item)
                else:
                    main_stake_var[i]["close_position"] = True

        try: 
            close_by_market_symbol_list_successfuly, problem_to_closing_by_market_list = [], []   
            close_by_market_symbol_list_successfuly, problem_to_closing_by_market_list = self.try_to_close_by_market_open_position_by_stake(try_to_closing_by_market_list)
            if close_by_market_symbol_list_successfuly:           
                for i, item in enumerate(main_stake):
                    if item["done_level"] == 6:
                        if item["symbol"] in close_by_market_symbol_list_successfuly:
                            main_stake_var[i]["close_position"] = True           
            
        except Exception as ex:
            print(ex)

        return main_stake_var, problem_to_closing_by_market_list, None
    
# ///////////////////////////////////////////////////////////////////////////////////

orders_utilss = UTILS_FOR_ORDERS() 

# open_pos = orders_utilss.get_open_positions()  
# # print(pos)
# open_pos_symbol_list = [x["symbol"] for x in open_pos]
# if symbol not in open_pos_symbol_list:
#     pass
# print(open_pos_symbol_list)

# ans = orders_utilss.cancel_all_orders_for_position(['BTCUSDT'])
# print(ans)
# item = {}
# # symbol = 'ETHUSDT' 
# symbol = open_pos_symbol_list
# item["symbol"] = symbol
# item["qnt"] = 0.006
# # item["atr"] = 475
# # is_closing = -1
# # type_market = 'STOP_MARKET'
# item["defender"] = -1
# # target_price = 30000

# close_pos = orders_utilss.try_to_close_by_market_open_position_by_stake([item])
# print(close_pos)



# # python -m API.orders_utils