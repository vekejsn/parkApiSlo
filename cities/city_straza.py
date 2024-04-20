from city import City, ParkingLot
from csv_2_obj import csv_to_obj
from d96_2_wgs import d96_to_wgs84

import requests
import pytz
from datetime import datetime
import hashlib

class CityStraza(City):
    timezone = pytz.timezone("Europe/Ljubljana")    
    def __init__(self):
        self.name = "Straža"
        self.id = "straza"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []

    def load_parking_lots(self):
        try:
            data = requests.get("https://podatki.gov.si/dataset/9ffefcf2-d7cd-4212-a2bf-8e5888c8ebed/resource/b9babd49-1594-45dc-9567-e9e2ecf50a94/download/strazaopsiparkirisca.csv")
            data.encoding = "utf-8"
            lots = csv_to_obj(data.text)
            self.lots = []
            self.last_downloaded = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.last_updated = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.data_source = "https://podatki.gov.si/"
            for lot in lots:
                park_lot = ParkingLot()
                park_lot.name = lot['\ufeffnaziv']
                coords = d96_to_wgs84(float(lot['lokacijska koordinata'].split(', ')[0]), float(lot['lokacijska koordinata'].split(', ')[1]))
                park_lot.coords = {"lat": coords[0], "lng": coords[1]}
                park_lot.state = "nodata"
                park_lot.total = int(lot['št. Park. Mest'])
                # park_lot.free = 0
                park_lot.id = hashlib.md5(f'{park_lot.name.encode()}/{park_lot.total}').hexdigest()
                self.lots.append(park_lot)
        except Exception as e:
            print(f"Error loading parking lots: {e}")
            return