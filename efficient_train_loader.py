from db_utility import *
import train_requests
import db_manager
from train_data import CombinedTrainEntry
from time import sleep
import stations
import message_logger
import traceback

class Station:
    def __init__(self, eva: int, look_back: int) -> None:
        self.eva = eva
        self.scheduled_trains : list = []
        self.next_check_hour = current_hour_to_string()
        self.next_check_date = current_date_to_string()
        self.exception_count = 0
        self.station_name = "undefined"
        self.look_back = look_back

    def get_next_trains(self):
        self.scheduled_trains = []
        times = create_time_window(current_date_to_string(), current_hour_to_string(), self.look_back)
        for time in times:
            self.scheduled_trains += train_requests.create_scheduled_train_entries(self.eva, time[0], time[1])
            sleep(1)

    def update_check_time(self):
        old_hour = self.next_check_hour
        self.next_check_hour = add_hour_from_string(current_hour_to_string(), self.look_back - 1)
        if self.next_check_hour < old_hour:
            self.next_check_date = tomorrow_date_to_string()
        else:
            self.next_check_date = current_date_to_string()

        if (self.station_name == "undefined" or self.station_name == "failed"):
            self.station_name = train_requests.get_station_name_from_eva(self.eva)
            
    
    def get_current_combined_entries(self):
        if (self.need_new_trains() or self.exception_count > 0):
            if (self.exception_count > 10):
                self.update_check_time()
                self.exception_count = 0
                return None
            self.get_next_trains()
            delayed_trains = train_requests.create_delayed_train_entries(self.eva)
            sleep(1)
            ret = train_requests.combine_entries(delayed_trains, self.scheduled_trains)
            self.scheduled_trains = []
            self.update_check_time()
            return ret
        else:
            return None
    
    def need_new_trains(self) -> bool:
        now = datetime.now()
        next_check_time = db_time_to_datetime(self.next_check_date + str(self.next_check_hour) + "00")
        return now > next_check_time
        


class EfficientDownloader:
    def __init__(self, eva_list: list, look_back: int) -> None:
        self.stations = []
        self.look_back = look_back
        for eva in eva_list:
            self.stations.append(Station(eva, look_back))

    
    def log_update_times(self):
        message_logger.log_normal(datetime.now())
        for station in self.stations:
            next_check_time = db_time_to_datetime(station.next_check_date + str(station.next_check_hour) + "00")
            message_logger.log_normal(str(station.station_name) + ": " + str(next_check_time))
            message_logger.log_normal(str(station.station_name) + " exc count: " + str(station.exception_count))
                
    def download2(self):
        counter = -1
        while(True):
            if (counter % 10000 == 0):
                self.log_update_times()
                counter = 0
            for station in self.stations:

                try:
                    trains = station.get_current_combined_entries()
                    if trains == None:
                        station.exception_count = 0
                        continue
                    db_manager.check_for_new_eva(station.eva, station.station_name)
                    for train in trains:
                        message_logger.log_debug(train)
                        db_manager.add_train_to_db(train)
                    
                    station.exception_count = 0
                
                except Exception as e:
                    message_logger.log_critical(str(e))
                    stack_trace = traceback.format_exc()
                    message_logger.log_critical(stack_trace)
                    station.exception_count += 1
                    message_logger.log_critical(f"Exception exception count: {station.exception_count}")


            counter += 1
            sleep(1)

# 19671
# 20742