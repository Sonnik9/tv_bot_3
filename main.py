import asyncio
import math
from API.bin_data_get import bin_data
from API.create_order import create_orders_obj
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


async def price_monitoring(main_stake, data_callback):
    url = f'wss://stream.binance.com:9443/stream?streams='
    main_stake_var = main_stake.copy()
    streams = [f"{k['symbol'].lower()}@kline_1s" for k in main_stake_var]
    print(f"start_socket_stake:___{len(main_stake_var)}")

    try:
        while True:   
            data_prep = None   
            ws = None            
            first_iter_flag = False
            done_flag = False             
            counter = 0  
            step = 0
                          
            try:
                # print('hi')
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(url) as ws:
                        subscribe_request = {
                            "method": "SUBSCRIBE",
                            "params": streams,
                            "id": 9457945
                        }
                        try:
                            data_prep = await ws.send_json(subscribe_request)                            
                        except:
                            pass
                   
                        if not data_prep and first_iter_flag:                                             
                            await asyncio.sleep(7)
                            continue                       

                        async for msg in ws:                            
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                try:                                    
                                    data = json.loads(msg.data)                                             
                                    symbol = data.get('data',{}).get('s')                                    
                                    close_price = float(data.get('data',{}).get('k',{}).get('c'))  
                                    # print(close_price) 
                                    
                                    for i, item in enumerate(main_stake_var):
                                        if symbol == item["symbol"]:
                                            main_stake_var[i]["current_price"] = close_price
                                            counter += 1                          
                                except:
                                    pass
                                
                                if counter == len(main_stake_var):
                                    main_stake_var, done_flag, step = await data_callback(main_stake_var, step)
                                    counter = 0
                                    first_iter_flag = True   
                                    print(f"step  {step}")                        

                                    if done_flag or len(main_stake_var) == 0:                               
                                        return 

            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(7)
                continue
    except:
        pass
    finally:
        await ws.close()
        return main_stake_var
   
async def process_data(main_stake, step):

    done_flag = False
    main_stake_var = main_stake.copy()

    if step != 4:
        try:
            main_stake_var, step = sl_strategies.usual_orders_assambler(main_stake_var, step)            
        except Exception as ex:
            print(f"main_105str:__ {ex}")
    elif step == 4:
        return main_stake, done_flag, step
        # sys.exit(0)
        try:
            main_stake_var, done_flag = sl_strategies.trailling_sl_controller(main_stake_var)      
        except Exception as ex:
            print(f"main_111str:__ {ex}")
    return main_stake, done_flag, step

def stake_generator(usual_defender_stake):
    
    universal_stake = [
        {
            # "approximate_profit": None,
            "symbol": s,
            "defender": d,
            "enter_deFacto_price": None, 
            "recalc_depo": None,           
            "current_price": None,            
            # "in_position": False,
            "close_position": False,
            "qnt": None, 
            "price_precision": None,  
            "tick_size": None,   
            "atr_aprox": atr_aprox,
            "atr": None,
            "rra": rra,
            "last_sl_order_id": None,            
            "static_tp_order_id": None,
            "static_tp_price": None,
            "static_sl_price": None,
            "checkpointt_flag": False,
            "checkpointt": None,
            "breakpointt": None,
            "done_level": 0,
            "position_problem": []       
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
    top_coins = [x for x in top_coins if x != 'ZECUSDT' and x != 'MKRUSDT']
    # print(top_coins)
    # top_coins = [x.replace('USDT', '') for x in top_coins]
    # print(top_coins)
    # finish_time = time.time() - start_time    
    # print(f"Общее время поиска:  {math.ceil(finish_time)} сек")

    firstt = False

    # sys.exit() 
    try:
        wait_time = kline_waiter(my_params.KLINE_TIME, my_params.TIME_FRAME)
        print(f"waiting time to close last candle is: {wait_time} sec")
        # await asyncio.sleep(wait_time)
    except Exception as ex:
        print(f"main__24:\n{ex}")
    
    while True:
        if firstt:
            break
        try:
            # await asyncio.sleep(2)
            if len(total_raport_list) >= 1:
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
                print(len(usual_defender_stake))
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
                main_stake = await price_monitoring(main_stake, process_data)
                firstt = True
                # if main_stake: 
                #     main_stake, _, _ = create_orders_obj.close_position_confidencer(main_stake)
                        
                intermedeate_raport_list = [x for x in main_stake if x["close_position"]] 
                total_raport_list += intermedeate_raport_list
                main_stake = [x for x in main_stake if not x["close_position"]]
                main_stake_busy_symbols_list = [x['symbol'] for x in main_stake]

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

