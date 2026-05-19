from ..base.adapters import BaseAdapter


class AdapterB(BaseAdapter):
    name = "system_b"

    def fetch(self):
        return [
            {"verb": "CREATE", "label": "bravo-1"},
            {"verb": "UPDATE", "label": "bravo-2"},
            {"verb": "UPDATE", "label": "bravo-3"},
        ]

    def transform(self, record):
        return {"action": record["verb"].lower(), "name": f"{self.name}:{record['label']}"}
