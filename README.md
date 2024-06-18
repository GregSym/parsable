# Python Parsable Lib

## utilities for quickly structuring text parsing

![test_suite](https://github.com/GregSym/parsable/actions/workflows/test-suite.yml/badge.svg?event=pull_request)

### intended for situations where full-blown ast parsing is unnecessary


```python
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
    
@dataclass
class Coordinates(Parsable):
    x: float
    y: float

    @staticmethod
    def pattern() -> "re.Pattern[str]":
        return re.compile(
            r"\"coordinates\":\s*\[\s*(?P<x>\d+(?:\.\d+)?)\,\s*(?P<y>\d+(?:\.\d+)?)\,?\s*\]"
        )

coordinates = Coordinates.from_str(EXAMPLE_TEXT)
print(coordinates)

```

which outputs:
```output
>>> [Coordinates(x=14.95685, y=69.91848)]
```

This particular functionality exploits the named capture groups feature in the version of regex used by python (available in many other typical implementations) to structure the desired data into a dataclass output that can be worked with easily for other tasks.

### usage recommendation / disclaimer
I should note, as I have done elsewhere, that despite the example using JSON (which was a quick and clear way of demonstrating parsing) the intended target is niche, loosely structed data for which one doesn't necessarily want to reach for a full AST parsing tool. JSON is not a recommended application - JSON itself will usually have a dedicated tool, but this also applies to any structured format which one would not typically parse with regex. A better example may be a body of text containing some emails one might like to auto-parse into a structured collection.
