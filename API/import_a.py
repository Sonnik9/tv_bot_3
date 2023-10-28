from imports__ import my_params, logging, os, inspect, get_apii, post_apii
from dotenv import load_dotenv
from API.config import Configg
import pandas as pd
import time
import hmac
import hashlib
import requests

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

# except Exception as ex:
#     logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 