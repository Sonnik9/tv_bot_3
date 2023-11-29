from ENGIN.get_signals import IND_STRATEGY_CONTROLLER
import logging, os, inspect

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

class ORDERS_TEMPL(IND_STRATEGY_CONTROLLER):

    def __init__(self) -> None:
        super().__init__()

    def make_market_order_temp_func(self, itemm):
        # print('kxbvjkbvkdbvjkbv')
        # itemm = item.copy()
        symbol = itemm["symbol"]
        enter_deJure_price = itemm["current_price"]

        try:                    
            itemm['qnt'], itemm["recalc_depo"], itemm["price_precision"] = self.calc_qnt_func(symbol, enter_deJure_price, self.DEPO) 
            print(itemm['qnt'], itemm["recalc_depo"], itemm["price_precision"])           
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        if itemm['qnt']:
            print('aejjhhfbjhdfvjhfjhdfjhdfjhf')
            open_market_order = None
            is_closing = 1
            success_flag = False
            market_type = 'MARKET'
            target_price = None
            try:          
                open_market_order, success_flag = self.make_order(itemm, is_closing, target_price, market_type)
                print(f"str74:  {open_market_order}") 
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex} \n {open_market_order}")
            if success_flag:                
                try:
                    itemm["enter_deFacto_price"] = self.get_DeFacto_price(symbol)
                    # print(f'str73 {symbol}:  {itemm["enter_deFacto_price"]}  (defacto_prtice)')
                    print(itemm["enter_deFacto_price"])
                    itemm["done_level"] = 1
                    itemm["in_position"] = True
                    
                except Exception as ex:
                    logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            # else:
            #     return None

        return itemm
    

    def tp_sl_make_orders(self, itemm):
        # itemm = item.copy()
        is_closing = -1   

        try: 
            # tp static order /////////////////////////////////////////////////////        
            success_flag = False   
            target_price = itemm["tp_price"]
            market_type = 'TAKE_PROFIT_MARKET'            
            open_static_tp_order, success_flag = self.make_order(itemm, is_closing, target_price, market_type)
            
            if success_flag:                                     
                itemm["done_level"] = 2            
        
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}\n {open_static_tp_order}")
            
        return itemm



