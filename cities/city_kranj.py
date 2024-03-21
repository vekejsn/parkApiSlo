from city import City, ParkingLot
from ical_2_osm import ical_to_osm

import requests
import pytz
from datetime import datetime

class CityKranj(City):
    timezone = pytz.timezone("Europe/Ljubljana")
    def __init__(self):
        self.name = "Kranj"
        self.id = "kranj"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []
        
    def load_parking_lots(self):
        try:
            data = requests.get("https://app-api.kranj.smartcity.si/api/v2/parkings?perPage=500").json()
            self.lots = []
            self.last_downloaded = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.last_updated = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.data_source = "https://pametni.kranj.si/"
            for lot in data['data']:
                if lot['spaces_ev_occupied'] is None and lot['spaces_regular'] is not None:
                    park_lot = ParkingLot()
                    park_lot.name = lot['name']
                    park_lot.coords = {"lat": float(lot['latitude']), "lng": float(lot['longitude'])}
                    if lot['active'] == 1:
                        park_lot.state = "open"
                    else:
                        park_lot.state = "closed"
                    
                    park_lot.total = lot['spaces_regular']
                    park_lot.free = lot['spaces_regular_available']
                    park_lot.fee_hours, park_lot.fee_price = ical_to_osm(lot['prices']) if lot['prices'] else ""
                    park_lot.fee_price += "/h"
                    park_lot.opening_hours = ical_to_osm(lot['working_hours']) if lot['working_hours'] else ""
                    park_lot.id = lot['id']

                    self.lots.append(park_lot)

        except Exception as e:
            print(f"Error loading parking lots: {e}")