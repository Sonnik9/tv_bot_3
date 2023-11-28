from ENGIN.get_signals import IND_STRATEGY_CONTROLLER 
from ENGIN.get_sl import SL_CONTROL
from TEMP.orders_templates import ORDERS_TEMPL
from UTILS.main_utils import MAIN_UTILSS

class POSITIONS_MONITORINGG(IND_STRATEGY_CONTROLLER, SL_CONTROL, ORDERS_TEMPL, MAIN_UTILSS):

    def __init__(self) -> None:
        super().__init__()

    def pos_monitoring_func(self, main_stake):
        pass
        # inn = self.INTERVAL
    