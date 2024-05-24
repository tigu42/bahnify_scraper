from db_conn import db_connection
from datetime import datetime
from stations import stations
DB_CONNECTION: db_connection = db_connection()

def average_delays_by_hour(eva: int, train_type: int, date: datetime) -> list:
    """
    Average delay of trains of a specific train station, grouped by hour 

    :param eva: train eva number
    :param train_type: 1 = REGIONAL | 2: INTERCITY TRAVEL | -1 DON'T CARE
    :param date: ANY date of the day
    :return: list of tuples containing the average delay of departing trains or "NA" when there wasn't enough data
    """


    regional_sql = "and (t.`type` like \"RE%\" or t.`type` like \"S%\" or t.`type` like \"BUS%\" or t.`type` like \"RB%\")\n"
    intercity_sql = "and (t.`type` like \"I%\" or t.`type` like \"E%\" or t.`type` like \"N%\" or t.`type` like \"RJ%\")\n"

    query = """select HOUR(t.scheduled_departure) as hour_of_day, SUM(abs(time_to_sec(timediff(d.current_departure, t.scheduled_departure))) / 60) / COUNT(*), COUNT(*)
            from train t 
            join delay d on t.id = d.train 
            where t.station = ? 
            """
    if (train_type == 1):
        query += regional_sql
    else:
        query += intercity_sql
    
    query += "AND (t.scheduled_departure >= ? AND t.scheduled_departure < ?)\n"
    query += "GROUP BY hour_of_day"

    start_time = date.replace(hour=0, minute=0, second=0, microsecond=0)

    end_time = date.replace(hour=23, minute=59, second=59)

    result = DB_CONNECTION.execute_query(query, (eva, start_time, end_time))

    return result

def punctuality_by_train_type(eva: int, direction: int, max_delay: int):
    """
    :param eva: eva number of the station
    :param direction: 1 = looks at arrival times, 2 = looks at departing times
    :param max_delay: number of minutes of when trains count as delayed

    :return: list of tuples [(type, punctuality (decimal), on time trains (int), not on time trains (int), average delay (decimal), max delay (decimal))]
    """
    sql_arriving = f"""select t.`type`, 
                    sum(case when (time_to_sec(timediff(d.current_arrival , t.scheduled_arrival)) / 60 < {max_delay} and d.status = 1) then 1 else 0 end) / COUNT(*) * 100, 
                    COUNT(case when (time_to_sec(timediff(d.current_arrival, t.scheduled_arrival)) / 60 < {max_delay} and d.status = 1) then 1 else null end), 
                    Count(*) - COUNT(case when (time_to_sec(timediff(d.current_arrival, t.scheduled_arrival)) / 60 < {max_delay} and d.status = 1) then 1 else null end),
                    sum(time_to_sec(timediff(d.current_arrival, t.scheduled_arrival)) / 60) / COUNT(*),
                    max(time_to_sec(timediff(d.current_arrival, t.scheduled_arrival)) / 60)
                    from train t 
                    join delay d on d.train = t.id
                    where not t.direction = 2
                    and t.station = ?
                    group by t.`type` """
    
    sql_departing = f"""select t.`type`, 
                    sum(case when (abs(time_to_sec(timediff(d.current_departure, t.scheduled_departure))) / 60 < {max_delay} and d.status = 1) then 1 else 0 end) / COUNT(*) * 100, 
                    COUNT(case when (abs(time_to_sec(timediff(d.current_departure, t.scheduled_departure))) / 60 < {max_delay} and d.status = 1) then 1 else null end), 
                    Count(*) - COUNT(case when (abs(time_to_sec(timediff(d.current_departure, t.scheduled_departure))) / 60 < {max_delay} and d.status = 1) then 1 else null end),
                    sum(abs(time_to_sec(timediff(d.current_departure, t.scheduled_departure))) / 60) / COUNT(*),
                    max(abs(time_to_sec(timediff(d.current_departure, t.scheduled_departure))) / 60)
                    from train t 
                    join delay d on d.train = t.id
                    where not t.direction = 1
                    and t.station = ?
                    group by t.`type` """
    
    if (direction == 1):
        query = sql_arriving
    else:
        query = sql_departing
    
    result = DB_CONNECTION.execute_query(query, (eva,))

    for r in result:
        print(r)

