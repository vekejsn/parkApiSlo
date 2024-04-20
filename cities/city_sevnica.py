from city import City, ParkingLot
from csv_2_obj import csv_to_obj

import requests
import pytz
from datetime import datetime
import hashlib
import chardet


class CitySevnica(City):
    timezone = pytz.timezone("Europe/Ljubljana")    
    def __init__(self):
        self.name = "Sevnica"
        self.id = "sevnica"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []

    def load_parking_lots(self):
        try:
            data = requests.get("https://podatki.gov.si/dataset/03dc44b7-5e74-41ec-9f93-d5f1f71cbef4/resource/c9abe5ec-068c-41ae-ae7d-7978244dc8c1/download/parkiriavsevnici.csv")
            data.encoding = 'Windows-1250' # fuck you
            lots = csv_to_obj(data.text)
            self.lots = []
            self.last_downloaded = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.last_updated = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.data_source = "https://podatki.gov.si/"
            for lot in lots:
                if lot['rezim_parkiranja'] == 'elektro vozila':
                    continue
                park_lot = ParkingLot()
                park_lot.name = lot['opis_lokacije']
                park_lot.coords = {"lat": float(lot['LAT']), "lng": float(lot['LON'])}
                park_lot.state = "nodata"
                park_lot.total = int(lot['st_parkirnih_mest'])
                park_lot.free = 0
                if lot['omejitev_modra_cona'] != '':
                    if 'od 6. do 16.' in lot['omejitev_modra_cona']:
                        park_lot.fee_hours = 'Mo-Fr 06:00-16:00'
                    else:
                        park_lot.fee_hours = 'Mo-Fr 07:00-17:00'
                    park_lot.fee_price = '0.5 EUR/h, 1h free'
                park_lot.opening_hours = '24/7'
                park_lot.id = hashlib.md5(f'{park_lot.name.encode()}/{park_lot.total}').hexdigest()
                self.lots.append(park_lot)
        except Exception as e:
            print(f"Error loading parking lots: {e}")
            return