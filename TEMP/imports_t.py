from imports__ import my_params, logging, os, inspect, post_apii, get_apii
from UTILS.calc_qnt import checkpoint_calc, calc_qnt_func

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)
