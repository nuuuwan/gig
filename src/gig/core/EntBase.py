class EntBase:
    def __init__(self, d):
        self.d = d

    @property
    def id(self):
        return self.d["id"]

    @property
    def name(self):
        return self.d["name"]

    def is_parent_id(self, cand_parent_id):
        return cand_parent_id in self.id

    def __getattr__(self, key: str):
        if key in self.d.keys():
            return self.d.get(key)
        return super().__getattr__(key)
