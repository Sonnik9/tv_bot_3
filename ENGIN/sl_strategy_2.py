from pparamss import my_params
from UTILS.calc_qnt import checkpoint_calc
import logging, os, inspect

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

class SL_TRAILING_STRATEGYY():

    def __init__(self) -> None:  
        self.trailing_sl_levels = my_params.TABULA_SL_TP_POINTS
        self.statik_sl = my_params.STATIC_SL_Q
        self.statik_tp = my_params.STATIC_TP_Q

    def trailling_sl_cycl(self, main_stake):
        main_stake_var = main_stake.copy()
        done_flag = False
        # print('hello trailing cycl')
        for i, item in enumerate(main_stake):
            main_stake_var[i], done_flag = self.tailling_sl(item)
        return main_stake_var, done_flag       

    def tailling_sl(self, item):

        # print(f"len_main_stake  {len(main_stake)}")
        itemm = item.copy() 
        done_flag = False   
        current_price = itemm["current_price"]        
        defender = itemm["defender"]              
        static_sl_price = itemm["static_sl_price"]            
        static_tp_price = itemm["static_tp_price"]
        # print(current_price)
        # print(defender)
        # print(static_sl_price)
        # print(static_tp_price)

        try: 
            q_trailing_sl = self.trailing_sl_levels[1][0]             
            q_trailing_tp = self.trailing_sl_levels[1][1]  
            # print(q_trailing_sl)    
            # print(q_trailing_tp)      
        except:
            pass

        if defender == 1:
            # print(current_price, static_sl_price, static_tp_price)
            if (current_price <= static_sl_price) or (current_price >= static_tp_price):
                itemm["done_level"] = 3
                done_flag = True 
                return itemm, done_flag

        elif defender == -1:
            # print(current_price, static_sl_price, static_tp_price)
            if (current_price >= static_sl_price) or (current_price <= static_tp_price):
                itemm["done_level"] = 3
                done_flag = True
                return itemm, done_flag

        if my_params.SL_STRATEGY_NUMBER == 2: 
            # print('hello my_params.SL_STRATEGY_NUMBER == 2')       
            if itemm["breakpointt"]:
                if itemm["checkpointt_flag"]:
                    if defender == 1:
                        if current_price <= itemm["breakpointt"]:
                            itemm["done_level"] = 3
                            done_flag = True
                            return itemm, done_flag
                    elif defender == -1:
                        if current_price >= itemm["breakpointt"]:
                            itemm["done_level"] = 3
                            done_flag = True  
                            return itemm, done_flag        

            if len(self.trailing_sl_levels) != 0:                    
                if not itemm["checkpointt_flag"]:
                    if not itemm["checkpointt"]:
                        try:
                            static_defender = 1
                            itemm["checkpointt"], itemm["breakpointt"] = checkpoint_calc(itemm["enter_deFacto_price"], itemm["atr"], q_trailing_sl, q_trailing_tp, itemm["defender"], itemm["price_precision"], static_defender, itemm["tick_size"])
                            print(f'str 193, checkpointt  {itemm["checkpointt"]}, breakpointt  {itemm["breakpointt"]}')   
                        except Exception as ex:
                            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")               
                    if itemm["checkpointt"]:
                        if defender == 1:
                            if current_price >= itemm["checkpointt"]:
                                print('checkpointt_flag!')
                                itemm["checkpointt_flag"] = True 

                        elif defender == -1:
                            if current_price <= itemm["checkpointt"]:
                                print('checkpointt_flag!')
                                itemm["checkpointt_flag"] = True
                    else:
                        print('str 207: Problem with calc checkpointt and breakpointt')

                if itemm["checkpointt_flag"]:
                    if my_params.SL_STRATEGY_NUMBER == 2:  
                        print('Hello checkpointt_flag!')
                        itemm["checkpointt_flag"] = False                
                        self.trailing_sl_levels.pop(0)                             
                        itemm["checkpointt"], itemm["breakpointt"] = None, None
            else:
                print('len(self.TABULA_SL_TP_POINTS) = 0!')
    
        return itemm, done_flag

sl_trailing_strategy = SL_TRAILING_STRATEGYY()

# python -m MONEY.stop_logic
