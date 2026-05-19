from dataclasses import dataclass


@dataclass
class Change:
    action: str
    name: str
