
class SL_CONTROL():
    
    def __init__(self) -> None:
        pass

    def sl_strategy_1_func(self, main_steak):    
        
        for i in range(len(main_steak)):
            last_atr = main_steak["atr"].iloc[i]
            slatr = 1.2*last_atr  
            last_close_price = main_steak["enter_deFacto_price"].iloc[i]      

            if main_steak["defender"].iloc[i] == 2:
                main_steak["tp_price"][i] = last_close_price + slatr
            elif main_steak["defender"].iloc[i] == 1:
                main_steak["tp_price"][i] = last_close_price - slatr
                    
        return main_steak

