from API.utils_api import UTILS_APII
import logging, os, inspect
import math
import os, shutil

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
            low = data['Low'].iloc[i]
            close = data['Close'].iloc[i - 1]
            true_range = max(abs(high - low), abs(high - close), abs(low - close))        
            true_ranges.append(true_range)
        atr = sum(true_ranges[-period:]) / period

        return atr

    def calc_atr_edition_func(self, main_stake):
        main_stakee = main_stake.copy()               

        for i, item in enumerate(main_stake):

            klines = None
            atr = None
            klines = self.get_klines(item["symbol"])
            atr = self.calculate_atr(klines)
            if atr:
                main_stakee[i]["atr"] = atr 
            else:
                main_stakee.pop(i)

        return main_stakee
    
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
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  
            
        if symbol_data:
            if self.market == 'futures':
                try:                
                    tick_size = float(symbol_data['filters'][0]["tickSize"])
                    price_precision = int(symbol_data['pricePrecision'])            
                    quantity_precision = int(symbol_data['quantityPrecision'])                 
                    min_qnt = float(symbol_data['filters'][1]['minQty'])
                    max_qnt = float(symbol_data['filters'][1]['maxQty'])
                except Exception as ex:
                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
            try:
                tick_size = self.count_multipliter_places(tick_size)
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

    def checkpoint_calc(enter_deFacto_price, atr, q_sl, q_tp, defender, price_precision, static_defender, tick_size, rounding_type='round'):

        checkpointt, breakpointt = None, None
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
                "tick_size": None,
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

# python -m UTILS.wait_candle


        

