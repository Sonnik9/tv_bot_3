from pparamss import my_params
from API.create_order import create_orders_obj
from API.orders_utils import orders_utilss
from API.bin_data_get import bin_data
from UTILS.calc_qnt import calc_qnt_func, checkpoint_calc


import logging
import os
import inspect

logging.basicConfig(filename='MONEY/stop_logic_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

class SL_STRATEGYY():
    def __init__(self) -> None:  
        self.trailing_sl_levels = my_params.TABULA_SL_TP_POINTS
        self.statik_sl = my_params.STATIC_SL_Q
        self.statik_tp = my_params.STATIC_TP_Q       

    def usual_orders_assambler(self, main_stake, step):

        main_stake_var = main_stake.copy()
        # print(f"len(main_stake_var)  {len(main_stake_var)}")

        for i, _ in enumerate(main_stake): 
            symbol = main_stake_var[i]["symbol"]             

            if step == 0:
                # print(f"step   {step}")
                try:
                    lev = create_orders_obj.set_leverage(symbol)                    
                except Exception as ex:
                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
                if lev and 'leverage' in lev and lev['leverage'] == my_params.LEVERAGE:
                    main_stake_var[i]["done_level"] = 1

            if step ==1:
                enter_deJure_price = main_stake_var[i]["current_price"]
                try:                    
                    main_stake_var[i]['qnt'], main_stake_var[i]["recalc_depo"],main_stake_var[i]["price_precision"], main_stake_var[i]["tick_size"] = calc_qnt_func(symbol, enter_deJure_price, my_params.DEPO)
                    # qnt = round(qnt, price_precision) 
                except Exception as ex:
                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

                if main_stake_var[i]['qnt']: 
                    main_stake_var[i]["done_level"] = 2

            if step == 2:
                is_closing = 1
                success_flag = False
                market_type = 'MARKET'
                target_price = None
                try:          
                    open_market_order, success_flag = create_orders_obj.make_order(main_stake_var[i], is_closing, target_price, market_type)
                    # print(f"str74:  {open_market_order}") 
                except Exception as ex:
                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex} \n {open_market_order}")
                if success_flag:
                    main_stake_var[i]["done_level"] = 3
                    try:
                        main_stake_var[i]["enter_deFacto_price"] = bin_data.get_position_price(symbol)
                        # print(f'str73 {symbol}:  {main_stake_var[i]["enter_deFacto_price"]}  (defacto_prtice)')
                        success_flag = False
                    except Exception as ex:
                        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            if step == 3:
              
                try:  
                    static_defender = -1
                    # print(main_stake_var[i]["enter_deFacto_price"], main_stake_var[i]["atr"], self.STATIC_SL_Q, self.STATIC_TP_Q, main_stake_var[i]["defender"])
                    main_stake_var[i]["static_tp_price"], main_stake_var[i]["static_sl_price"] = checkpoint_calc(main_stake_var[i]["enter_deFacto_price"], main_stake_var[i]["atr"], self.statik_sl, self.statik_tp, main_stake_var[i]["defender"],main_stake_var[i]["price_precision"], static_defender, main_stake_var[i]["tick_size"]) 

                    # print(f'str 73: static_tp_price:  {main_stake_var[i]["static_tp_price"]}, static_sl_price:  {main_stake_var[i]["static_sl_price"]}')

                except Exception as ex:
                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                
                try:  
                    # sl static order  
                    is_closing = -1
                    success_flag = False   
                    target_price = main_stake_var[i]["static_sl_price"]
                    market_type = 'STOP_MARKET'                                 
                    open_static_sl_order, success_flag = create_orders_obj.make_order(main_stake_var[i], is_closing, target_price, market_type)
                    # print(f'open_static_sl_order  {open_static_sl_order}')
                    if success_flag:                                                
                        main_stake_var[i]["done_level"] = 4   
                        success_flag = False    
                              
                except Exception as ex:
                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex} \n {open_static_sl_order}") 
                
                try: 
                    # tp static order 
                    is_closing = -1
                    success_flag = False   
                    target_price = main_stake_var[i]["static_tp_price"]
                    market_type = 'TAKE_PROFIT_MARKET' 
                    if main_stake_var[i]["done_level"] == 4: 
                        open_static_tp_order, success_flag = create_orders_obj.make_order(main_stake_var[i], is_closing, target_price, market_type)     

                        # print(f'open_static_tp_order  {open_static_tp_order}')
                        if success_flag:                        
                            main_stake_var[i]["done_level"] = 5 
                            success_flag = False   
                
                except Exception as ex:
                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}\n {open_static_tp_order}")  

        if step == 0:
            main_stake_var = [x for x in main_stake_var if x["done_level"] == 1]
            step = 1
            return main_stake_var, step
        if step == 1:
            main_stake_var = [x for x in main_stake_var if x["done_level"] == 2]
            step = 2
            return main_stake_var, step
        if step == 2:
            main_stake_var = [x for x in main_stake_var if x["done_level"] == 3]
            # main_stake_var = list(filter(lambda x: x != None, main_stake_var))
            # print(f"chenging_len(main_stake_var)  {len(main_stake_var)}")
            if my_params.SL_STRATEGY_NUMBER != 1:
                step = 3
            else:
                step = 4
            return main_stake_var, step
        if my_params.SL_STRATEGY_NUMBER != 1:
            if step == 3:
                main_stake_var = [x for x in main_stake_var if x["done_level"] == 5]
                step = 4
                return main_stake_var, step     

    def trailling_sl_controller(self, main_stake, step):

        # print(f"len_main_stake  {len(main_stake)}")    
        done_flag = False
        main_stake_var = main_stake.copy()       
        
        for i, _ in enumerate(main_stake): 

            symbol = main_stake_var[i]["symbol"]         
            current_price = main_stake_var[i]["current_price"]           
            price_precision = main_stake_var[i]["price_precision"]            
            defender = main_stake_var[i]["defender"]
            enter_deFacto_price = main_stake_var[i]["enter_deFacto_price"]            
            static_sl_price = main_stake_var[i]["static_sl_price"]            
            static_tp_price = main_stake_var[i]["static_tp_price"]
            atr = main_stake_var[i]["atr"]
            # print(f"symbol  {symbol}")    
            # print(f'main_stake_var[i]["tick_size"] {main_stake_var[i]["tick_size"]}
            # # print(f"current_price  {current_price}")')  
            # print(f"price_precision  {price_precision}")
            # print(f"defender  {defender}")
            # print(f'last_sl_order_id {main_stake_var[i]["last_sl_order_id"]}')
            # print(f"enter_deFacto_price  {enter_deFacto_price}")
            # print(f"static_sl_price  {static_sl_price}")
            # print(f"static_tp_price  {static_tp_price}")
            # print(f"atr  {atr}")
            try: 
                q_trailing_sl = self.trailing_sl_levels[1][0]
                # print(f"q_trailing_sl  {q_trailing_sl}")
                q_trailing_tp = self.trailing_sl_levels[1][1] 
                # print(f"q_trailing_tp  {q_trailing_tp}") 
            except:
                pass

            if defender == 1:
                if (current_price <= static_sl_price) or (current_price >= static_tp_price):
                    main_stake_var[i]["done_level"] = 6
                    done_flag = True 
                # else:
                #     print('not yet')    

            elif defender == -1:
                if (current_price >= static_sl_price) or (current_price <= static_tp_price):
                    main_stake_var[i]["done_level"] = 6
                    done_flag = True
                # else:
                #     print('not yet') 

            if my_params.SL_STRATEGY_NUMBER == 2.0 or my_params.SL_STRATEGY_NUMBER == 2.1:        
                if main_stake_var[i]["breakpointt"]:
                    if main_stake_var[i]["checkpointt_flag"]:
                        if defender == 1:
                            if current_price <= main_stake_var[i]["breakpointt"]:
                                main_stake_var[i]["done_level"] = 6
                                done_flag = True
                        elif defender == -1:
                            if current_price >= main_stake_var[i]["breakpointt"]:
                                main_stake_var[i]["done_level"] = 6
                                done_flag = True          

                if len(self.trailing_sl_levels) != 0:                    
                    if not main_stake_var[i]["checkpointt_flag"]:
                        if not main_stake_var[i]["checkpointt"]:
                            try:
                                static_defender = 1
                                main_stake_var[i]["checkpointt"], main_stake_var[i]["breakpointt"] = checkpoint_calc(main_stake_var[i]["enter_deFacto_price"], main_stake_var[i]["atr"], q_trailing_sl, q_trailing_tp, main_stake_var[i]["defender"], main_stake_var[i]["price_precision"], static_defender, main_stake_var[i]["tick_size"]) 

                                # print(f'str 193, checkpointt  {main_stake_var[i]["checkpointt"]}, breakpointt  {main_stake_var[i]["breakpointt"]}')   
                            except Exception as ex:
                                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")               
                        if main_stake_var[i]["checkpointt"]:
                            if defender == 1:
                                if current_price >= main_stake_var[i]["checkpointt"]:
                                    print('checkpointt_flag!')
                                    main_stake_var[i]["checkpointt_flag"] = True 
                                # else:
                                #     print('it is no checkpointt_flag')

                            elif defender == -1:
                                if current_price <= main_stake_var[i]["checkpointt"]:
                                    print('checkpointt_flag!')
                                    main_stake_var[i]["checkpointt_flag"] = True
                                # else:
                                #     print('it is no checkpointt_flag')
                        else:
                            print('str 207: Problem with calc checkpointt and breakpointt')

                    if main_stake_var[i]["checkpointt_flag"]:
                        # if my_params.SL_STRATEGY_NUMBER == 2.0:                            
                        #     main_stake_var[i] = self.limit_order_pattern(main_stake_var[i])
                        if my_params.SL_STRATEGY_NUMBER == 2.1:  
                            print('Hello checkpointt_flag!')
                            main_stake_var[i]["checkpointt_flag"] = False                
                            self.trailing_sl_levels.pop(0)                             
                            main_stake_var[i]["checkpointt"], main_stake_var[i]["breakpointt"] = None, None 

                else:
                    print('len(self.TABULA_SL_TP_POINTS) = 0!')
            # print(f"len_main_stake_var  {len(main_stake_var)}")
        
        return main_stake_var, done_flag, step
    
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
    
sl_strategies = SL_STRATEGYY()

# python -m MONEY.stop_logic
