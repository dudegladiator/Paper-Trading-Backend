import time
import datetime
from pytz import timezone

def get_current_time_IST():
    ist_timezone = timezone('Asia/Kolkata')
    current_time_ist = datetime.datetime.now(tz=ist_timezone)
    return current_time_ist

if __name__ == '__main__':
    print(get_current_time_IST() + + datetime.timedelta(days=30))