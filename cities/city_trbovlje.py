from city import City, ParkingLot
from csv_2_obj import csv_to_obj

import requests
import pytz
from datetime import datetime
import hashlib

class CityTrbovlje(City):
    timezone = pytz.timezone("Europe/Ljubljana")    
    def __init__(self):
        self.name = "Trbovlje"
        self.id = "trbovlje"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []

    def load_parking_lots(self):
        try:
            data = requests.get("https://podatki.gov.si/dataset/7627d311-f8a2-43cd-abe6-ca63b7c9d8ba/resource/f233bc56-b13e-4e15-b257-c65b719732c7/download/trbovljeopsiparkirisca.csv")
            # Fix encoding to utf-8
            data.encoding = "utf-8"
            lots = csv_to_obj(data.text)
            self.lots = []
            self.last_downloaded = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.last_updated = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.data_source = "https://podatki.gov.si/"
            for lot in lots:
                park_lot = ParkingLot()
                park_lot.name = lot['\ufeffNaziv']
                park_lot.coords = {"lat": float(lot['Lokacijska koordinata (GMAPS - WGS84)'].split(', ')[0]), "lng": float(lot['Lokacijska koordinata (GMAPS - WGS84)'].split(', ')[1])}
                park_lot.state = "nodata"
                park_lot.total = int(lot['Število parkirnih mest'])
                park_lot.free = 0
                lot_id = f'{park_lot.name}/{park_lot.total}'
                park_lot.id = hashlib.md5(lot_id.encode()).hexdigest()
                self.lots.append(park_lot)
        except Exception as e:
            print(f"Error loading parking lots: {e}")
            return