from .dataclasses import Change


class BaseAdapter:
    def __init__(self):
        self.changes = []

    def populate(self):
        self.changes.append(Change(action="create", name="thing_one"))
        self.changes.append(Change(action="update", name="thing_two"))
        self.changes.append(Change(action="delete", name="thing_three"))

    def count(self, action=None, data_type=None):
        return sum(
            1
            for c in self.changes
            if (action is None or c.action == action) and (data_type is None or isinstance(c, data_type))
        )
