from pparamss import my_params
from API.create_order import create_orders_obj
from UTILS.calc_qnt import calc_qnt_func

class SL_STRATEGYY():
    def __init__(self) -> None:
        self.t_p = None
        self.s_l = None
        self.sl_atr_multiplier = 1.2 #2.0 
        self.tp_art_multipler = 0.07 

    def sl_controller(self, main_stake):
        profit_flag = False  
        print(f"len_main_stake  {len(main_stake)}")    

        for item in main_stake:
            profit = None  
            open_order = None   
            close_order = None 
            is_closing = 1 
            qnt = None
            qnt_exit = None
        
            try:
                enter_price = item['enter_price']                
                symbol = item["symbol"]
            except Exception as ex:
                print(f"MONEY/stop_logic_1.py_str36:___{ex}")      
                continue

            if item['in_position'] == False:
                qnt = calc_qnt_func(symbol, enter_price, my_params.DEPO, qnt_exit, is_closing)   
                item['qnt'] = qnt       
                
                try:
                    if qnt:                        
                        open_order = create_orders_obj.make_order(item, is_closing)
                        print(open_order)
                        
                except Exception as ex:           
                    print(f"MONEY/stop_logic_1.py_str41:___{ex}")
                if open_order and 'status' in open_order and open_order['status'] == 'NEW':
                    item['in_position'] = True
                else:
                    main_stake.remove(item)
                    break                    

                 
        return main_stake, profit_flag  


sl_strategies = SL_STRATEGYY()
