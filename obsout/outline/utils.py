import time
import datetime
import os

def local_datetime(path: str) -> datetime.datetime:
    # seconds = os.path.getmtime(path)
    # t_obj = time.strptime(time.ctime(seconds))
    # iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", t_obj)
    stat = os.stat(path)
    dt = datetime.datetime.utcfromtimestamp(stat.st_mtime)
    return dt