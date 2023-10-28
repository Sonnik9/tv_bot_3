from pparamss import my_params

import asyncio
import aiohttp
import json
import math
from API.get_api import get_apii
from API.post_api import post_apii
from API.utils_api import utils_apii

from ENGIN.main_strategy_controller import strateg_controller  
from ENGIN.sl_strategy_controller import sl_manager_func  

from UTILS.waiting_candle import kline_waiter
from UTILS.clean_cashe import cleanup_cache
from UTILS.calc_atr import calc_atr_edition_func
from UTILS.time_keeper import time_keeper_func
from UTILS.stake_generator import stake_generator_func
from MONEY.asumm import asum_counter
from PROCESS.websockett import price_monitoring

import sys 

import logging
import os
import inspect

logging.basicConfig(filename='API/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)