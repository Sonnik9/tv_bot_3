from ENGIN.import_e import my_params, make_market_order_temp_func, tp_sl_make_orders, terminate_all_func, pos_cleaner_func, sl_trailing_strategy 
 

async def sl_manager_func(main_stake, step, time_to_check_open_positions, done_flag, finish_flag):

    main_stake_var = main_stake.copy()
    done_flag = False
    # print(f"len(main_stake_var)  {len(main_stake_var)}")
    for i, _ in enumerate(main_stake):                 

        if step == 0:  
            if not main_stake_var[i]["in_position"]:
                main_stake_var[i] = make_market_order_temp_func(main_stake_var[i])  
                if main_stake_var[i]["done_level"] == 1:
                    if my_params.SL_STRATEGY_NUMBER == 1:
                        main_stake_var[i] = tp_sl_make_orders(main_stake_var[i])
        if step == 1:
            if my_params.SL_STRATEGY_NUMBER == 1:
                time_to_check_open_positions += 1
                if time_to_check_open_positions == 31:
                    problem_closing_list = []
                    problem_closing_list = terminate_all_func(main_stake_var)
                    finish_flag = True
                    print(problem_closing_list)
                    print('time_to_check_open_positions_flag = True')
                    main_stake_var, done_flag = pos_cleaner_func(main_stake_var)
                    time_to_check_open_positions = 0
            elif my_params.SL_STRATEGY_NUMBER == 2:
                main_stake_var[i], done_flag, step = sl_trailing_strategy.tailling_sl(main_stake_var[i], step)

    if step == 0:
        main_stake_var = [x for x in main_stake_var if x["done_level"] == 1]
        step = 1

    return main_stake_var, step, time_to_check_open_positions, done_flag, finish_flag
    
