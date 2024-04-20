from city import City, ParkingLot
from csv_2_obj import csv_to_obj

import requests
import pytz
from datetime import datetime
import hashlib

class CityMirnaPec(City):
    timezone = pytz.timezone("Europe/Ljubljana")    
    def __init__(self):
        self.name = "Mirna Peč"
        self.id = "mirna_pec"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []

    def load_parking_lots(self):
        try:
            data = requests.get("https://podatki.gov.si/dataset/4084cfa9-6fe8-44f8-a1e9-9ff0589e1257/resource/d17e893c-23fb-41c8-b78e-6baf0b753027/download/mirnapecopsiparkirisca.csv")
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
                park_lot.coords = {"lat": float(lot['Lokacijska koordinata'].split(', ')[0]), "lng": float(lot['Lokacijska koordinata'].split(', ')[1])}
                park_lot.state = "nodata"
                park_lot.total = int(lot['Število parkirnih mest'])
                park_lot.free = 0
                park_lot.id = hashlib.md5(f'{park_lot.name.encode()}/{park_lot.total}').hexdigest()
                self.lots.append(park_lot)
        except Exception as e:
            print(f"Error loading parking lots: {e}")
            return