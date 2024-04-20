from city import City, ParkingLot

import requests
import pytz
from datetime import datetime
import hashlib
from shapely.geometry import LineString
from shapely.wkt import loads

def get_centroid_from_wkt(wkt_linestring):
    # Convert the WKT LINESTRING to a Shapely LineString object
    line = loads(wkt_linestring)
    
    # Calculate the centroid of the LineString
    centroid = line.centroid
    
    # Return the centroid coordinates as a tuple
    return (centroid.x, centroid.y)

def calc_fee_hours(tariffs):
    fee_hours = []
    for tariff in tariffs:
        day = ""
        if tariff['fromToDayInWeek'] == 'Ponedeljek - Petek':
            day = "Mo-Fr"
        elif tariff['fromToDayInWeek'] == 'Sobota':
            day = "Sa"
        elif tariff['fromToDayInWeek'] == 'Nedelja':
            day = "Su"
        elif tariff['fromToDayInWeek'] == 'Nedelja - Četrtek':
            day = "Su-Th"
        elif tariff['fromToDayInWeek'] == 'Ponedeljek - Sobota':
            day = "Mo-Sa"
        elif tariff['fromToDayInWeek'] == 'Četrtek - Nedelja':
            day = "Th-Su"
        elif tariff['fromToDayInWeek'] == 'Četrtek - Petek':
            day = "Th-Fr"
        else:
            print(f"Unknown day: {tariff['fromToDayInWeek']}")
            continue
        fee_hours.append(f"{day} {tariff['parkingPlaceWorkingTimes'][0]['workingFrom']}-{tariff['parkingPlaceWorkingTimes'][0]['workingTo']}")
    return '; '.join(fee_hours)


class CityCelje(City):
    timezone = pytz.timezone("Europe/Ljubljana")    
    def __init__(self):
        self.name = "Celje"
        self.id = "celje"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []

    def load_parking_lots(self):
        try:
            data = requests.get("https://moc.margento.org/MocMiddlewareWS/Parking/ParkingsAndTariffs?terminalId=12",
                                headers={
                                    'requestId': 'a517de0e-bcfc-48e2-9e8b-7a4aad555e50',
                                    'App-Version': '30',
                                    'Platform-ID': '1',
                                    'App-Language': 'sl'
                                }
                                ).json()
            self.lots = []
            self.last_downloaded = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.last_updated = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.data_source = "https://centralka.celje.si/"
            for parking_group in data['parkingGroups']:
                for parking_place in parking_group['parkingPlaces']:
                    if len(parking_place['parkingPlaceCharts']) == 0:
                        continue
                    park_lot = ParkingLot()
                    park_lot.name = parking_place['name']
                    park_lot.total = parking_place['totalSpaces']
                    park_lot.free = parking_place['freeSpaces'] if parking_place['freeSpaces'] != -1 else None
                    park_lot.state = "open" if parking_place['freeSpaces'] != -1 else "nodata"
                    park_lot.id = parking_place['id']
                    coords = get_centroid_from_wkt(parking_place['parkingPlaceCharts'])
                    park_lot.coords = {"lat": coords[1], "lng": coords[0]}
                    park_lot.opening_hours = "24/7"
                    park_lot.fee_hours = calc_fee_hours(parking_place['parkingPlaceWorkingDays'])
                    self.lots.append(park_lot)
        except Exception as e:
            print(f"Error loading parking lots: {e}")
            return