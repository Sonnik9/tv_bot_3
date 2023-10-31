from pparamss import my_params
import pytz
from datetime import datetime, time

def time_keeper_func():
    now = datetime.now()
    desired_timezone = pytz.timezone('Europe/Kiev')
    now_in_desired_timezone = now.astimezone(desired_timezone)
    current_time = now_in_desired_timezone.strftime('%H:%M')
    print(current_time)
    if time(my_params.REST_TIME["from"], 0) <= time(int(current_time.split(':')[0]), int(current_time.split(':')[1])) <= time(my_params.REST_TIME["to"], 0):
        return True
    else:
        return False