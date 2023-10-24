
def calculate_atr(data, period=14):
    # print('hi')
    true_ranges = []
    # print(data)
    for i in range(1, len(data)):
        # try:
        high = data['High'].iloc[i]
        low = data['Low'].iloc[i]
        close = data['Close'].iloc[i - 1]
        true_range = max(abs(high - low), abs(high - close), abs(low - close))        
        true_ranges.append(true_range)
    atr = sum(true_ranges[-period:]) / period
    # print(atr)

    return atr
