from pparamss import my_params
from API.create_order import create_orders_obj
from API.bin_data_get import bin_data
from UTILS.calc_qnt import calc_qnt_func

class SL_STRATEGYY():
    def __init__(self) -> None:
        # self.sl_atr_multiplier = 1.2 #2.0 
        # self.tp_art_multipler = 0.07 
        self.BUNCH_VARIANT = 1 
        self.TABULA_STATIC_SL_TP_POINTS = my_params.SL_TABULA_LIST[my_params.SL_TABULA_NUMBER][0]        
        self.TABULA_SL_TP_POINTS = my_params.SL_TABULA_LIST[my_params.SL_TABULA_NUMBER][1]             
        self.STATIC_SL_Q = self.TABULA_STATIC_SL_TP_POINTS[0]        
        self.STATIC_TP_Q = self.TABULA_STATIC_SL_TP_POINTS[1]
        
    def sl_controller(self, main_stake):        
        print(f"len_main_stake  {len(main_stake)}")       
        done_flag = False
        main_stake_var = main_stake.copy()
        
        for i, _ in enumerate(main_stake): 
            qnt = None 
            step_size = None  
            lev = None
            open_market_order = None
            open_static_sl_order = None
            open_static_tp_order = None
            open_dinamic_sl_order = None
            cancel_order = None
            try:
                symbol = main_stake_var[i]["symbol"]                 
                current_price = main_stake_var[i]["current_price"] 
                defender = main_stake_var[i]["defender"]                               
            except Exception as ex:
                print(f"MONEY/stop_logic_1.py_str45:___{ex}")  
                main_stake_var[i] = None    
                continue 

            if main_stake_var[i]["done_level"] == 5:
                if defender == 1:
                    if (current_price >= main_stake_var[i]["static_tp_price"]) or (current_price <= main_stake_var[i]["breakpointt"]):
                        main_stake_var[i]["done_level"] = 6
                        done_flag = True
                        
                elif defender == -1:
                    if (current_price <= main_stake_var[i]["static_tp_price"]) or (current_price >= main_stake_var[i]["breakpointt"]):
                        main_stake_var[i]["done_level"] = 6
                        done_flag = True          
                continue

            if not main_stake_var[i]['in_position']:         
                enter_deJure_price = current_price         
    
                try:                    
                    qnt, step_size = calc_qnt_func(symbol, enter_deJure_price, my_params.DEPO) 
                    print(f"step_size__{step_size}")  
                    qnt = round(qnt, step_size)
                    main_stake_var[i]['qnt'] = qnt  
                    main_stake_var[i]["step_size_for_price"] = step_size  
                except Exception as ex:
                    print(f"MONEY/stop_logic_1.py_str57:___{ex}")  
                    main_stake_var[i] = None 
                    continue        
                try:
                    if qnt:                        
                        try:
                            lev = create_orders_obj.set_leverage(symbol)
                            # print(f"str59:  {lev}") 
                        except Exception as ex:           
                            print(f"MONEY/stop_logic_1.py_str64:___{ex}")
                        if lev and 'leverage' in lev and lev['leverage'] == my_params.LEVERAGE:
                            pass 
                        else:
                            main_stake_var[i] = None 
                            main_stake_var[i]["position_problem"].append(lev)   
                            continue
                     
                        is_closing = 1
                        type_market = 'MARKET' 
                        target_price = None 
                        try:          
                            open_market_order = create_orders_obj.make_order(main_stake_var[i], is_closing, type_market, target_price)
                            print(f"str74:  {open_market_order}") 
                        except Exception as ex:           
                            print(f"MONEY/stop_logic_1.py_str76:___{ex}")
                            main_stake_var[i] = None 
                            continue  
                    else:
                        main_stake_var[i] = None 
                        continue                       
                except Exception as ex:           
                    print(f"MONEY/stop_logic_1.py_str83:___{ex}")
                    main_stake_var[i] = None 
                    continue  

                if open_market_order and 'status' in open_market_order and open_market_order['status'] == 'NEW':
                    print("open market order")
                    main_stake_var[i]['in_position'] = True 
                    main_stake_var[i]["done_level"] = 1
                           
                    try:
                        enter_deFacto_price = bin_data.get_position_price(symbol)
                        # print(f"str80: {enter_deFacto_price}")
                        
                        main_stake_var[i]["enter_deFacto_price"] = enter_deFacto_price
                    except Exception as ex:           
                        print(f"MONEY/stop_logic_1.py_str98:___{ex}")  
                        main_stake_var[i] = None 
                        continue  
                    # ///////////////////////////////////////////////////// 
                    is_closing = -1
                    type_market = 'LIMIT'                    
                    # /////////////////////////////////////////////////////       
                    try:
                        # sl static order   
                        print('sl static order')                     
                        target_price = round(enter_deFacto_price - (defender * self.STATIC_SL_Q * main_stake_var[i]["atr"]), step_size)
                        print(f"target_price__str113: {target_price}")
                        main_stake_var[i]["static_sl_price"] = target_price
                        open_static_sl_order = create_orders_obj.make_order(main_stake_var[i], is_closing, type_market, target_price)
                        print(f"str117: {open_static_sl_order}")
                        if open_static_sl_order and 'status' in open_static_sl_order and open_static_sl_order['status'] == 'NEW':
                            main_stake_var[i]["last_sl_order_id"] = open_static_sl_order["orderId"]                            
                            main_stake_var[i]["done_level"] = 2 
                        else:
                            main_stake_var[i]["position_problem"].append(open_static_sl_order)               
                    except Exception as ex:           
                        print(f"MONEY/stop_logic_1.py_str117:___{ex}")
                        main_stake_var[i]["position_problem"].append(open_static_sl_order)
                        continue  
                    try:
                        if main_stake_var[i]["done_level"] == 2:
                            # tp static order  
                            target_price = round(enter_deFacto_price + (defender * self.STATIC_TP_Q * main_stake_var[i]["atr"]), step_size)
                            main_stake_var[i]["static_tp_price"] = target_price
                            open_static_tp_order = create_orders_obj.make_order(main_stake_var[i], is_closing, type_market, target_price)
                            print(f"str126: {open_static_tp_order}")
                            if open_static_tp_order and 'status' in open_static_tp_order and open_static_tp_order['status'] == 'NEW':
                                main_stake_var[i]["static_tp_order_id"] = open_static_tp_order["orderId"]                            
                                main_stake_var[i]["done_level"] = 3  
                            else:
                                main_stake_var[i]["position_problem"].append(open_static_tp_order)              
                    except Exception as ex:           
                        print(f"MONEY/stop_logic_1.py_str133:___{ex}") 
                        main_stake_var[i]["position_problem"].append(open_static_tp_order) 
                        continue                     
                else:
                    main_stake_var[i] = None
                    continue                    
            if main_stake_var[i]['in_position']: 
                if len(self.TABULA_SL_TP_POINTS) != 0:                    
                    if main_stake_var[i]["done_level"] == 3:
                        main_stake_var[i]["checkpointt"] = round(main_stake_var[i]["enter_deFacto_price"] + (defender * main_stake_var[i]["atr"] * self.TABULA_SL_TP_POINTS[1][1]), step_size)
                        main_stake_var[i]["breakpointt"] = round(main_stake_var[i]["enter_deFacto_price"] + (defender * main_stake_var[i]["atr"] * self.TABULA_SL_TP_POINTS[1][0]), step_size)                      
                        main_stake_var[i]["done_level"] = 4
                    if main_stake_var[i]["done_level"] == 4:
                        if defender == 1:
                            if current_price >= main_stake_var[i]["checkpointt"]:
                                checkpointt_flag = True 
                            elif (current_price <= main_stake_var[i]["static_sl_price"]) or (current_price <= main_stake_var[i]["breakpointt"]):
                                main_stake_var[i]["done_level"] = 6
                                done_flag = True
                        elif defender == -1:
                            if current_price <= main_stake_var[i]["checkpointt"]:
                                checkpointt_flag = True 
                            elif (current_price >= main_stake_var[i]["static_sl_price"]) or (current_price >= main_stake_var[i]["breakpointt"]):
                                main_stake_var[i]["done_level"] = 6
                                done_flag = True
                        if checkpointt_flag:                        
                            type_market = 'LIMIT'
                            is_closing = -1
                            target_price = main_stake_var[i]["breakpointt"]
                            try:
                                open_dinamic_sl_order = create_orders_obj.make_order(main_stake_var[i], is_closing, type_market, target_price)
                                print(f"str169:  {open_dinamic_sl_order}")                              
                                if open_dinamic_sl_order and 'status' in open_dinamic_sl_order and open_dinamic_sl_order['status'] == 'NEW':
                                    checkpointt_flag = False
                                    self.TABULA_SL_TP_POINTS.pop(0)                                    
                                    try:                                        
                                        cancel_order = create_orders_obj.cancel_order_by_id(symbol, main_stake_var[i]["last_sl_order_id"])
                                        print(f"str175: {cancel_order}")
                                        if cancel_order and 'status' in cancel_order and cancel_order['status'] == 'CANCELED':
                                            main_stake_var[i]["last_sl_order_id"] = open_dinamic_sl_order["orderId"]
                                            main_stake_var[i]["done_level"] = 3
                                        else:
                                            main_stake_var[i]["position_problem"].append(cancel_order)
                                    except Exception as ex:           
                                        print(f"MONEY/stop_logic_1.py_str177:___{ex}")
                                        main_stake_var[i]["position_problem"].append(cancel_order)
                                else:
                                    main_stake_var[i]["position_problem"].append(open_static_sl_order)               
                            except Exception as ex:   
                                checkpointt_flag = False        
                                print(f"MONEY/stop_logic_1.py_str183:___{ex}")
                                main_stake_var[i]["position_problem"].append(cancel_order)
                else:
                    main_stake_var[i]["done_level"] = 5  

        main_stake_var = list(filter(lambda x: x != None, main_stake_var))
        print(f"len_main_stake_var  {len(main_stake_var)}")
        
        return main_stake_var, done_flag
    
sl_strategies = SL_STRATEGYY()

# print(sl_strategies.TABULA_SL_TP_POINTS)
# print(sl_strategies.TABULA_SL_TP_POINTS.pop(0))
# print(sl_strategies.TABULA_SL_TP_POINTS)
# print(sl_strategies.STATIC_SL_Q)
# print(sl_strategies.STATIC_TP_Q)
# print(sl_strategies.TABULA_SL_TP_POINTS)


# python -m MONEY.stop_logic
