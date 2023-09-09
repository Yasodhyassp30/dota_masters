from cerberus import Validator

def validate_prediction(data):
    schema = {
        'radiant': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'id': {'type': 'integer', 'required': True},
                    'position': {'type': 'integer', 'required': True},
                    'gpm': {'type': 'integer', 'required': True},
                    'name':{ 'type': 'string', 'required': False}
                }
            },'required':True,'maxlength':5
        },
        'dire': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'id': {'type': 'integer', 'required': True},
                    'position': {'type': 'integer', 'required': True},
                    'gpm': {'type': 'integer', 'required': True},
                    'name':{ 'type': 'string', 'required': False}
                }
            },'required':True,'maxlength':5
        }
    }
    v = Validator(schema)

    if not v.validate(data):
        raise ValueError(v.errors)