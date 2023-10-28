from imports__ import my_params, get_apii, os, math, inspect, logging
import shutil

if not os.path.exists("UTILS"):
    os.makedirs("UTILS")

log_file = "UTILS/calc_qnt.log"

logging.basicConfig(filename=log_file, level=logging.ERROR)
current_file = os.path.basename(__file__)
