from pparamss import my_params

def stake_generator_func(usual_defender_stake):
    
    universal_stake = [
        {            
            "symbol": s,
            "defender": d,
            "enter_deFacto_price": None, 
            "recalc_depo": None,           
            "current_price": None,  
            "in_position": False,         
            "close_position": False,
            "qnt": None, 
            "price_precision": None,  
            "tick_size": None,
            "atr": None,           
            "last_sl_order_id": None,           
            "static_tp_price": None,
            "static_sl_price": None,
            "checkpointt_flag": False,
            "checkpointt": None,
            "breakpointt": None,
            "trailing_sl_levels": my_params.TABULA_SL_TP_POINTS,
            "statik_sl": my_params.STATIC_SL_Q,
            "statik_tp": my_params.STATIC_TP_Q,
            "done_level": 0
            # "approximate_profit": None,
            # "in_position": False,  
            # "atr_aprox": atr_aprox,
            # "rra": rra,         
        }
            for s, d, atr_aprox, rra in usual_defender_stake            
    ] 

    return universal_stake