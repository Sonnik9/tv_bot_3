from itertools import accumulate

def asum_counter(total_raport_list):
    # print(total_raport_list)
    win_per = None
    profitt_list = [x['profit'] for x in total_raport_list]
    win_rate = sum([1 for x in profitt_list if x >0])
    lose_rate = sum([1 for x in profitt_list if x <0])
    
    total = sum(profitt_list)
    try:
        win_per = (win_rate * 100)/(win_rate + lose_rate)
    except:
        pass

    cash_flows = list(accumulate(profitt_list))
    max_drawdown = min(cash_flows)
    max_flow_profit = max(cash_flows)

    max_profit_rate = max(profitt_list)
    max_lose_rate = min(profitt_list)

    result = f"Total: {total} $ \nWin_per: {win_per} % \nMax_flow_profit {max_flow_profit} \nMax_drawdown {max_drawdown} \nMax_profit_rate {max_profit_rate} \nMax_lose_rate {max_lose_rate}"

    with open('result.txt', 'w') as txt_file:
        txt_file.write(result) 