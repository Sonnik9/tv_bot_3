import time

def kline_waiter(kline_time, time_frame):
    wait_time = 0  

    if time_frame == 'm':
        wait_time = ((60*kline_time) - (time.time()%60) + 1)
    elif time_frame == 'h':
        wait_time = ((3600*kline_time) - (time.time()%3600) + 1)
    elif time_frame == 'd':
        wait_time = ((86400*kline_time) - (time.time()%86400) + 1)

    return int(wait_time)

# python -m UTILS.wait_candle