import http.client
import xml.etree.ElementTree as ET
from datetime import datetime
from train_data import *
from db_utility import current_date_to_string, current_hour_to_string
client_id = "CLIENT ID"
secret = "CLIENT SECRET"
DEBUG : bool = True
import time
import message_logger

def combine_entries(delayed_entries, scheduled_entries):
    combined_entries = []
    found = False
    for scheduled_entry in scheduled_entries: 
        for delayed_entry in delayed_entries:
            if delayed_entry.id == scheduled_entry.id:
                combined_entry = CombinedTrainEntry(scheduled_entry, delayed_entry)
                combined_entries.append(combined_entry)
                found = True
                break  
        if not found:
            combined_entries.append(CombinedTrainEntry(scheduled_entry))
        found = False

    return combined_entries

headers = {
    'DB-Client-Id': client_id,
    'DB-Api-Key': secret,
    'accept': "application/xml"
}

def request_fchg(eva):
    conn = http.client.HTTPSConnection("apis.deutschebahn.com")
    message_logger.log_normal(str(datetime.now()) + f" /db-api-marketplace/apis/timetables/v1/fchg/{eva}")
    conn.request("GET", f"/db-api-marketplace/apis/timetables/v1/fchg/{eva}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data.decode("utf-8")


def request_plan(eva, date, hour):
    conn = http.client.HTTPSConnection("apis.deutschebahn.com")
    message_logger.log_normal(str(datetime.now()) + f" /db-api-marketplace/apis/timetables/v1/plan/{eva}/{date}/{hour}")
    conn.request("GET", f"/db-api-marketplace/apis/timetables/v1/plan/{eva}/{date}/{hour}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data.decode("utf-8")

def create_delayed_train_entries(eva):
    root = ET.fromstring(request_fchg(eva))
    timetable_entries = [DelayedTrainEntry(s) for s in root.findall(".//s")]
    ret = []
    for te in timetable_entries:
        if (te.id == "id"):
            return ret
        ret.append(te)
    return ret


def get_station_name_from_eva(eva):
    root = ET.fromstring(request_plan(eva, current_date_to_string(), current_hour_to_string()))
    station = root.get('station')
    if not station == None:
        return station
    else:
        return "failed"

def create_scheduled_train_entries(eva, date= -1, hour= -1):
    if (date == -1):
        date = current_date_to_string()
    if (hour == -1): 
        hour = current_hour_to_string()

    root = ET.fromstring(request_plan(eva, date, hour))
    station = root.get('station')
    timetable_entries = [ScheduledTrainEntry(s, station, eva) for s in root.findall(".//s")]
    ret = []
    for te in timetable_entries:
        if (te.id == "id"):
            continue
        ret.append(te)
    return ret

def create_scheduled_train_entries_timespan(eva, start_date, start_hour, look_back):
    pass

def create_alternative_train_entries(eva):
    root = ET.fromstring(request_fchg(eva))
    station = root.get('station')
    timetable_entries = [AlternativeTrainEntry(s, station, eva) for s in root.findall(".//s") if s.find('ref') != None]
    ret = []
    for te in timetable_entries:
        if (te.id == "id"):
            return ret
        ret.append(te)
    return ret

def debug_delayed_entries():
    for entry in create_delayed_train_entries("8002794"):
        print(f"ID: {entry.id}, Arrival PT: {entry.actual_arrival}, Departure PT: {entry.actual_departure}")

def debug_scheduled_trains():
    for entry in create_scheduled_train_entries("8002794"):
        print(f"ID: {entry.id}, Arrival PT: {entry.arrival}, Departure PT: {entry.departure}, Origin: {entry.origin_stations}, Destination: {entry.destination_stations},  Train Type: {entry.train_type}, Train Num: {entry.train_alias}, Platform: {entry.platform}")
        print(" ")

def create_combined_train_entries(eva, date=-1, hour=-1):
    if (date == -1):
        date = current_date_to_string()
    if (hour == -1): 
        hour = current_hour_to_string()

    delayed_entries = create_delayed_train_entries(eva)
    scheduled_entries = create_scheduled_train_entries(eva, date, hour)
    combined_entries = combine_entries(delayed_entries, scheduled_entries)
    return combined_entries


def debug_combine(eva):
    delayed_entries = create_delayed_train_entries(eva)
    scheduled_entries = create_scheduled_train_entries(eva)
    combined_entries = combine_entries(delayed_entries, scheduled_entries)
    print("snens")
    for entry in combined_entries:
        print(entry)
    
    print(len(scheduled_entries))
    print(len(combined_entries))
    if (len(scheduled_entries) != len(combined_entries)) and DEBUG:
        raise Exception("combined entries and scheduled entries differ")
    
def debug_alternative(eva):
    alternative_entries = create_alternative_train_entries(eva)
    for a in alternative_entries:
        print(a)

