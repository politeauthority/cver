"""
    Cver Client
    Model - Base

"""


class Base:

    def __init__(self):
        """Base client model constructor."""
        self.entity_name = None
        self.field_map = {}

    def __desc__(self):
        print(f"{self}")
        for field_name, field_info in self.field_map.items():
            fied_value = getattr(self, field_name)
            print(f"\t{field_name}:   {fied_value}")

    def build(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        return True

# End File: cver/src/cver_client/models/base.py
