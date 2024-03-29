from __future__ import annotations

from enum import Enum
from typing import override


class Tiki(str, Enum):
    WIKIWIKI = "WIKIWIKI"
    KAPU = "KAPU"
    NUI = "NUI"
    EEPO = "EEPO"
    HUHU = "HUHU"
    LOKAHI = "LOKAHI"
    HOOKIPA = "HOOKIPA"
    AKAMAI = "AKAMAI"
    NANI = "NANI"

    @override
    def __repr__(self) -> str:
        return self.value


class Action(str, Enum):
    UP_ONE = "+1"
    UP_TWO = "+2"
    UP_THREE = "+3"
    TIKI_TOPPLE = "topple"
    TIKI_TOAST = "toast"
