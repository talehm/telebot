from enum import Enum

class ProductStatus(Enum):
    AVAILABLE = 'AVAILABLE'
    SOLD_OUT = 'SOLD_OUT'
    DISCONTINUED = 'DISCONTINUED'

class Platform(Enum):
    AMAZON = 'AMAZON'


class Country(Enum):
    GERMANY = 'GERMANY'
    USA = 'USA'
   