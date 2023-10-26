import asyncio
import aiohttp 
import json
import logging
import os
import inspect
from MONEY.stop_logic import sl_strategies
from API.orders_utils import orders_utilss
from pparamss import my_params

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

async def price_monitoring(main_stake, data_callback):
    url = f'wss://stream.binance.com:9443/stream?streams='
    main_stake_var = main_stake.copy()
    streams = [f"{k['symbol'].lower()}@kline_1s" for k in main_stake_var]
    print(f"start_socket_stake:___{len(main_stake_var)}")
    step = 0
    try:
        while True:   
            # data_prep = None 
            # # first_iter_flag = False  
            ws = None   
            done_flag = False             
            counter = 0 
            time_to_check_open_positions = 0           
                          
            try:
                # print('hi')
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(url) as ws:
                        subscribe_request = {
                            "method": "SUBSCRIBE",
                            "params": streams,
                            "id": 9457949
                        }
                        try:
                            data_prep = await ws.send_json(subscribe_request)                            
                        except Exception as ex:
                            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")                  

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
                                            # print(f"socket counter {counter}")                       
                                except Exception as ex:
                                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")                                  
                                    await asyncio.sleep(1)
                                    continue

                                if counter == len(main_stake_var):
                                    # print(f"counter == len(main_stake_var):  {counter == len(main_stake_var)}")
                                    main_stake_var, done_flag, step, time_to_check_open_positions = await data_callback(main_stake_var, step, time_to_check_open_positions)
                                    counter = 0  
                                    # print(f"done_flag  {done_flag}")   
                                    # print(f"len(main_stake_var) after call_back{len(main_stake_var)}")              

                                    if done_flag or len(main_stake_var) == 0:                               
                                        return 

            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                await asyncio.sleep(7)
                continue
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
    finally:
        await ws.close()
        return main_stake_var

async def process_data(main_stake, step, time_to_check_open_positions):

    done_flag = False
    main_stake_var = main_stake.copy()    
    if step != 4:
        try:
            main_stake_var, step = sl_strategies.usual_orders_assambler(main_stake_var, step)            
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
            
    elif step == 4:
        try:
            if my_params.SL_STRATEGY_NUMBER != 1:
                main_stake_var, done_flag, step = sl_strategies.trailling_sl_controller(main_stake_var, step) 
# ///////////////////////////////////////////////////////////////////////////////////
            else:
                time_to_check_open_positions += 1
                if time_to_check_open_positions == 31:
                    print('time_to_check_open_positions_flag = True')
                    # time_to_check_open_positions_flag = True
                    open_pos = orders_utilss.get_open_positions()            
                    open_pos_symbol_list = [x["symbol"] for x in open_pos]
                    current_pos_symbol_list = [(i, x["symbol"]) for i, x in enumerate(main_stake_var)]
                    time_to_check_open_positions = 0
                    # print(open_pos_symbol_list)
                    try_to_cancel_all_orders_by_symbol = []
                    for i, cur_symbol in current_pos_symbol_list:
                        if cur_symbol not in open_pos_symbol_list:
                                try_to_cancel_all_orders_by_symbol.append(cur_symbol)
                                print('dhkbghkerbg')
                                main_stake_var[i]["done_level"] = 6
                                main_stake_var[i]["close_position"] = True
                                done_flag = True 
                    cancel_all_orders_answer = None
                    cancel_all_orders_answer = orders_utilss.cancel_all_orders_for_position(try_to_cancel_all_orders_by_symbol)    

        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

    return main_stake_var, done_flag, step, time_to_check_open_positions