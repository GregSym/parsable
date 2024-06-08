from __future__ import annotations
import re
from typing import Self, TYPE_CHECKING
if TYPE_CHECKING:
    import pandas as pd  # type: ignore


class Parsable:
    @staticmethod
    def pattern() -> re.Pattern[str]: ...
    @classmethod
    def from_str(cls, text: str) -> list[Self]:
        return [cls(**m.groupdict()) for m in cls.pattern().finditer(text)]

    @classmethod
    def from_str_or_default(cls, text: str, default: Self | None = None) -> Self | None:
        """return first from the string or some default"""
        res = cls.from_str(text)
        if len(res) == 0:
            return default
        return res[0]


class ParsableCollection[T: Parsable](list[T]):
    @staticmethod
    def runtime_type() -> type[T]: ...
    @classmethod
    def from_str(cls, text: str) -> Self:
        return cls(cls.runtime_type().from_str(text))

    @property
    def df(self) -> "pd.DataFrame":
        import pandas as pd  # type: ignore

        return pd.DataFrame(self)
