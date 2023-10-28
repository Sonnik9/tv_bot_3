# from binance.client import Client

# # Replace with your Binance API key and secret
# BINANCE_API_PUBLIC_KEY_FUTURES_TEST = "96f214ce691b0dd8fc65b23002ee4e5ce0b55684598645c2eb2d0a819a6d387a" # test
# BINANCE_API_PRIVATE_KEY_FUTURES_TEST = "46e1372c84151cd7d486a4734cc21023ba1724d067b5967ce48ce769025cf0d2" # test

# api_key = "96f214ce691b0dd8fc65b23002ee4e5ce0b55684598645c2eb2d0a819a6d387a"
# api_secret = "46e1372c84151cd7d486a4734cc21023ba1724d067b5967ce48ce769025cf0d2"

# # Initialize the Binance client
# client = Client(api_key, api_secret, testnet=True)

# # Define the order parameters
# symbol = 'BTCUSDT'  # The trading pair symbol
# quantity = 0.001   
#    # The quantity to buy or sell
# atr = 475
# enter_price = 31000 
# callback_rate = 1.0 # The callback rate for the trailing stop (1.0% in this example)
# callback_rate =  round((int(atr/1.618) * 100)/enter_price, 1)
# precessionPrice = 2
# stopPrice = round(enter_price - (atr * 1.618), precessionPrice)
# # print(stopPrice)

# # print(callback_rate)

# # Create a MARKET order
# order = client.create_order(
#     symbol=symbol,
#     side= 'BUY',  # Replace with BUY if you want to buy
#     type='MARKET',
#     quantity=quantity,

# )

# print(order)
# import time
# # Create a TRAILING_STOP_MARKET order
# time.sleep(2)
# order = client.create_order(
#     symbol=symbol,
#     side= 'SELL',  # Replace with BUY if you want to buy
#     type='TRAILING_STOP_MARKET',
#     quantity=quantity,
# #     activationPrice=None,  # Optional: The activation price
# #     stopPrice= stopPrice,        # Optional: The initial stop price
# #     callbackRate=callback_rate
# # )

# # print(order)

# def count_multipliter_places(number):
#     if isinstance(number, (int, float)):
#         number_str = str(number)
#         if '.' in number_str:
#             return len(number_str.split('.')[1])
#     return 0

# # a = 1.2378347683478
# # b = 0.1 
# # q = count_multipliter_places(b)

# # c = round(a,q)
# # print(c)

# from decimal import Decimal, ROUND_HALF_UP
# import math

# tick_size = 0.001
# d = 5.12656748759348593457893048573048573048957
# r = 5.12656748759348593457893048573048573048957
# c = 5.12656748759348593457893048573048573048957
# f = 5.12656748759348593457893048573048573048957
# value = Decimal(str(d))
# rounded_value = value.quantize(Decimal(str(tick_size)), rounding=ROUND_HALF_UP)
# print(f"decimal:  {rounded_value}")
# # //////////////////////////////////////////////////
# tick_size = count_multipliter_places(tick_size) 
# r = round(r, tick_size)
# print(f"round:  {r}")
# # //////////////////////////////////////////////////
# c = math.ceil(c * 10 ** tick_size) / (10 ** tick_size)
# print(f"ceil:  {c}")
# print(f"tick_size:  {tick_size}")

# f = math.floor(f * 10 ** tick_size) / (10 ** tick_size)
# print(f"floor:  {f}")
# print(f"tick_size:  {tick_size}")


