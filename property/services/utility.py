import time, calendar
from uuid import uuid4

def get_current_timestamp():
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    return f"{time_stamp}{uuid4()}"