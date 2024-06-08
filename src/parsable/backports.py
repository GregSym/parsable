from __future__ import annotations
import abc
import sys
from typing import TYPE_CHECKING, TypeVar
from parsable.main import Parsable

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self
if TYPE_CHECKING:
    import pandas as pd  # type: ignore

T = TypeVar("T", bound=Parsable)


class ParsableCollection(list["T"]):  # type: ignore[valid-type, name-defined]
    @staticmethod
    @abc.abstractmethod
    def runtime_type() -> "type[T]": ...  # type: ignore[name-defined]

    @classmethod
    def from_str(cls, text: "str") -> "Self":
        return cls(cls.runtime_type().from_str(text))  # type: ignore[abstract]

    @property
    def df(self) -> "pd.DataFrame":
        import pandas as pd  # type: ignore

        return pd.DataFrame(self)
