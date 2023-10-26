import asyncio
import math
from API.bin_data_get import bin_data
from API.create_order import create_orders_obj
from API.orders_utils import orders_utilss

from pparamss import my_params
from ENGIN.main_strategy_controller import strateg_controller   
from UTILS.waiting_candle import kline_waiter
# from UTILS.indicators import calculate_atr
from UTILS.calc_qnt import calc_qnt_func
from UTILS.clean_cashe import cleanup_cache
from UTILS.indicators import calculate_atr
from MONEY.asumm import asum_counter
from MONEY.stop_logic import sl_strategies
from pparamss import my_params
from API.bin_data_get import bin_data
from API.websockett import price_monitoring, process_data
import pytz
from datetime import datetime, time
import asyncio
import aiohttp
import json
import sys 

import logging
import os
import inspect

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

def stake_generator(usual_defender_stake):
    
    universal_stake = [
        {            
            "symbol": s,
            "defender": d,
            "enter_deFacto_price": None, 
            "recalc_depo": None,           
            "current_price": None,           
            "close_position": False,
            "qnt": None, 
            "price_precision": None,  
            "tick_size": None,
            "atr": None,           
            "last_sl_order_id": None,           
            "static_tp_price": None,
            "static_sl_price": None,
            "checkpointt_flag": False,
            "checkpointt": None,
            "breakpointt": None,
            "done_level": 0
            # "approximate_profit": None,
            # "in_position": False,  
            # "atr_aprox": atr_aprox,
            # "rra": rra,         
        }
            for s, d, atr_aprox, rra in usual_defender_stake            
    ] 

    return universal_stake

async def main(start_time):
    first_flag = True
    top_coins = []  
    usual_defender_stake = []
    total_raport_list = [] 
    intermedeate_raport_list = [] 
    main_stake_busy_symbols_list = []
    problem_to_closing_by_market_list = []
    recalculated_depo = None
    atr_corrector_list = []
    # print(my_params.limit_selection_coins)
    try:
        top_coins = bin_data.get_top_pairs()
    except Exception as ex:
        print(f"main__15:\n{ex}")    
    print(len(top_coins)) 
    # print(top_coins) 
    # 'ZECUSDT'
    problem_pairs = ['SOLUSDT', 'ZECUSDT', 'MKRUSDT']
    top_coins = [x for x in top_coins if x not in problem_pairs]
    # print(top_coins)
    # top_coins = [x.replace('USDT', '') for x in top_coins]
    # print(top_coins)
    # finish_time = time.time() - start_time    
    # print(f"Общее время поиска:  {math.ceil(finish_time)} сек")

    firstt = False

    # sys.exit() 
    try:
        wait_time = kline_waiter(my_params.KLINE_TIME, my_params.TIME_FRAME)
        # print(f"waiting time to close last candle is: {wait_time} sec")
        # await asyncio.sleep(wait_time)
    except Exception as ex:
        print(f"main__24:\n{ex}")
    
    while True:
        # if firstt:
        #     break
        try:
            # await asyncio.sleep(2)
            if len(total_raport_list) >= 5:
                print('it is time to assuming!')  
                # asum_counter(total_raport_list)
                # create_orders_obj.cancel_all_orderss()
                # create_orders_obj.calcel_all_futures_positions()
                cleanup_cache()
                break

            # now = datetime.now()
            # desired_timezone = pytz.timezone('Europe/Kiev')
            # now_in_desired_timezone = now.astimezone(desired_timezone)
            # current_time = now_in_desired_timezone.strftime('%H:%M')
            # print(current_time)
            # if time(0, 0) <= time(int(current_time.split(':')[0]), int(current_time.split(':')[1])) <= time(1, 0):
            #     print('it is time to assuming!') 
            #     if len(total_raport_list) >= 1:   
            #         pass            
            #         # asum_counter(total_raport_list)
            #     break

            try:
                usual_defender_stake = strateg_controller.main_strategy_control_func(top_coins)
                # print(len(usual_defender_stake))
                usual_defender_stake = [x for x in usual_defender_stake if x[0] not in main_stake_busy_symbols_list]
                # print(usual_defender_stake)
            except Exception as ex:
                print(f"192___{ex}") 
            try:
                if len(usual_defender_stake) == 0:
                    await asyncio.sleep(15)
                    continue
                else:
                    if first_flag:                                            
                        if len(usual_defender_stake) > my_params.DIVERCIFICATION_NUMDER:
                            usual_defender_stake = usual_defender_stake[:my_params.DIVERCIFICATION_NUMDER]
                        universal_stake = stake_generator(usual_defender_stake)
                        main_stake = universal_stake
                        first_flag = False  
                    else:
                        try:
                            decimal = my_params.DIVERCIFICATION_NUMDER - len(main_stake)
                            if len(usual_defender_stake) > decimal:
                                usual_defender_stake = usual_defender_stake[:decimal]
                            universal_stake = stake_generator(usual_defender_stake)
                            main_stake = main_stake + universal_stake
                        except Exception as ex:
                            print(f"212___{ex}") 
            except Exception as ex:
                print(f"214___{ex}")

            try:
                main_stakee = main_stake.copy()               

                for i, item in enumerate(main_stakee):
                    # print(item["symbol"])
                    klines = None
                    atr = None
                    klines = bin_data.get_klines(item["symbol"])
                    atr = calculate_atr(klines)
                    if atr:
                        main_stake[i]["atr"] = atr 
                    else:
                        main_stake.pop(i)
            except:
                pass
            # print(main_stake)
            # sys.exit()
                             
            # ///////////////////////////////////////////////////////////////////////
            try:
                # main_stake = [{'symbol': 'ETHUSDT', 'defender': 1, 'enter_deFacto_price': None, 'recalc_depo': None, 'current_price': None, 'close_position': False, 'qnt': None, 'price_precision': None, 'tick_size': None, 'atr_aprox': 94.46000000000004, 'atr': 75.36071428571431, 'rra': 301.10690804, 'last_sl_order_id': None, 'static_tp_price': None, 'static_sl_price': None, 'checkpointt_flag': False, 'checkpointt': None, 'breakpointt': None, 'done_level': 0,}]

                main_stake = await price_monitoring(main_stake, process_data)
                # firstt = True
                if main_stake: 
                    main_stake, problem_to_closing_by_market_list, _ = orders_utilss.close_position_confidencer(main_stake)
                        
                intermedeate_raport_list = [x for x in main_stake if x["close_position"]] 
                total_raport_list += intermedeate_raport_list
                main_stake = [x for x in main_stake if not x["close_position"]]
                main_stake_busy_symbols_list = [x['symbol'] for x in main_stake] + problem_to_closing_by_market_list

            except Exception as ex:
                print(f"main__192:\n{ex}")         

        except Exception as ex:
            print(f"main__195:\n{ex}")
            await asyncio.sleep(5)
   
    
    print("There was a good!")

if __name__ == "__main__":
    start_time = None
    # import time
    # start_time = time.time()  
    # try:
    #     atexit.register(cleanup_cache)
    # except Exception as ex:
    #     print(f"461____{ex}")
    asyncio.run(main(start_time))
    # sys.exit()

# killall -9 python
# killall -r /path/to/.venv

