from ENGIN.get_sl import SL_CONTROL
from TEMP.orders_templates import ORDERS_TEMPL

class POSITIONS_MONITORINGG(ORDERS_TEMPL, SL_CONTROL):

    def __init__(self) -> None:
        super().__init__()

    def pos_monitoring_func(self, main_stake):
        for i, item in enumerate(main_stake):
            print('hi1')
            main_stake[i] = self.make_market_order_temp_func(item)
            if main_stake[i]["done_level"] == 1:
                print("done_level == 1")
                main_stake[i] = self.sl_strategy_1_func(item)
                print(main_stake[i])
                main_stake[i] = self.tp_sl_make_orders(item)
                print(main_stake[i])

        return main_stake
    