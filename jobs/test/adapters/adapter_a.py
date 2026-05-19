from ..base.adapters import BaseAdapter


class AdapterA(BaseAdapter):
    name = "system_a"

    def fetch(self):
        return [
            {"op": "create", "id": "alpha-1"},
            {"op": "update", "id": "alpha-2"},
            {"op": "delete", "id": "alpha-3"},
            {"op": "create", "id": "alpha-4"},
        ]

    def transform(self, record):
        return {"action": record["op"], "name": f"{self.name}:{record['id']}"}
