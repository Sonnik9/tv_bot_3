from tradingview_ta import *
# from pparamss import my_params

def sigmals_handler_one(all_coins_indicators):

    orders_stek = []
    recommendation = None
    indicator = None

    for _, item in all_coins_indicators.items():
        try:
            close_price = item.indicators['close']           
            high = item.indicators['high']
            low = item.indicators['low'] 
            indicator = item.symbol
            recommendation = item.summary["RECOMMENDATION"]
            atr = (sum([abs(high - low), abs(high - close_price), abs(low - close_price)]) / 3) * 3
            # atr_a = (max(abs(high - low), abs(high - close_price), abs(low - close_price))) * 1.8
        except Exception as ex:
            pass
            
        if recommendation == 'STRONG_BUY':
            try:
                orders_stek.append((indicator, 1, atr))          
            except:
                pass
        # elif recommendation == 'STRONG_SELL' and my_params.MARKET == 'futures':
        elif recommendation == 'STRONG_SELL':  
            try:          
                orders_stek.append((indicator, -1, atr))             
            except:
                pass

    return orders_stek 


