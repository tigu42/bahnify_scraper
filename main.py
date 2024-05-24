import time
from stations import stations_common as stations
from datetime import datetime
import add_current_trains
import efficient_train_loader

station_list = [getattr(stations, attr) for attr in dir(stations) if not callable(getattr(stations, attr)) and not attr.startswith("__")]

downloader = efficient_train_loader.EfficientDownloader(station_list, 5)
downloader.download2()
