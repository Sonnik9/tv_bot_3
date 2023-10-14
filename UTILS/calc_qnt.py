from pparamss import my_params
from API.bin_data_get import bin_data
import logging
import os
import inspect
import math 
logging.basicConfig(filename='my_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

def calc_qnt_func(symbol, price, depo, qnt_exit, is_closing): 

    symbol_info = None
    symbol_data = None 
    quantity = None
    
    try:
        url = f"{my_params.URL_PATTERN_DICT['exchangeInfo_url']}?symbol={symbol}"
        symbol_info = bin_data.get_excangeInfo(url)
    except Exception as ex:
        logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")   

    if symbol_info:
        symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)

    if symbol_data:
        step_size = float(symbol_data['filters'][1]['stepSize'])
        if my_params.MARKET == 'spot':
            min_notional = float(symbol_data['filters'][6]['minNotional'])
        elif my_params.MARKET == 'futures':
            min_notional = float(symbol_data['filters'][5]['notional'])

        # price_precision = abs(int(math.log10(step_size)))
        quantity_precision = abs(int(math.log10(1 / min_notional)))
        decimal = depo * 0.2

        if is_closing == 1:
            for _ in range(5):
                quantity = depo / price  
                try:  
                    quantity = round((round(quantity / step_size, quantity_precision) * step_size), quantity_precision)
                except:
                    pass

                if quantity * price < min_notional:                 
                    depo = depo + decimal  
                    quantity = None   
                    continue
                else:               
                    break
        else:
            quantity = round((round(qnt_exit / step_size, quantity_precision) * step_size), quantity_precision)

            if quantity * price < min_notional:
                quantity = None

    return quantity
