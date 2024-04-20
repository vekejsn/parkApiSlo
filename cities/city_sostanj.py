from city import City, ParkingLot
from csv_2_obj import csv_to_obj
from deg_2_dec import deg_to_dec

import requests
import pytz
from datetime import datetime
import hashlib

class CitySostanj(City):
    timezone = pytz.timezone("Europe/Ljubljana")    
    def __init__(self):
        self.name = "Šoštanj"
        self.id = "sostanj"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []

    def load_parking_lots(self):
        try:
            data = requests.get("https://podatki.gov.si/dataset/5c8ffae5-3ed0-45b5-b42a-9ec91deb8011/resource/1a336c1f-7501-4502-a5eb-9543a926aab3/download/sostanjopsiparkirisca.csv")
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
                lat = lot['Lokacijska koordinata'].split(';')[0]
                lat = lat.replace('°', ' ').replace('\'', ' ').replace('\'\'', ' ').replace(',', '.').split(' ')
                lat = deg_to_dec(float(lat[0]), float(lat[1]), float(lat[2]))
                lng = lot['Lokacijska koordinata'].split('; ')[1]
                lng = lng.replace('°', ' ').replace('\'', ' ').replace('\'\'', ' ').replace(',', '.').split(' ')
                lng = deg_to_dec(float(lng[0]), float(lng[1]), float(lng[2]))
                park_lot.coords = {"lat": lat, "lng": lng}
                park_lot.state = "nodata"
                park_lot.total = int(lot['Število parkirnih mest'])
                park_lot.free = 0
                if lot['Plačljivo'] != 'ne':
                    park_lot.fee_price = '2h limit (free)'
                park_lot.id = hashlib.md5(f'{park_lot.name.encode()}/{str(park_lot.total).encode()}').hexdigest()
                self.lots.append(park_lot)
        except Exception as e:
            print(f"Error loading parking lots: {e}")
            return