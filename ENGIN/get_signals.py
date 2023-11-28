from tradingview_ta import *
from API.utils_api import UTILS_APII

class IND_STRATEGY_CONTROLLER(UTILS_APII):

    def __init__(self)-> None:
        super().__init__()

    def get_tv_signals(self, top_coins):

        all_coins_indicators = None        
        symbols = [f"BINANCE:{x}" for x in top_coins if x]

        all_coins_indicators = get_multiple_analysis(symbols=symbols,
                            screener='crypto',                    
                            interval=self.INTERVAL)
        
        return all_coins_indicators
    
    def tv_sigmals_handler(self, all_coins_indicators):

        orders_stek = []

        for _, item in all_coins_indicators.items():
            recommendation = None
            indicator = None
            try:
                indicator = item.symbol
                recommendation = item.summary["RECOMMENDATION"]
            except Exception as ex:
                continue
            if (recommendation == 'STRONG_BUY'): #or (recommendation == 'BUY'):
                orders_stek.append((indicator, 2))          

            elif (recommendation == 'STRONG_SELL'): #or (recommendation == 'SELL'):     
                orders_stek.append((indicator, 1))             

        return orders_stek 
    
    def ind_strategy_control_func(self, top_coins):
        usual_defender_stake = []
        all_coins_indicators = None
        try:
            all_coins_indicators = self.get_tv_signals(top_coins) 
        except Exception as ex:
            print(ex)  

        usual_defender_stake = self.tv_sigmals_handler(all_coins_indicators)           
        
        return usual_defender_stake

# strateg_controller = STRATEGY_CONTROLLER()

