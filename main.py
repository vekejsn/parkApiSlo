from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.inmemory import InMemoryBackend
import uvicorn

app = FastAPI()

FastAPICache.init(InMemoryBackend())

cities = {}


@app.get("/")
def return_cities():
    return {
        "api_version": "1.0",
        "server_version": "1.0.0",
        "reference": "https://github.com/offenesdresden/ParkAPI",
        "cities": {cities[city].get_id(): {
            "active_support": False,
            "attribution": None,
            "source": "",
            "url": "",
            "coords": {"lat": 0, "lng": 0},
            "name": city
        } for city in cities}
    }
    
@app.get("/{cityId}")
@cache(expire=120)
def return_city(cityId: str):
    for city in cities:
        if cities[city].get_id() == cityId:
            cities[city].load_parking_lots()
            return cities[city].to_dict()
    return {"error": "City not found"}
    

from cities.city_kranj import CityKranj
from cities.city_trbovlje import CityTrbovlje
from cities.city_sevnica import CitySevnica
from cities.city_kostanjevica_na_krki import CityKostanjevicaNaKrki
from cities.city_sostanj import CitySostanj
from cities.city_radece import CityRadece
from cities.city_mirna_pec import CityMirnaPec
from cities.city_straza import CityStraza
from cities.city_trebnje import CityTrebnje
from cities.city_velenje import CityVelenje

if __name__ == "__main__":
    cities['Kranj'] = CityKranj()
    cities['Trbovlje'] = CityTrbovlje()
    cities['Sevnica'] = CitySevnica()
    cities['Kostanjevica Na Krki'] = CityKostanjevicaNaKrki()
    cities['Sostanj'] = CitySostanj()
    cities['Radeče'] = CityRadece()
    cities['Mirna Peč'] = CityMirnaPec()
    cities['Straža'] = CityStraza()
    cities['Trebnje'] = CityTrebnje()
    cities['Velenje'] = CityVelenje()
    uvicorn.run(app, port=16000, host="0.0.0.0")
