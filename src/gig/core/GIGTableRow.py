from utils import String

IGNORE_KEYS = ['entity_id', 'total_population']


def float_or_int(v):
    f = String(v).float
    if (f % 1) == 0:
        return int(f)
    return f


class GIGTableRow:
    def __init__(self, d):
        self.d = d

    @property
    def id(self):
        return self.d['entity_id']

    def __getattr__(self, key: str):
        if key in IGNORE_KEYS:
            raise AttributeError

        if key in self.d:
            return String(self.d.get(key)).float

        return super().__getattr__(key)

    @property
    def dict(self):
        d = {
            k: float_or_int(v)
            for k, v in self.d.items()
            if k not in IGNORE_KEYS
        }

        sorted_d = {
            k: v
            for k, v in sorted(
                d.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        }
        return sorted_d

    @property
    def total(self):
        return sum(self.dict.values())