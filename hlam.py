
    # def calculate_profit_part(self, defender, enter_price, current_price, atr, target_point_level):
    #     profit_flag = False
    #     target_point = None

    #     if defender == 1:
    #         target_point = enter_price + (target_point_level * atr*self.tp_art_multipler)
    #         # print(f"target_poin_{target_point}")
    #         dinamic_sl = enter_price + ((target_point - enter_price)/2)
            
    #         if current_price >= target_point:
    #             target_point_level += 1
    #             if target_point_level == 3:                
    #                 profit_flag = True
    #         if (target_point_level == 2) and (current_price < target_point) and (current_price >= dinamic_sl):
    #             profit_flag = True

    #     elif defender == -1:
    #         target_point = enter_price - (target_point_level * atr*self.tp_art_multipler)
    #         # print(f"target_poin_{target_point}")
    #         dinamic_sl = enter_price - ((enter_price - target_point)/2)        

    #         if current_price <= target_point:                               
    #             target_point_level += 1
    #             if target_point_level == 3:                                      
    #                 profit_flag = True

    #         if (target_point_level == 2) and (current_price > target_point) and (current_price <= dinamic_sl):
    #             profit_flag = True

    #     return profit_flag, target_point_level



    # def sl_strategy_two(self, item, target_point_level):
    #     profit = None
    #     static_sl, profit_flag = None, False        
        
    #     defender, enter_price, current_price, atr, qnt = item["defender"], item["enter_price"], item["current_price"], item["atr"], item["qnt"]

    #     profit_flag, target_point_level = self.calculate_profit_part(defender, enter_price, current_price, atr, target_point_level)

    #     if defender == 1:
    #         static_sl = enter_price - atr * self.sl_atr_multiplier
    #         if (current_price <= static_sl) or profit_flag:
    #             profit = (current_price - enter_price) * qnt
    #             return profit, target_point_level
    #     elif defender == -1:
    #         static_sl = enter_price + atr * self.sl_atr_multiplier
    #         if (current_price >= static_sl) or profit_flag:
    #             profit = (enter_price - current_price) * qnt
    #             return profit, target_point_level

    #     return profit, target_point_level


   
    # def close_all_position(self):
    #     url = my_params.URL_PATTERN_DICT['positions_url']
    #     all_pos = None
    #     close_position = None
    #     params = {}
    #     method = 'GET'       
    #     params = self.get_signature(params)
    #     all_pos = self.HTTP_request(url, method=method, headers=self.header, params=params)

    #     for position in all_pos:
    #         order_params = {}
    #         method = 'POST'
    #         order_url = my_params.URL_PATTERN_DICT['create_order_url']
    #         if position['symbol'] == 'ATOMUSDT':
    #             print(position)
    #             # return
    #             if float(position['positionAmt']) != 0:
    #                 symbol = position['symbol']
    #                 # abs(float(position['positionAmt']))
    #                 print(abs(float(position['positionAmt'])))
    #                 order_params = {
    #                     'symbol': symbol,
    #                     'side': 'BUY',
    #                     'type': 'MARKET',
    #                     'quantity': 48.00
    #                 }
    #                 order_params = self.get_signature(order_params)
    #                 close_position = self.HTTP_request(order_url, method=method, headers=self.header, params=order_params)
    #                 print(close_position)
    #     return


                # if not first_iter_flag:                                
                #     enter_price_list = intermedeate_data_list
                #     first_iter_flag = True
                #     intermedeate_data_list = []
                #     continue

# await asyncio.sleep(5)

    # def HTTP_request(self, url, **kwargs):
    #     response = None
    #     retries = 3  
    #     retry_delay = 2  
    #     exceptionss = []

    #     for _ in range(retries):
    #         try:
    #             response = requests.request(url=url, **kwargs)
    #             excHttp = response.raise_for_status()
    #             print(excHttp)
    #             response = response.json()
    #             break
    #         except requests.exceptions.RequestException as ex:
    #             print(f"HTTP Request Error: {ex}")
    #             exceptionss.append(ex)
    #         except ValueError as ex:
    #             print(f"JSON Parsing Error: {ex}")
    #             exceptionss.append(ex)
    #         except Exception as ex:
    #             print(f"Unknown Error: {ex}")
    #             exceptionss.append(ex)

    #         if _ < retries - 1:
    #             time.sleep(retry_delay)
    #             retry_delay *= 2  

    #     return response, exceptionss

    # symbol_to_item = {item['symbol']: item for item in main_stake}    
    # done_flag = False
    # for symbol, current_price in intermediate_data_list:
    #     if symbol in symbol_to_item:
    #         symbol_to_item[symbol]['current_price'] = current_price

    # main_stake = list(symbol_to_item.values())


# import os
# import logging

# # Убедитесь, что папка "MONEY" существует
# if not os.path.exists("MONEY"):
#     os.makedirs("MONEY")

# # Установите имя файла лога
# log_file = "MONEY/stop_logic_log.log"

# # Настройка логирования
# logging.basicConfig(filename=log_file, level=logging.ERROR)
# current_file = os.path.basename(__file__)


# def calc_qnt_func(symbol, price, depo): 

#     symbol_info = None
#     symbol_data = None 
#     quantity = None
    
#     try:       
#         symbol_info = bin_data.get_excangeInfo(symbol)
#     except Exception as ex:
#         logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")   

#     if symbol_info:
#         symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)

#     if symbol_data:
#         step_size = float(symbol_data['filters'][1]['stepSize'])
#         if my_params.MARKET == 'spot':
#             min_notional = float(symbol_data['filters'][6]['minNotional'])
#         elif my_params.MARKET == 'futures':
#             min_notional = float(symbol_data['filters'][5]['notional'])

#         # price_precision = abs(int(math.log10(step_size)))
#         quantity_precision = abs(int(math.log10(1 / min_notional)))
#         decimal = depo * 0.2

#         for _ in range(5):
#             quantity = depo / price  
#             try:  
#                 quantity = round((round(quantity / step_size, quantity_precision) * step_size), quantity_precision)
#             except:
#                 pass

#             if quantity * price < min_notional:                 
#                 depo = depo + decimal  
#                 quantity = None   
#                 continue
#             else:               
#                 break

#     return quantity

# def count_multipliter_places(number):
#     if isinstance(number, (int, float)):
#         number_str = str(number)
#         if '.' in number_str:
#             return len(number_str.split('.')[1])
#     return 0


# symbol, price, depo = 'BTCUSDT', 28000, 30000000000000

# quantity, recalc_depo, price_precision = calc_qnt_func(symbol, price, depo)
# print(quantity, recalc_depo, price_precision)


# {'symbol': 'BTCUSDT', 'pair': 'BTCUSDT', 'contractType': 'PERPETUAL', 'deliveryDate': 4133404802000, 'onboardDate': 1569398400000, 'status': 'TRADING', 'maintMarginPercent': '2.5000', 'requiredMarginPercent': '5.0000', 'baseAsset': 'BTC', 'quoteAsset': 'USDT', 'marginAsset': 'USDT', 'pricePrecision': 2, 'quantityPrecision': 3, 'baseAssetPrecision': 8, 'quotePrecision': 8, 'underlyingType': 'COIN', 'underlyingSubType': [], 'settlePlan': 0, 'triggerProtect': '0.0500', 'liquidationFee': '0.020000', 'marketTakeBound': '0.30', 'maxMoveOrderLimit': 1000, 'filters': [{'maxPrice': '809484', 'minPrice': '261.10', 'tickSize': '0.10', 'filterType': 'PRICE_FILTER'}, {'minQty': '0.001', 'stepSize': '0.001', 'filterType': 'LOT_SIZE', 'maxQty': '1000'}, {'minQty': '0.001', 'maxQty': '1000', 'filterType': 'MARKET_LOT_SIZE', 'stepSize': '0.001'}, {'limit': 200, 'filterType': 'MAX_NUM_ORDERS'}, {'limit': 10, 'filterType': 'MAX_NUM_ALGO_ORDERS'}, {'filterType': 'MIN_NOTIONAL', 'notional': '5'}, {'multiplierDown': '0.5000', 'filterType': 'PERCENT_PRICE', 'multiplierUp': '1.5000', 'multipliermultipliter': '4'}], 'orderTypes': ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET'], 'timeInForce': ['GTC', 'IOC', 'FOK', 'GTX', 'GTD']}


# main_stake_var = list(filter(lambda x: x != None, main_stake_var))

        # self.sl_atr_multiplier = 1.2 #2.0 
        # self.tp_art_multipler = 0.07 



    # def open_limit_order(self, item, is_closing, target_price):

    #     response = None
    #     success_flag = False
    #     url = my_params.URL_PATTERN_DICT['create_order_url']
    #     params = {}
    #     method = 'POST'
    #     params["symbol"] = item["symbol"] 
    #     params["quantity"] = item['qnt']
    #     params["type"] = 'LIMIT'
    #     params["price"] = target_price
    #     params["timeinForce"] = 'GTC' 
         
    #     if item["defender"] == 1*is_closing:
    #         side = 'BUY'
    #     elif item["defender"] == -1*is_closing:
    #         side = "SELL" 
    #     params["side"] = side
    #     # print(item, is_closing, target_price)
    #     params = self.get_signature(params)
    #     response = self.HTTP_request(url, method=method, headers=self.header, params=params)
    #     if response and 'status' in response and response['status'] == 'NEW':
    #         success_flag = True

    #     return response, success_flag


# type_market = 'TRAILING_STOP_MARKET'
# is_closing = -1
# item["qnt"] = 0.001
# target_price = None
# item["enter_deFacto_price"] = 31276
# open_trailing_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)
# print(open_trailing_order)



# open_pos = create_orders_obj.get_open_positions(symbol)
# print(open_pos)

# answer_list = create_orders_obj.try_to_close_by_market_all_open_positions()
# print(answer_list)



# {'symbol': 'BTCUSDT', 'positionAmt': '0.001', 'entryPrice': '28050.0', 'breakEvenPrice': '28061.22', 'markPrice': '28355.00586813', 'unRealizedProfit': '0.30500586', 'liquidationPrice': '0', 'leverage': '1', 'maxNotionalValue': '5.0E8', 'marginType': 'cross', 'isolatedMargin': '0.00000000', 'isAutoAddMargin': 'false', 'positionSide': 'BOTH', 'notional': '28.35500586', 'isolatedWallet': '0', 'updateTime': 1697469250488, 'isolated': False, 'adlQuantile': 1}



# all_orders = None 
# make_order = None 
# item = {}
# symbol = 'BTCUSDT'
# item["symbol"] = 'BTCUSDT'
# item["qnt"] = 0.001
# is_closing = 1
# type_market = 'MARKET'
# item["defender"] = 1
# target_price = None

# make_order = create_orders_obj.make_order(item, is_closing, type_market, target_price)
# print(make_order)
# url = None
# symbol_info = bin_data.get_excangeInfo(item["symbol"])

# symbol_data = None
# if symbol_info:
#     symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)

# print(symbol_data)

# position_price = None

# position_price = bin_data.get_position_price(symbol)

# print(position_price)




# is_closing = -1
# target_price = make_order["price"] * 500 * 0.9
# type_market = 'LIMIT'
# make_order = create_orders_obj.make_order(item, is_closing, type_market, target_price)
# print(make_order)

# is_closing = -1
# target_price = make_order["price"] * 500 * 1.2
# type_market = 'LIMIT'
# make_order = create_orders_obj.make_order(item, is_closing, type_market, target_price)
# print(make_order)

# target_price = 26500
# item["defender"] = 1
# make_order = create_orders_obj.make_order(item, is_closing, type_market, target_price)
# print(make_order)

# time.sleep(5)

# all_orders = create_orders_obj.get_all_orders()
# print(all_orders)

# item["last_sl_order_id"] = '3486091588'
# cancel_orders = None 
# cancel_orders = create_orders_obj.cancel_order_by_id(item["symbol"], item["last_sl_order_id"])
# print(cancel_orders)


# resp = None
# resp = create_orders_obj.close_all_position()
# print(resp)

# python -m API.create_order

# {'orderId': 3486091588, 'symbol': 'BTCUSDT', 'status': 'CANCELED', 'clientOrderId': '6TNC4fs0Xzmp1Dth3o7lLh', 'price': '30500.00', 'avgPrice': '0.00', 'origQty': '0.001', 'executedQty': '0.000', 'cumQty': '0.000', 'cumQuote': '0.00000', 'timeInForce': 'GTC', 'type': 'LIMIT', 'reduceOnly': False, 'closePosition': False, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '0.00', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'LIMIT', 'priceMatch': 'NONE', 'selfTradePreventionMode': 'NONE', 'goodTillDate': 0, 'updateTime': 1697468019394}


        # ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET']
        # print(item)

        # try: 
        #     close_by_market_symbol_list, dont_close_by_market_symbol_list = [], []   
        #     close_by_market_symbol_list, dont_close_by_market_symbol_list = self.try_to_close_by_market_open_position_by_item(try_to_close_by_market_list)
        #     if close_by_market_symbol_list:           
        #         for i, item in enumerate(main_stake):
        #             if item["done_level"] == 6:
        #                 if item["symbol"] in close_by_market_symbol_list:
        #                     main_stake_var[i]["close_position"] = True           
            
        #     symbol_list_to_cancel_orders = [x["symbol"] for x in main_stake_var if x["close_position"]]
        #     cancel_all_orders_answer = self.cancel_all_orders_for_position(symbol_list_to_cancel_orders)
        # except Exception as ex:
        #     print(ex) 



















    # def try_to_close_by_market_all_open_positions(self, main_stake):
    #     all_positions = None        
    #     close_pos_by_market = None        
    #     close_pos_by_market_answer_list = []      
    #     is_closing = -1
    #     target_price = None
    #     type_market = 'MARKET'
    #     symbol = None
    #     all_symbols = []
    #     try:
    #         all_positions = self.get_open_positions(symbol)  
    #     except Exception as ex:
    #         print(ex)

    #     all_symbols = [x["symbol"] for x in all_positions]
    #     main_stakee = [x for x in main_stake if x["symbol"] in all_symbols]

    #     for item in main_stakee:
    #         try:
    #             close_pos_by_market = self.make_order(item, is_closing, type_market, target_price)
    #             close_pos_by_market_answer_list.append(close_pos_by_market)
    #         except Exception as ex:
    #             print(ex)
    #             close_pos_by_market_answer_list.append(ex)
    #             continue

    #     return close_pos_by_market_answer_list

                # main_stake = [{'symbol': 'ETHUSDT', 'defender': 1, 'enter_deFacto_price': None, 'recalc_depo': None, 'current_price': None, 'close_position': False, 'qnt': None, 'price_precision': None, 'tick_size': None, 'atr_aprox': 94.46000000000004, 'atr': 75.36071428571431, 'rra': 301.10690804, 'last_sl_order_id': None, 'static_tp_price': None, 'static_sl_price': None, 'checkpointt_flag': False, 'checkpointt': None, 'breakpointt': None, 'done_level': 0,}]

                # firstt = True
                # if main_stake: 
                #     main_stake, problem_to_closing_by_market_list, _ = orders_utilss.close_position_confidencer(main_stake)

    # print(top_coins)
    # top_coins = [x.replace('USDT', '') for x in top_coins]
    # print(top_coins)
    # finish_time = time.time() - start_time    
    # print(f"Общее время поиска:  {math.ceil(finish_time)} сек")

    # def limit_order_pattern(self, itemm, success_flag = False):
    #     item = itemm.copy()
    #     try:
    #         if item["last_sl_order_id"]:                                        
    #             cancel_order, success_flag = orders_utilss.cancel_order_by_id(item["symbol"], item["last_sl_order_id"])
    #             # print(f"str175: {cancel_order}")
    #         if success_flag:
    #             print('The canceled last order was Successully') 
                
    #         else:
    #             print('The canceled last order was unsuccessully')                            
    #     except Exception as ex:
    #         logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}\n {cancel_order}") 
    #     try:
    #         is_closing = -1
    #         success_flag = False   
    #         target_price = item["breakpointt"]
    #         market_type = 'LIMIT'                                 
    #         open_dinamic_sl_order, success_flag = create_orders_obj.make_order(item, is_closing, target_price, market_type)
    #         # print(f'open_static_sl_order  {open_static_sl_order}')

    #         if success_flag:
    #             item["checkpointt_flag"] = False                
    #             self.trailing_sl_levels.pop(0) 
    #             item["last_sl_order_id"] = open_dinamic_sl_order["orderId"] 
    #             item["checkpointt"], item["breakpointt"] = None, None 
    
    #     except Exception as ex:
    #         logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

    #     return item

            # print(f"symbol  {symbol}")    
            # print(f'itemm["tick_size"] {itemm["tick_size"]}
            # # print(f"current_price  {current_price}")')  
            # print(f"price_precision  {price_precision}")
            # print(f"defender  {defender}")
            # print(f'last_sl_order_id {itemm["last_sl_order_id"]}')
            # print(f"enter_deFacto_price  {enter_deFacto_price}")
            # print(f"static_sl_price  {static_sl_price}")
            # print(f"static_tp_price  {static_tp_price}")
            # print(f"atr  {atr}")


# from API.post_api import CREATE_BINANCE_ORDER
# from pparamss import my_params


# class OTHERS_FOR_ORDERS(CREATE_BINANCE_ORDER):

#     def __init__(self) -> None:
#         super().__init__()


#     def try_to_close_by_market_all_open_positions(self, main_stake):
#         all_positions = None        
#         close_pos_by_market = None        
#         close_pos_by_market_answer_list = []      
#         is_closing = -1
#         target_price = None
#         type_market = 'MARKET'
#         symbol = None
#         all_symbols = []
#         try:
#             all_positions = self.get_open_positions(symbol)  
#         except Exception as ex:
#             print(ex)

#         all_symbols = [x["symbol"] for x in all_positions]
#         main_stakee = [x for x in main_stake if x["symbol"] in all_symbols]

#         for item in main_stakee:
#             try:
#                 close_pos_by_market = self.make_order(item, is_closing, type_market, target_price)
#                 close_pos_by_market_answer_list.append(close_pos_by_market)
#             except Exception as ex:
#                 print(ex)
#                 close_pos_by_market_answer_list.append(ex)
#                 continue

#         return close_pos_by_market_answer_list
    
#     def cancel_all_open_orders(self):
#         cancel_orders = None
#         all_orders = None

#         all_orders = self.get_all_orders()

#         for item in all_orders:
#             params = {}
#             params["symbol"] = item["symbol"]
#             params = self.get_signature(params)
#             url = my_params.URL_PATTERN_DICT['cancel_all_orders_url']
#             method = 'DELETE'
#             cancel_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)
#             print(cancel_orders)

#         return 


#     def close_position_confidencer(self, main_stake):

#         main_stake_var = main_stake.copy()
#         open_pos = None
#         cancel_all_orders_answer = None
#         open_pos_symbol_list = []
#         try_to_closing_by_market_list = []        
#         problem_to_closing_by_market_list = []

# # ///////////////////////////////////////////////////////////////////////////////////////////////////

#         cancel_all_orders_for_position_candidate_symbol_list = [x["symbol"] for x in main_stake_var if x["done_level"] == 6]
#         cancel_all_orders_answer = self.cancel_all_orders_for_position(cancel_all_orders_for_position_candidate_symbol_list)
#         print(cancel_all_orders_answer)
# # //////////////////////////////////////////////////////////////////////////////////////////////////

#         open_pos = self.get_open_positions()   
#         open_pos_symbol_list = [x["symbol"] for x in open_pos]

#         for i, item in enumerate(main_stake):
#             if item["done_level"] == 6:
#                 if item["symbol"] in open_pos_symbol_list:
#                     try_to_closing_by_market_list.append(item)
#                 else:
#                     main_stake_var[i]["close_position"] = True

#         try: 
#             close_by_market_symbol_list_successfuly, problem_to_closing_by_market_list = [], []   
#             close_by_market_symbol_list_successfuly, problem_to_closing_by_market_list = self.try_to_close_by_market_open_position_by_stake(try_to_closing_by_market_list)
#             if close_by_market_symbol_list_successfuly:           
#                 for i, item in enumerate(main_stake):
#                     if item["done_level"] == 6:
#                         if item["symbol"] in close_by_market_symbol_list_successfuly:
#                             main_stake_var[i]["close_position"] = True           
            
#         except Exception as ex:
#             print(ex)

#         return main_stake_var, problem_to_closing_by_market_list, None



# make_order = None 
# item = {}
# symbol = 'BTCUSDT'
# item["symbol"] = 'BTCUSDT'
# item["qnt"] = 0.001
# item["atr"] = 475
# is_closing = 1
# type_market = 'MARKET'
# item["defender"] = 1
# target_price = None
# open_market_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)

# symbol = 'BTCUSDT'
# item["symbol"] = 'BTCUSDT'
# item["qnt"] = 0.001
# item["atr"] = 475
# is_closing = -1
# type_market = 'STOP_MARKET'
# item["defender"] = 1
# target_price = 30000
# open_market_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)

# symbol = 'BTCUSDT'
# item["symbol"] = 'BTCUSDT'
# item["qnt"] = 0.001
# item["atr"] = 475
# is_closing = -1
# type_market = 'TAKE_PROFIT_MARKET'
# item["defender"] = 1
# target_price = 40000
# open_market_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)

# print(open_market_order)

# symbol = 'ETHUSDT'
# item["symbol"] = 'ETHUSDT'
# item["qnt"] = 0.003
# item["atr"] = 475
# is_closing = 1
# type_market = 'LIMIT'
# item["defender"] = 1
# target_price = 1800
# open_market_order = create_orders_obj.make_order(item, is_closing, target_price, type_market)

# print(open_market_order)

# symbol_list_to_cancel_orders = ['BTCUSDT']
# cancel_all_orders_answer = create_orders_obj.cancel_all_orders_for_position(symbol_list_to_cancel_orders)


# python -m API.create_order

        
        # if market_type == 'MARKET' or market_type == 'LIMIT' or market_type == 'TAKE_PROFIT_MARKET':
   


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

# def terminate_all_func(main_stake):

#     main_stake_var = main_stake.copy()
#     open_pos = None
#     cancel_all_orders_answer = None
#     open_pos_symbol_list = []
#     try_to_closing_by_market_list = []        
#     problem_to_closing_by_market_list = []

# # ///////////////////////////////////////////////////////////////////////////////////////////////////

#     cancel_all_orders_for_position_candidate_symbol_list = [x["symbol"] for x in main_stake_var]
#     cancel_all_orders_answer = delete_apii.cancel_all_orders_for_position(cancel_all_orders_for_position_candidate_symbol_list)
#     print(cancel_all_orders_answer)
# # //////////////////////////////////////////////////////////////////////////////////////////////////

#     open_pos = get_apii.get_open_positions()   
#     open_pos_symbol_list = [x["symbol"] for x in open_pos]

#     for i, item in enumerate(main_stake):
#         if item["done_level"] == 6:
#             if item["symbol"] in open_pos_symbol_list:
#                 try_to_closing_by_market_list.append(item)
#             else:
#                 main_stake_var[i]["close_position"] = True

#     try: 
#         close_by_market_symbol_list_successfuly, problem_to_closing_by_market_list = [], []   
#         close_by_market_symbol_list_successfuly, problem_to_closing_by_market_list = utils_apii.try_to_close_by_market_open_position_by_stake(try_to_closing_by_market_list)
#         if close_by_market_symbol_list_successfuly:           
#             for i, item in enumerate(main_stake):
#                 if item["done_level"] == 6:
#                     if item["symbol"] in close_by_market_symbol_list_successfuly:
#                         main_stake_var[i]["close_position"] = True           
        
#     except Exception as ex:
#         print(ex)

#     return main_stake_var, problem_to_closing_by_market_list, None

   


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



# symbol = 'LTCUSDT'
# price = 33500
# depo = 66
# quantity, recalc_depo, price_precision, tick_size = calc_qnt_func(symbol, price, depo)

# print(quantity, recalc_depo, price_precision, tick_size) 

# {'symbol': 'BTCUSDT', 'pair': 'BTCUSDT', 'contractType': 'PERPETUAL', 'deliveryDate': 4133404802000, 'onboardDate': 1569398400000, 'status': 'TRADING', 'maintMarginPercent': '2.5000', 'requiredMarginPercent': '5.0000', 'baseAsset': 'BTC', 'quoteAsset': 'USDT', 'marginAsset': 'USDT', 'pricePrecision': 2, 'quantityPrecision': 3, 'baseAssetPrecision': 8, 'quotePrecision': 8, 'underlyingType': 'COIN', 'underlyingSubType': [], 'settlePlan': 0, 'triggerProtect': '0.0500', 'liquidationFee': '0.020000', 'marketTakeBound': '0.30', 'maxMoveOrderLimit': 1000, 'filters': [{'maxPrice': '809484', 'minPrice': '261.10', 'tickSize': '0.10', 'filterType': 'PRICE_FILTER'}, {'minQty': '0.001', 'stepSize': '0.001', 'filterType': 'LOT_SIZE', 'maxQty': '1000'}, {'minQty': '0.001', 'maxQty': '1000', 'filterType': 'MARKET_LOT_SIZE', 'stepSize': '0.001'}, {'limit': 200, 'filterType': 'MAX_NUM_ORDERS'}, {'limit': 10, 'filterType': 'MAX_NUM_ALGO_ORDERS'}, {'filterType': 'MIN_NOTIONAL', 'notional': '5'}, {'multiplierDown': '0.5000', 'filterType': 'PERCENT_PRICE', 'multiplierUp': '1.5000', 'multipliermultipliter': '4'}], 'orderTypes': ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET'], 'timeInForce': ['GTC', 'IOC', 'FOK', 'GTX', 'GTD']}

# from binance.client import Client

# # Replace with your Binance API key and secret
# BINANCE_API_PUBLIC_KEY_FUTURES_TEST = "96f214ce691b0dd8fc65b23002ee4e5ce0b55684598645c2eb2d0a819a6d387a" # test
# BINANCE_API_PRIVATE_KEY_FUTURES_TEST = "46e1372c84151cd7d486a4734cc21023ba1724d067b5967ce48ce769025cf0d2" # test

# api_key = "96f214ce691b0dd8fc65b23002ee4e5ce0b55684598645c2eb2d0a819a6d387a"
# api_secret = "46e1372c84151cd7d486a4734cc21023ba1724d067b5967ce48ce769025cf0d2"

# # Initialize the Binance client
# client = Client(api_key, api_secret, testnet=True)

# # Define the order parameters
# symbol = 'BTCUSDT'  # The trading pair symbol
# quantity = 0.001   
#    # The quantity to buy or sell
# atr = 475
# enter_price = 31000 
# callback_rate = 1.0 # The callback rate for the trailing stop (1.0% in this example)
# callback_rate =  round((int(atr/1.618) * 100)/enter_price, 1)
# precessionPrice = 2
# stopPrice = round(enter_price - (atr * 1.618), precessionPrice)
# # print(stopPrice)

# # print(callback_rate)

# # Create a MARKET order
# order = client.create_order(
#     symbol=symbol,
#     side= 'BUY',  # Replace with BUY if you want to buy
#     type='MARKET',
#     quantity=quantity,

# )

# print(order)
# import time
# # Create a TRAILING_STOP_MARKET order
# time.sleep(2)
# order = client.create_order(
#     symbol=symbol,
#     side= 'SELL',  # Replace with BUY if you want to buy
#     type='TRAILING_STOP_MARKET',
#     quantity=quantity,
# #     activationPrice=None,  # Optional: The activation price
# #     stopPrice= stopPrice,        # Optional: The initial stop price
# #     callbackRate=callback_rate
# # )

# # print(order)

# def count_multipliter_places(number):
#     if isinstance(number, (int, float)):
#         number_str = str(number)
#         if '.' in number_str:
#             return len(number_str.split('.')[1])
#     return 0

# # a = 1.2378347683478
# # b = 0.1 
# # q = count_multipliter_places(b)

# # c = round(a,q)
# # print(c)

# from decimal import Decimal, ROUND_HALF_UP
# import math

# tick_size = 0.001
# d = 5.12656748759348593457893048573048573048957
# r = 5.12656748759348593457893048573048573048957
# c = 5.12656748759348593457893048573048573048957
# f = 5.12656748759348593457893048573048573048957
# value = Decimal(str(d))
# rounded_value = value.quantize(Decimal(str(tick_size)), rounding=ROUND_HALF_UP)
# print(f"decimal:  {rounded_value}")
# # //////////////////////////////////////////////////
# tick_size = count_multipliter_places(tick_size) 
# r = round(r, tick_size)
# print(f"round:  {r}")
# # //////////////////////////////////////////////////
# c = math.ceil(c * 10 ** tick_size) / (10 ** tick_size)
# print(f"ceil:  {c}")
# print(f"tick_size:  {tick_size}")

# f = math.floor(f * 10 ** tick_size) / (10 ** tick_size)
# print(f"floor:  {f}")
# print(f"tick_size:  {tick_size}")
# def checkpoint_calc(enter_deFacto_price, atr, q_sl, q_tp, defender, price_precision, static_defender, rounding_type='round'):

#     checkpointt, breakpointt = None, None
#     try:
#         if rounding_type == 'round':
#             checkpointt = round(enter_deFacto_price + (defender * atr * q_tp), price_precision)
#         elif rounding_type == 'ceil':
#             checkpointt = math.ceil((enter_deFacto_price + (defender * atr * q_tp)) * 10 ** price_precision) / (10 ** price_precision)
#         elif rounding_type == 'floor':
#             checkpointt = math.floor((enter_deFacto_price + (defender * atr * q_tp)) * 10 ** price_precision) / (10 ** price_precision)

#     except Exception as ex:
#         logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
#     try:
#         if rounding_type == 'round':
#             breakpointt = round(enter_deFacto_price + (static_defender * defender * atr * q_sl), price_precision)
#         elif rounding_type == 'ceil':
#             breakpointt = math.ceil((enter_deFacto_price + (static_defender * defender * atr * q_sl)) * 10 ** price_precision) / (10 ** price_precision)
#         elif rounding_type == 'floor':
#             breakpointt = math.floor((enter_deFacto_price + (static_defender * defender * atr * q_sl)) * 10 ** price_precision) / (10 ** price_precision)
#     except Exception as ex:
#         logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

#     return checkpointt, breakpointt 

