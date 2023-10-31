from pparamss import my_params 
import logging, os, inspect
from API.post_api import post_apii
from UTILS.calc_qnt import checkpoint_calc

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

def tp_sl_make_orders(item):
    itemm = item.copy()
    is_closing = -1
    static_defender = -1

    try: 
        itemm["static_tp_price"], itemm["static_sl_price"] = checkpoint_calc(itemm["enter_deFacto_price"], itemm["atr"], my_params.STATIC_SL_Q, my_params.STATIC_TP_Q       , itemm["defender"],itemm["price_precision"], static_defender, itemm["tick_size"])
        # print(f'str 73: static_tp_price:  {itemm["static_tp_price"]}, static_sl_price:  {itemm["static_sl_price"]}')
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
    
    try:  
        # sl static order //////////////////////////////////////////////        
        success_flag = False   
        target_price = itemm["static_sl_price"]
        market_type = 'STOP_MARKET'                                 
        open_static_sl_order, success_flag = post_apii.make_order(itemm, is_closing, target_price, market_type)
        # print(f'open_static_sl_order  {open_static_sl_order}')
        if success_flag:  
            try: 
                # tp static order /////////////////////////////////////////////////////        
                success_flag = False   
                target_price = itemm["static_tp_price"]
                market_type = 'TAKE_PROFIT_MARKET' 
                # if itemm["done_level"] == 4: 
                open_static_tp_order, success_flag = post_apii.make_order(itemm, is_closing, target_price, market_type)
                # print(f'open_static_tp_order  {open_static_tp_order}')
                if success_flag:                                     
                    itemm["done_level"] = 2            
            
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}\n {open_static_tp_order}") 
                                
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex} \n {open_static_sl_order}")

    return itemm
