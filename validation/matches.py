from cerberus import Validator

def validate_match(data):
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
        },
        'created': {
            'type':'string',
            'required':True
        },
        'prediction':{
            'type':'dict',
            'schema':{
                'radiant':{'type':'integer','required':True},
                'dire':{'type':'integer','required':True}
            },'required':True,
        },
        'feedback':{'type': 'integer', 'required': False},
        'uid':{'type':'string','required':True}
    }
    v = Validator(schema)

    if not v.validate(data):
        raise ValueError(v.errors)