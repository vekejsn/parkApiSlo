from city import City, ParkingLot
from csv_2_obj import csv_to_obj
from d96_2_wgs import d96_to_wgs84

import requests
import pytz
from datetime import datetime
import hashlib

class CityRadece(City):
    timezone = pytz.timezone("Europe/Ljubljana")    
    def __init__(self):
        self.name = "Radeče"
        self.id = "radece"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []

    def load_parking_lots(self):
        try:
            data = requests.get("https://podatki.gov.si/dataset/a43bf285-835b-4ab3-bc7a-1ea47e564dfa/resource/f7cb69e8-a6df-4e75-8f55-8d6a5fee9b20/download/opsiradecejavnaparkirisca.csv")
            data.encoding = "windows-1252" # fuck you
            lots = csv_to_obj(data.text)
            self.lots = []
            self.last_downloaded = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.last_updated = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.data_source = "https://podatki.gov.si/"
            for lot in lots:
                park_lot = ParkingLot()
                park_lot.name = lot['naslov'].replace('è', 'č') # also fuck you
                coords = d96_to_wgs84(float(lot['koordinata y (D96/TM)']), float(lot['koordinata x (D96/TM)']))
                park_lot.coords = {"lat": coords[0], "lng": coords[1]}
                park_lot.state = "nodata"
                park_lot.total = int(lot['št. parkirnih mest'])
                park_lot.free = 0
                park_lot.id = hashlib.md5(park_lot.name.encode()).hexdigest()
                self.lots.append(park_lot)
        except Exception as e:
            print(f"Error loading parking lots: {e}")
            return