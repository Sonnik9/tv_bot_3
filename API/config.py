import os
from dotenv import load_dotenv
from pparamss import my_params
import hmac 
import hashlib 
import requests
# from requests.exceptions import HTTPError
import time

import logging
import os
import inspect

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

load_dotenv()

class Configg():

    header = None

    def __init__(self) -> None:
        if not my_params.TEST_FLAG:
            self.api_key  = os.getenv("BINANCE_API_PUBLIC_KEY_REAL", "")
            self.api_secret = os.getenv("BINANCE_API_PRIVATE_KEY_REAL", "")
        else:
            self.api_key  = os.getenv("BINANCE_API_PUBLIC_KEY_FUTURES_TEST", "")
            self.api_secret = os.getenv("BINANCE_API_PRIVATE_KEY_FUTURES_TEST", "")
        # print(self.api_key)
        # print(self.api_secret)
        self.header = {
            'X-MBX-APIKEY': self.api_key
        }

    def get_signature(self, params):
        try:
            params['timestamp'] = int(time.time() *1000)
            params_str = '&'.join([f'{k}={v}' for k,v in params.items()])
            hash = hmac.new(bytes(self.api_secret, 'utf-8'), params_str.encode('utf-8'), hashlib.sha256)        
            params['signature'] = hash.hexdigest()
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

        return params
   
    def HTTP_request(self, url, **kwards):

        response = None
        decimal = 2

        for i in range(2):
            try:
                response = requests.request(url=url, **kwards)
                if response.status_code == 200:
                    break
                else:
                    time.sleep((i+1)* decimal)              
   
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
                time.sleep((i+1)* decimal)                
                
        try:
            response = response.json()
        except:
            pass

        return response

# python -m API.config
