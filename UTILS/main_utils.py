from API.utils_api import UTILS_APII
import logging, os, inspect
import math
import os, shutil
import time
import random

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

class MAIN_UTILSS(UTILS_APII):

    def __init__(self) -> None:
        super().__init__()

    # ///////////////////////////////////////////////////////////////////////

    def calculate_atr(self, data, period=14):

        true_ranges = []

        for i in range(1, len(data)):
            high = data['High'].iloc[i]
            # print(high)
            low = data['Low'].iloc[i]
            close = data['Close'].iloc[i - 1]
            true_range = max(abs(high - low), abs(high - close), abs(low - close))        
            true_ranges.append(true_range)
        atr = sum(true_ranges[-period:]) / period

        return atr

    def calc_atr_edition_func(self, main_stake):
        # main_stakee = main_stake.copy()               

        for i, item in enumerate(main_stake):

            klines = None
            atr = None
            custom_period = 1000
            klines = self.get_klines(item["symbol"], custom_period)
            # print(f"klines: {klines}")
            atr = self.calculate_atr(klines)
            # print(f"atr: {atr}")
            if atr:
                main_stake[i]["atr"] = atr 
            else:
                main_stake.pop(i)
            t_random_add = (random.randrange(1, 3) / 2) + (random.randrange(1, 9) / 10)
            time.sleep(t_random_add)

        return main_stake
    
    # ///////////////////////////////////////////////////////////////////////

    def count_multipliter_places(self, number):
        if isinstance(number, (int, float)):
            number_str = str(number)
            if '.' in number_str:
                return len(number_str.split('.')[1])
        return 0

    def calc_qnt_func(self, symbol, price, depo, rounding_type='round'): 
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
            symbol_info = self.get_excangeInfo(symbol)
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")   

        if symbol_info:
            try:
                symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
                # print(symbol_data)
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  
            
        if symbol_data:
            if self.market == 'spot':
                try:
                    tick_size = float(symbol_data['filters'][0]["tickSize"])
                    lot_size_filter = next((f for f in symbol_data.get('filters', []) if f.get('filterType') == 'LOT_SIZE'), None)
                    if lot_size_filter:
                        quantity_precision = -int(math.log10(float(lot_size_filter.get('stepSize', '1'))))
                        print(quantity_precision)
                 
                    min_qnt = float(next((f['minQty'] for f in symbol_data['filters'] if f['filterType'] == 'LOT_SIZE'), 0))
                    max_qnt = float(next((f['maxQty'] for f in symbol_data['filters'] if f['filterType'] == 'LOT_SIZE'), 0))

                except Exception as ex:
                    logging.error(f"An error occurred: {ex}")

                try:
                    price_precision = self.count_multipliter_places(tick_size)                    
                except Exception as ex:
                    print(ex) 

            if self.market == 'futures':
                try:                
                    # tick_size = float(symbol_data['filters'][0]["tickSize"])
                    price_precision = int(symbol_data['pricePrecision'])            
                    quantity_precision = int(symbol_data['quantityPrecision'])                 
                    min_qnt = float(symbol_data['filters'][1]['minQty'])
                    max_qnt = float(symbol_data['filters'][1]['maxQty'])
                except Exception as ex:
                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
                # try:
                #     price_precision = self.count_multipliter_places(tick_size)                    
                # except Exception as ex:
                #     print(ex) 
            
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

        return quantity, recalc_depo, price_precision

    def checkpoint_calc(enter_deFacto_price, atr, q_sl, q_tp, defender, price_precision, static_defender, rounding_type='round'):

        checkpointt, breakpointt = None, None
        try:
            if rounding_type == 'round':
                checkpointt = round(enter_deFacto_price + (defender * atr * q_tp), price_precision)
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
        # try:
        #     if rounding_type == 'round':
        #         breakpointt = round(enter_deFacto_price + (static_defender * defender * atr * q_sl), price_precision)
        # except Exception as ex:
        #     logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

        return checkpointt, breakpointt 
    
    # /////////////////////////////////////////////////////////////////////

    def cleanup_cache(self):
        project_root = os.getcwd()  # Получаем корневую папку проекта
        folders_to_clear = [project_root, "API", "ENGIN", "MONEY", "UTILS"]

        for folder in folders_to_clear:
            folder_path = os.path.join(project_root, folder)
            pycache_path = os.path.join(folder_path, "__pycache__")

            if os.path.exists(pycache_path):
                shutil.rmtree(pycache_path)  

    # /////////////////////////////////////////////////////////////////////

    def stake_generator_func(self, usual_defender_stake):
        
        universal_stake = [
            {            
                "symbol": s,
                "defender": d,
                "enter_deFacto_price": None, 
                "recalc_depo": None,           
                "current_price": None,  
                "in_position": False,         
                "close_position": False,
                "qnt": None, 
                "price_precision": None,  
                # "tick_size": None,
                "atr": None,                  
                "tp_price": None,
                "done_level": 0
        
            }
                for s, d in usual_defender_stake            
        ] 

        return universal_stake
    
    # /////////////////////////////////////////////////////////////////////

    def time_keeper_func(self):
        import pytz
        from datetime import datetime, time
        now = datetime.now()
        desired_timezone = pytz.timezone('Europe/Kiev')
        now_in_desired_timezone = now.astimezone(desired_timezone)
        current_time = now_in_desired_timezone.strftime('%H:%M')
        # print(current_time)
        if time(self.break_time["from"], 0) <= time(int(current_time.split(':')[0]), int(current_time.split(':')[1])) <= time(self.break_time["to"], 0):
            return True
        else:
            return False
        
        # ///////////////////////////////////////////////////////////////////////

    def kline_waiter(self, kline_time, time_frame):
        import time
        wait_time = 0  

        if time_frame == 'm':
            wait_time = ((60*kline_time) - (time.time()%60) + 1)
        elif time_frame == 'h':
            wait_time = ((3600*kline_time) - (time.time()%3600) + 1)
        elif time_frame == 'd':
            wait_time = ((86400*kline_time) - (time.time()%86400) + 1)

        return int(wait_time)  

    # ///////////////////////////////////////////////////////////////////
    def get_current_price(self, symbol):
        method = 'GET'
        current_price = None
        url = self.URL_PATTERN_DICT['current_ptice_url']
        params = {'symbol': symbol}
        try:
            current_price = self.HTTP_request(url, method=method, params=params)    
            current_price = float(current_price["price"])
        except Exception as ex:
            print(ex)

        return current_price  

    def get_current_price_edition_func(self, main_stake):    
        for index, stake in enumerate(main_stake):
            cur_price = None            
            try:
                cur_price = self.get_current_price(stake["symbol"])
                if cur_price:
                    stake["current_price"] = cur_price
                else:
                    main_stake.pop(index)
            except Exception as ex:                
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 


            t_random_add = (random.randrange(1, 3) / 2) + (random.randrange(1, 9) / 10)
            time.sleep(t_random_add)

        return main_stake



# python -m UTILS.wait_candle

# для спот: 
# {'symbol': 'MEMEUSDT', 'status': 'TRADING', 'baseAsset': 'MEME', 'baseAssetPrecision': 8, 'quoteAsset': 'USDT', 'quotePrecision': 8, 'quoteAssetPrecision': 8, 'baseCommissionPrecision': 8, 'quoteCommissionPrecision': 8, 'orderTypes': ['LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'], 'icebergAllowed': True, 'ocoAllowed': True, 'quoteOrderQtyMarketAllowed': True, 'allowTrailingStop': True, 'cancelReplaceAllowed': True, 'isSpotTradingAllowed': True, 'isMarginTradingAllowed': True, 'filters': [{'filterType': 'PRICE_FILTER', 'minPrice': '0.00000100', 'maxPrice': '100.00000000', 'tickSize': '0.00000100'}, {'filterType': 'LOT_SIZE', 'minQty': '1.00000000', 'maxQty': '913205152.00000000', 'stepSize': '1.00000000'}, {'filterType': 'ICEBERG_PARTS', 'limit': 10}, {'filterType': 'MARKET_LOT_SIZE', 'minQty': '0.00000000', 'maxQty': '22348040.90000000', 'stepSize': '0.00000000'}, {'filterType': 'TRAILING_DELTA', 'minTrailingAboveDelta': 10, 'maxTrailingAboveDelta': 2000, 'minTrailingBelowDelta': 10, 'maxTrailingBelowDelta': 2000}, {'filterType': 'PERCENT_PRICE_BY_SIDE', 'bidMultiplierUp': '5', 'bidMultiplierDown': '0.2', 'askMultiplierUp': '5', 'askMultiplierDown': '0.2', 'avgPriceMins': 5}, {'filterType': 'NOTIONAL', 'minNotional': '5.00000000', 'applyMinToMarket': True, 'maxNotional': '9000000.00000000', 'applyMaxToMarket': False, 'avgPriceMins': 5}, {'filterType': 'MAX_NUM_ORDERS', 'maxNumOrders': 200}, {'filterType': 'MAX_NUM_ALGO_ORDERS', 'maxNumAlgoOrders': 5}], 'permissions': ['SPOT', 'MARGIN', 'TRD_GRP_005', 'TRD_GRP_009', 'TRD_GRP_010', 'TRD_GRP_011', 'TRD_GRP_012', 'TRD_GRP_013', 'TRD_GRP_014', 'TRD_GRP_016', 'TRD_GRP_017', 'TRD_GRP_018', 'TRD_GRP_019', 'TRD_GRP_020', 'TRD_GRP_021', 'TRD_GRP_022', 'TRD_GRP_023', 'TRD_GRP_024', 'TRD_GRP_025'], 'defaultSelfTradePreventionMode': 'EXPIRE_MAKER', 'allowedSelfTradePreventionModes': ['EXPIRE_TAKER', 'EXPIRE_MAKER', 'EXPIRE_BOTH']}


# для фьючерсов:
# {'symbol': 'SOLUSDT', 'pair': 'SOLUSDT', 'contractType': 'PERPETUAL', 'deliveryDate': 4133404800000, 'onboardDate': 1569398400000, 'status': 'TRADING', 'maintMarginPercent': '2.5000', 'requiredMarginPercent': '5.0000', 'baseAsset': 'SOL', 'quoteAsset': 'USDT', 'marginAsset': 'USDT', 'pricePrecision': 4, 'quantityPrecision': 0, 'baseAssetPrecision': 8, 'quotePrecision': 8, 'underlyingType': 'COIN', 'underlyingSubType': [], 'settlePlan': 0, 'triggerProtect': '0.0005', 'liquidationFee': '0.020000', 'marketTakeBound': '0.10', 'maxMoveOrderLimit': 10000, 'filters': [{'filterType': 'PRICE_FILTER', 'minPrice': '0.7500', 'tickSize': '0.0100', 'maxPrice': '1261.3700'}, {'filterType': 'LOT_SIZE', 'maxQty': '10000000', 'stepSize': '1', 'minQty': '1'}, {'minQty': '1', 'stepSize': '1', 'filterType': 'MARKET_LOT_SIZE', 'maxQty': '10000000'}, {'limit': 200, 'filterType': 'MAX_NUM_ORDERS'}, {'limit': 10, 'filterType': 'MAX_NUM_ALGO_ORDERS'}, {'filterType': 'MIN_NOTIONAL', 'notional': '5'}, {'multiplierUp': '1.1000', 'multiplierDown': '0.9000', 'multiplierDecimal': '4', 'filterType': 'PERCENT_PRICE'}], 'orderTypes': ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET'], 'timeInForce': ['GTC', 'IOC', 'FOK', 'GTX', 'GTD']}


        

