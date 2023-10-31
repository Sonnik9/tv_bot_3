from API.utils_api import utils_apii
from API.delete_api import delete_apii

def terminate_all_func(main_stake):
    
    succes_closed_symbol_list, dont_closed_symbol_list = [], []   
    succes_closed_symbol_list, dont_closed_symbol_list = utils_apii.try_to_close_by_market_all_open_positions(main_stake)
    cancel_all_orders_answer = delete_apii.cancel_all_open_orders()

    return succes_closed_symbol_list, dont_closed_symbol_list


