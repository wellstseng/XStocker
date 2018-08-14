from datetime import timedelta, date
import datetime
import os


def daterange(start_date, end_date):
    for n in range(int ((start_date - end_date).days)):
        yield start_date - timedelta(n)

def get_latest_file_date(relative_path):
    p = os.path.abspath(relative_path)
    max_date = None
    for  _, _, filenames in os.walk(p):
        for file_name in filenames:            
            if ".csv" in file_name:
                d = int(file_name.replace(".csv", ""))
                if max_date == None or max_date < d:
                    max_date = d
    if max_date == None:
        return "2000/1/1"
    d = datetime.datetime.strptime(str(max_date), "%Y%m%d").date().strftime("%Y/%m/%d")
    return d

def get_abs_path(relative_path:str):
    return os.path.abspath(relative_path)
