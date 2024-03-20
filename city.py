class City:
    def __init__(self):
        self.name = ""
        self.id = ""
        self.last_updated = ""
        self.last_downloaded = ""
        self.data_source = ""
        self.lots = []
        
    def add_parking_lot(self, parking_lot):
        self.lots.append(parking_lot)
        
    def load_parking_lots(self):
        raise NotImplementedError("This method must be implemented in a subclass")
       
    def to_key_value(self):
        return {
            self.name: self.id
        }    
        
    def get_id(self):
        return self.id

    def to_dict(self):
        return {
            "last_updated": self.last_updated,
            "last_downloaded": self.last_downloaded,
            "data_source": self.data_source,
            "lots": [p.to_dict() for p in self.lots]
        }
        
    def __str__(self):
        return f"City: {self.name} ({self.id})"
    
    def __repr__(self):
        return self.__str__()
    
    
class ParkingLot:
    def __init__(self):
        self.name = ""
        self.coords = {}
        self.total = 0
        self.free = 0
        self.state = ""
        self.id = ""
        self.forecast = False
        self.region = ""
        self.address = ""
        self.lot_type = ""
        self.opening_hours = ""
        self.fee_hours = ""
        self.url = ""
        
    def set(self, key, name):
        self[key] = name
        
    def to_dict(self):
        return {
            "name": self.name,
            "coords": self.coords,
            "total": self.total,
            "free": self.free,
            "state": self.state,
            "id": self.id,
            "forecast": self.forecast,
            "region": self.region,
            "address": self.address,
            "lot_type": self.lot_type,
            "opening_hours": self.opening_hours,
            "fee_price": self.fee_price if hasattr(self, 'fee_price') else "",
            "fee_hours": self.fee_hours,
            "url": self.url
        }