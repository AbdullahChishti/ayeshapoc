from jsonschema import validate, ValidationError

def validate_json_schema(instance, schema):
    try:
        validate(instance=instance, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)
