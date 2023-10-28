from TEMP.imports_t import *

def make_market_order_temp_func(item):

    itemm = item.copy()
    symbol = itemm["symbol"]
    try:
        lev = post_apii.set_leverage(symbol)                    
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
    if lev and 'leverage' in lev and lev['leverage'] == my_params.LEVERAGE:
        enter_deJure_price = itemm["current_price"]
        try:                    
            itemm['qnt'], itemm["recalc_depo"],itemm["price_precision"], itemm["tick_size"] = calc_qnt_func(symbol, enter_deJure_price, my_params.DEPO)            
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        if itemm['qnt']:
            is_closing = 1
            success_flag = False
            market_type = 'MARKET'
            target_price = None
            try:          
                open_market_order, success_flag = post_apii.make_order(itemm, is_closing, target_price, market_type)
                # print(f"str74:  {open_market_order}") 
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex} \n {open_market_order}")
            if success_flag:                
                try:
                    itemm["enter_deFacto_price"] = get_apii.get_position_price(symbol)
                    # print(f'str73 {symbol}:  {itemm["enter_deFacto_price"]}  (defacto_prtice)')
                    itemm["done_level"] = 1
                    itemm["in_position"] = True
                    
                except Exception as ex:
                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

    return itemm
