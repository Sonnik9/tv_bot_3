# # import random

# # for i in range(9):
# #     c = (random.randrange(1,3)/2) + (random.randrange(1,9)/10)
# #     print(c)

# # import math

# # c = -int(math.log10(0.14895000))

# # print(c)

# import math

# # Предположим, что lot_size_filter['stepSize'] равен '0.001'
# lot_size_filter = {'filterType': 'LOT_SIZE', 'stepSize': '0.001'}

# # Вычисляем quantity_precision
# quantity_precision = -round(math.log10(0.001))

# # Выводим результат
# print(quantity_precision)

# def count_multipliter_places(number):
#     if isinstance(number, (int, float)):
#         number_str = str(number)
#         if '.' in number_str:
#             return len(number_str.split('.')[1])
#     return 0
# number = 0.001
# c = count_multipliter_places(number)
# print(c)



