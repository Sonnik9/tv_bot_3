from pparamss import my_params 
from API.get_api import get_apii

def calculate_atr(data, period=my_params.ATR_PERIOD):

    true_ranges = []

    for i in range(1, len(data)):
        high = data['High'].iloc[i]
        low = data['Low'].iloc[i]
        close = data['Close'].iloc[i - 1]
        true_range = max(abs(high - low), abs(high - close), abs(low - close))        
        true_ranges.append(true_range)
    atr = sum(true_ranges[-period:]) / period

    return atr

def calc_atr_edition_func(main_stake):
    main_stakee = main_stake.copy()               

    for i, item in enumerate(main_stake):

        klines = None
        atr = None
        klines = get_apii.get_klines(item["symbol"])
        atr = calculate_atr(klines)
        if atr:
            main_stakee[i]["atr"] = atr 
        else:
            main_stakee.pop(i)

    return main_stakee

