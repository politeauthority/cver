"""
    Cver Client
    Model - Base

"""
import logging

from cver.cver_client import CverClient


class Base(CverClient):

    def __init__(self):
        """Base client model constructor."""
        super().__init__()
        self.entity_name = None
        self.field_map = {}

    def __repr__(self):
        """Base model representation."""
        if hasattr(self, "id") and self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def __desc__(self):
        print(f"{self}")
        for field_name, field_info in self.field_map.items():
            fied_value = getattr(self, field_name)
            print(f"\t{field_name}:   {fied_value}")

    def setup(self):
        """Add the fieldmap fields as class attributes to the model."""
        for field_name, field_info in self.field_map.items():
            setattr(self, field_name, None)

    def build(self, data: dict) -> bool:
        for key, value in data.items():
            setattr(self, key, value)
        return True

    def get_by_name(self, name: str):
        """Get an entity by name.
        @todo: Not all entities have names, this should be restricted to just those entities.
        """
        data = {
            "name": name
        }
        response = self.make_request(self.model_name, payload=data)
        if response["status"] == "success":
            return self.build(response["object"])
        else:
            return False

    def save(self) -> int:
        """Save a model to the Cver Api."""
        data = self._get_model_fields()
        self.response = self.make_request(self.model_name, method="POST", payload=data)
        if "object" not in self.response:
            print("Warning: request error")
            return False
        entity = self.response["object"]

        for field_name, field_value in entity.items():
            setattr(self, field_name, field_value)
        logging.info(f"Saved {entity} successfully")
        return self.id

    def _get_model_fields(self) -> dict:
        """Get the class atribute keys and values that are model fields."""
        data = {}
        for field_name, field_info in self.field_map.items():
            if not getattr(self, field_name):
                continue
            data[field_name] = getattr(self, field_name)
        return data

# End File: cver/src/cver_client/models/base.py
