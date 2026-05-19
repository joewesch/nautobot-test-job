class BaseAdapter:
    name = None

    def fetch(self):
        raise NotImplementedError

    def transform(self, record):
        raise NotImplementedError
