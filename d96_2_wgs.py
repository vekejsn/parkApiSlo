import pyproj
from pyproj import Transformer

def d96_to_wgs84(x, y):
    transformer = Transformer.from_crs("EPSG:3794", "EPSG:4326")
    return transformer.transform(x, y)