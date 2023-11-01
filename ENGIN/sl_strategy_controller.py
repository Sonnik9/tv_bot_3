from pparamss import my_params
from TEMP.market_order_temp import make_market_order_temp_func
from TEMP.tp_sl_template import tp_sl_make_orders
from TERMINATE.terminate_all import terminate_all_func
from TERMINATE.pos_cleaner import pos_cleaner_func
from TERMINATE.just_a_closer import average_closer_func
from ENGIN.sl_strategy_2 import sl_trailing_strategy
from UTILS.calc_qnt import checkpoint_calc
import logging, os, inspect

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

async def sl_manager_func(main_stake, step, time_to_check_open_positions, done_flag, finish_flag):

    main_stake_var = main_stake.copy()
    done_flag = False
    problem_to_closing_by_market_list = []
    # print(f"len(main_stake_var)  {len(main_stake_var)}")
    if step == 0: 
        # print(step)
        for i, _ in enumerate(main_stake):            
            if not main_stake_var[i]["in_position"]:
                main_stake_var[i] = make_market_order_temp_func(main_stake_var[i])  
                if main_stake_var[i]["done_level"] == 1:
                    static_defender = -1
                    try: 
                        main_stake_var[i]["static_tp_price"], main_stake_var[i]["static_sl_price"] = checkpoint_calc(main_stake_var[i]["enter_deFacto_price"], main_stake_var[i]["atr"], my_params.STATIC_SL_Q, my_params.STATIC_TP_Q       , main_stake_var[i]["defender"],main_stake_var[i]["price_precision"], static_defender, main_stake_var[i]["tick_size"])
                        # print(f'str 73: static_tp_price:  {main_stake_var[i]["static_tp_price"]}, static_sl_price:  {main_stake_var[i]["static_sl_price"]}')
                    except Exception as ex:
                        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
    
                    if my_params.SL_STRATEGY_NUMBER == 1:
                        main_stake_var[i] = tp_sl_make_orders(main_stake_var[i])

        if my_params.SL_STRATEGY_NUMBER == 1:
            main_stake_var = [x for x in main_stake_var if x["done_level"] == 2]
        else:
            main_stake_var = [x for x in main_stake_var if x["done_level"] == 1]

        step = 1
        
        return main_stake_var, problem_to_closing_by_market_list, step, time_to_check_open_positions, done_flag, finish_flag

    if step == 1:
        # print(step)
        if my_params.SL_STRATEGY_NUMBER == 1:
            time_to_check_open_positions += 1
            if finish_flag:
                print("time for terminate")
                problem_closing_list = []
                succes_closed_symbol_list, problem_to_closing_by_market_list = terminate_all_func(main_stake_var)                
                print(f"problem_to_closing_by_market_list  {problem_to_closing_by_market_list}") 

            if time_to_check_open_positions == 31:
                # print('time_to_check_open_positions_flag = True')
                main_stake_var, done_flag = pos_cleaner_func(main_stake_var)
                time_to_check_open_positions = 0

        elif my_params.SL_STRATEGY_NUMBER == 2:
            ready_to_close_list = []            
            main_stake_var, done_flag, step = sl_trailing_strategy.trailling_sl_cycl(main_stake_var, step)
            ready_to_close_list = [x for x in main_stake if x["done_level"] == 3]
            if len(ready_to_close_list) != 0:
                main_stake_var, problem_to_closing_by_market_list = average_closer_func(main_stake_var, ready_to_close_list)

        return main_stake_var, problem_to_closing_by_market_list, step, time_to_check_open_positions, done_flag, finish_flag


    
