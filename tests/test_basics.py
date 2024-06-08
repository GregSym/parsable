from dataclasses import dataclass
from re import Pattern
import re
from parsable import Parsable
from parsable.main import ParsableCollection


EXAMPLE_TEXT = """

{
  "border": "{{int(1, 5)}}px {{random(solid, dotted, dashed)}} {{color()}}",
  "coordinates": {
    "type": "array",
    "count": 2,
    "items": "{{float(0, 120, 5)}}"
  },
  "password": "xX{{animal()}}-{{string(6, 10, *)}}"
}

{
  "border": "2px dashed gray",
  "coordinates": [
    14.95685,
    69.91848
  ],
  "password": "xXearthworm-*******"
}

"""

def test_basics() -> None:
    @dataclass
    class Coordinates(Parsable):
        x: float
        y: float

        @staticmethod
        def pattern() -> Pattern[str]:
            return re.compile(r"\"coordinates\":\s*\[\s*(?P<x>\d+(?:\.\d+)?)\,\s*(?P<y>\d+(?:\.\d+)?)\,?\s*\]")
        
        def __post_init__(self) -> None:
            self.x = float(self.x) if isinstance(self.x, str) else self.x
            self.y = float(self.y) if isinstance(self.y, str) else self.y
    
    coordinates = Coordinates.from_str(EXAMPLE_TEXT)

    assert len(coordinates) == 1
    assert coordinates[0].x == 14.95685
    assert coordinates[0].y == 69.91848

    class CoordinatesCollection(ParsableCollection[Coordinates]):
        @staticmethod
        def runtime_type() -> type:
            return Coordinates
    
    coordinates_alt = CoordinatesCollection.from_str(EXAMPLE_TEXT)
    assert len(coordinates_alt) == 1
    assert coordinates_alt[0].x == 14.95685
    assert coordinates_alt[0].y == 69.91848
