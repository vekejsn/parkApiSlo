from city import City, ParkingLot
from csv_2_obj import csv_to_obj

import requests
import pytz
from datetime import datetime
import hashlib
import chardet


class CityKostanjevicaNaKrki(City):
    timezone = pytz.timezone("Europe/Ljubljana")    
    def __init__(self):
        self.name = "Kostanjevica na Krki"
        self.id = "kostanjevica_na_krki"
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []

    def load_parking_lots(self):
        try:
            data = requests.get("https://podatki.gov.si/dataset/57fb6039-4fc7-4b8d-a244-63c247d490f9/resource/cfd9b893-ecfd-4c1b-850d-d7b92fe44c53/download/parkiria.csv")
            data.encoding = 'Windows-1250' # fuck you
            lots = csv_to_obj(data.text)
            self.lots = []
            self.last_downloaded = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.last_updated = pytz.utc.localize(datetime.utcnow()).isoformat()
            self.data_source = "https://podatki.gov.si/"
            for lot in lots:
                if lot['opis_lokacije'] == '':
                    continue
                if lot['rezim_parkiranja'] == 'elektro vozila':
                    continue
                park_lot = ParkingLot()
                park_lot.name = lot['opis_lokacije']
                park_lot.coords = {"lat": float(lot['LAT']), "lng": float(lot['LON'])}
                park_lot.state = "nodata"
                park_lot.total = int(lot['st_parkirnih_mest'] if '+' not in lot['st_parkirnih_mest'] else sum([int(entry) for entry in lot['st_parkirnih_mest'].split('+')]))
                if lot['omejitev_modra_cona'] != '':
                    if 'od 6. do 16.' in lot['omejitev_modra_cona']:
                        park_lot.fee_hours = 'Mo-Fr 06:00-16:00'
                    else:
                        park_lot.fee_hours = 'Mo-Fr 07:00-17:00'
                    park_lot.fee_price = '0.5 EUR, 1h free'
                park_lot.opening_hours = '24/7'
                lot_id = f'{park_lot.name}/{park_lot.total}'
                park_lot.id = hashlib.md5(lot_id.encode()).hexdigest()
                self.lots.append(park_lot)
        except Exception as e:
            print(f"Error loading parking lots: {e}")
            return