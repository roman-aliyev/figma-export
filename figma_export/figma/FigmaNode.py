from dataclasses import dataclass


@dataclass(frozen=True)
class FigmaNode:
    id: str
    name: str
    path: str
