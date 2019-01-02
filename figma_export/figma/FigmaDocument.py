from dataclasses import dataclass
from typing import List
from .FigmaNode import FigmaNode


@dataclass(frozen=True)
class FigmaDocument:
    id: str
    name: str
    components: List[FigmaNode]
