from datetime import datetime, timedelta

def current_date_to_string():
    now = datetime.now()
    return(now.strftime("%Y%m%d"))[2:]

def current_hour_to_string():
    now = str(datetime.now().hour)
    if len(now) == 1:
        now = "0" + now
    return(now)

def subtract_hour_from_string(hour: str, sub: int):
    hour = int(hour)
    hour = str((hour - sub) % 24)
    if len(hour) == 1:
        hour = "0" + hour
    return hour

def add_hour_from_string(hour: str, add: int):
    hour = int(hour)
    hour = str((hour + add) % 24)
    if len(hour) == 1:
        hour = "0" + hour
    return hour

def yesterday_date_to_string():
    time = datetime.now()
    time = time - timedelta(days=1)
    return(time.strftime("%Y%m%d"))[2:]

def tomorrow_date_to_string():
    time = datetime.now()
    time = time + timedelta(days=1)
    return(time.strftime("%Y%m%d"))[2:]

def db_time_to_datetime(db_time):
    db_time = int(db_time)
    # bsp.: 2311271637 = 2023-11-27 16:37
    jahr = db_time // 100000000
    monat = (db_time // 1000000) % 100
    tag = (db_time // 10000) % 100
    stunde = (db_time // 100) % 100
    minute = db_time % 100

    return datetime(2000 + jahr, monat, tag, stunde, minute)

def subtract_hours_from_api_datetime(date: str, hour: str, sub: int):
    if (sub > 23):
        raise Exception("subtraction of more than 23 hours are not supported")
    res_hour = subtract_hour_from_string(hour, sub)
    res_date = date
    if (int(res_hour) > int(hour)):
        res_date = yesterday_date_to_string()
    return (res_date, res_hour)

def create_time_window(date: str, hour: str, look_back: int):
    datetime_list: list = []
    for t in range(0, look_back + 1):
        datetime_list.append(subtract_hours_from_api_datetime(date, hour, t))
    return datetime_list