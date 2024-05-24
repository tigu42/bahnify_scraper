import time
from stations import stations_common as stations
from datetime import datetime
import add_current_trains
import efficient_train_loader

station_list = [getattr(stations, attr) for attr in dir(stations) if not callable(getattr(stations, attr)) and not attr.startswith("__")]

def download_data(station_list: list, interval: int, lookback_hour: int):
    station_count = len(station_list)
    print(f"Pause time: {int(interval * 60 / (station_count * 2))}")
    while(True):
        
        for station in station_list:
            add_current_trains.add_current_entries(station, 0)
            print(f"Downloaded data from station {station} without lookback")
            time.sleep(int(interval * 60 / (station_count * 2)))
            add_current_trains.add_current_entries(station, lookback_hour)
            print(f"Downloaded data from station {station} with {lookback_hour} hours lookback")
            time.sleep(int(interval * 60 / (station_count * 2)))
        

# download_data(station_list, 2, 1)

def download_data_efficient(station_list: list, interval: int, look_back: int):
    downloader = efficient_train_loader.EfficientDownloader(station_list, look_back)
    downloader.download(interval)

#download_data_efficient(station_list, 1, 3)
downloader = efficient_train_loader.EfficientDownloader(station_list, 5)
downloader.download2()
