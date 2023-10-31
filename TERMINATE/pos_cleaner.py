from API.get_api import get_apii
from API.delete_api import delete_apii

def pos_cleaner_func(main_stake):

    done_flag = False
    main_stake_var = main_stake.copy()
    print('time_to_check_open_positions_flag = True')
    # time_to_check_open_positions_flag = True
    open_pos = get_apii.get_open_positions()            
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
    cancel_all_orders_answer = delete_apii.cancel_all_orders_for_position(try_to_cancel_all_orders_by_symbol) 

    return main_stake_var, done_flag