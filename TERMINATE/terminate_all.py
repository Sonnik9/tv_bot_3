from imports__ import get_apii, utils_apii
from API.delete_api import delete_apii

def terminate_all_func(main_stake):
    
    problem_to_closing_by_market_list = []
    # current_position_symbol_list = [x["symbol"] for x in main_stake_var]
    cancel_all_orders_answer = delete_apii.cancel_all_open_orders()
    problem_to_closing_by_market_list = utils_apii.try_to_close_by_market_all_open_positions(main_stake)

    return problem_to_closing_by_market_list


