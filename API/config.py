import os
from dotenv import load_dotenv
from pparamss import my_params
import hmac 
import hashlib 
import requests
import time

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

        self.header = {
            'X-MBX-APIKEY': self.api_key
        }

    def get_signature(self, params):
        
        params['timestamp'] = int(time.time() *1000)
        params_str = '&'.join([f'{k}={v}' for k,v in params.items()])
        hash = hmac.new(bytes(self.api_secret, 'utf-8'), params_str.encode('utf-8'), hashlib.sha256)        
        params['signature'] = hash.hexdigest() 

        return params
        
    def HTTP_request(self, url, **kwards):

        response = None

        for _ in range(2):
            try:
                response = requests.request(url=url, **kwards)
                response = response.json()
                break
            except Exception as ex:
                time.sleep(2)
                print(f"Config_47str:  {ex}") 
                continue

        return response

# python -m API.config
