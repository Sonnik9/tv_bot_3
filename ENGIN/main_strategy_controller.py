from pparamss import my_params
from ENGIN.ind_strategy_1 import sigmals_handler_one
from ENGIN.ind_strategy_2 import sigmals_handler_two
from tradingview_ta import *

class STRATEGY_CONTROLLER():

    def __init__(self)-> None:
        pass

    def get_tv_signals(self, top_coins):

        all_coins_indicators = None        
        symbols = [f"BINANCE:{x}" for x in top_coins if x]

        all_coins_indicators = get_multiple_analysis(symbols=symbols,
                            screener='crypto',                    
                            interval=my_params.INTERVAL)
        
        return all_coins_indicators

    def main_strategy_control_func(self, top_coins):
        usual_defender_stake = []
        all_coins_indicators = None
        try:
            all_coins_indicators = self.get_tv_signals(top_coins) 
        except Exception as ex:
            print(ex)  

        if my_params.MAIN_STRATEGY_NUMBER == 1:
            usual_defender_stake = sigmals_handler_one(all_coins_indicators)           
            
        elif my_params.MAIN_STRATEGY_NUMBER == 2:
            # print('dkfjbgv')
            usual_defender_stake = sigmals_handler_two(all_coins_indicators)
        
        return usual_defender_stake

strateg_controller = STRATEGY_CONTROLLER()

