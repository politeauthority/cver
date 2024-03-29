"""
    Cver Client
    Model
    Base

"""
from datetime import datetime
import logging

import arrow

from cver.client import Client as CverClient
from cver.shared.utils import date_utils


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
        """Hydrates a model object, setting all the data as class vars, properly typed as they
        should be.
        """
        for key, value in data.items():
            if key not in self.field_map:
                logging.error('Unknown field "%s" for %s model' % (key, self))
            if self.field_map[key]["type"] == "datetime":
                value = date_utils.from_str(value)
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
        self.response_last = response
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
        # logging.info("Saving %s: %s" % (self.model_name, data))
        self.response = self.make_request(self.model_name, method="POST", payload=data)
        if "object" not in self.response:
            logging.warning("Request error")
            return False
        entity = self.response["object"]

        for field_name, field_value in entity.items():
            setattr(self, field_name, field_value)
        # logging.info(f"Saved {self} successfully")
        return self.id

    def delete(self) -> dict:
        if not self.id:
            logging.warning("Cant delete %s with out an ID." % self)
            return False
        data = self._get_model_fields()
        logging.debug("Deleting %s" % self)
        self.response = self.make_request(f"{self.model_name}/{self.id}", method="DELETE", payload=data)
        return self.response

    def _get_model_fields(self) -> dict:
        """Get the class atribute keys and values that are model fields."""
        data = {}
        for field_name, field_info in self.field_map.items():
            if field_name == "id" and not getattr(self, "id"):
                continue
            if field_info["type"] == "datetime":
                data[field_name] = getattr(self, field_name)
                if data[field_name]:
                    if isinstance(data[field_name], datetime):
                        data[field_name] = date_utils.json_date(data[field_name])
                    elif isinstance(data[field_name], arrow.arrow.Arrow):
                        data[field_name] = date_utils.json_date(data[field_name])
                    else:
                        data[field_name] = data[field_name]
            else:
                data[field_name] = getattr(self, field_name)
        return data

# End File: cver/src/cver_client/models/base.py
