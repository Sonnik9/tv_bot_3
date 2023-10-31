from pparamss import my_params
from API.utils_api import utils_apii
from ENGIN.main_strategy_controller import strateg_controller  
from ENGIN.sl_strategy_controller import sl_manager_func
from UTILS.waiting_candle import kline_waiter
from UTILS.calc_atr import calc_atr_edition_func
from UTILS.time_keeper import time_keeper_func
from UTILS.stake_generator import stake_generator_func
from MONEY.asumm import asum_counter
from PROCESS.websockett import price_monitoring
import asyncio
import logging
import os
import inspect
import sys 

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

async def main(start_time):
    first_flag = True
    finish_flag = False
    top_coins = []  
    usual_defender_stake = []
    total_raport_list = [] 
    intermedeate_raport_list = [] 
    main_stake_busy_symbols_list = []
    problem_to_closing_by_market_list = []

    try:
        top_coins = utils_apii.assets_filters()
        top_coins = [x for x in top_coins if x not in my_params.problem_pairs]
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
   
    print(f"len_candidates_pairs: {len(top_coins)}")
    # print(f"len_candidates_pairs: {top_coins}")
    # sys.exit() 
    try:
        wait_time = kline_waiter(my_params.KLINE_TIME, my_params.TIME_FRAME)
        print(f"waiting time to close last candle is: {wait_time} sec")
        # await asyncio.sleep(wait_time)
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
    
    while True:
        if finish_flag:
            break
        try:
            # await asyncio.sleep(2)
            if len(total_raport_list) >= 3:
                print('it is time to assuming!')                
                break
            if my_params.TERMINATE_TIMER_FLAG:
                it_is_time = time_keeper_func()
                if it_is_time:
                    break
                print('it is time to assuming!')
            try:
                usual_defender_stake = strateg_controller.main_strategy_control_func(top_coins)                
                usual_defender_stake = [x for x in usual_defender_stake if x[0] not in main_stake_busy_symbols_list]                
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

            try:
                if len(usual_defender_stake) == 0:
                    await asyncio.sleep(15)
                    continue
                else:
                    if first_flag:                                            
                        if len(usual_defender_stake) > my_params.DIVERCIFICATION_NUMDER:
                            usual_defender_stake = usual_defender_stake[:my_params.DIVERCIFICATION_NUMDER]
                        universal_stake = stake_generator_func(usual_defender_stake)
                        main_stake = universal_stake
                        first_flag = False  
                    else:
                        try:
                            decimal = my_params.DIVERCIFICATION_NUMDER - len(main_stake)
                            if len(usual_defender_stake) > decimal:
                                usual_defender_stake = usual_defender_stake[:decimal]
                            universal_stake = stake_generator_func(usual_defender_stake)
                            main_stake = main_stake + universal_stake
                        except Exception as ex:
                            print(f"212___{ex}") 
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            try:
            # //////////////////////////////////////////////////////////////////////
            # atr calculation
                main_stake = calc_atr_edition_func(main_stake)
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
                          
            # ///////////////////////////////////////////////////////////////////////
            try:
                main_stake, problem_to_closing_by_market_list, finish_flag = await price_monitoring(main_stake, sl_manager_func)                        
                intermedeate_raport_list = [x for x in main_stake if x["close_position"]] 
                total_raport_list += intermedeate_raport_list
                main_stake = [x for x in main_stake if not x["close_position"]]
                main_stake_busy_symbols_list = [x['symbol'] for x in main_stake] + problem_to_closing_by_market_list
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")       

        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
            await asyncio.sleep(5)   
    
    print("There was a good!")

if __name__ == "__main__":
    start_time = None
    asyncio.run(main(start_time))

# killall -9 python
# killall -r /path/to/.venv

