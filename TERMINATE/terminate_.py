from API.utils_api import UTILS_APII

class TERMINATE(UTILS_APII):
    def __init__(self) -> None:
        super().__init__()

    def terminate_all_func(self, main_stake):
        
        succes_closed_symbol_list, dont_closed_symbol_list = [], []   
        succes_closed_symbol_list, dont_closed_symbol_list = self.try_to_close_by_market_all_open_positions(main_stake)
        cancel_all_orders_answer = self.cancel_all_open_orders()

        return succes_closed_symbol_list, dont_closed_symbol_list
    
    def pos_cleaner_func(self, main_stake):

        done_flag = False
        main_stake_var = main_stake.copy()   
        # time_to_check_open_positions_flag = True
        open_pos = self.get_open_positions()            
        open_pos_symbol_list = [x["symbol"] for x in open_pos]
        current_pos_symbol_list = [(i, x["symbol"]) for i, x in enumerate(main_stake_var)]
        # print(open_pos_symbol_list)
        try_to_cancel_all_orders_by_symbol = []
        
        for i, cur_symbol in current_pos_symbol_list:
            if cur_symbol not in open_pos_symbol_list:
                try_to_cancel_all_orders_by_symbol.append(cur_symbol)
                # print('dhkbghkerbg')
                main_stake_var[i]["done_level"] = 4
                main_stake_var[i]["close_position"] = True
                done_flag = True 
        cancel_all_orders_answer = None
        cancel_all_orders_answer = self.cancel_all_orders_for_position(try_to_cancel_all_orders_by_symbol) 

        return main_stake_var, done_flag
    
    def average_closer_func(self, main_stake, ready_to_close_list):
        
        main_stake_var = main_stake.copy()
        good_closed_by_market_symbol_list = []
        problem_to_closing_by_market_symbol_list = []    
        good_closed_by_market_symbol_list, problem_to_closing_by_market_symbol_list = self.try_to_close_by_market_open_position_by_stake(ready_to_close_list)
        for i, _ in enumerate(main_stake):
            if main_stake_var[i]["symbol"] in good_closed_by_market_symbol_list:
                main_stake_var[i]["close_position"] = True     

        return main_stake_var, problem_to_closing_by_market_symbol_list


