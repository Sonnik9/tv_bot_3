
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