"""
    Cver Api - Controller Model
    Base

"""
import json
import logging

from flask import make_response, request, jsonify


def get_model(model, entity_id: int = None) -> dict:
    """Base GET operation for a model.
    :unit-test: TestCtrlModelsBase::test__get_model
    """
    entity = model()

    data = {
        "status": "error",
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

    data["status"] = "success"
    data["object"] = entity.json()
    return data


def post_model(model, entity_id: int = None, generated_data: dict = {}):
    """Base POST operation for a model. Create or modify a entity.
    To edit an entity it's strongly encouraged you pass the entity ID in the URL. Otherwise we rely
    on database keys.
    If a model is immutabel then we can skip looking for the entity in the database.
    If a model is not createable, an model MUST be found in the database.
    @param entity_id: The ID of the entity. Used when UPDATING and entity.
    @param generated_data: This is used in instances like ApiKey generation, where fields are
        determined server side.
    """
    data = {
        "status": "error"
    }
    entity = model()
    if not entity.immutable:
        if entity_id:
            if not entity.get_by_id(entity_id):
                data["status"] = "Error"
                data["message"] = "Could not find %s ID: %s" % (entity.model_name, entity_id)
                return make_response(jsonify(data), 404)
            else:
                logging.info("POST - Found entity by ID: %s" % entity)

    # Dont allow api creates on api uncreateble models
    if not entity.id and not entity.createable:
        data["message"] = "Not allowed to create entity %s" % entity.model_name
        logging.warning("Attempting to create an ID ")
        return make_response(jsonify(data), 400)

    # If we cant decode a JSON payload return an error.
    try:
        request_data = request.get_json()
    except json.decoder.JSONDecodeError as e:
        logging.warning(f"Recieved data that cant be decoded to JSON: {e}")
        return make_response("ERROR", 401)

    # If there's api generated data, override the request data with that info.
    if generated_data:
        request_data.update(generated_data)

    # Check through the fields and see if they should be applied to the entity.
    for field_name, field_value in request_data.items():
        update_field = False
        for entity_field_name, entity_field in entity.field_map.items():
            if entity_field["name"] == field_name:
                if "api_writeable" not in entity_field and field_name not in generated_data:
                    logging.warning("Entity %s can not write field %s via an API request" % (
                        entity,
                        field_name))
                    continue
                else:
                    update_field = True
        if update_field:
            logging.info("Entity: %s updating field: %s value: %s" % (
                entity,
                field_name,
                field_value))
            setattr(entity, field_name, field_value)

    entity.save()
    data["status"] = "success"
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
    return make_response(jsonify(data), 202)


# End File: cver/src/api/controllers/ctrl_modles/ctrl_base.py
