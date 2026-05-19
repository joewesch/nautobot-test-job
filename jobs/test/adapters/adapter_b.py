from ..base.adapters import BaseAdapter
from ..base.dataclasses import Change


class AdapterB(BaseAdapter):
    name = "system_b"

    def fetch(self):
        return [
            {"verb": "CREATE", "label": "bravo-1"},
            {"verb": "UPDATE", "label": "bravo-2"},
            {"verb": "UPDATE", "label": "bravo-3"},
        ]

    def transform(self, record):
        return Change(action=record["verb"].lower(), name=f"{self.name}:{record['label']}")

    def change_class_id(self):
        return id(Change)
