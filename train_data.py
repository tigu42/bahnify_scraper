class AlternativeTrainEntry:
    def __init__(self, s_element, station_name, station_eva): # Check if ref object exists before creating object
        self.id = s_element.get('id')

        ar_elem = s_element.find(".//ar")
        dp_elem = s_element.find(".//dp")

        if (ar_elem != None):

            self.actual_arrival = ar_elem.get('ct')
            if (self.actual_arrival == None):
                self.actual_arrival = ar_elem.get('pt')
            if self.actual_arrival == None:
                cs = ar_elem.get('cs') 
                if (cs == 'c'):
                    self.actual_arrival = 'canceled'
                elif (cs != None):
                    self.actual_arrival = cs
                else:
                    self.actual_arrival = "Error"

            self.origin_stations = ar_elem.get('cpth')
            if self.origin_stations == None:
                self.origin_stations = ar_elem.get('ppth')
            if (self.origin_stations == None):
                self.origin_stations = "hmm?"
        else: 
            self.actual_arrival = "NA"
            self.origin_stations = "NA"

        if (dp_elem != None):
            self.actual_departure = dp_elem.get('ct')
            if (self.actual_departure == None):
                self.actual_departure = dp_elem.get('pt')
            if self.actual_departure == None:
                cs = dp_elem.get('cs')
                if (cs == 'c'):
                    self.actual_departure = "canceled"
                elif (cs != None):
                    self.actual_departure = cs
                else:
                    self.actual_departure = "Error"

            self.destination_stations = dp_elem.get('cpth')
            if self.destination_stations == None:
                self.destination_stations = dp_elem.get('ppth')
            if (self.destination_stations == None):
                self.destination_stations = "hmm?"
            
        else: 
            self.actual_departure = "NA"
            self.destination_stations = "NA"

        tl_element = s_element.find(".//tl")
        self.train_type = tl_element.get('c')
        self.train_number = tl_element.get('n')


        ref_elem = s_element.find('.//ref/tl')
        self.info = f"Replacement train for {ref_elem.get('c')} {ref_elem.get('n')}"

        self.station_name = station_name
        self.station_eva = station_eva

    def readable_time(self, time):
        if len(time) != 10 or not time.isdigit:
            return time
        time = time[6:]
        return time[:2] + ":" + time[2:]
    
    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Station Name: {self.station_name}\n"
            f"Station EVA: {self.station_eva}\n"
            f"Actual Arrival: {self.readable_time(self.actual_arrival)}\n"
            f"Actual Departure: {self.readable_time(self.actual_departure)}\n"
            f"Origin Stations: {self.origin_stations}\n"
            f"Destination Stations: {self.destination_stations}\n"
            f"Train Type: {self.train_type}\n"
            f"Train Number: {self.train_number}\n"
            f"Info: {self.info}\n"
        )

class DelayedTrainEntry:
    def __init__(self, s_element):
        #try:
            self.id = s_element.get('id')
            self.info = "Warning available"
            ar_elem = s_element.find(".//ar")
            dp_elem = s_element.find(".//dp")

            if (ar_elem != None):
                self.actual_arrival = ar_elem.get('ct')
                if (self.actual_arrival == None):
                    self.actual_arrival = ar_elem.get('pt')
                #if self.actual_arrival == None:
                cs = ar_elem.get('cs') 
                if (cs == 'c'):
                    self.actual_arrival = 'canceled'
                    self.info += "|canceled arrival"
                elif (cs == 'c'):
                    self.actual_arrival = "[NA] - Arrival remains unchanged"
                    self.info += "|cancelation revoked"
                elif (cs != None):
                    self.actual_arrival = cs
                    self.info += "|cancelation status unknown"
                if (self.actual_arrival == None):
                    self.actual_arrival = "[NA] arrival has warning - no info"
                
                self.actual_origin_stations = ar_elem.get('cpth')
                if (self.actual_origin_stations == None):
                    self.actual_origin_stations = "[NA] - Origin Path remains unchanged"
                else: 
                    self.info += "|Origin changed"
            else: 
                self.actual_arrival = "[NA] - Arrival remains unchanged"
                self.actual_origin_stations = "[NA] - Arrival remains unchanged"

            if (dp_elem != None):
                self.actual_departure = dp_elem.get('ct')
                if (self.actual_departure == None):
                    self.actual_departure = dp_elem.get('pt')
                #if self.actual_departure == None:
                cs = dp_elem.get('cs')
                if (cs == 'c'):
                    self.actual_departure = "canceled"
                    self.info += "|canceled departure"
                elif (cs == 'p'):
                    self.actual_departure = "[NA] - Departure remains unchanged"
                    self.info += "|departure cancelation revoked"
                elif (cs != None):
                    self.actual_departure = cs
                    self.info += "|cancelation status unknown"
                if (self.actual_departure == None):
                    self.actual_departure = "[NA] departure has warning - no info"
                
                self.actual_destination_stations = dp_elem.get('cpth')
                if (self.actual_destination_stations == None):
                    self.actual_destination_stations = "[NA] - Destination path remains unchanged"
                else:
                    self.info += "|Destination changed"
            else: 
                self.actual_departure = "[NA] - Departure remains unchanged"
                self.actual_destination_stations = "[NA] - Departure remains unchanged"

        #except:
            if (False):
                self.id = "id"
                self.ar_pt = "ar"
                self.dp_pt = "dp"

class ScheduledTrainEntry:
    def __init__(self, s_element, station_name, station_eva):
        #try:
            self.id = s_element.get('id')
            self.info = "Planned train"
            ar_elem = s_element.find(".//ar")
            dp_elem = s_element.find(".//dp")

            if ar_elem != None:
                self.arrival = ar_elem.get('pt')
            else:
                self.arrival = "[NA]"

            if dp_elem != None:
                self.departure = dp_elem.get('pt')
            else:
                self.departure = "[NA]"

            if (self.arrival != "[NA]"):
                self.origin_stations = ar_elem.get('ppth')
            else:
                self.origin_stations = "[NA]"

            if (self.departure != "[NA]"):
                self.destination_stations = dp_elem.get('ppth')
            else:
                self.destination_stations = "[NA]"


            tl_element = s_element.find(".//tl")
            self.train_type = tl_element.get('c')
            self.train_number = tl_element.get('n')

            if (dp_elem != None):
                self.train_alias = dp_elem.get('l')
            else:
                self.train_alias = ar_elem.get('l')
            if (self.train_alias == None): 
                self.train_alias = "[NA]"

            if (dp_elem != None):
                self.platform = dp_elem.get('pp')
            else:
                self.platform = ar_elem.get('pp')

            if (self.platform == "" or self.platform == None):
                self.platform = "[NA]"

            self.station_name = station_name
            self.station_eva = station_eva

        #except:
            if (False):
                self.id = "id"
                self.ar_pt = "ar"
                self.dp_pt = "dp"
                self.origin_stations = "os"
                self.destination_stations = "ds"
                self.train_type = "tt"
                self.train_alias = "tn"
                self.platform = "pl"
                self.station_name = "sn"
                self.station_eva = "se"

class CombinedTrainEntry:
    def __init__(self, scheduled_entry, delayed_entry=None):
        if delayed_entry:
            self.id = delayed_entry.id
            self.actual_arrival = delayed_entry.actual_arrival
            self.actual_departure = delayed_entry.actual_departure
            self.actual_origin_stations = delayed_entry.actual_origin_stations
            self.actual_destination_stations = delayed_entry.actual_destination_stations
            self.info = delayed_entry.info
        else:
            self.id = scheduled_entry.id
            self.actual_arrival = scheduled_entry.arrival
            self.actual_departure = scheduled_entry.departure
            self.actual_origin_stations = scheduled_entry.origin_stations
            self.actual_destination_stations = scheduled_entry.destination_stations
            self.info = scheduled_entry.info

        # common attributes
        self.arrival = scheduled_entry.arrival
        self.departure = scheduled_entry.departure
        self.origin_stations = scheduled_entry.origin_stations
        self.destination_stations = scheduled_entry.destination_stations
        self.train_type = scheduled_entry.train_type
        self.train_alias = scheduled_entry.train_alias
        self.platform = scheduled_entry.platform
        self.station_name = scheduled_entry.station_name
        self.station_eva = scheduled_entry.station_eva
        self.train_number = scheduled_entry.train_number
        
    def readable_time(self, time):
        if len(time) != 10 or not time.isdigit:
            return time
        time = time[6:]
        return time[:2] + ":" + time[2:]

    def __str__(self):
        return f"ID: {self.id}\n"\
               f"Scheduled Arrival: {self.readable_time(self.arrival)}\n"\
               f"Scheduled Departure: {self.readable_time(self.departure)}\n"\
               f"Actual Arrival: {self.readable_time(self.actual_arrival)}\n"\
               f"Actual Departure: {self.readable_time(self.actual_departure)}\n"\
                f"Origin Stations: {self.origin_stations}\n"\
               f"Destination Stations: {self.destination_stations}\n"\
               f"Actual Origin Stations: {self.actual_origin_stations}\n"\
               f"Actual Destination Stations: {self.actual_destination_stations}\n"\
               f"Train Type: {self.train_type}\n"\
               f"Train Alias: {self.train_alias}\n"\
               f"Train Number: {self.train_number}\n"\
               f"Platform: {self.platform}\n"\
               f"Station Name: {self.station_name}\n"\
               f"Station eva: {self.station_eva}\n"\
               f"Info: {self.info}\n"