from city import City, ParkingLot
from csv_2_obj import csv_to_obj
from d96_2_wgs import d96_to_wgs84

import requests
import pytz
from datetime import datetime
import hashlib

class CityVelenje(City):
    timezone = pytz.timezone("Europe/Ljubljana")    
    def __init__(self):
        self.name = "Velenje"
        self.id = "velenje"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []

    def load_parking_lots(self):
        try:
            data = requests.get("https://podatki.gov.si/dataset/915582c8-ccb3-48b5-b8ad-3d7f32e3ae22/resource/cddb1e93-bd57-40e6-b971-5407f1db9481/download/velenjeopsiparkirisca.csv")
            # Fix encoding to utf-8
            data.encoding = "utf-8"
            lots = csv_to_obj(data.text)
            self.lots = []
            self.last_downloaded = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.last_updated = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.data_source = "https://podatki.gov.si/"
            for lot in lots:
                if lot['Število parkirnih mest'] == '':
                    continue
                park_lot = ParkingLot()
                park_lot.name = lot['\ufeffNaziv']
                park_lot.coords = {"lat": float(lot['Lokacijska koordinata (GMAPS - WGS84)'].split(', ')[0]), "lng": float(lot['Lokacijska koordinata (GMAPS - WGS84)'].split(', ')[1])}
                park_lot.state = "nodata"
                park_lot.total = int(lot['Število parkirnih mest'])
                if (lot['Plačljivo'] == 'da'):
                    park_lot.fee_price = lot['Cena'].replace(',','.') + "/h"
                # park_lot.free = 0
                park_lot.id = hashlib.md5(f'{park_lot.name.encode()}/{park_lot.total}').hexdigest()
                self.lots.append(park_lot)
        except Exception as e:
            print(f"Error loading parking lots: {e}")
            return