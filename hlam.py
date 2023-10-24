
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