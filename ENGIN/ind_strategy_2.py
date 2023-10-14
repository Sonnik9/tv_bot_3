from pparamss import my_params

def bunch_handler_func(close_price, upper, lower, macd, signal, rsi, fastk, slowk, current_bunch):
    b_bband_q, s_bband_q, b_rsi_lev, s_rsi_lev, b_macd__q, s_macd_q, b_stoch_q, s_stoch_q = 1, 1, 45, 55, 1, 1, 23, 77
    # 33, 67
    # 25, 75

    signals_sum = []
    buy_signals_counter = 0
    sell_signals_counter = 0
    buy_total_signal, sell_total_signal = False, False

    if 'bband_flag' in current_bunch:             
        buy_bband_signal = close_price >= lower * b_bband_q
        sell_bband_signal = close_price <= upper * s_bband_q
        signals_sum.append((buy_bband_signal, sell_bband_signal))

    if 'macd_lite_flag' in current_bunch:              
        buy_lite_macd_signal = macd > signal * b_macd__q
        sell_lite_macd_signal = macd < signal * s_macd_q
        signals_sum.append((buy_lite_macd_signal, sell_lite_macd_signal))

    if 'macd_strong_flag' in current_bunch:            
        buy_strong_macd_signal = (macd > signal * b_macd__q) & (macd < 0)
        sell_strong_macd_signal = (macd < signal * s_macd_q) & (macd > 0)
        signals_sum.append((buy_strong_macd_signal, sell_strong_macd_signal))

    if 'rsi_flag' in current_bunch:                
        buy_rsi_signal = rsi <= b_rsi_lev
        sell_rsi_signal = rsi >= s_rsi_lev
        signals_sum.append((buy_rsi_signal, sell_rsi_signal))

    if 'stoch_flag' in current_bunch:
        buy_stoch_signal = (fastk > slowk) & (fastk < b_stoch_q)
        sell_stoch_signal = (fastk < slowk) & (fastk > s_stoch_q)
        signals_sum.append((buy_stoch_signal, sell_stoch_signal))

    for buy_signal, sell_signal in signals_sum:
        if buy_signal:
            buy_signals_counter += 1
        if sell_signal:
            sell_signals_counter += 1

    if 'U' in current_bunch:
        if buy_signals_counter == len(signals_sum):
            buy_total_signal = True 
    if 'D':
        if sell_signals_counter == len(signals_sum):
            sell_total_signal = True
    if 'F' in current_bunch:
        if buy_signals_counter == len(signals_sum):
            buy_total_signal = True 
        if sell_signals_counter == len(signals_sum):
            sell_total_signal = True

    return buy_total_signal, sell_total_signal

def trends_defender(close_price, adx, sma):

    if close_price > sma and adx > 25:
        return "U"
    elif close_price < sma and adx > 25:
        return "D"
    else:
        return "F"

def sigmals_handler_two(all_coins_indicators): 
    
    close_price, adx, sma, upper, lower, macd, signal, rsi, fastk, slowk = None, None, None, None, None, None, None, None, None, None
    atr = None
    orders_stek = []
     
    for _, item in all_coins_indicators.items():
        try: 
            # print(item.indicators)
            close_price = item.indicators['close']           
            high = item.indicators['high']
            low = item.indicators['low']            
            adx = item.indicators["ADX"] 
            sma = item.indicators["SMA20"] 
            upper, lower = item.indicators["BB.upper"], item.indicators["BB.lower"] 
            macd, signal = item.indicators["MACD.macd"], item.indicators["MACD.signal"]     
            rsi = item.indicators["RSI"]
            fastk, slowk = item.indicators["Stoch.K"], item.indicators["Stoch.D"]
            atr = (sum([abs(high - low), abs(high - close_price), abs(low - close_price)]) / 3) * 3
            indicator = item.symbol            
        except Exception as ex:
            pass

        buy_signal, sell_signal = False, False
        trende_sign = trends_defender(close_price, adx, sma)
                                    
        if trende_sign == 'U':
            if my_params.BUNCH_VARIANT == 1:
                current_bunch = ['bband_flag', 'macd_strong_flag', 'U']
            elif my_params.BUNCH_VARIANT == 2:
                current_bunch = ['bband_flag', 'macd_lite_flag', 'rsi_flag', 'U']
            # current_bunch = ['bband_flag', 'macd_lite_flag', 'U']            
            
        if trende_sign == 'D':
            if my_params.BUNCH_VARIANT == 1:
                current_bunch = ['bband_flag', 'macd_strong_flag', 'D']
            elif my_params.BUNCH_VARIANT == 2:
                current_bunch = ['bband_flag', 'macd_lite_flag', 'rsi_flag', 'D']
            # current_bunch = ['bband_flag', 'macd_lite_flag', 'D']
            
            
        if trende_sign == 'F':
            if my_params.BUNCH_VARIANT == 1:               
                current_bunch = ['macd_strong_flag', 'stoch_flag', 'F']
            elif my_params.BUNCH_VARIANT == 2:
                current_bunch = ['macd_lite_flag', 'stoch_flag', 'F']

        buy_signal, sell_signal = bunch_handler_func(close_price, upper, lower, macd, signal, rsi, fastk, slowk, current_bunch)

        if buy_signal:
            orders_stek.append((indicator, 1, atr))
        # elif sell_signal and my_params.MARKET == 'futures':
        elif sell_signal:        
            orders_stek.append((indicator, -1, atr))

    return orders_stek