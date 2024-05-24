from db_conn import db_connection
from  train_requests import create_combined_train_entries, CombinedTrainEntry
import sys
from datetime import datetime, timedelta
import time
from db_utility import *
stations: list = []
operators: list = []
has_operators: bool = False
has_stations: bool = False
DB_CONNECTION: db_connection = db_connection()

def truncate_string(s, max_length):
    if len(s) <= max_length:
        return s
    else:
        return s[:max_length]


def update_station_list():
    global has_stations
    if (not has_stations):
        stations_tuple = DB_CONNECTION.execute_query("SELECT STATION.EVA FROM STATION")
        for s in stations_tuple:
            global stations
            stations += s
        has_stations = True

def check_for_new_eva(eva, station_name):
    update_station_list()
    if (eva not in stations): 

        stations.append(eva)
        
        DB_CONNECTION.execute_insert("INSERT INTO STATION (eva, description, city) VALUES (?, ?, ?)", (eva, station_name, station_name))

def update_operator_list():
    global has_operators
    if (not has_operators):
        operators_tuple = DB_CONNECTION.execute_query("SELECT OPERATORS.OPERATOR FROM OPERATORS")
        for o in operators_tuple:
            global operators
            operators += o
        has_operators = True

def check_for_new_operator(type):
    update_operator_list()
    if (type not in operators):

        operators.append(type)

        DB_CONNECTION.execute_insert("INSERT INTO OPERATORS (operator, travel_type, description) VALUES (?, ?, ?)", (type, "unknown", "unknown"))


def evaluate_planned_direction(arrival, departure):

    if ("[NA]" in arrival and "[NA]" in departure):
        raise Exception("Train doesn't depart or arrive")
    if ("[NA]" in arrival and not "[NA]" in departure):
        return 2 # DB direction id for "departing"
    elif ("[NA]" not in arrival and "[NA]" in departure):
        return 1 # DB direction id for "arriving"
    else:
        return 3 # both arriving and departing

def get_last_station(station_name: str, destination: str, direction: int):
    if (direction == 3 or direction == 2):
        station = destination.split("|")
        return station[-1]
    else:
        return station_name

def add_train_to_db(train: CombinedTrainEntry):

    db_id = train.id


    if (train.arrival.isdigit()):
        db_scheduled_arrival = db_time_to_datetime(train.arrival)
    else:
        db_scheduled_arrival = None
    if (train.departure.isdigit()):
        db_scheduled_departure = db_time_to_datetime(train.departure)
    else:
        db_scheduled_departure = None

    db_direction = evaluate_planned_direction(train.arrival, train.departure)

    db_type = train.train_type

    check_for_new_operator(db_type)

    db_alias = train.train_alias

    db_train_number = train.train_number

    db_planned_platform = train.platform

    db_station = train.station_eva

    db_scheduled_origin = train.origin_stations
    db_scheduled_destination = train.destination_stations

    db_last_station = get_last_station(train.station_name, db_scheduled_destination, db_direction)

    DB_CONNECTION.execute_insert("INSERT IGNORE INTO TRAIN \
                                 (ID, TYPE, ALIAS, TRAIN_NUMBER, PLATFORM, STATION, SCHEDULED_DEPARTURE, SCHEDULED_ARRIVAL, SCHEDULED_ORIGIN, SCHEDULED_DESTINATION, DIRECTION, LAST_STATION)\
                                  VALUES\
                                  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\
                                 ", (db_id, db_type, db_alias, db_train_number, db_planned_platform, db_station, db_scheduled_departure, db_scheduled_arrival, truncate_string(db_scheduled_origin, 800), truncate_string(db_scheduled_destination, 800), db_direction, db_last_station))
    

    delay_id = db_id

    if ("cancel" in train.actual_departure or "cancel" in train.actual_arrival):
        delay_current_departure = None
        delay_current_arrival = None
        delay_status = 2
    else:
        delay_status = 1
        if (train.actual_arrival.isdigit()):
            delay_current_arrival = db_time_to_datetime(train.actual_arrival)
        else:
            delay_current_arrival = db_scheduled_arrival

        if (train.actual_departure.isdigit()):
            delay_current_departure = db_time_to_datetime(train.actual_departure)
        else:
            delay_current_departure = db_scheduled_departure

    if ("[NA]" in train.actual_origin_stations):
        delay_current_origin = db_scheduled_origin
    else:
        delay_current_origin = train.actual_origin_stations

    if ("[NA]" in train.actual_destination_stations):
        delay_current_destination = db_scheduled_destination
    else:
        delay_current_destination = train.actual_destination_stations

    delay_info = train.info

    if (db_direction == 1):
        if (delay_status == 2):
            delay_current_last_station = "canceled"
        elif (delay_current_origin.split("|")[-1] == db_scheduled_origin.split("|")[-1]):
            delay_current_last_station = train.station_name
        else:
            delay_current_last_station = get_last_station("", delay_current_origin, 2)
    else:
        if (delay_status == 2):
            delay_current_last_station = "canceled"
        elif (delay_current_destination.split("|")[-1] == db_scheduled_destination.split("|")[-1]):
            delay_current_last_station = db_last_station
        else:
            delay_current_last_station = get_last_station("", delay_current_destination, 2)

    sql_query = """
    INSERT INTO DELAY
    (TRAIN, CURRENT_ARRIVAL, CURRENT_DEPARTURE, CURRENT_ORIGIN, CURRENT_DESTINATION, INFO, STATUS, CURRENT_LAST_STATION)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON DUPLICATE KEY UPDATE
    CURRENT_ARRIVAL = VALUES(CURRENT_ARRIVAL),
    CURRENT_DEPARTURE = VALUES(CURRENT_DEPARTURE),
    CURRENT_ORIGIN = VALUES(CURRENT_ORIGIN),
    CURRENT_DESTINATION = VALUES(CURRENT_DESTINATION),
    INFO = VALUES(INFO),
    STATUS = VALUES(STATUS),
    CURRENT_LAST_STATION = VALUES(CURRENT_LAST_STATION)
    """

    DB_CONNECTION.execute_insert(sql_query,\
                                (db_id, delay_current_arrival, delay_current_departure, truncate_string(delay_current_origin, 800), truncate_string(delay_current_destination, 800), delay_info, delay_status, delay_current_last_station))
    
    # if (db_direction == 1 or db_direction == 3):
    #    DB_CONNECTION.execute_insert("INSERT INTO ARRIVAL_TIMES (TRAIN, TIME_ADDED, TIME) VALUES (?, ?, ?)",\
    #                                 (db_id, datetime.now(), delay_current_arrival))
    # if (db_direction == 2 or db_direction == 3):
    #     DB_CONNECTION.execute_insert("INSERT INTO DEPARTURE_TIMES (TRAIN, TIME_ADDED, TIME) VALUES (?, ?, ?)",\
    #                                  (db_id, datetime.now(), delay_current_departure))
    

    


    
    
    