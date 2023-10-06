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

    def get_by_id(self, entity_id: int) -> bool:
        """Get an entity by ID."""
        url = "%s/%s" % (self.model_name, entity_id)
        response = self.make_request(url)
        if response["status"] == "success":
            return self.build(response["object"])
        else:
            return False

    def get_by_name(self, name: str = None) -> bool:
        """Get an entity by name.
        @todo: Not all entities have names, this should be restricted to just those entities.
        """
        if not name:
            name = self.name
        data = {
            "name": name
        }
        response = self.make_request(self.model_name, payload=data)
        if response["status"] == "success":
            return self.build(response["object"])
        else:
            return False

    def get_by_fields(self, fields: dict = {}):
        """ Get an entity by any api searchable fields."""
        payload = {}
        for field_name, field_value in fields.items():
            if field_name not in self.field_map:
                continue
            if "api_searchable" not in self.field_map[field_name]:
                logging.debug("Cannot search for %s with field: %s" % self, field_name)
                continue
            elif not self.field_map[field_name]["api_searchable"]:
                logging.debug("Cannot search for %s with field: %s" % self, field_name)
                continue
            payload[field_name] = field_value

        response = self.make_request(self.model_name, payload=payload)
        if response["status"] == "success":
            return self.build(response["object"])
        else:
            return False

    def save(self) -> int:
        """Save a model to the Cver Api."""
        data = self._get_model_fields()
        logging.debug("Saving %s: %s" % (self.model_name, data))
        self.response = self.make_request(self.model_name, method="POST", payload=data)
        if "object" not in self.response:
            logging.warning("Request error")
            return False
        entity = self.response["object"]

        for field_name, field_value in entity.items():
            setattr(self, field_name, field_value)
        # logging.info(f"Saved {self} successfully")
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
