from API.utils_api import utils_apii

def average_closer_func(main_stake, ready_to_close_list):
    
    main_stake_var = main_stake.copy()
    good_closed_by_market_symbol_list = []
    problem_to_closing_by_market_symbol_list = []    
    good_closed_by_market_symbol_list, problem_to_closing_by_market_symbol_list = utils_apii.try_to_close_by_market_open_position_by_stake(ready_to_close_list)
    for i, _ in enumerate(main_stake):
        if main_stake_var[i]["symbol"] in good_closed_by_market_symbol_list:
            main_stake_var[i]["close_position"] = True     

    return main_stake_var, problem_to_closing_by_market_symbol_list