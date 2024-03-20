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
        "cities": {city: cities[city].get_id() for city in cities}
    }
    
@app.get("/{cityId}")
@cache(expire=120)
def return_city(cityId: str):
    for city in cities:
        if cities[city].get_id() == cityId:
            cities[city].load_parking_lots()
            return cities[city].to_dict()
    return {"error": "City not found"}
    

from city_kranj import CityKranj

if __name__ == "__main__":
    cities['Kranj'] = CityKranj()
    uvicorn.run(app, port=16000)