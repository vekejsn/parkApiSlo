from city import City, ParkingLot

import requests
import pytz
from datetime import datetime

class CityTrzic(City):
    timezone = pytz.timezone("Europe/Ljubljana")
    def __init__(self):
        self.name = "Tržič"
        self.id = "trzic"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []
        
    def load_parking_lots(self):
        try:
            data = requests.get("https://api.ontime.si/api/v1/parking/").json()
            self.lots = []
            self.last_downloaded = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.last_updated = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.data_source = "https://trzic.si/"
            for lot in data['results']:
                if lot['name'].index("Tržič") != -1:
                    park_lot = ParkingLot()
                    park_lot.name = lot['name']
                    park_lot.coords = {"lat": lot['lat'], "lng": lot['lng']}
                    park_lot.state = "open"                    
                    park_lot.total = lot['capacity']
                    park_lot.free = lot['occupancy'] # very badly named
                    park_lot.fee_hours = "Mo-Fr 07:00-16:00"
                    park_lot.fee_price = "0.40EUR/h, 1h free"
                    park_lot.opening_hours = "24/7"
                    park_lot.id = lot['parking_id']

                    self.lots.append(park_lot)

        except Exception as e:
            print(f"Error loading parking lots: {e}")