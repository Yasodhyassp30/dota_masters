from cerberus import Validator

def validate_pick(data):
    schema = {
        'hero': {
            'type': 'list',
            'schema': {
                'type': 'integer'
            },'required':True,'maxlength':9,'minlength':9
        }
    }

    v = Validator(schema)
    if not v.validate(data):
        raise ValueError(v.errors)