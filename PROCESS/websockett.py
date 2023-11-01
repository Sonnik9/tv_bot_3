import asyncio, aiohttp, json
import logging, os, inspect

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)


async def price_monitoring(main_stake, data_callback):
    url = f'wss://stream.binance.com:9443/stream?streams='
    main_stake_var = main_stake.copy()
    main_stake_arg = main_stake.copy()
    streams = [f"{k['symbol'].lower()}@kline_1s" for k in main_stake_var]
    print(f"start_socket_stake:___{len(main_stake_var)}")
    step = 0
    finish_flag = False
    try:
        while True:   
            ws = None   
            done_flag = False             
            counter = 0 
            time_to_check_open_positions = 0   
            problem_to_closing_by_market_list = []        
                          
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
                                    try:
                                        for i, item in enumerate(main_stake_var):
                                            if symbol == item["symbol"]:
                                                main_stake_arg[i]["current_price"] = close_price
                                                counter += 1   
                                                # print(f"socket counter {counter}")      
                                    except Exception as ex:
                                        print(f"websocket 52: {ex}")                 
                                except Exception as ex:
                                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")                                  
                                    await asyncio.sleep(1)
                                    continue

                                if counter == len(main_stake_var):
                                    # print(f"counter == len(main_stake_var):  {counter == len(main_stake_var)}")
                                    try:
                                        main_stake_var, problem_to_closing_by_market_list, step, time_to_check_open_positions, done_flag, finish_flag = await data_callback(main_stake_arg, step, time_to_check_open_positions, done_flag, finish_flag)
                                        main_stake_arg = main_stake_var
                                        counter = 0  
                                        # print(problem_to_closing_by_market_list, step, time_to_check_open_positions, done_flag, finish_flag)
                                        # print(f"done_flag  {done_flag}")   
                                        # print(f"len(main_stake_var) after call_back{len(main_stake_var)}")              

                                        if done_flag or finish_flag or len(main_stake_var) == 0:                               
                                            return 
                                    except Exception as ex:
                                        print(ex)

            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                await asyncio.sleep(7)
                continue
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
    finally:
        await ws.close()
        return main_stake_var, problem_to_closing_by_market_list, finish_flag

