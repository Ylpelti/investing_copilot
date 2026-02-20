from dataclasses import dataclass
from typing import Optional

@dataclass
class PortfolioInternal:
    user_id: int
    name: Optional[str]
    description: Optional[str] = None
    