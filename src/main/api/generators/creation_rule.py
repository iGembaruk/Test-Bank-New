from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class CreationRule:
    regex: Optional[str] = None
    min: Optional[Union[float, int]] = None
    max: Optional[Union[float, int]] = None