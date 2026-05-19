from dataclasses import dataclass, field


@dataclass
class Change:
    action: str
    name: str


@dataclass
class Result:
    changes: list = field(default_factory=list)

    def count(self, action=None, data_type=None):
        return sum(
            1
            for c in self.changes
            if (action is None or c.action == action) and (data_type is None or isinstance(c, data_type))
        )
