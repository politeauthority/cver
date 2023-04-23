"""
    Cver Test Unit
    Api Model: BaseEntityMeta

"""
from cver.api.models.base_entity_meta import BaseEntityMeta


BASE_MAP = {
    "id": {
        "name": "id",
        "type": "int",
        "primary": True,
    },
    "created_ts": {
        "name": "created_ts",
        "type": "datetime",
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
    },
}


class TestBaseEntityMeta:

    def test____init__(self):
        """Test the BaseEntityMeta Model's initialization.
        :method: Base().__init__
        """
        base = BaseEntityMeta()
        assert hasattr(base, "table_name")
        assert hasattr(base, "backend")
        assert hasattr(base, "field_map")
        assert hasattr(base, "meta")
        assert isinstance(base.meta, dict)

    # def test____repr__(self):
    #     """Test the Base Model's representation.
    #     :method: Base().__repr__
    #     """
    #     base = Base()
    #     assert str(base) == "<Base>"


# End File: cver/tests/unit/api/models/test_base_entity_meta.py
