
class SL_CONTROL():
    
    def __init__(self) -> None:
        pass

    def sl_strategy_1_func(self, item):  

        last_atr = item["atr"]
        slatr = 1.2*last_atr  
        last_close_price = item["enter_deFacto_price"]      

        if item["defender"]== 1:
            item["tp_price"] = round((last_close_price + slatr), item["price_precision"])
            
        elif item["defender"] == -1:
            item["tp_price"] = round((last_close_price - slatr), item["price_precision"])
                    
        return item

