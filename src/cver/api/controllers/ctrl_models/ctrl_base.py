"""
    Cver Api - Controller Model
    Base

"""
import logging

from flask import make_response, request, jsonify


def get_model(model, entity_id: int = None) -> dict:
    """Base GET operation for a model.
    :unit-test: TestCtrlModelsBase::test__get_model
    """
    print("NOW HERE")
    entity = model()

    data = {
        "status": "Error",
        "message": "",
        "object": {},
        "object_type": entity.model_name
    }
    r_args = request.args

    # Search for model base on searchable fields
    search_fields = []
    for r_arg_key, r_arg_value in r_args.items():
        for field_name, field in entity.field_map.items():
            if field["name"] != r_arg_key:
                continue
        if "api_searchable" not in entity.field_map[r_arg_key]:
            continue
        search_field = {
            "field": r_arg_key,
            "value": r_arg_value,
            "op": "eq"
        }
        search_fields.append(search_field)

    # Missing data to retrieve the model.
    if not entity_id and not search_fields:
        data["message"] = "Missing required search ctriteria."
        return make_response(jsonify(data), 400)

    # Search for entity
    entity_found = False
    if search_fields:
        entity_found = entity.get_by_fields(search_fields)
    elif entity_id:
        entity_found = entity.get_by_id(entity_id)
    else:
        logging.error("Unexpected endpoint")

    # Entity not found
    if not entity_found:
        data["message"] = "Object not found"
        return make_response(jsonify(data), 404)

    data["status"] = "Success"
    data["status"] = "Entity found"
    data["object"] = entity.json()
    return data


def post_model(model, entity_id: int = None):
    """Base POST operation for a model. Create or modify a entity."""
    data = {
        "status": "Error"
    }
    entity = model()
    if entity_id:
        if not entity.get_by_id(entity_id):
            data["status"] = "Error"
            data["message"] = "Could not find %s ID: %s" % (entity.model_name, entity_id)
            return jsonify(data), 404
        else:
            logging.info("POST - Found entity: %s" % entity)

    # Check through the fields and see if they should be applied to the model.
    request_data = request.get_json()
    for field_name, field_value in request_data.items():
        update_field = False
        for entity_field_name, entity_field in entity.field_map.items():
            if entity_field["name"] == field_name:
                if "api_writeable" not in entity_field:
                    logging.warning("Entity: %s does not allow api writing of field: %s" % (
                        entity,
                        entity_field["name"]))
                    data["status"] = "Error"
                    data["message"] = "Cant modify field: %s" % field_name
                    return make_response(jsonify(data), 400)
                else:
                    update_field = True
        if update_field:
            logging.info("Entity: %s updating field: %s value: %s" % (
                entity,
                field_name,
                field_value))
            setattr(entity, field_name, field_value)

    entity.save()

    data["object"] = entity.json()
    data["object_type"] = entity.model_name
    return data, 201


def delete_model(model, entity_id: int):
    """Base DELETE a model."""
    entity = model()
    data = {
        "status": "Success",
        "object_type": entity.model_name
    }
    if not entity.get_by_id(entity_id):
        data["status"] = "Error"
        data["message"] = "Entity not found"
        return make_response(jsonify(data), 404)
    entity.delete()
    data["message"] = "User deleted successfully"
    data["object"] = entity.json()
    return make_response(jsonify(data), 201)


# End File: cver/src/api/controllers/ctrl_modles/ctrl_base.py
