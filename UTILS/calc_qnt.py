from pparamss import my_params
from API.bin_data_get import bin_data

import inspect
import os
import logging

if not os.path.exists("UTILS"):
    os.makedirs("UTILS")

log_file = "UTILS/calc_qnt.log"

logging.basicConfig(filename=log_file, level=logging.ERROR)
current_file = os.path.basename(__file__)

def count_multipliter_places(number):
    if isinstance(number, (int, float)):
        number_str = str(number)
        if '.' in number_str:
            return len(number_str.split('.')[1])
    return 0

def calc_qnt_func(symbol, price, depo): 
    symbol_info = None
    symbol_data = None 
    price_precision = None
    quantity_precision = None
    quantity = None  
    min_qnt = None 
    max_qnt = None 
    min_depo = None
    max_depo = None
    
    try:
        symbol_info = bin_data.get_excangeInfo(symbol)
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
            min_depo = min_qnt * price           
            max_depo = max_qnt * price
            if depo < min_depo:
                depo = min_depo               
            elif depo > max_depo:
                depo = max_depo 
            else:         
                quantity = round(depo / price, quantity_precision)
                recalc_depo = quantity * price 

            try:
                tick_size = count_multipliter_places(tick_size)
            except Exception as ex:
                print(ex) 
                
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

    return quantity, recalc_depo, price_precision, tick_size


# symbol = 'BTCUSDT'
# price = 30000 
# depo = 100
# quantity, recalc_depo, price_precision, tick_size = calc_qnt_func(symbol, price, depo)

# print(quantity, recalc_depo, price_precision, tick_size)
# {'symbol': 'BTCUSDT', 'pair': 'BTCUSDT', 'contractType': 'PERPETUAL', 'deliveryDate': 4133404802000, 'onboardDate': 1569398400000, 'status': 'TRADING', 'maintMarginPercent': '2.5000', 'requiredMarginPercent': '5.0000', 'baseAsset': 'BTC', 'quoteAsset': 'USDT', 'marginAsset': 'USDT', 'pricePrecision': 2, 'quantityPrecision': 3, 'baseAssetPrecision': 8, 'quotePrecision': 8, 'underlyingType': 'COIN', 'underlyingSubType': [], 'settlePlan': 0, 'triggerProtect': '0.0500', 'liquidationFee': '0.020000', 'marketTakeBound': '0.30', 'maxMoveOrderLimit': 1000, 'filters': [{'maxPrice': '809484', 'minPrice': '261.10', 'tickSize': '0.10', 'filterType': 'PRICE_FILTER'}, {'minQty': '0.001', 'stepSize': '0.001', 'filterType': 'LOT_SIZE', 'maxQty': '1000'}, {'minQty': '0.001', 'maxQty': '1000', 'filterType': 'MARKET_LOT_SIZE', 'stepSize': '0.001'}, {'limit': 200, 'filterType': 'MAX_NUM_ORDERS'}, {'limit': 10, 'filterType': 'MAX_NUM_ALGO_ORDERS'}, {'filterType': 'MIN_NOTIONAL', 'notional': '5'}, {'multiplierDown': '0.5000', 'filterType': 'PERCENT_PRICE', 'multiplierUp': '1.5000', 'multipliermultipliter': '4'}], 'orderTypes': ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET'], 'timeInForce': ['GTC', 'IOC', 'FOK', 'GTX', 'GTD']}


# python -m UTILS.calc_qnt