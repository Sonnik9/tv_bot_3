from ENGIN.pos_monitor import POSITIONS_MONITORINGG
from MONEY.asumm import asum_counter
import logging
import os
import inspect
import time
import sys 

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

class MAIN_(POSITIONS_MONITORINGG):

    def __init__(self) -> None:
        super().__init__()

    def iteration_result(self, main_stake, intermedeate_raport_list, total_raport_list, main_stake_busy_symbols_list, problem_to_closing_by_market_list):
        try:
            # main_stake, problem_to_closing_by_market_list, finish_flag
            main_stake = self.pos_monitoring_func(main_stake)                        
            intermedeate_raport_list = [x for x in main_stake if x["close_position"]] 
            total_raport_list += intermedeate_raport_list
            main_stake = [x for x in main_stake if not x["close_position"]]
            main_stake_busy_symbols_list = [x['symbol'] for x in main_stake] + problem_to_closing_by_market_list
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  

        return main_stake, intermedeate_raport_list, total_raport_list, main_stake_busy_symbols_list, problem_to_closing_by_market_list

    def init_main(self):
        first_flag = True    
        top_coins = []  
        usual_defender_stake = []
        total_raport_list = [] 
        intermedeate_raport_list = [] 
        main_stake_busy_symbols_list = []
        problem_to_closing_by_market_list = []
        
        while True:
            if not first_flag:
                return
            try:
                top_coins = self.assets_filters()            
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
        
            print(f"len_candidates_pairs: {len(top_coins)}")
            # print(f"len_candidates_pairs: {top_coins}")
            # sys.exit() 
            try:
                wait_time = self.kline_waiter(self.KLINE_TIME, self.TIME_FRAME)
                print(f"waiting time to close last candle is: {wait_time} sec")
                # time.sleep(wait_time)
                # await asyncio.sleep(wait_time)
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            try:
                usual_defender_stake = self.ind_strategy_control_func(top_coins)                
                usual_defender_stake = [x for x in usual_defender_stake if x[0] not in main_stake_busy_symbols_list]                
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

            try:
                if len(usual_defender_stake) == 0 and first_flag:
                    time.sleep(15)
                    continue

                elif len(usual_defender_stake) == 0 and not first_flag:
                    main_stake, intermedeate_raport_list, total_raport_list, main_stake_busy_symbols_list, problem_to_closing_by_market_list= self.iteration_result(self, main_stake, intermedeate_raport_list, total_raport_list, main_stake_busy_symbols_list, problem_to_closing_by_market_list)
                
                elif len(usual_defender_stake) != 0:
                    if first_flag:                                            
                        if len(usual_defender_stake) > self.DIVERCIFICATION_NUMDER:
                            usual_defender_stake = usual_defender_stake[:self.DIVERCIFICATION_NUMDER]
                        universal_stake = self.stake_generator_func(usual_defender_stake)
                        main_stake = universal_stake
                        first_flag = False  
                    else:
                        try:
                            decimal = self.DIVERCIFICATION_NUMDER - len(main_stake)
                            if len(usual_defender_stake) > decimal:
                                usual_defender_stake = usual_defender_stake[:decimal]
                            universal_stake = self.stake_generator_func(usual_defender_stake)
                            main_stake = main_stake + universal_stake
                        except Exception as ex:
                            print(f"212___{ex}") 

                    # print(main_stake)
                    # //////////////////////////////////////////////////////////////////
                    # atr calculation
                    try:    
                        main_stake = self.calc_atr_edition_func(main_stake)
                    except Exception as ex:
                        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
                                
                    # //////////////////////////////////////////////////////////////////# get prices
                    try:
                        main_stake = self.get_current_price_edition_func(main_stake)
                    except Exception as ex:
                        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

                    # print(main_stake)
                    # return                                
                    # //////////////////////////////////////////////////////////////////
                    main_stake, intermedeate_raport_list, total_raport_list, main_stake_busy_symbols_list, problem_to_closing_by_market_list = self.iteration_result(main_stake, intermedeate_raport_list, total_raport_list, main_stake_busy_symbols_list, problem_to_closing_by_market_list)

            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

if __name__ == "__main__":    
    main_class = MAIN_()
    main_class.init_main()


# killall -9 python
# killall -r /path/to/.venv

