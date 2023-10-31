import math 
from pparamss import my_params 
from API.get_api import get_apii
import logging, os, inspect

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)



def count_multipliter_places(number):
    if isinstance(number, (int, float)):
        number_str = str(number)
        if '.' in number_str:
            return len(number_str.split('.')[1])
    return 0

def calc_qnt_func(symbol, price, depo, rounding_type=my_params.QNT_ROUNDING_TYPE): 
    symbol_info = None
    symbol_data = None 
    price_precision = None
    quantity_precision = None
    quantity = None  
    recalc_depo = None
    min_qnt = None 
    max_qnt = None 
    min_depo = None
    max_depo = None
    
    try:
        symbol_info = get_apii.get_excangeInfo(symbol)
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")   

    if symbol_info:
        try:
            symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  
        
    if symbol_data:
        if my_params.MARKET == 'futures':
            try:                
                tick_size = float(symbol_data['filters'][0]["tickSize"])
                price_precision = int(symbol_data['pricePrecision'])            
                quantity_precision = int(symbol_data['quantityPrecision'])                 
                min_qnt = float(symbol_data['filters'][1]['minQty'])
                max_qnt = float(symbol_data['filters'][1]['maxQty'])
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
        try:
            tick_size = count_multipliter_places(tick_size)
        except Exception as ex:
            print(ex) 
        
        try:
            min_depo = min_qnt * price           
            max_depo = max_qnt * price
            if depo <= min_depo:
                depo = min_depo               
            elif depo >= max_depo:
                depo = max_depo 
            if rounding_type == 'round':
                quantity = round(depo / price, quantity_precision)
            elif rounding_type == 'ceil':
                quantity = math.ceil((depo / price) * 10 ** quantity_precision) / (10 ** quantity_precision)
            elif rounding_type == 'floor':
                # print('hi floor!')
                quantity = math.floor((depo / price) * 10 ** quantity_precision) / (10 ** quantity_precision)
            recalc_depo = quantity * price
            # print(f"{symbol}:  {quantity, recalc_depo, price_precision, tick_size}")
                
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

    return quantity, recalc_depo, price_precision, tick_size

def checkpoint_calc(enter_deFacto_price, atr, q_sl, q_tp, defender, price_precision, static_defender, tick_size, rounding_type=my_params.QNT_ROUNDING_TYPE):

    checkpointt, breakpointt = None, None
    # print(enter_deFacto_price, defender, atr, q_sl,  q_tp, static_defender, tick_size)
    try:
        if rounding_type == 'round':
            checkpointt = round(enter_deFacto_price + (defender * atr * q_tp), tick_size)
        elif rounding_type == 'ceil':
            checkpointt = math.ceil((enter_deFacto_price + (defender * atr * q_tp)) * 10 ** tick_size) / (10 ** tick_size)
        elif rounding_type == 'floor':
            checkpointt = math.floor((enter_deFacto_price + (defender * atr * q_tp)) * 10 ** tick_size) / (10 ** tick_size)

    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
    try:
        if rounding_type == 'round':
            breakpointt = round(enter_deFacto_price + (static_defender * defender * atr * q_sl), tick_size)
        elif rounding_type == 'ceil':
            breakpointt = math.ceil((enter_deFacto_price + (static_defender * defender * atr * q_sl)) * 10 ** tick_size) / (10 ** tick_size)
        elif rounding_type == 'floor':
            breakpointt = math.floor((enter_deFacto_price + (static_defender * defender * atr * q_sl)) * 10 ** tick_size) / (10 ** tick_size)
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

    return checkpointt, breakpointt 

# python -m UTILS.calc_qnt