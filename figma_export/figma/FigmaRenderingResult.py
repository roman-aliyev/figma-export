from dataclasses import dataclass
from .FigmaNode import FigmaNode


@dataclass(frozen=True)
class FigmaRenderingResult:
    node: FigmaNode
    format: str
    scale: float
    data: bytes
