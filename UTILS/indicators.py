
def calculate_atr(data, period=14):
    true_ranges = []

    for i in range(1, len(data)):
        high = data['High'].iloc[i]
        low = data['Low'].iloc[i]
        close = data['Close'].iloc[i - 1]

        true_range = max(high - low, abs(high - close), abs(low - close))
        true_ranges.append(true_range)

    atr = sum(true_ranges[:period]) / period

    return atr
