from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ApiContext:
    auth: Dict[str, Any] = field(default_factory=dict)
    response: Optional[Any] = None
    board: Dict[str, Any] = field(default_factory=dict)
    boards: list = field(default_factory=list)
    audit: list = field(default_factory=list)


@dataclass
class UiContext:
    app: Optional[Any] = None
    board: Dict[str, Any] = field(default_factory=dict)
    card: Dict[str, Any] = field(default_factory=dict)
    card_count: int = 0
