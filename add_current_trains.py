from db_utility import *
import train_requests
import db_manager


def add_current_entries(eva: int, lookback_hours: int):

    datehour = subtract_hours_from_api_datetime(current_date_to_string(), current_hour_to_string(), lookback_hours)

    trains = train_requests.create_combined_train_entries(eva, datehour[0], datehour[1])

    station_name = trains[0].station_name
    db_manager.check_for_new_eva(eva, station_name)

    for train in trains:
        print(train)
        db_manager.add_train_to_db(train)